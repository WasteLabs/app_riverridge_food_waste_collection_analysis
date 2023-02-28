import os
import sys
import logging
import plotly.express as px
import streamlit as st

from streamlit.runtime.secrets import AttrDict
import yaml
from kedro.framework.startup import bootstrap_project
from src.dashboards.utils.check_password import check_password
from src.dashboards.utils.filters import filter_dataframe
from src.dashboards.utils.generate_map import generate_map
import streamlit.components.v1 as components

st.set_page_config(
    page_title="RiverRidge food waste collection analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT_DIR = os.getcwd()
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

if not os.path.exists("conf/local"):
    os.makedirs("conf/local")


def pure_dict(dict_object):
    if type(dict_object) is not AttrDict:
        return dict_object
    else:
        return {key: pure_dict(dict_object[key]) for key in dict_object}


def create_credentials_file():
    with open("conf/local/credentials.yml", "w") as f:
        yaml.dump(pure_dict(st.secrets["credentials"]), f)


create_credentials_file()

bootstrap_project(PROJECT_DIR)

from src.dashboards import config  # noqa: I100,I201,E402
from src.dashboards import decorators  # noqa: I100,I201,E402


import os
import sys
import logging

import streamlit as st  # noqa: I201
from src.dashboards.utils.check_password import check_password
from pandas.api.types import CategoricalDtype
from src.dashboards import config  # noqa: I100,I201,E402
from src.dashboards import decorators  # noqa: I100,I201,E402
from src.dashboards.shared import io

log = logging.getLogger(__name__)

RESULTS_ORDER = ["scenario", "collection_day", "depot_name", "shift_name", "route_id"]

COLLECTION_DAY_REPLACEMENT = {
    "Monday": "1 Monday",
    "Tuesday": "2 Tuesday",
    "Wednesday": "3 Wednesday",
    "Thursday": "4 Thursday",
    "Friday": "5 Friday",
}

ID_COLUMNS = ["route_id"]
ID_COLUMNS_RENAME = ["Route"]
FILTER_COLUMNS_LOAD = ["scenario", "collection_day", "depot_name", "shift_name"]
FILTER_COLUMNS_RENAME = ["Scenario", "Collection day", "Depot", "Shift"]
METRIC_COLUMNS_LOAD = [
    "demand__kg",
    "n_bins",
    "n_stops",
    "n_sites",
    "travel_duration__h",
    "travel_distance__km",
    "serivice_duration__h",
    "ave_speed_kmh",
    "total_duration__h",
    "shift_duration__h",
    "available_service_duration__h",
    "available_service_duration_per_stop__min",
]
METRIC_COLUMNS_RENAME = [
    "Total demand (kg)",
    "Number of bins",
    "Number of stops",
    "Number of sites",
    "Total travel duration (h)",
    "Total distance (km)",
    "Total service duration (h)",
    "Average speed (km/h)",
    "Total duration (h)",
    "Shift duration (h",
    "Available service duration (h)",
    "Available service duration per stop (min)",
]

ID_RENAME_COLUMNS = dict(zip(ID_COLUMNS, ID_COLUMNS_RENAME))
FILTER_RENAME_COLUMNS = dict(zip(FILTER_COLUMNS_LOAD, FILTER_COLUMNS_RENAME))
METRIC_RENAME_COLUMNS = dict(zip(METRIC_COLUMNS_LOAD, METRIC_COLUMNS_RENAME))


FILTER_COLUMNS = ["Scenario", "Collection day", "Depot", "Shift"]
METRIC_COLUMNS = [
    "Number of sites",
    "Total demand (kg)",
    "Total distance (km)",
    "Total duration (h)",
    "Total travel duration (h)",
    "Total service duration (h)",
    "Number of bins",
    "Number of stops",
    "Average speed (km/h)",
    "Available service duration (h)",
    "Available service duration per stop (min)",
]


def convert_units(data):
    data = (
        data.assign(
            collection_day=data["collection_day"].replace(COLLECTION_DAY_REPLACEMENT),
            demand__kg=data["demand__kg"].round().astype(int),
            travel_duration__h=data["travel_duration__h"].round(2),
            travel_distance__km=data["travel_distance__km"].round(0).astype(int),
            serivice_duration__h=data["serivice_duration__h"].round(2),
            ave_speed_kmh=data["ave_speed_kmh"].round(0).astype(int),
            total_duration__h=data["total_duration__h"].round(2),
            shift_duration__h=data["shift_duration__h"].round(0).astype(int),
            available_service_duration__h=data["available_service_duration__h"].round(
                2
            ),
            available_service_duration_per_stop__min=data[
                "available_service_duration_per_stop__min"
            ]
            .round(0)
            .astype(int),
        )
        .sort_values(RESULTS_ORDER)
        .reset_index(drop=True)
    )
    return data


@decorators.kedro_context_required(
    project_dir=config.PROJECT_DIR,
    project_conf_dir=config.PROJECT_CONF_DIR,
    package_name=config.PROJECT_PACKAGE_NAME,
)
@st.cache_data
def retrieve_summary_data():
    data = io.retrieve_data(
        "solution_report_route_totals", "solution_report_route_totals"
    )
    # st.experimental_data_editor(data, disabled=True)
    data = convert_units(data)
    data = (
        data[ID_COLUMNS + FILTER_COLUMNS_LOAD + METRIC_COLUMNS_LOAD]
        .rename(columns=ID_RENAME_COLUMNS)
        .rename(columns=FILTER_RENAME_COLUMNS)
        .rename(columns=METRIC_RENAME_COLUMNS)
    )
    if "data" not in st.session_state:
        st.session_state["data"] = {}
    return data


@decorators.kedro_context_required(
    project_dir=config.PROJECT_DIR,
    project_conf_dir=config.PROJECT_CONF_DIR,
    package_name=config.PROJECT_PACKAGE_NAME,
)
@st.cache_data
def retrieve_route_data():
    assigned_stops = io.retrieve_data(
        "solution_report_assigned_stops", "solution_report_route"
    )
    unassigned_stops = io.retrieve_data(
        "solution_report_unassigned_stops", "solution_report_unassigned_stops"
    )
    assigned_routes = io.retrieve_data(
        "solution_report_assigned_routes", "solution_report_assigned_routes"
    )
    return assigned_stops, unassigned_stops, assigned_routes


@decorators.kedro_context_required(
    project_dir=config.PROJECT_DIR,
    project_conf_dir=config.PROJECT_CONF_DIR,
    package_name=config.PROJECT_PACKAGE_NAME,
)
def load_results_report():
    report = io.retrieve_data("solution_report", "solution_report")
    return report


def filter_scenarios(data, scenario_filter):
    return data.loc[data["scenario"].isin(scenario_filter)]


def filter_routes(data, route_filter):
    return data.loc[data["route_id"].isin(route_filter)]


def filter_double(data, scenario_filter, route_filter):
    return data.loc[
        data["scenario"].isin(scenario_filter) & data["route_id"].isin(route_filter)
    ]


@st.cache_data
def filter_assigned_stops(data, assigned_stops, unassigned_stops, assigned_routes):
    scenarios = data["Scenario"].unique()
    routes = data["Route"].unique()
    assigned_stops = filter_double(assigned_stops, scenarios, routes).copy()
    unassigned_stops = filter_scenarios(unassigned_stops, scenarios).copy()
    assigned_routes = filter_scenarios(assigned_routes, scenarios).copy()
    return assigned_stops, unassigned_stops, assigned_routes


@st.cache_data
def show_map(assigned_stops, unassigned_stops, assigned_routes, time_animation):
    map_html = generate_map(
        assigned_stops, unassigned_stops, assigned_routes, time_animation
    )
    return map_html


def display_route_kpis(data, metric_columns=METRIC_COLUMNS):
    for metric_column in metric_columns:
        st.write(f"#### {metric_column}")
        fig = px.bar(data, x="Route", y=metric_column, color="Depot")
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True, height=600)
        st.caption(f"**{metric_column}** per route.")


if not check_password():
    st.warning("Please log-in to continue.")
    st.stop()  # App won't run anything after this line

with st.spinner("Loading data..."):
    report = load_results_report()
    summary_data = retrieve_summary_data()
    assigned_stops, unassigned_stops, assigned_routes = retrieve_route_data()

sidebar = st.sidebar

scenarios = summary_data["Scenario"].unique()

scenario_filter = sidebar.multiselect("Select the scenario to analyse", scenarios)
if not scenario_filter:
    scenario_filter = scenarios

metric_filter = sidebar.multiselect("Select the metric to analyse", METRIC_COLUMNS)

if not metric_filter:
    metric_filter = METRIC_COLUMNS

summary_data_filtered = filter_dataframe.filter_dataframe(
    summary_data.loc[summary_data["Scenario"].isin(scenario_filter)],
    widget_key=f"summary_data_kpi_table_filter",
    base=sidebar,
)

if summary_data_filtered.empty:
    st.warning("No data to display. Please change your filter.")
    st.stop()

(
    filtered_assigned_stops,
    filtered_unassigned_stops,
    filtered_assigned_routes,
) = filter_assigned_stops(
    summary_data_filtered, assigned_stops, unassigned_stops, assigned_routes
)

tab0, tab1, tab2, tab3 = st.tabs(
    ["Report", "View route KPIs", "View route map", "View raw route table"]
)

with tab0:
    st.markdown(report)

with tab1:
    st.header("Route KPIs")
    for i, scenario in enumerate(scenario_filter):
        scenarios_display = scenario.replace("_", " ")
        st.write(f"### Scenario {i+1}: {scenarios_display}")
        scenario_data = summary_data_filtered[
            summary_data_filtered["Scenario"] == scenario
        ]
        display_route_kpis(scenario_data, metric_filter)

with tab2:
    st.header("Route map")
    st.markdown("It is recommended to only display a single scenario at a time.")
    height_map = st.slider(
        "Change the height of the map", min_value=400, max_value=1200, value=800
    )
    time_animation = st.checkbox("Show time-annimation", value=False)
    route_map = show_map(
        filtered_assigned_stops,
        filtered_unassigned_stops,
        filtered_assigned_routes,
        time_animation=time_animation,
    )
    components.html(route_map, height=height_map)

with tab3:
    st.header("Raw route tables")
    st.subheader("Summary")
    st.write(summary_data_filtered)
    st.subheader("Assigned stops")
    st.write(filtered_assigned_stops)
    st.subheader("Unassigned stops")
    st.write(filtered_unassigned_stops)

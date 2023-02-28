import os
import sys

from kedro.framework.startup import bootstrap_project
import streamlit as st  # noqa: I201
from streamlit.runtime.secrets import AttrDict
import yaml
from src.dashboards.utils.check_password import check_password

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
FILTER_COLUMNS = ["scenario", "collection_day", "depot_name", "shift_name"]
FILTER_COLUMNS_RENAME = ["Scenario", "Collection day", "Depot", "Shift"]
METRIC_COLUMNS = [
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
FILTER_RENAME_COLUMNS = dict(zip(FILTER_COLUMNS, FILTER_COLUMNS_RENAME))
METRIC_RENAME_COLUMNS = dict(zip(METRIC_COLUMNS, METRIC_COLUMNS_RENAME))


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
        data[ID_COLUMNS + FILTER_COLUMNS + METRIC_COLUMNS]
        .rename(columns=ID_RENAME_COLUMNS)
        .rename(columns=FILTER_RENAME_COLUMNS)
        .rename(columns=METRIC_RENAME_COLUMNS)
    )
    if "data" not in st.session_state:
        st.session_state["data"] = {}
    st.session_state["data"]["summary"] = data.copy()


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

    if "data" not in st.session_state:
        st.session_state["data"] = {}
    st.session_state["data"]["assigned_stops"] = assigned_stops.copy()
    st.session_state["data"]["unassigned_stops"] = unassigned_stops.copy()
    st.session_state["data"]["assigned_routes"] = assigned_routes.copy()


if not check_password():
    st.warning("Please log-in to continue.")
    st.stop()  # App won't run anything after this line

if "data" not in st.session_state:
    with st.spinner("Loading data..."):
        retrieve_summary_data()
        retrieve_route_data()


@decorators.kedro_context_required(
    project_dir=config.PROJECT_DIR,
    project_conf_dir=config.PROJECT_CONF_DIR,
    package_name=config.PROJECT_PACKAGE_NAME,
)
def load_results_report():
    return io.retrieve_data("solution_report", "solution_report")


results_text = load_results_report()
st.markdown(results_text, unsafe_allow_html=True)
retrieve_summary_data()
retrieve_route_data()

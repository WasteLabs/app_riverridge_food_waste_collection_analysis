from shapely import wkt
from keplergl import KeplerGl
import geopandas as gpd


def return_map_config():
    config = {
        "version": "v1",
        "config": {
            "visState": {
                "filters": [
                    # {
                    #     'dataId': ['Depot area coverage'],
                    #     'id': '448elfjkf',
                    #     'name': ['scenario'],
                    #     'type': 'multiSelect',
                    #     'value': ['customer_to_depot_weekday_shift_assignment'],
                    #     'enlarged': False,
                    #     'plotType': 'histogram',
                    #     'animationWindow': 'free',
                    #     'yAxis': None,
                    #     'speed': 1
                    # },
                    # {
                    #     'dataId': ['Assigned stops'],
                    #     'id': 'lihbes318',
                    #     'name': ['scenario'],
                    #     'type': 'multiSelect',
                    #     'value': ['customer_to_depot_weekday_shift_assignment'],
                    #     'enlarged': False,
                    #     'plotType': 'histogram',
                    #     'animationWindow': 'free',
                    #     'yAxis': None,
                    #     'speed': 1
                    # },
                    {
                        "dataId": ["Assigned stops"],
                        "id": "ilawi1c8",
                        "name": ["arrival_time"],
                        "type": "timeRange",
                        "value": [0, 999999999999999],
                        "enlarged": True,
                        "plotType": "histogram",
                        "animationWindow": "free",
                        "yAxis": None,
                        "speed": 1,
                    }
                ],
                "layers": [
                    {
                        "id": "4zc1mi",
                        "type": "point",
                        "config": {
                            "dataId": "Route depots",
                            "label": "Depots",
                            "color": [255, 254, 230],
                            "highlightColor": [252, 242, 26, 255],
                            "columns": {
                                "lat": "latitude",
                                "lng": "longitude",
                                "altitude": None,
                            },
                            "isVisible": True,
                            "visConfig": {
                                "radius": 10,
                                "fixedRadius": False,
                                "opacity": 0.8,
                                "outline": True,
                                "thickness": 1,
                                "strokeColor": None,
                                "colorRange": {
                                    "name": "Global Warming",
                                    "type": "sequential",
                                    "category": "Uber",
                                    "colors": [
                                        "#5A1846",
                                        "#900C3F",
                                        "#C70039",
                                        "#E3611C",
                                        "#F1920E",
                                        "#FFC300",
                                    ],
                                },
                                "strokeColorRange": {
                                    "name": "Global Warming",
                                    "type": "sequential",
                                    "category": "Uber",
                                    "colors": [
                                        "#5A1846",
                                        "#900C3F",
                                        "#C70039",
                                        "#E3611C",
                                        "#F1920E",
                                        "#FFC300",
                                    ],
                                },
                                "radiusRange": [0, 50],
                                "filled": False,
                            },
                            "hidden": False,
                            "textLabel": [
                                {
                                    "field": None,
                                    "color": [255, 255, 255],
                                    "size": 18,
                                    "offset": [0, 0],
                                    "anchor": "start",
                                    "alignment": "center",
                                }
                            ],
                        },
                        "visualChannels": {
                            "colorField": None,
                            "colorScale": "quantile",
                            "strokeColorField": None,
                            "strokeColorScale": "quantile",
                            "sizeField": None,
                            "sizeScale": "linear",
                        },
                    },
                    {
                        "id": "x546igj",
                        "type": "point",
                        "config": {
                            "dataId": "Assigned stops",
                            "label": "Assigned stops",
                            "color": [18, 92, 119],
                            "highlightColor": [252, 242, 26, 255],
                            "columns": {
                                "lat": "latitude",
                                "lng": "longitude",
                                "altitude": None,
                            },
                            "isVisible": True,
                            "visConfig": {
                                "radius": 10,
                                "fixedRadius": False,
                                "opacity": 0.8,
                                "outline": True,
                                "thickness": 0.5,
                                "strokeColor": [25, 20, 16],
                                "colorRange": {
                                    "name": "Uber Viz Qualitative 4",
                                    "type": "qualitative",
                                    "category": "Uber",
                                    "colors": [
                                        "#12939A",
                                        "#DDB27C",
                                        "#88572C",
                                        "#FF991F",
                                        "#F15C17",
                                        "#223F9A",
                                        "#DA70BF",
                                        "#125C77",
                                        "#4DC19C",
                                        "#776E57",
                                        "#17B8BE",
                                        "#F6D18A",
                                        "#B7885E",
                                        "#FFCB99",
                                        "#F89570",
                                        "#829AE3",
                                        "#E79FD5",
                                        "#1E96BE",
                                        "#89DAC1",
                                        "#B3AD9E",
                                    ],
                                },
                                "strokeColorRange": {
                                    "name": "Global Warming",
                                    "type": "sequential",
                                    "category": "Uber",
                                    "colors": [
                                        "#5A1846",
                                        "#900C3F",
                                        "#C70039",
                                        "#E3611C",
                                        "#F1920E",
                                        "#FFC300",
                                    ],
                                },
                                "radiusRange": [0, 50],
                                "filled": True,
                            },
                            "hidden": False,
                            "textLabel": [],
                        },
                        "visualChannels": {
                            "colorField": {"name": "route_id", "type": "string"},
                            "colorScale": "ordinal",
                            "strokeColorField": None,
                            "strokeColorScale": "quantile",
                            "sizeField": None,
                            "sizeScale": "linear",
                        },
                    },
                    {
                        "id": "w54tdb",
                        "type": "geojson",
                        "config": {
                            "dataId": "Assigned stops",
                            "label": "Travel legs",
                            "color": [241, 92, 23],
                            "highlightColor": [252, 242, 26, 255],
                            "columns": {"geojson": "travel_path_to_stop"},
                            "isVisible": True,
                            "visConfig": {
                                "opacity": 0.8,
                                "strokeOpacity": 0.8,
                                "thickness": 0.5,
                                "strokeColor": None,
                                "colorRange": {
                                    "name": "Global Warming",
                                    "type": "sequential",
                                    "category": "Uber",
                                    "colors": [
                                        "#5A1846",
                                        "#900C3F",
                                        "#C70039",
                                        "#E3611C",
                                        "#F1920E",
                                        "#FFC300",
                                    ],
                                },
                                "strokeColorRange": {
                                    "name": "Uber Viz Qualitative 4",
                                    "type": "qualitative",
                                    "category": "Uber",
                                    "colors": [
                                        "#12939A",
                                        "#DDB27C",
                                        "#88572C",
                                        "#FF991F",
                                        "#F15C17",
                                        "#223F9A",
                                        "#DA70BF",
                                        "#125C77",
                                        "#4DC19C",
                                        "#776E57",
                                        "#17B8BE",
                                        "#F6D18A",
                                        "#B7885E",
                                        "#FFCB99",
                                        "#F89570",
                                        "#829AE3",
                                        "#E79FD5",
                                        "#1E96BE",
                                        "#89DAC1",
                                        "#B3AD9E",
                                    ],
                                },
                                "radius": 10,
                                "sizeRange": [0, 10],
                                "radiusRange": [0, 50],
                                "heightRange": [0, 500],
                                "elevationScale": 1,
                                "enableElevationZoomFactor": True,
                                "stroked": True,
                                "filled": False,
                                "enable3d": False,
                                "wireframe": False,
                            },
                            "hidden": False,
                            "textLabel": [
                                {
                                    "field": None,
                                    "color": [255, 255, 255],
                                    "size": 18,
                                    "offset": [0, 0],
                                    "anchor": "start",
                                    "alignment": "center",
                                }
                            ],
                        },
                        "visualChannels": {
                            "colorField": None,
                            "colorScale": "quantile",
                            "strokeColorField": {"name": "route_id", "type": "string"},
                            "strokeColorScale": "ordinal",
                            "sizeField": None,
                            "sizeScale": "linear",
                            "heightField": None,
                            "heightScale": "linear",
                            "radiusField": None,
                            "radiusScale": "linear",
                        },
                    },
                    {
                        "id": "2i1df3",
                        "type": "point",
                        "config": {
                            "dataId": "Unserviced stops",
                            "label": "Unserviced stops",
                            "color": [30, 150, 190],
                            "highlightColor": [252, 242, 26, 255],
                            "columns": {
                                "lat": "latitude",
                                "lng": "longitude",
                                "altitude": None,
                            },
                            "isVisible": True,
                            "visConfig": {
                                "radius": 10,
                                "fixedRadius": False,
                                "opacity": 0.8,
                                "outline": True,
                                "thickness": 2,
                                "strokeColor": [187, 0, 0],
                                "colorRange": {
                                    "name": "Global Warming",
                                    "type": "sequential",
                                    "category": "Uber",
                                    "colors": [
                                        "#5A1846",
                                        "#900C3F",
                                        "#C70039",
                                        "#E3611C",
                                        "#F1920E",
                                        "#FFC300",
                                    ],
                                },
                                "strokeColorRange": {
                                    "name": "Global Warming",
                                    "type": "sequential",
                                    "category": "Uber",
                                    "colors": [
                                        "#5A1846",
                                        "#900C3F",
                                        "#C70039",
                                        "#E3611C",
                                        "#F1920E",
                                        "#FFC300",
                                    ],
                                },
                                "radiusRange": [0, 50],
                                "filled": False,
                            },
                            "hidden": False,
                            "textLabel": [
                                {
                                    "field": None,
                                    "color": [255, 255, 255],
                                    "size": 18,
                                    "offset": [0, 0],
                                    "anchor": "start",
                                    "alignment": "center",
                                }
                            ],
                        },
                        "visualChannels": {
                            "colorField": None,
                            "colorScale": "quantile",
                            "strokeColorField": None,
                            "strokeColorScale": "quantile",
                            "sizeField": None,
                            "sizeScale": "linear",
                        },
                    },
                    {
                        "id": "xrmmpjk",
                        "type": "geojson",
                        "config": {
                            "dataId": "Depot area coverage",
                            "label": "Depot area coverage",
                            "color": [136, 87, 44],
                            "highlightColor": [252, 242, 26, 255],
                            "columns": {"geojson": "depot_convex_hull"},
                            "isVisible": True,
                            "visConfig": {
                                "opacity": 0.01,
                                "strokeOpacity": 0.8,
                                "thickness": 0.5,
                                "strokeColor": [25, 20, 16],
                                "colorRange": {
                                    "name": "Sunrise 3",
                                    "type": "sequential",
                                    "category": "Uber",
                                    "colors": ["#355C7D", "#C06C84", "#F8B195"],
                                },
                                "strokeColorRange": {
                                    "name": "Ice And Fire 3",
                                    "type": "diverging",
                                    "category": "Uber",
                                    "colors": ["#0198BD", "#FAFEB3", "#D50255"],
                                },
                                "radius": 10,
                                "sizeRange": [0, 10],
                                "radiusRange": [0, 50],
                                "heightRange": [0, 500],
                                "elevationScale": 5,
                                "enableElevationZoomFactor": True,
                                "stroked": False,
                                "filled": True,
                                "enable3d": False,
                                "wireframe": False,
                            },
                            "hidden": False,
                            "textLabel": [
                                {
                                    "field": None,
                                    "color": [255, 255, 255],
                                    "size": 18,
                                    "offset": [0, 0],
                                    "anchor": "start",
                                    "alignment": "center",
                                }
                            ],
                        },
                        "visualChannels": {
                            "colorField": {"name": "depot_name", "type": "string"},
                            "colorScale": "ordinal",
                            "strokeColorField": None,
                            "strokeColorScale": "quantile",
                            "sizeField": None,
                            "sizeScale": "linear",
                            "heightField": None,
                            "heightScale": "linear",
                            "radiusField": None,
                            "radiusScale": "linear",
                        },
                    },
                ],
                "interactionConfig": {
                    "tooltip": {
                        "fieldsToShow": {
                            "Depot area coverage": [
                                {"name": "scenario", "format": None},
                                {"name": "depot_name", "format": None},
                            ],
                            "Unserviced stops": [
                                {"name": "scenario", "format": None},
                                {"name": "collection_day", "format": None},
                                {"name": "shift_name", "format": None},
                                {"name": "customer_id", "format": None},
                                {"name": "address_info1", "format": None},
                                {"name": "address_info2", "format": None},
                                {"name": "city", "format": None},
                                {"name": "post_code", "format": None},
                            ],
                            "Route depots": [
                                {"name": "route_name", "format": None},
                                {"name": "vehicle_name", "format": None},
                                {"name": "shift_name", "format": None},
                                {"name": "depot_name", "format": None},
                                {"name": "waste_type", "format": None},
                            ],
                            "Assigned stops": [
                                {"name": "route_id", "format": None},
                                {"name": "site_name", "format": None},
                                {"name": "job_sequence", "format": None},
                                {"name": "arrival_time", "format": None},
                                {"name": "departure_time", "format": None},
                                {"name": "demand", "format": None},
                                {"name": "scenario", "format": None},
                                {"name": "collection_day", "format": None},
                                {"name": "shift_name", "format": None},
                                {"name": "address_info1", "format": None},
                                {"name": "address_info2", "format": None},
                                {"name": "city", "format": None},
                                {"name": "post_code", "format": None},
                                {"name": "n_bins", "format": None},
                                {"name": "waste_bin_type", "format": None},
                                {"name": "depot_name", "format": None},
                            ],
                        },
                        "compareMode": False,
                        "compareType": "absolute",
                        "enabled": True,
                    },
                    "brush": {"size": 0.5, "enabled": False},
                    "geocoder": {"enabled": False},
                    "coordinate": {"enabled": False},
                },
                "layerBlending": "normal",
                "splitMaps": [],
                "animationConfig": {"currentTime": None, "speed": 1},
            },
            "mapState": {
                "bearing": 0,
                "dragRotate": False,
                "latitude": 54.573185172560116,
                "longitude": -6.520503895162236,
                "pitch": 0,
                "zoom": 7.851348953775596,
                "isSplit": False,
            },
            "mapStyle": {
                "styleType": "dark",
                "topLayerGroups": {},
                "visibleLayerGroups": {
                    "label": True,
                    "road": True,
                    "border": False,
                    "building": True,
                    "water": True,
                    "land": True,
                    "3d building": False,
                },
                "threeDBuildingColor": [
                    9.665468314072013,
                    17.18305478057247,
                    31.1442867897876,
                ],
                "mapStyles": {},
            },
        },
    }
    return config


def generate_convex_hullassigned_stops(assigned_stops):
    def calc_convex(stops):
        stops_geo = gpd.GeoDataFrame(
            stops,
            geometry=gpd.points_from_xy(stops.longitude, stops.latitude),
            crs="EPSG:4326",
        )
        convex = stops_geo.unary_union.convex_hull
        return convex

    convex_hulls = (
        assigned_stops.groupby(["scenario", "depot_name"])
        .apply(calc_convex)
        .reset_index()
        .rename(columns={0: "depot_convex_hull"})
    )
    convex_hulls = convex_hulls.assign(
        depot_convex_hull=convex_hulls["depot_convex_hull"].apply(wkt.dumps)
    )
    return convex_hulls


def generate_map(assigned_stops, unassigned_stops, assigned_routes):
    convex_hulls = generate_convex_hullassigned_stops(assigned_stops)
    assigned_stops_map = assigned_stops[
        [
            "route_id",
            "site_name",
            "job_sequence",
            "arrival_time",
            "departure_time",
            "demand",
            "scenario",
            "collection_day",
            "shift_name",
            "address_info1",
            "address_info2",
            "city",
            "post_code",
            "n_bins",
            "waste_bin_type",
            "depot_name",
            "latitude",
            "longitude",
            "travel_path_to_stop",
        ]
    ].fillna("")
    map = KeplerGl(
        data={
            "Depot area coverage": convex_hulls,
            "Unserviced stops": unassigned_stops,
            "Route depots": assigned_routes,
            "Assigned stops": assigned_stops_map,
        },
        height=800,
        config=return_map_config(),
    )
    return map._repr_html_()

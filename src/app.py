import dash_leaflet as dl
import dash
from dash import html, Input, Output
import gpxpy
import gpxpy.gpx
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc

def process_gpx_to_df(file_name):
    data = []
    columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
    gpx_df = pd.DataFrame(data, columns=columns)
    points = []

    try:
        gpx = gpxpy.parse(open(file_name))
    except:
        raise Exception(f'failed with {str(file_name)}')

    # (1)make DataFrame
    track = gpx.tracks[0]
    segment = track.segments[0]
    # Load the data into a Pandas dataframe (by way of a list)

    segment_length = segment.length_3d()
    for point_idx, point in enumerate(segment.points):
        data.append([point.longitude, point.latitude, point.elevation,
                     point.time, segment.get_speed(point_idx)])


    # 2(make points tuple for line)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(tuple([point.latitude, point.longitude]))

    #return folium.PolyLine(points, color='purple', weight=2.5, opacity=.6).add_to(m)
    return gpx_df, points

pub_dict = {"Rendevous Kro": [59.93498989098532, 10.780328058613252],
                    "Li Li's": [59.93118724388547, 10.77861276691262],
                    "Wings Bar": [59.92977387943943, 10.780331137142344],
                    "Pizzeria Valentino": [59.92942066428848, 10.77829610612493],
                    "Bella Notte": [59.92646493278491, 10.775931126366864],
                    "Szechuan Chengdu": [59.92318950272041, 10.771788011608823],
                    "Perla": [59.92268279074624, 10.769334381118076],
                    "Pane & Vino": [59.92102450083967, 10.770355137948018],
                    "Ocean Cafe & Bar": [59.920022667376934, 10.76613985851109],
                    "Konoji": [59.91978391264513, 10.765486111688837],
                    "Gråbein Bar": [59.91866942341721, 10.765035500608464],
                    "Ludus Cafe & sportsbar": [59.91907006470726, 10.763638853258064],
                    "Hersleb Grill og Bar AS": [59.918762197736235, 10.762615589294827],
                    "Schouskjelleren Mikrobryggeri": [59.918279544998, 10.760290672930624]}

original_pub = ["Rendevous Kro",
                 "Li Li's",
                 "Wings Bar",
                 "Pizzeria Valentino",
                 "Bella Notte",
                 "Szechuan Chengdu",
                 "Perla",
                 "Pane & Vino",
                 "Ocean Cafe & Bar",
                 "Konoji",
                 "Gråbein Bar",
                 "Ludus Cafe & sportsbar",
                 "Hersleb Grill og Bar AS",
                 "Schouskjelleren Mikrobryggeri"]

polyline_list = []
file_name = 'TdT.gpx'
df, points = process_gpx_to_df(file_name)
polyline_list.append(dl.Polyline(positions=points, color='blue', weight=10, opacity=1, id="polyline"))
polyline_list.append(dl.TileLayer())
polyline_list.append(dl.LayerGroup(id="layer"))
polyline_list.append( dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}))
for pub in original_pub:
    polyline_list.append(dl.Marker(position=pub_dict[pub],
                                   children=[dl.Tooltip(pub, permanent=True), dl.Popup(pub)]))




app = dash.Dash(external_stylesheets=['https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
                                      dbc.themes.BOOTSTRAP],
                prevent_initial_callbacks=False)
server = app.server

app.layout = html.Div([
    dl.Map(
    children=polyline_list,
    id="map",
    style={'width': '375px', 'height': '461px', 'margin': "auto", "display": "block"},
    center=[59.9351816485413,10.780315299805943],
    zoom=18

    ),
    dcc.Store(id="store", data=["Rendevous Kro",
                 "Li Li's",
                 "Wings Bar",
                 "Pizzeria Valentino",
                 "Bella Notte",
                 "Szechuan Chengdu",
                 "Perla",
                 "Pane & Vino",
                 "Ocean Cafe & Bar",
                 "Konoji",
                 "Gråbein Bar",
                 "Ludus Cafe & sportsbar",
                 "Hersleb Grill og Bar AS",
                 "Schouskjelleren Mikrobryggeri"]),
    dcc.Store(id="store2", data=[5,10,15,20,25,31,36,41,46,53,61,68,75,82,100]),
    dbc.Alert("Husk å kjøpe pizza på neste stopp, du er halvveis!!", id="alert-pizza", is_open=False, duration=10000,
              style={'width': '375px', 'height': '70px', 'margin': "auto", "display": "block"}),
    dbc.Alert("Bare 3 stopp igjen, hold ut du klarer det!", id="alert-3stopp", is_open=False, duration=10000,
              style={'width': '375px', 'height': '50px', 'margin': "auto", "display": "block"}),
    dbc.Alert("Du ankommer SISTE stopp, Gratulerer med gjennomført Tour de Trondheimsveien 2023!",
              id="alert-final", is_open=False, duration=10000,
              style={'width': '375px', 'height': '70px', 'margin': "auto", "display": "block"}),
    dbc.Progress(id='progress',label="1øl 2øl 3øl 4øl 5øl 6øl 7øl 8øl 9øl 10øl 11øl 12øl 13øl 14øl I mål",
                 color= 'success',
                 value=10,
                 style={'width': '375px', 'height': '20px', 'margin': "auto", "display": "block"}),
    dbc.Button("Neste Bar", id="next", color="primary", className="mr-1", n_clicks=0,
               style={'width': '375px', 'height': '50px', 'margin': "auto", "display": "block"}),
    dbc.Button("Reset", id="reset", color="danger", className="mr-1", n_clicks=0,
                style={'width': '375px', 'height': '35px', 'margin': "auto", "display": "block"}),

])


@app.callback(
    [Output("map", "children"),
     Output("map", "center"),
     Output("store", "data"),
     Output("next", "n_clicks"),
     Output("reset", "n_clicks"),
     Output("progress", "value"),
     Output("alert-pizza", "is_open"),
    Output("alert-3stopp", "is_open"),
    Output("alert-final", "is_open"),
    ],
    [Input("next", "n_clicks"),
     Input("reset", "n_clicks"),
     Input("store", "data"),
     Input("store2", "data")
     ])

def update_map(n_clicks, reset_clicks,live_pub,progress_value):
    alert_pizza = False
    alert_3stopp = False
    alert_final = False
    print(n_clicks)
    print(live_pub)
    polyline_list_return = []
    center_location_return = [59.9351816485413,10.780315299805943]
    store_data_return = live_pub
    progress_value_return = 0
    if  n_clicks == 0:
        print(live_pub)

        polyline_list = []
        polyline_list.append(dl.Polyline(positions=points, color='blue', weight=10, opacity=1, id="polyline"))
        polyline_list.append(dl.TileLayer())
        polyline_list.append(dl.LayerGroup(id="layer"))
        polyline_list.append(dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}))

        for pub in live_pub:
            polyline_list.append(dl.Marker(position=pub_dict[pub],
                                           children=[dl.Tooltip(pub, permanent=True), dl.Popup(pub)]))

        polyline_list_return = polyline_list
        store_data_return = live_pub


    else:
        try:
            live_pub.pop(0)
            polyline_list = []
            polyline_list.append(dl.Polyline(positions=points, color='blue', weight=10, opacity=1, id="polyline"))
            polyline_list.append(dl.TileLayer())
            polyline_list.append(dl.LayerGroup(id="layer"))
            polyline_list.append(dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}))

            for pub in live_pub:
                polyline_list.append(dl.Marker(position=pub_dict[pub],
                                               children=[dl.Tooltip(pub, permanent=True), dl.Popup(pub)]))
            center_location = pub_dict[live_pub[0]]
            print(center_location)
            polyline_list_return = polyline_list
            center_location_return = center_location
            store_data_return = live_pub
            progress_value_return = progress_value[n_clicks-1]
            if live_pub[0] == "Pane & Vino":
                alert_pizza = True
            if live_pub[0] == "Ludus Cafe & sportsbar":
                alert_3stopp = True
            if live_pub == ['Schouskjelleren Mikrobryggeri'] and n_clicks == 13:
                alert_final = True


        except:
            polyline_list = []
            polyline_list.append(dl.Polyline(positions=points, color='blue', weight=10, opacity=1, id="polyline"))
            polyline_list.append(dl.TileLayer())
            polyline_list.append(dl.LayerGroup(id="layer"))
            polyline_list.append(dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}))


            polyline_list.append(dl.Marker(position=pub_dict[original_pub[-1]],
                                               children=[dl.Tooltip(original_pub[-1], permanent=True), dl.Popup(original_pub[-1])]))
            polyline_list_return = polyline_list
            center_location_return = pub_dict[original_pub[-1]]
            store_data_return = live_pub
            progress_value_return = 100

    print(live_pub)
    if reset_clicks == 0:
        return polyline_list_return, center_location_return, store_data_return, n_clicks, 0, progress_value_return, alert_pizza, alert_3stopp, alert_final
    elif reset_clicks == 1:
        polyline_list_return = []
        polyline_list_return.append(dl.Polyline(positions=points, color='blue', weight=10, opacity=1, id="polyline"))
        polyline_list_return.append(dl.TileLayer())
        polyline_list_return.append(dl.LayerGroup(id="layer"))
        polyline_list_return.append(dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}))
        polyline_list_return.append(dl.Marker(position=pub_dict[original_pub[0]],
                                               children=[dl.Tooltip(original_pub[0], permanent=True), dl.Popup(original_pub[0])]))
        center_location_return = pub_dict[original_pub[0]]
        store_data_return = original_pub
        return polyline_list_return, center_location_return, store_data_return, 0, 0, 0, alert_pizza, alert_3stopp, alert_final

    else:
        store_data_return = original_pub
        polyline_list_return.append(dl.Marker(position=pub_dict[original_pub[0]],
                                               children=[dl.Tooltip(original_pub[0], permanent=True), dl.Popup(original_pub[0])]))
        return polyline_list_return, center_location_return, store_data_return, 0, 0, 0, alert_pizza, alert_3stopp, alert_final








if __name__ == '__main__':
    app.run_server(debug=True)
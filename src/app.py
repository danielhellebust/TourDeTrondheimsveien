import dash_leaflet as dl
import dash
from dash import html, Input, Output
import gpxpy
import gpxpy.gpx
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import random

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

lov_mild =[
'Bli itj nå fæst uten skinnvæst',
'Bli itj nå fin uten mokkasin',
'Bli itj nå fart uten bart',
'Får itj råna uten Ascona',
'Bli itj nå trønder-rock uten tennis-sokk',
'Bli itj nå barsk uten karsk',
'Du e itj kvass uten adidas',
'Du veit ka du får, med bleika hår',
'Du e itj så racer uten blæzer',
'Det bli itj svin-hett uten alpefett',
'Du får itj klådd uten sodd',
'Du bli itj pula uten Bula',
'Du bli homofil med japansk bil',
'Det bli itj nå knullings uten rullings',
'Det bli itj nå liv uten kniv',
'Ho bli itj fin uten brennevin',
'Du e itj kar før du bli tatt i radar',
'Du e itj kar hvis du syns at Tore Strømøy e rar',
'Det bli itj døll så læng du har øl',
'Det e itj nå håp uten grønnsåp',
'Det bli itj nå vilt hvis du itj har kilt',
'Du får itj rota hvis rutan itj e sota',
'Du e itj rett hvis du kjem fra Klett',
'Du e itj millionær før du kjøpe sukker og gjær',
'Du e litt på jorde hvis du digge Tore På Spore',
]

lov_mid = [
'Det e bare å flytt hvis du itj følle med på Midt-Nytt',
'Du bli itj idrettsmainn uten spritkainn',
'Du bli itj tøff som Rocky før du legg an en skikkeli hockey',
'Du får itj læs kart når du e svart',
'Du e liten uten spriten',
'Du e litt rar hvis du tømme dæ i en ainna kar',
'Det bli itj nå fæst uten prest',
'Det e itj klær hvis det itj e laga av lær',
'Bli itj nå trøst uten hængbrøst',
'Deinn bli itj stiv uten underliv',
'Det bli itj nå mus uten snus',
'Deinn skli lettar in me vaselin',
'Du får itj gå før du hi fått stå',
'Det bli itj nå sorg om du hold med rosenborg',
'Du e itj naken, før du vise fræm staken!',
'Det bli itj nå mus uten Rohypnol å brus',
'Du e itj helt me om du fortsatt digge Tande P',
'Saken e i boks om du har bartevoks',
'Du får itj pul når du itj har vaska dæ siden jul',
'Du e litt uavslutta om du e mann og like gutta',
'Du må drekk meir om du kjenne at synet bli beir',
'Det e itj tøft før du våkne i ei grøft',
'Du e itj full om du e i stand te å knull',
'Du e mistilpassa når du itj har hår på brøstkassa',
'Du e tøffar enn toget om du høre på han Åge',
]

lov_grov = [
"Det bli fart på rattet me smårips'n i krattet",
'Du e itj mannj før du har lært dæ å bannj',
'Det bli itj no darlings me klær fra Carlings',
'Det e itj no fæst om du itj havne i fyllearrest',
'Du e litt femi om du hete Kurt Remi',
"Det bli itj no sphænk ut'n bil me sænk",
'Du e itj nå tess hvis du ikke kjøre mokasiner te dress',
'Du e itj sprø uten fuggelfrø',
"Du blir itj knall ut'n kjall",
'E itj orntli vors om du itj må reng røde kors',
'Du treng itj nå mus hvis du kjøre trailer med grus',
'Ska du ha dametække må du dra brække',
'Det e litt flaut om du itj kan å braut',
"Når du har sopp på taska e det på tide å få'n vaska",
"Det e itj no tess ut'n grilldress",
'Du e heit når du e småfeit',
'E du søring e du itj verdt ein femtiøring',
'Du e verdig om du får stå mens du sjer på RBK',
"Du e itj klar før du får'n hard av å sjå ein ainna kar bar",
"Du e itj kar hves du itj får'n hard",
'Du blir itj snasen uten skrå opp nasen',
"Du sjer berre svin hves du itj' dunke bensin",
"Du får itj no skreppa ut'n ein pris under leppa",
"Det blir itj' mus uten siestabrus",
"Bruke du trus kan du glømm å få dæ mus",
]



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
    style={'width': '375px', 'height': '440px', 'margin': "auto", "display": "block"},
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
    dcc.Store(id="store2", data=[5,10,15,21,26,32,37,42,48,55,62,70,75,82,100]),
    dbc.Alert("Husk å kjøpe pizza på neste stopp, du er halvveis!!", id="alert-pizza", is_open=False, duration=10000,
              style={'width': '375px', 'height': '70px', 'margin': "auto", "display": "block"}),
    dbc.Alert("Bare 3 stopp igjen, hold ut du klarer det!", id="alert-3stopp", is_open=False, duration=10000,
              style={'width': '375px', 'height': '50px', 'margin': "auto", "display": "block"}),
    dbc.Alert("Du ankommer SISTE stopp, Gratulerer med gjennomført Tour de Trondheimsveien 2023!",
              id="alert-final", is_open=False, duration=10000,
              style={'width': '375px', 'height': '70px', 'margin': "auto", "display": "block"}),
    dbc.Alert(children = "", id="vits", is_open=False, duration=4000,
              style={'width': '375px', 'height': '70px', 'margin': "auto", "display": "block"}),
    dbc.Progress(id='progress',label="1øl 2øl 3øl 4øl 5øl 6øl 7øl 8øl 9øl 10øl 11øl 12øl 13øl 14øl I mål",
                 color= 'success',
                 value=10,
                 style={'width': '375px', 'height': '20px', 'margin': "auto", "display": "block"}),
    dbc.Button(children="Neste Bar", id="next", color="primary", className="mr-1", n_clicks=0,
               style={'width': '375px', 'height': '50px', 'margin': "auto", "display": "block"}),

    dbc.Button(children="Gi meg en trøndervits", id="vits_button", color="success", className="mr-1", n_clicks=0,
               style={'width': '375px', 'height': '50px', 'margin': "auto", "display": "block"}),

    dbc.Button(children="Reset", id="reset", color="danger", className="mr-1", n_clicks=0,
                style={'width': '375px', 'height': '35px', 'margin': "auto", "display": "block"},
               disabled=True),

])

@app.callback(
    [Output("vits", "children"),
     Output("vits", "is_open")],
    [Input("vits_button", "n_clicks")])

def update_vits(n_clicks):
    if n_clicks == 0:
        return "", False
    else:
        return random.choice(lov_grov), True

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
    Output("next", "children"),
    Output("reset", "disabled"),

    ],
    [Input("next", "n_clicks"),
     Input("reset", "n_clicks"),
     Input("store", "data"),
     Input("store2", "data"),
     ])

def update_map(n_clicks, reset_clicks,live_pub,progress_value):
    alert_pizza = False
    alert_3stopp = False
    alert_final = False
    reset_button = True

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
            reset_button = False

    print(live_pub)
    try:
        next_text = "Gå til Neste Bar : " + live_pub[1]
    except:
        next_text = "Siste Stopp er nådd"


    if reset_clicks == 0:
        return polyline_list_return, center_location_return, store_data_return, n_clicks, 0, progress_value_return, \
               alert_pizza, alert_3stopp, alert_final, next_text, reset_button
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
        return polyline_list_return, center_location_return, store_data_return, 0, 0, 0, alert_pizza, alert_3stopp, alert_final, next_text, reset_button

    else:
        store_data_return = original_pub
        polyline_list_return.append(dl.Marker(position=pub_dict[original_pub[0]],
                                               children=[dl.Tooltip(original_pub[0], permanent=True), dl.Popup(original_pub[0])]))
        return polyline_list_return, center_location_return, store_data_return, 0, 0, 0, alert_pizza, alert_3stopp, alert_final, next_text, reset_button








if __name__ == '__main__':
    app.run_server(debug=True)
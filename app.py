import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# This is a third-party library that makes it easy to write responsive, well-styled apps
# Documentation: https://dash-bootstrap-components.opensource.faculty.ai/docs/
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
from urllib.request import urlopen

# TODO: Automatic import of data from the HDX API for daily updates.
# TODO: Figure out why choropleth is so slowww... maybe geojson is too big?
# TODO: Add data upload date to graph tooltip.

token = open(".mapbox-token").read()
app = dash.Dash(external_stylesheets=[dbc.themes.LITERA])

server = app.server


with urlopen('https://www.geoboundaries.org/data/geoBoundariesCGAZ-3_0_0/ADM0/simplifyRatio_10/geoBoundariesCGAZ_ADM0.geojson') as response:
    countries = json.load(response)

def layout():
    """
    Wrapping this in a function makes it easier to write the layout. All that's
    happening here is that a card is being defined. 
    So in the final product, you see a card with a header, some body text, and a graph.

    There is also a dropdown that controls the type of visual, and the options are 
    populated with a list comprehension.
    """

    columns = [
        'Children in Need', 
        'IDPs', 
        'People in Food Crisis/Emergency (IPC phase 3+)', 
        'People Targeted for Assistance',
        'Schools Closed due to Insecurity'
        ]

    navbar = dbc.NavbarSimple(
        brand="Global Crisis Figures",
        brand_href="#",
        color="primary",
        dark=True,
    )

    card = dbc.Card(
        dbc.CardBody(
            [
                html.P(
                    "Select a crisis type to see up-to-date figures at a country level. This data is curated by the ReliefWeb editorial team based on its relevance to the humanitarian community.",
                    className="card-text",
                ),
                dbc.Select(
                    id="selector",
                    options=[
                        {"label": column, "value": column}
                        for column in columns
                    ],
                    value="IDPs",
                    placeholder="Select a crisis...",
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(id="graph")),
                        dbc.Col(dcc.Graph(id="map")),
                    ]
                ),                
            ]
        ),
    )

    items = dbc.Container(
        [card, dcc.Store(id="data-store"), dcc.Location(id="url"),], className="p-5",
    )

    page = html.Div([
        navbar,
        items
    ])

    return page


app.layout = layout()


@app.callback(
    Output("graph", "figure"),
    [Input("selector", "value"), Input("data-store", "data")],
)
def make_graph(crisis_type, data):
    # So this callback is to generate the appropriate graph from the data.
    # We're saying that whenever the source data or the user input changes,
    # we want to update the graph. 
    # graph_type = the option selected from the dropdown
    # data = the data in the data-store

    df = pd.DataFrame(data)
    df_sel = df[df.figure_name == crisis_type]
    df_sel = df_sel.sort_values(by='figure_value', ascending=True)
    fig = px.bar(
        df_sel, 
        y='crisis_name', 
        x='figure_value', 
        orientation='h', 
        labels={
            'crisis_name': 'Country',
            'figure_value': 'Count'
        },
        color_discrete_sequence=['#eb5b34'],
        template='simple_white')
    return fig

@app.callback(
    Output("map", "figure"), 
    [Input("selector", "value"), Input("data-store", "data")])
def display_choropleth(crisis_type, data):
    # Creating the choropleth map with the same data as the bar chart.

    # TODO: Function to select the data so this doesn't have to be repeated.
    df = pd.DataFrame(data)
    df_sel = df[df.figure_name == crisis_type]
    fig = px.choropleth(
        df_sel, 
        color='figure_value',
        locations="crisis_iso3",
        color_continuous_scale=px.colors.sequential.Redor,
        locationmode='ISO-3',
        projection='natural earth')
    return fig

@app.callback(
    Output("data-store", "data"), 
    [Input("url", "pathname")])
def populate_data(pathname):
    # In this callback, you could hit an API endpoint where the data comes from.
    # If the data is coming from some API that refreshes daily, it would make sense to
    # pull from there. The data refresh could also be run as a script as part of the app.
    # This function is triggered on page load, and it would be wise to make this function
    # as lightweight as possible to make the page load faster.

    return pd.read_csv('data/crises-figures.csv').to_dict()

if __name__ == "__main__":
    app.run_server(debug=True)


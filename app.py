import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# This is a third-party library that makes it easy to write responsive, well-styled apps
# Documentation: https://dash-bootstrap-components.opensource.faculty.ai/docs/
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# TODO: Automatic import of data from the HDX API for daily updates.
# TODO: Choropleth map visualization. 


app = dash.Dash(external_stylesheets=[dbc.themes.LITERA])

server = app.server


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
        ]

    navbar = dbc.NavbarSimple(
        brand="Current Crisis Figures",
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
                    value=0,
                    placeholder="Select a crisis...",
                ),
                dcc.Graph(id="graph"),
            ]
        ),
    )

    items = dbc.Container(
        [card, dcc.Store(id="data-store"), dcc.Location(id="url"),], className="p-5",
    )

    page = html.Div([
        navbar,
        items,
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
    return px.bar(df_sel, y='crisis_name', x='figure_value', orientation='h')

@app.callback(Output("data-store", "data"), [Input("url", "pathname")])
def populate_data(pathname):
    # In this callback, you could hit an API endpoint where the data comes from.
    # If the data is coming from some API that refreshes daily, it would make sense to
    # pull from there. The data refresh could also be run as a script as part of the app.
    # This function is triggered on page load, and it would be wise to make this function
    # as lightweight as possible to make the page load faster.

    return pd.read_csv('data/crises-figures.csv').to_dict()

if __name__ == "__main__":
    app.run_server(debug=True)


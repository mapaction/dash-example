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

card_style = {
    "borderRadius": "0px",
    "boxShadow": "rgba(0, 0, 0, 0.05) 0px 0px 5px 2px",
    "marginTop": "20px",
}


def layout():
    """
    Wrapping this in a function makes it easier to write the layout. All that's
    happening here is that a card is being defined.
    So in the final product, you see a card with a header, some body text, and a graph.

    There is also a dropdown that controls the type of visual, and the options are
    populated with a list comprehension.
    """

    # TODO: Load this from the options in the spreadsheet
    columns = [
        "Children in Need",
        "IDPs",
        "People in Food Crisis/Emergency (IPC phase 3+)",
        "People Targeted for Assistance",
        "Schools Closed due to Insecurity",
    ]

    navbar = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/ma_logo.png", height="75px")),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "Global Crisis Figures Dashboard",
                            )
                        ),
                    ],
                    align="center",
                    no_gutters=False,
                ),
                href="https://mapaction.org/",
            ),
        ],
        color="#19458D",
        dark=True,
    )

    title = html.P(
        "This dashboard contains key figures (topline numbers) on the world's most pressing humanitarian crises. Select a crisis type to see up-to-date figures at a country level. This data is curated by the ReliefWeb editorial team based on its relevance to the humanitarian community.",
        className="card-text",
    )

    selector = dcc.Dropdown(
        id="selector",
        options=[{"label": column, "value": column} for column in columns],
        value="IDPs",
        placeholder="Select a crisis...",
        style=card_style,
    )

    fig1 = dbc.Card(
        style=card_style,
        children=[
            dbc.CardBody(dcc.Graph(id="graph"), style={"padding": "10px"}),
        ],
    )
    fig2 = dbc.Card(
        style=card_style,
        children=[
            dbc.CardBody(dcc.Graph(id="map"), style={"padding": "10px"}),
        ],
    )

    figures = dbc.Row(
        [
            dbc.Col(fig1),
            dbc.Col(fig2),
        ]
    )

    table = dbc.Card(style=card_style, id="table-card")

    items = dbc.Container(
        [
            title,
            selector,
            figures,
            table,
            dcc.Store(id="data-store"),
            dcc.Location(id="url"),
        ],
        className="p-5",
        style={"padding": "15px"},
    )

    page = html.Div([navbar, html.Div(items, style={"backgroundColor": "#F2F2F2"})])

    return page

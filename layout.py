import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

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

    table_text = html.P(
        "The full dataset for the selected crisis is shown in the table below. The data source for each country is linked in the entry in the 'Source' column of the table.",
        className="card_text",
        style={"marginTop": "20px"},
    )

    table = dbc.Card(style=card_style, id="table-card")

    items = dbc.Container(
        [
            title,
            selector,
            figures,
            table_text,
            table,
            dcc.Store(id="data-store"),
            dcc.Location(id="url"),
        ],
        className="p-5",
        style={"padding": "15px"},
    )

    page = html.Div([html.Div(items, style={"backgroundColor": "#F2F2F2"})])

    return page

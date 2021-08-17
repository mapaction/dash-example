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
from layout import layout

from hdx.utilities.easy_logging import setup_logging
from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset


# TODO: Automatic import of data from the HDX API for daily updates.
# TODO: Better mapbox map

token = open(".mapbox-token").read()
app = dash.Dash(external_stylesheets=[dbc.themes.LITERA])

server = app.server

setup_logging()


with urlopen(
    "https://www.geoboundaries.org/data/geoBoundariesCGAZ-3_0_0/ADM0/simplifyRatio_10/geoBoundariesCGAZ_ADM0.geojson"
) as response:
    countries = json.load(response)


app.layout = layout()


@app.callback(
    [
        Output("graph", "figure"),
        Output("map", "figure"),
        Output("table-card", "children"),
    ],
    [Input("selector", "value"), Input("data-store", "data")],
)
def display_figs(crisis_type, data):

    df = pd.DataFrame(data)
    df_sel = df[df.figure_name == crisis_type].sort_values(
        by="figure_value", ascending=False
    )

    # Create the bar chart
    fig_bar = px.bar(
        df_sel.head(5).sort_values(by="figure_value", ascending=True),
        y="crisis_name",
        x="figure_value",
        orientation="h",
        labels={"crisis_name": "Country", "figure_value": "People affected"},
        color_discrete_sequence=["#E53D2F"],
        template="simple_white",
        title="Top crisis affected countries",
    )

    # Create the choropleth map
    fig_map = px.choropleth(
        df_sel,
        color="figure_value",
        locations="crisis_iso3",
        color_continuous_scale=px.colors.sequential.Redor,
        locationmode="ISO-3",
        projection="natural earth",
        title="Location of affected countries",
    )
    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # Create the table
    df_sel.figure_source = df_sel.apply(
        lambda x: html.A(
            html.P(x["figure_source"]), href=x["figure_url"], target="_blank"
        ),
        axis=1,
    )

    df_sel_table = df_sel[
        ["crisis_name", "figure_value", "figure_source", "figure_date"]
    ].rename(
        columns={
            "crisis_name": "Country",
            "figure_value": "People affected",
            "figure_source": "Source",
            "figure_date": "Last updated",
        }
    )

    table = dbc.Table.from_dataframe(
        df_sel_table, striped=False, bordered=True, hover=True
    )

    return fig_bar, fig_map, table


@app.callback(
    [Output("data-store", "data"), Output("selector", "options")],
    [Input("url", "pathname")],
)
def populate_data(pathname):
    # In this callback, you could hit an API endpoint where the data comes from.
    # If the data is coming from some API that refreshes daily, it would make sense to
    # pull from there. The data refresh could also be run as a script as part of the app.
    # This function is triggered on page load, and it would be wise to make this function
    # as lightweight as possible to make the page load faster.

    Configuration.create(
        hdx_site="prod", user_agent="mapaction-dash-example", hdx_read_only=True
    )
    dataset = Dataset.read_from_hdx("reliefweb-crisis-figures")
    print(dataset.get_dataset_date())

    df = pd.read_csv("data/crises-figures.csv")
    crises = df.figure_name.unique()
    options = [{"label": column, "value": column} for column in crises]

    return df.to_dict(), options


if __name__ == "__main__":
    app.run_server(debug=True)

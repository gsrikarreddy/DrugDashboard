# pages/drug_analysis.py
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px

from utils.data import generate_fake_data, generate_dummy_county_mentions, generate_dummy_posts
from utils.layout_components import make_posts_table

dash.register_page(__name__, path_template="/drug/<drug_name>")

geojson_url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"

layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Div([
        dcc.Link("← Back to Home", href="/", className="back-link")
    ], style={'textAlign': 'left'}),

    html.H2(id='drug-title', style={'textAlign': 'center'}),

    html.Div([
        dcc.Graph(id='drug-trend-graph', style={'flex': 2}),
        html.Div(id='top-posts-table', style={'flex': 1, 'padding': '10px', 'maxHeight': '400px', 'overflowY': 'scroll'})
    ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '30px'}),

    dcc.Graph(id='hotspot-map')
])

@dash.callback(
    Output('drug-title', 'children'),
    Output('drug-trend-graph', 'figure'),
    Output('hotspot-map', 'figure'),
    Output('top-posts-table', 'children'),
    Input('url', 'pathname')
)
def display_drug_analysis(pathname):
    drug = pathname.split("/")[-1]
    df_trend = generate_fake_data(drug)

    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(x=df_trend['Date'], y=df_trend['Mentions'], mode='lines+markers', name=drug))
    line_fig.update_layout(title=f"Trend of {drug}", xaxis_title="Date", yaxis_title="Mentions", template="plotly_white")

    df_posts = generate_dummy_posts(drug)
    table_html = make_posts_table(df_posts)

    df_county = generate_dummy_county_mentions(drug)
    map_fig = px.choropleth(df_county, geojson=geojson_url, locations="fips", color="Mentions", scope="usa", color_continuous_scale="Blues")
    map_fig.update_traces(marker_line_width=0)
    map_fig.update_layout(title="County-level Mentions (Simulated)", geo=dict(lakecolor="white", bgcolor="white"), height=600)

    return f"Drug Analysis: {drug}", line_fig, map_fig, table_html

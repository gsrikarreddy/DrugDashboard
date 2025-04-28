import dash
from dash import dcc, html, Input, Output
import json
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from utils.layout_components import drug_emoji_table




from utils.data import generate_dummy_trending
dash.register_page(__name__, path="/")

# Load drug names from JSON
with open("data/chemical_list_email.json", "r") as f:
    drug_data = json.load(f)
drug_names = list(drug_data.keys())

layout = html.Div([
    html.H1("DOD Drug Detection Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select a Drug for Detailed Analysis", className="label"),
        dcc.Dropdown(
            id='drug-dropdown',
            options=[{'label': name, 'value': name} for name in drug_names],
            placeholder="Choose a drug"
        ),
        html.Div(id='selected-drug-text', className="selected-drug-text")
    ], className="centered-box"),

    html.Div([
        html.Label("Select Trending View", className="label"),
        dcc.RadioItems(
            id='time-range',
            options=[
                {'label': 'Weekly', 'value': 'weekly'},
                {'label': 'Monthly', 'value': 'monthly'},
                {'label': 'Yearly', 'value': 'yearly'}
            ],
            value='monthly',
            labelStyle={'display': 'inline-block', 'marginRight': '20px'}
        )
    ], className="radio-box"),

    # 🆕 Line Chart and Pie Chart side by side
    html.Div([
        dcc.Graph(id='trending-line-chart', style={'width': '70%', 'height': '500px'}),
        dcc.Graph(id='trending-pie-chart', style={'width': '30%', 'height': '400px'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'start', 'gap': '20px', 'marginBottom': '30px'}),

    # 🆕 Keyword Chart and Emoji Table side by side
    html.Div([
        dcc.Graph(id='keyword-bar-chart', style={'width': '60%', 'height': '500px'}),
        html.Div(
            drug_emoji_table(["Fentanyl", "Xylazine", "Metonitazene", "Flubromazepam", "MDMA"]),
            style={'width': '40%', 'padding': '20px'}
        )
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'start', 'gap': '20px', 'marginBottom': '30px'}),

    dcc.Location(id='redirect', refresh=True)
])




@dash.callback(
    [Output('trending-line-chart', 'figure'),
     Output('trending-pie-chart', 'figure')],
    Input('time-range', 'value')
)
def update_trending_graph(selected_range):
    df = generate_dummy_trending(selected_range)

    line_fig = go.Figure()
    for col in df.columns[1:]:
        line_fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df[col],
            mode='lines+markers',
            name=col
        ))
    line_fig.update_layout(
        title=f"Top 5 Trending Drugs ({selected_range.capitalize()})",
        xaxis_title='Date',
        yaxis_title='Mentions',
        template='plotly_white'
    )

    total_mentions = df.drop(columns='Date').sum()
    pie_fig = go.Figure(data=[go.Pie(
        labels=total_mentions.index,
        values=total_mentions.values,
        hole=0.4
    )])
    pie_fig.update_layout(
        title="Total Mentions Distribution (Top 5 Drugs)",
        template='plotly_white'
    )

    return line_fig, pie_fig


@dash.callback(
    Output('keyword-bar-chart', 'figure'),
    Input('time-range', 'value')
)
def update_keywords_chart(selected_range):
    np.random.seed(hash(selected_range) % 9999)
    keywords = [f"#trend{i}" for i in range(10)]
    counts = np.random.randint(30, 200, size=10)

    df_kw = pd.DataFrame({
        'Keyword': keywords,
        'Mentions': counts
    }).sort_values(by='Mentions', ascending=True)

    fig = go.Figure(go.Bar(
        x=df_kw['Mentions'],
        y=df_kw['Keyword'],
        orientation='h',
        marker_color='lightskyblue'
    ))

    fig.update_layout(
        title='Top Keywords / Hashtags',
        xaxis_title='Mentions',
        template='plotly_white',
        margin=dict(l=80, r=10, t=40, b=40)
    )

    return fig


@dash.callback(
    Output('redirect', 'pathname'),
    Input('drug-dropdown', 'value'),
    Input('trending-line-chart', 'clickData'),
    Input('time-range', 'value'),
    prevent_initial_call=True
)
def redirect_based_on_selection(drug, clickData, selected_range):
    # Case 1: Dropdown selection
    if drug:
        return f"/drug/{drug}"

    # Case 2: Line chart click
    if clickData:
        clicked_drug = clickData['points'][0]['curveNumber']
        df = generate_dummy_trending(selected_range)  # match the selected trending range
        drug_names = list(df.columns[1:])
        if 0 <= clicked_drug < len(drug_names):
            selected_drug = drug_names[clicked_drug]
            return f"/drug/{selected_drug}"

    # Default: No update
    return dash.no_update


import dash
from dash import dcc, html, Input, Output
import json
import plotly.graph_objs as go
import pandas as pd
import numpy as np

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

    dcc.Graph(id='trending-line-chart'),

    html.Div([
        dcc.Graph(id='trending-pie-chart', style={'width': '50%'}),
        dcc.Graph(id='keyword-bar-chart', style={'width': '50%'})
    ], style={'display': 'flex', 'justifyContent': 'center'}),

    dcc.Location(id='redirect', refresh=True)
])


@dash.callback(
    Output('redirect', 'pathname'),
    Input('drug-dropdown', 'value')
)
def go_to_drug_page(drug):
    if drug:
        return f"/drug/{drug}"
    return dash.no_update


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
    Output('selected-drug-text', 'children'),
    Input('drug-dropdown', 'value')
)
def show_selected_drug(drug):
    return f"Selected Drug: {drug}" if drug else ""

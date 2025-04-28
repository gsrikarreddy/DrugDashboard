from dash import html
import random
from utils.data import DRUG_EMOJIS

def make_posts_table(df):
    return html.Div([
        html.H3("Recent Posts", style={'textAlign': 'center'}),
        html.Table([
            html.Thead(html.Tr([
                html.Th("Time"),
                html.Th("Post")
            ])),
            html.Tbody([
                html.Tr([
                    html.Td(row["Time"]),
                    html.Td(row["Post"])
                ]) for _, row in df.iterrows()
            ])
        ], style={
            'width': '100%',
            'borderCollapse': 'collapse'
        })
    ], style={
        'width': '90%',
        'margin': 'auto',
        'border': '1px solid #ccc',
        'borderRadius': '10px',
        'overflow': 'hidden',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
        'padding': '20px',
        'marginTop': '30px',
        'backgroundColor': '#fff'
    })

def drug_emoji_table(drug_list):
    return html.Div([
        html.H3("Top Drugs (Emoji Version)", style={'textAlign': 'center'}),
        html.Table([
            html.Thead(html.Tr([
                html.Th("Drug Name"),
                html.Th("Emoji")
            ])),
            html.Tbody([
                html.Tr([
                    html.Td(drug),
                    html.Td(
                        " ".join(random.sample(DRUG_EMOJIS.get(drug, ["❓"]), k=2))

                    )
                ]) for drug in drug_list
            ])
        ], style={
            'width': '60%',
            'margin': 'auto',
            'border': '1px solid #ccc',
            'borderRadius': '10px',
            'overflow': 'hidden',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            'marginTop': '30px'
        })
    ])

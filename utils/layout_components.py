from dash import html

def make_posts_table(df):
    return html.Table([
        html.Thead(html.Tr([
            html.Th("User"),
            html.Th("Time"),
            html.Th("Post")
        ])),
        html.Tbody([
            html.Tr([
                html.Td(row["User"]),
                html.Td(row["Time"]),
                html.Td(row["Post"])
            ]) for _, row in df.iterrows()
        ])
    ])

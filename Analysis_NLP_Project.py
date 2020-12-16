import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

app = dash.Dash()
app.title = 'NLP Project'
server = app.server


data = pd.read_csv('sentiment_score_final_V213.csv')
data['political_lean_rescaled'].replace('', np.nan, inplace=True)
data.dropna(subset=['political_lean_rescaled'], inplace=True)
data['text'] = '<a href=\"' +  data['Url'] + '\">' + '_</a>'.format("Text")
df = pd.DataFrame({"x":data['pos'].to_list(),
                  "y":data['neg'].to_list(),
                   "hover":data['Title'].to_list(),
                   "compound":data['compound'].to_list(),
                   "engagement":data['Total Engagement'].to_list(),
                   "share":data['Total Shares'].to_list(),
                   "conv":data['Total Conversations'].to_list(),
                    "lean":data['political_lean_rescaled'].to_list(),
                   "text":data['text'].to_list()})
data_index  = data.copy()
data_index.set_index('Domain', inplace=True)
options = []
for domain in data_index.index:
    options.append({'label':'{}'.format(domain), 'value':domain})

# Create a Dash layout that contains a Graph component:
app.layout = html.Div([
    # html.Div([
    #     html.H3('Select News Source:', style={'paddingRight': '30px'}),
    #     dcc.Dropdown(
    #         id='my_ticker_symbol',
    #         options=options,
    #         value=['breitbart.com'],
    #         multi=True
    #     ) ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%'}),
    # html.Div([
    #     html.Button(
    #         id='submit-button',
    #         n_clicks=0,
    #         children='Submit',
    #         style={'fontSize':24, 'marginLeft':'30px'}
    #     ),
    # ], style={'display':'inline-block'}),
dcc.Graph(
        id='Fig0',
        figure={
            'data': [
                go.Scatter(x=df["lean"],
                           y=df["compound"],
                           mode="markers+text",
                           # Just pick one of the two
                           hovertext=df["hover"],
                           text=df["text"],
                           textposition="top center",
                           textfont_size=4,
                           marker=dict(
                               size=7,
                               color=df["compound"],  # set color equal to a variable
                               colorscale='tropic',  # one of plotly colorscales
                               showscale=True
                           )
                )
            ],
            'layout': go.Layout(
                title='Alexa Top Website Sentiment Score',  # Graph title
                xaxis=dict(title='<---Leanness---->'),  # x-axis label
                yaxis=dict(title='<---Negative Sentiment-----0-----Positive Sentiment---->'),  # y-axis label
            )
        }
    ),
    dcc.Graph(
        id='Fig1',
        figure={
            'data': [
                go.Scatter(x=df["x"],
                           y=df["y"],
                           mode="markers+text",
                           # Just pick one of the two
                           hovertext=df["hover"],
                           text=df["text"],
                           textposition="top center",
                           textfont_size=4,
                           marker=dict(
                               size=7,
                               color=df["compound"],  # set color equal to a variable
                               colorscale='tropic',  # one of plotly colorscales
                               showscale=True
                           )
                )
            ],
            'layout': go.Layout(
                title='Alexa Top Website Sentiment Score',  # Graph title
                xaxis=dict(title='<---Positive Score---->'),  # x-axis label
                yaxis=dict(title='<---Negative Score---->'),  # y-axis label
            )
        }
    ),

    dcc.Graph(
        id='Fig2',
        figure={
            'data': [
                go.Scatter(x=df["compound"],
                           y=df["engagement"],
                           mode="markers+text",
                           # Just pick one of the two
                           hovertext=df["hover"],
                           text=df["text"],
                           textposition="top center",
                           textfont_size=4,
                           marker=dict(
                               size=7,
                               color=df["compound"],  # set color equal to a variable
                               colorscale='electric',  # one of plotly colorscales
                               showscale=True
                           ))
            ],
            'layout': go.Layout(
                title='Alexa Top Website Popularity vs Sentiment Score',  # Graph title
                xaxis=dict(title='<---Negative Sentiment-----0-----Positive Sentiment---->'),  # x-axis label
                yaxis=dict(title='<---Popularity Score---->'),  # y-axis label
            )
        }
    ),
    dcc.Graph(
        id='Fig3',
        figure={
            'data': [
                go.Scatter(x=df["compound"],
                           y=df["conv"],
                           mode="markers+text",
                           hovertext=df["hover"],
                           text=df["text"],
                           textposition="top center",
                           textfont_size=4,
                           marker=dict(
                               size=7,
                               color=df["compound"],
                               colorscale='Viridis',
                               showscale=True
                           ))
            ],
            'layout': go.Layout(
                title='Alexa Top Website Number of Conversation vs Sentiment Score',  # Graph title
                xaxis=dict(title='<---Negative Sentiment-----0-----Positive Sentiment---->'),  # x-axis label
                yaxis=dict(title='<---Number of Conversation---->'),  # y-axis label
            )
        }
    ),
    dcc.Graph(
        id='Fig4',
        figure={
            'data': [
                go.Scatter(x=df["compound"],
                           y=df["share"],
                           mode="markers+text",
                           hovertext=df["hover"],
                           text=df["text"],
                           textposition="top center",
                           textfont_size=4,
                           marker=dict(
                               size=7,
                               color=df["compound"],  # set color equal to a variable
                               colorscale='rainbow',  # 'Viridis', # one of plotly colorscales
                               showscale=True
                           ))
            ],
            'layout': go.Layout(
                title='Alexa Top Website Total Share vs Sentiment Score',  # Graph title
                xaxis=dict(title='<---Negative Sentiment-----0-----Positive Sentiment---->'),  # x-axis label
                yaxis=dict(title='<---Number of time story Shared---->'),  # y-axis label
            )
        }
    )
])
# Add the server clause:
if __name__ == '__main__':
    app.run_server()

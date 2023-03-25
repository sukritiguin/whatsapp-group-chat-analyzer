import base64
import io

import matplotlib.pyplot as plt

import dash
from dash import Dash,html,dcc
from dash.dependencies import Input, Output, State
import pandas as pd

import plotly.graph_objs as go
import plot_utilities
import utilities

global df
df = pd.DataFrame()
chat_df = None

import preprocessing

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div("Select Date and Time formar first then upload chat"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div([
        html.Label('Select date format:'),
        dcc.RadioItems(
            id='date-format',
            options=[
                {'label': 'dd/mm/yyyy', 'value': '123'},
                {'label': 'mm/dd/yyyy', 'value': '213'}
            ],
            value='123',
            labelStyle={'display': 'inline-block', 'margin': '10px'}
        ),
        html.Label('Select time format:'),
        dcc.RadioItems(
            id='time-format',
            options=[
                {'label': '24hr', 'value': '24hr'},
                {'label': '12hr', 'value': '12hr'}
            ],
            value='24hr'
        ),
    ]),

    # user vs total message
    html.Div(id='output-data'),
    html.H2("User vs. Total Message Plot",style={
        'color':'green'
    }),
    html.H3("Select Chart Type : "),
    dcc.RadioItems(
        id='chart-type',
        options=[
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Pie Chart', 'value': 'pie'},
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Scatter Chart', 'value': 'scatter'},
            {'label': 'Bubble Plot', 'value' : 'bubble'}
        ],
        value='bar'
    ),
    dcc.Graph(id='user_vs_total_message_chart'),


    # user vs total message deleted

    html.H2("User vs. Total Deleted Message Plot", style={
        'color': 'green'
    }),
    html.H3("Select Chart Type : "),
    dcc.RadioItems(
        id='chart-type-user-vs-total-deleted-message',
        options=[
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Pie Chart', 'value': 'pie'},
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Scatter Chart', 'value': 'scatter'},
            {'label': 'Bubble Plot', 'value': 'bubble'}
        ],
        value='bar'
    ),
    dcc.Graph(id='user_vs_total_deleted_message_chart'),

    # user vs total media sent

    html.H2("User vs. Total Media Plot", style={
        'color': 'green'
    }),
    html.H3("Select Chart Type : "),
    dcc.RadioItems(
        id='chart-type-user-vs-total-media',
        options=[
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Pie Chart', 'value': 'pie'},
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Scatter Chart', 'value': 'scatter'},
            {'label': 'Bubble Plot', 'value': 'bubble'}
        ],
        value='bar'
    ),
    dcc.Graph(id='user_vs_total_media_chart'),

    # Sunbust Graph
    html.H2("Sunbust Graph",
            style={
                'color':'green'
            }),
    dcc.RadioItems(
        id='year_month_weekday_user_totalMessage_Sunburst_chart_show',
        options=[
            {'label': "Don't Show Chart", 'value': '0'},
            {'label': 'Show Chart', 'value':'1'}
        ]
    ),
    dcc.Graph(id='year_month_weekday_user_totalMessage_Sunburst_chart'),

    # Most used emoji

    html.H2("Most Used Emoji",
            style={
                'color':'green'
            }),
    dcc.RadioItems(
        id='emoji_df_show',
        options=[
            {'label': "Don't Show Chart", 'value': '0'},
            {'label': 'Show Chart', 'value': '1'}
        ]
    ),
    dcc.Graph(id='emoji_df_chart'),

    # Word Cloud
    html.H2("Word Cloud of Messages",
            style={
                'color':'green'
            }),
    dcc.RadioItems(
        id='word_cloud_show',
        options=[
            {'label': "Don't Show Chart", 'value': '0'},
            {'label': 'Show Chart', 'value': '1'}
        ],
        value='0'
    ),
    # dcc.Graph(id='word_cloud_messages_chart')
    html.Div(id='output-image')
])

@app.callback(Output('output-data', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('date-format', 'value'),
              State('time-format', 'value'))
def update_output(contents, filename, date_format, time_format):
    if contents is not None:
        content_type, content_string = contents.split(',')

        file_content = contents.encode("utf8").split(b";base64,")[1]
        decoded = base64.decodebytes(file_content).decode('utf-8')
        lines = decoded.splitlines()

        df = pd.DataFrame()
        try:
            if 'txt' in filename:
                if time_format=="12hr":
                    df = preprocessing.f12(lines,day_ind=int(date_format[0]),month_ind=int(date_format[1]),year_ind=int(date_format[2]))
                else:
                    df = preprocessing.f24(lines, day_ind=int(date_format[0]), month_ind=int(date_format[1]),
                                           year_ind=int(date_format[2]))
                global chat_df
                chat_df = df
        except Exception as e:
            print("ERROR",e)
        # return utilities.show_table_df(df)
        return "DF generated"




@app.callback(
    Output('user_vs_total_deleted_message_chart', 'figure'),
    Input('chart-type-user-vs-total-deleted-message', 'value')
)
def update_chart(chart_type):
    global chat_df
    # print(chat_df[:5])
    df_new = utilities.get_user_vs_total_deleted_message_df(chat_df)
    # print(df_new)
    if chart_type == 'bar':
        return plot_utilities.bar_plotting(df=df_new,x='user',y='total_deleted_message',title="",x_title="",y_title="")
    elif chart_type == 'pie':
        return plot_utilities.pie_plotting(df=df_new,x='user',y='total_deleted_message',title="")
    elif chart_type == 'line':
        return plot_utilities.line_plotting(df=df_new,x='user',y='total_deleted_message',title_="",x_title="",y_title="")
    elif chart_type == 'scatter':
        return plot_utilities.scatter_ploting(df=df_new,x='user',y='total_deleted_message',x_title="",y_title="",title="")
    else:
        return plot_utilities.bubble_ploting(df=df_new,x='user',y='total_deleted_message',x_title="",y_title="",title="")


@app.callback(
    Output('user_vs_total_message_chart', 'figure'),
    Input('chart-type', 'value')
)
def update_chart(chart_type):
    global chat_df
    # print(chat_df[:5])
    df_new = utilities.get_user_vs_total_message_df(chat_df)
    # print(df_new)
    if chart_type == 'bar':
        return plot_utilities.bar_plotting(df=df_new,x='user',y='message',title="",x_title="",y_title="")
    elif chart_type == 'pie':
        return plot_utilities.pie_plotting(df=df_new,x='user',y='message',title="")
    elif chart_type == 'line':
        return plot_utilities.line_plotting(df=df_new,x='user',y='message',title_="",x_title="",y_title="")
    elif chart_type == 'scatter':
        return plot_utilities.scatter_ploting(df=df_new,x='user',y='message',x_title="",y_title="",title="")
    else:
        return plot_utilities.bubble_ploting(df=df_new,x='user',y='message',x_title="",y_title="",title="")


@app.callback(
    Output('user_vs_total_media_chart', 'figure'),
    Input('chart-type-user-vs-total-media', 'value')
)
def update_chart(chart_type):
    global chat_df
    # print(chat_df[:5])
    df_new = utilities.get_user_vs_total_media_df(chat_df)
    # print(df_new)
    if chart_type == 'bar':
        return plot_utilities.bar_plotting(df=df_new,x='user',y='total_media',title="",x_title="",y_title="")
    elif chart_type == 'pie':
        return plot_utilities.pie_plotting(df=df_new,x='user',y='total_media',title="")
    elif chart_type == 'line':
        return plot_utilities.line_plotting(df=df_new,x='user',y='total_media',title_="",x_title="",y_title="")
    elif chart_type == 'scatter':
        return plot_utilities.scatter_ploting(df=df_new,x='user',y='total_media',x_title="",y_title="",title="")
    else:
        return plot_utilities.bubble_ploting(df=df_new,x='user',y='total_media',x_title="",y_title="",title="")

@app.callback(
    Output('year_month_weekday_user_totalMessage_Sunburst_chart','figure'),
    Input('year_month_weekday_user_totalMessage_Sunburst_chart_show','value')
)
def update_chart(isShow):
    if isShow=='0':return go.Figure()
    global chat_df
    return plot_utilities.year_month_weekday_user_totalMessage_Sunburst(df=chat_df)


@app.callback(
    Output('emoji_df_chart','figure'),
    Input('emoji_df_show','value')
)
def update_chart(isShow):
    if isShow == '0': return go.Figure()
    global chat_df
    emoji_df = utilities.get_emoji_df(df=chat_df)
    return plot_utilities.pie_plotting(df=emoji_df,x="emoji",y="count",title="Emoji vs. Number of times sent")

@app.callback(Output('output-image', 'children'),
              [Input('word_cloud_show', 'value')])
def update_chart(input_value):
    if input_value=='0':
        return "Generating Word Cloud"
    global chat_df
    print("Generating")
    word_cloud = plot_utilities.get_word_cloud(df=chat_df)
    # Save the wordcloud as an image
    img = io.BytesIO()
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.savefig(img, format='png')
    plt.close()

    # Encode the image to base64 and display it in the app
    encoded_image = base64.b64encode(img.getvalue()).decode('utf-8')
    temp = html.Div([
        html.H4("Word Cloud Generated:"),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image))
    ])
    print("Generated")
    return temp

if __name__ == '__main__':
    app.run_server(debug=True)
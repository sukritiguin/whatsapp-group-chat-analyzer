import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px
import colorsys
from dash.dependencies import Input, Output

# Load data
# df = pd.read_csv('whatsapp_chat.csv')
df = pd.read_csv("sukriti_chat.csv")
df = df[df['date'] != '00/00/0000']
df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d')
df['time'] = pd.to_datetime(df['time'], format='%H:%M').dt.time

# Define the number of colors to generate
num_colors = 100

# Define the saturation and value (brightness) for the colors
saturation = 0.6
value = 0.9

# Generate the colors using the hue value
colors = []
for i in range(num_colors):
    hue = float(i) / num_colors
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    color = "#{:02x}{:02x}{:02x}".format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
    colors.append(color)

# Define the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    # html.H1("WhatsApp Chat Analysis", style={'text-align': 'center'}),
    # html.Br(),
    # html.Label("Select a date range:"),
    # dcc.DatePickerRange(
    #     id='date-picker-range',
    #     min_date_allowed=df['date'].min(),
    #     max_date_allowed=df['date'].max(),
    #     start_date=df['date'].min(),
    #     end_date=df['date'].max(),
    #     display_format='MMM Do, YYYY',
    #     style={'margin': '10px'}
    # ),
    # dcc.Graph(id='message-counts-graph', style={'height': '500px'})

    html.H1("WhatsApp Chat Analysis", style={'text-align': 'center'}),
    html.Br(),
    html.Label("Select a date range:"),
    dcc.DatePickerRange(
        id='date-picker-range',
        min_date_allowed=df['date'].min(),
        max_date_allowed=df['date'].max(),
        start_date=df['date'].min(),
        end_date=df['date'].max(),
        display_format='MMM Do, YYYY',
        style={'margin': '10px'}
    ),
    dcc.Graph(id='message-counts-graph', style={'height': '500px'}),
    html.Div(id='table-container', style={'margin-top': '30px'})
])

"""
# Define the callback function for the scatter plot
@app.callback(
    Output('message-counts-graph', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)


def update_graph(start_date, end_date):
    # Filter the data based on the date range
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Group the chat messages by user and day
    grouped = filtered_df.groupby(['user', pd.Grouper(key='date', freq='D')])

    # Count the number of messages per day and user
    daily_counts = grouped.size().reset_index(name='counts')

    # Create a scatter plot of the daily message counts
    fig = px.scatter(daily_counts, x='date', y='counts', color='user',
                     color_discrete_sequence=colors, title="Daily Message Counts",
                     hover_data={'user': True, 'date': '|%b %d, %Y'})

    fig.update_traces(mode='markers+lines')
    fig.update_layout(hovermode='x unified', hoverlabel=dict(bgcolor='white', font_size=12))
    fig.update_xaxes(showspikes=True, spikemode='across', spikethickness=1, spikecolor='black', spikesnap='cursor')
    fig.update_yaxes(showspikes=True, spikemode='across', spikethickness=1, spikecolor='black', spikesnap='cursor')

    return fig
"""




# Define the callback function for the scatter plot
@app.callback(
    Output('message-counts-graph', 'figure'),
    Output('hovermode-store', 'data'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_graph(start_date, end_date):
    # Filter the data based on the date range
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Group the chat messages by user and day
    grouped = filtered_df.groupby(['user', pd.Grouper(key='date', freq='D')])

    # Count the number of messages per day and user
    daily_counts = grouped.size().reset_index(name='counts')

    # Create a scatter plot of the daily message counts
    fig = px.scatter(daily_counts, x='date', y='counts', color='user',
                     color_discrete_sequence=colors, title="Daily Message Counts",
                     hover_data={'user': True, 'date': '|%b %d, %Y'})

    fig.update_traces(mode='markers+lines')
    fig.update_layout(hovermode='x unified', hoverlabel=dict(bgcolor='white', font_size=12))
    fig.update_xaxes(showspikes=True, spikemode='across', spikethickness=1, spikecolor='black', spikesnap='cursor')
    fig.update_yaxes(showspikes=True, spikemode='across', spikethickness=1, spikecolor='black', spikesnap='cursor')

    # Store the hovermode in the app's store
    hovermode = fig['layout']['hovermode']
    store_data = {'hovermode': hovermode}

    return fig, store_data


# Define the callback function for the table
@app.callback(
    Output('date-range-table', 'children'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('hovermode-store', 'data')
)
def update_table(start_date, end_date, store_data):
    # Extract the hovermode from the app's store
    hovermode = store_data['hovermode']

    # Create a table with the selected date range and hovermode
    table = html.Table([
        html.Tr([html.Th('Selected Date Range:'), html.Td('{} - {}'.format(start_date, end_date))]),
        html.Tr([html.Th('Selected Hover Mode:'), html.Td(hovermode)])
    ], style={'margin': '20px auto'})

    return table


# Define the app layout
app.layout = html.Div([
    html.H1("WhatsApp Chat Analysis", style={'text-align': 'center'}),
    html.Br(),
    html.Label("Select a date range:"),
    dcc.DatePickerRange(
        id='date-picker-range',
        min_date_allowed=df['date'].min(),
        max_date_allowed=df['date'].max(),
        start_date=df['date'].min(),
        end_date=df['date'].max(),
        display_format='MMM Do, YYYY',
        style={'margin': '10px'}
    ),
    dcc.Graph(id='message-counts-graph', style={'height': '500px'}),
    html.Div(id='date-range-table'),
    dcc.Store(id='hovermode-store')
])


# Run the app
if __name__ == '__main__':
    app.run_server(port=8050)

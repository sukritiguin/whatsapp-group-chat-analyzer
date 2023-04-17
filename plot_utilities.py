import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import emoji
import streamlit as st
from dash import Dash,dcc
import plotly.tools as tls

def bar_plotting(df,x,y,title,x_title,y_title):
    fig = px.bar(x=df[x], y=df[y],color=df[x])
    fig.update_xaxes(title=x_title)
    fig.update_yaxes(title=y_title)
    # set the background color to transparent
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title={
            'text': f"<b><span style='color: #fff;'>{title}</span></b>",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20},
            'y': 0.9,
            'pad': {'b': 10}
        },yaxis=dict(
            range=[0, max(df[y])+20]  # adjust the upper limit as needed
        )
    )
    # update the width of the bars
    fig.update_layout(
        barmode='group',  # specify that we want grouped bars
        bargap=0.2,  # set the gap between bars
        bargroupgap=0.1,  # set the gap between groups of bars
        width=1000,  # set the width of the chart
        height=500,  # set the height of the chart
        margin=dict(l=50, r=50, t=50, b=50)  # set the margins
    )
    fig.update_traces(width=0.5)
    # set the tick angle to 45 degrees
    fig.update_xaxes(tickangle=45)
    # fig.update_traces(width=10)
    # st.plotly_chart(fig)
    # fig.show()
    # return dcc.Graph(figure=fig)
    return fig


def pie_plotting(df,x,y,title):

    fig = px.pie(df, values=y, names=x)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    # set the background color to transparent
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title={
            'text': f"<b><span style='color: #fff;'>{title}</span></b>",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20},
            'y': 0.95,
            'pad': {'b': 10}
        }
    )
    # st.plotly_chart(fig)
    return fig

def scatter_ploting(df,x,y,x_title="",y_title="",title=""):
    fig = px.scatter(x=df[x], y=df[y],color=df[x])
    fig.update_xaxes(title=x_title)
    fig.update_yaxes(title=y_title)
    # set the background color to transparent
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title={
            'text': f"<b><span style='color: #fff;'>{title}</span></b>",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20},
            'y': 0.9,
            'pad': {'b': 10}
        }
    )
    # st.plotly_chart(fig)
    return fig

def area_ploting(df,x,y,x_title="",y_title="",title=""):
    # fig = px.area(x=group_by_user_message_df['user'], y=group_by_user_message_df['message'], color=group_by_user_message_df['user'])
    fig = px.area(df, x=x, y=y, color=x)
    fig.update_xaxes(title=x_title)
    fig.update_yaxes(title=y_title)
    # set the background color to transparent
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title={
            'text': f"<b><span style='color: #fff;'>{title}</span></b>",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20},
            'y': 0.9,
            'pad': {'b': 10}
        }
    )
    fig.update_traces(
    marker_coloraxis=None
    )
    # st.plotly_chart(fig)
    return fig

def bubble_ploting(df,x,y,x_title="",y_title="",title=""):
    # fig = px.scatter(x=group_by_user_message_df['user'], y=group_by_user_message_df['message'],color=group_by_user_message_df['user'])

    fig = px.scatter(df, x=x, y=y,
	         size=df[y], color=x)


    fig.update_xaxes(title=x_title)
    fig.update_yaxes(title=y_title)
    # set the background color to transparent
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title={
            'text': "<b><span style='color:#fff;'>User vs. Total Messages Scatter Plot</span></b>",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20},
            'y': 0.9,
            'pad': {'b': 10}
        }
    )
    # st.plotly_chart(fig)
    return fig



def line_plotting(df, x, y, title_, x_title, y_title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[x], y=df[y], mode='lines', name=y))

    fig.update_layout(
        title={
            'text': f"<b><span style='color: #000;'>{title_}</span></b>",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20},
            'y': 0.9,
            'pad': {'b': 10}
        },
        xaxis_title=x_title,
        yaxis_title=y_title,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def year_month_weekday_user_totalMessage_Sunburst(df):
    df['weekday'] = df['date'].dt.strftime('%A')
    # Group by year, month, weekday, and user
    grouped_df = df.groupby(['year', 'month', 'weekday','user']).count().reset_index()

    # Create sunburst chart
    fig = px.sunburst(grouped_df, path=['year', 'month', 'weekday', 'user'], values='message', color='message',
                    color_continuous_scale='RdYlBu_r', hover_data=['message'])
    # fig.update_layout(title='Year vs. Month vs. Total Messages Sunburst Chart')

    fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title={
                'text': "<b><span style='color: #fff;'>Year ➡ Month ➡ WeekDay ➡ User ➡ Total Messages Sunburst Chart</span></b>",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 20},
                'y': 0.95,
                'pad': {'b': 10}
            }
        )
    return fig



def get_word_cloud(df):
    all_messages = df['message']
    message = ""
    for m in all_messages:
        m = m.strip()
        if m=='<Media omitted>' or m=='This message was deleted' or m==' ':continue
        message += m+" "


    all_emoji = set()
    for ch in message:
        if emoji.is_emoji(ch):all_emoji.add(ch)

    for emoji_ in all_emoji:
        message = message.replace(emoji_,"")

    wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(message)

    # Display the generated image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    return wordcloud

    # # Save the image
    # plt.savefig("wordcloud.png")
    # # plt.show()
    # # return tls.mpl_to_plotly(plt)
    # plt.close()






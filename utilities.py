import numpy as np
import pandas as pd
import emoji
import re
import streamlit as st
import dash
from dash import Dash,html

def show_table_df(df):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(len(df))
        ])
    ])

def count_total_media_sent(df,user="all"):
    if user != 'all':
        df = df[df['user']==user]
    count = 0
    for message_ in df['message'].tolist():
        message_ = message_.strip().strip("\n")
        if '<Media omitted>' in message_:count+=1
    return count

def total_deleted_message(df,user='all'):
    if user != 'all':
        df = df[df['user']==user]
    messages = df['message']
    count = 0
    for message in messages:
        message = message.strip().strip("\n")
        if "This message was deleted" in message: count += 1
    return count

def get_user_vs_total_media_df(df):
    users = list(set(df['user'].tolist()))
    total_media = [count_total_media_sent(df,user) for user in users]

    user_vs_total_media_df = pd.DataFrame()
    user_vs_total_media_df['user'] = users
    user_vs_total_media_df['total_media'] = total_media
    return user_vs_total_media_df

def get_user_vs_total_deleted_message_df(df):
    users = list(set(df['user'].tolist()))
    total_deleted_message_list = [total_deleted_message(df,user) for user in users]

    user_vs_total_deleted_message_df = pd.DataFrame()
    user_vs_total_deleted_message_df['user'] = users
    user_vs_total_deleted_message_df['total_deleted_message'] = total_deleted_message_list
    return user_vs_total_deleted_message_df


def get_user_vs_total_message_df(df):
    try:
        df = df[['user','message']].groupby("user").count().reset_index()
    except:
        print("Error is occuring while converting to user vs total messages")
        df = pd.DataFrame()
    return df

def get_emoji_df(df):
    all_messages = df['message']
    message = ""
    for m in all_messages:
        m = m.strip()
        if m=='<Media omitted>' or m=='This message was deleted':continue
        message += m

    emoji_map = {}
    for ch in message:
        if emoji.is_emoji(ch):
            if ch not in emoji_map.keys():
                emoji_map[ch]=1
            else:
                emoji_map[ch] += 1

    emoji_df = pd.DataFrame.from_dict(emoji_map,orient='index').reset_index()
    emoji_df = emoji_df.rename(columns={"index":"emoji",0:"count"})
    return emoji_df




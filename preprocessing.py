import pandas as pd
import re
import numpy as np

def f12(chat, day_ind=1, month_ind=2, year_ind=3):
    def check_is_date(s, ind):
        return ind < len(s) and ((s[ind] >= '0' and s[ind] <= '9') or (s[ind] == '/'))

    # Read the chat file
    # with open(file_name, 'r', encoding="utf8") as file:
    #     chat = file.readlines()

    # chat = file_name.read().decode('utf-8').splitlines()
    # with file_name as f:
    #     chat = f.readlines()

    # chat = file_name.readlines()

    new_chat = []
    for curr in chat:
        if check_is_date(curr, 0) and check_is_date(curr, 1) and check_is_date(curr, 2) and check_is_date(curr,3) and check_is_date(curr, 4) and check_is_date(curr, 5):
            new_chat += [curr]
        else:
            new_chat[-1] = new_chat[-1] + curr
    chat = new_chat

    # Create empty lists for each column
    dates = []
    times = []
    users = []
    messages = []

    # Loop through each line of the chat file and extract the relevant data
    for line in chat:
        # if line.strip():
        try:
            # Extract date, time, user, and message
            datetime, message = line.strip().split(' - ', maxsplit=1)
            # Checking that if any one changed the group name
            pattern = '(.*) changed the subject from "(.*)" to "(.*)"'
            pattern_result = re.search(pattern, message)
            if pattern_result: continue

            date, time = datetime.split(', ')
            user, message = message.split(': ', maxsplit=1)
        except ValueError:
            message = line.strip()
            continue

        # Append the extracted data to the corresponding list
        dates.append(date)
        times.append(time)
        users.append(user)
        messages.append(message)

    # Create a pandas dataframe with the extracted data
    df = pd.DataFrame({
        'date': dates,
        'time': times,
        'user': users,
        'message': messages
    })

    # convert time column to datetime object
    df['time'] = pd.to_datetime(df['time'], format='%I:%M %p')

    # format time column to 24-hour time
    df['time'] = df['time'].dt.strftime('%H:%M')

    # extract day, month, and year from date column and create new columns
    df[['day', 'year']] = df['date'].str.split('/', n=2, expand=True)[[day_ind - 1, year_ind - 1]]
    df['day'] = df['day']
    df['year'] = df['year']

    months_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']
    month = []

    for date in df['date']:
        try:
            m = date.split("/", maxsplit=2)[month_ind - 1]
            m = int(m)
            month.append(months_list[m - 1])
        except:
            month.append(None)
    df['month'] = month

    df.dropna(inplace=True)
    df = df[df['date'] != '00/00/0000']
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

    return df


def f24(chat, day_ind=2, month_ind=1, year_ind=3):
    # check_is_date
    def check_is_date(s, ind):
        return ind < len(s) and ((s[ind] >= '0' and s[ind] <= '9') or (s[ind] == '/'))

    # Creating date object with 2 digit day, 2 digit month, 4 digit year
    # year_ind = 3
    # month_ind = 1
    # day_ind = 2

    def get_4_digit_year_month_day(date):
        year_ind = 3
        if len(date.split("/")[year_ind - 1]) != 4:
            date_list = date.split("/")
            date = date_list[0] + "/" + date_list[1] + "/" + "20" + date_list[2]
        if len(date.split("/")[month_ind - 1]) != 2:
            date_list = date.split("/")
            date = date_list[0] + "/" + "0" + date_list[1] + "/" + date_list[2]
        if len(date.split("/")[day_ind - 1]) != 2:
            date_list = date.split("/")
            date = "0" + date_list[0] + "/" + date_list[1] + "/" + date_list[2]
        return date

    def get_perfect_date(date: str) -> str:
        day, month, year = "00", "00", "0000"
        try:
            if day_ind == 1 and month_ind == 2 and year_ind == 3:
                day, month, year = date.split("/")
            elif day_ind == 1 and month_ind == 3 and year_ind == 2:
                day, year, month = date.split("/")
            elif day_ind == 2 and month_ind == 1 and year_ind == 3:
                month, day, year = date.split("/")
            elif day_ind == 3 and month_ind == 1 and year_ind == 2:
                month, year, day = date.split("/")
            elif day_ind == 2 and month_ind == 3 and year_ind == 1:
                year, day, month = date.split("/")
            elif day_ind == 3 and month_ind == 2 and year_ind == 1:
                year, month, day = date.split("/")
        except:
            pass

        if len(day) == 1: day = "0" + day
        if len(month) == 1: month = "0" + month
        if len(year) == 2: year = "20" + year

        return day + "/" + month + "/" + year

    # read the chat file
    # with open(file_name, 'r', encoding="utf8") as f:
    #     chat = f.readlines()

    # chat = file_name.read().decode('utf-8').splitlines()

    new_chat = []
    for curr in chat:
        check = True
        for i in range(6): check = check & check_is_date(curr, i);
        if check:
            new_chat += [curr]
        else:
            new_chat[-1] = new_chat[-1] + curr
    chat = new_chat

    # create empty lists for each column
    date = []
    time = []
    user = []
    messages = []

    # loop through each line of the chat file and extract the relevant information
    for line in chat:
        try:
            # split the line by the first occurrence of ' - '
            datetime, message = line.split(' - ', maxsplit=1)

            # Checking that if any one changed the group name
            pattern = '(.*) changed the subject from "(.*)" to "(.*)"'
            pattern_result = re.search(pattern, message)
            if pattern_result: continue

            # extract the date, time, and user from the datetime string
            date_string, time_string = datetime.split(', ', maxsplit=1)
            user_string, message = message.split(': ', maxsplit=1)

            # time_string = pd.to_datetime(time_string, format='%I:%M %p').strftime('%H:%M')

            # append the extracted information to their respective lists
            date.append(date_string)
            time.append(time_string.strip())
            user.append(user_string)
            messages.append(message)
        except:
            # print(line)
            # if there is an error, append NaN values to the lists
            date.append(pd.NaT)
            time.append(pd.NaT)
            user.append(pd.NaT)
            messages.append(pd.NaT)

    # create the dataframe from the lists
    df = pd.DataFrame({'date': date, 'time': time, 'user': user, 'message': messages})

    # drop any rows with missing values
    # df.dropna(inplace=True)

    # reset the index of the dataframe
    df.reset_index(drop=True, inplace=True)

    df['date'] = df['date'].apply(get_perfect_date)

    # extract day, month, and year from date column and create new columns
    months_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']
    df[['day', 'year']] = df['date'].str.split('/', n=2, expand=True)[[0, 2]]
    df['day'] = df['day'].astype(int)
    df['year'] = df['year'].astype(int)

    month = []
    for date in df['date']:
        try:
            m = date.split("/", maxsplit=2)[1]
            m = int(m)
            month.append(months_list[m - 1])
        except:
            month.append(None)
    df['month'] = month

    df = df[df['date'] != '00/00/0000']
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

    return df
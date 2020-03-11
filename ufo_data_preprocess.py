import pandas as pd

from datetime import datetime, timedelta

def data_preprocess(filename):
    df = pd.read_csv(filename, error_bad_lines=False)

    new_datetime = []
    new_year = []
    new_month = []
    new_day = []
    for date in df['datetime']:
        if date[-5:-3] == '24':
            date = date[:-5] + '0' + date[-3:]
            date = datetime.strptime(date, '%m/%d/%Y %H:%M') + timedelta(days=1)
        else:
            date = datetime.strptime(date, '%m/%d/%Y %H:%M')

        new_datetime.append(date)
        new_year.append(str(date.year))
        new_month.append(str(date.month))
        new_day.append(str(date.day))

    df['datetime'] = new_datetime
    df['year'] = new_year
    df['month'] = new_month
    df['day'] = new_day

    new_posted = []

    for date in df['date posted']:
        date = datetime.strptime(date, '%m/%d/%Y')
        new_posted.append(date)

    df['date posted'] = new_posted

    hours = []

    for date in df['datetime']:
        hours.append(date.hour)

    df['time'] = hours


    duration = []
    for du in df['duration (seconds)']:
        try:
            duration.append(float(du))
        except:
            print(du)
            duration.append(float(du[:-1]))
    df['duration (seconds)'] = duration

    new_datetime = []
    for date in df['datetime']:
        day = str(date.month) + '/' + str(date.day)
        new_datetime.append(day)
    df['monAndDay'] = new_datetime

    new_datetime = []
    for date in df['datetime']:
        day = str(date.month) + '/' + str(date.day) + '/' + str(date.year)
        new_datetime.append(day)
    df['monADayAYear'] = new_datetime

    df_us = df[df['country'] == 'us']

    return df_us


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from wordcloud import WordCloud



sns.set_style("whitegrid")

def clean(x):
    x = x.lower()
    if x[-1] in ['.', ',', ')', '\"']:
        x = x[:-1]
    return x

def func(x):
    try:
        word_list = x.split(' ')
        word_list = list(map(clean, word_list))
        return word_list
    except:
        pass

def funcshape(vals):
    vals = round(vals, 1)
    return f'{vals} %'

def data_wordcloud(df,city=''):
    if(city is not ''):
        df_tmp = df[df['city'] == city]
    else:
        df_tmp = df
    # word_list = []
    # for line in df['comments']:
    #     try:
    #         word_list = word_list + line.split(' ')
    #     except:
    #         pass
    word_lists = list(map(func, list(df_tmp['comments'])))
    out = []
    for word_list in word_lists:
        try:
            out += word_list
        except:
            pass
    freq_dict = dict(pd.Series(out).value_counts())
    stop_words = list(stopwords.words('english'))
    stop_words2 = ['saw', 'shaped', 'seen', 'like', 'two', '3', 'across', 'one', '2', 'shape', 'three', 'pd))',
                   '((nuforc', 'looked', 'around', 'near', '20', 'made'
                                                                 'observed', '5', '4', 'minutes', '-', 'looking',
                   'away', 'area', 'went', 'time', 'noticed', 'seconds', '', 'came', 'changed', 'pm', 'could', 'second',
                   'going', 'direction', 'see', 'witnessed', 'possible', 'side', 'light', '&amp;', 'feet', 'us',
                   'changing', 'four', 'close', 'altitude', 'right', 'ca',
                   'several', 'left', 'towards', '1', 'note:', 'min', '30', 'extremely', '6', '10', 'size', 'mile',
                   'ft', 'times', 'hour', 'approximately', 'pa', 'almost']
    stop_words = stop_words + stop_words2
    keys = list(freq_dict.keys())

    for word in keys:
        if word in stop_words:
            # removing stopwords
            del freq_dict[word]

        # merging singular and plural of the same word
        if len(word) > 1 and word[-1] == 's' and word[:-1] in keys:
            try:
                freq_dict[word[:-1]] += freq_dict[word]
                del freq_dict[word]
            except:
                pass
    freq_sorted = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
    wordcloud = WordCloud(width=2000, height=1000).generate_from_frequencies(freq_dict)


    plt.figure(figsize=(20, 15))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def show_freq_by_shape(df):
    #1 all
    print("shape")
    plt.figure(figsize=(16, 16), dpi=100)

    shape = df['shape'].value_counts().keys()
    values = df['shape'].value_counts().values
    print(shape)
    explode = [0, .1, .1, .1, .1]
    colors = ['grey', 'red', 'orange', 'green', 'blue']

    shape2 = ['others/unknown']
    values2 = np.zeros(5)
    for i in range(len(shape)):
        if shape[i] in ['light', 'triangle', 'circle', 'formation']:
            shape2.append(shape[i])
            values2[['light', 'triangle', 'circle', 'formation'].index(shape[i]) + 1] += values[i]
        else:
            values2[0] += values[i]



    plt.pie(values2, labels=shape2, explode=explode, shadow=True, textprops=dict(color="black", fontsize=30),
            autopct=lambda ptc: funcshape(ptc),
            startangle=90, colors=colors)
    # plt.setp(autotexts, size=30, weight="bold")
    plt.show()

    #2 pie tinley park

    # plt.figure(figsize=(16, 16), dpi=100)

    shape = df[df['city'] == 'tinley park']['shape'].value_counts().keys()
    values = df[df['city'] == 'tinley park']['shape'].value_counts().values

    shape2 = ['others/unknown']
    values2 = np.zeros(5)
    for i in range(len(shape)):
        if shape[i] in ['light', 'triangle', 'circle', 'formation']:
            shape2.append(shape[i])
            values2[['light', 'triangle', 'circle', 'formation'].index(shape[i]) + 1] += values[i]
        else:
            values2[0] += values[i]



    colors = ['grey', 'red', 'orange', 'green', 'blue']

    plt.pie(values2, labels=shape2, explode=explode, shadow=True, textprops=dict(color="black", fontsize=30),
            autopct=lambda ptc: funcshape(ptc),
            startangle=90, colors=colors)

    plt.show()


def show_freq_by_city(df):
    citystate = []
    for i in range(len(df['city'])):
        try:
            citystate.append(df['city'][i] + ', ' + df['state'][i])
        except:
            citystate.append(float('nan'))

    df['city, state'] = citystate

    #1 not normalized
    plt.figure(figsize=(16, 16), dpi=100)

    cities = df['city, state'].value_counts().keys()[:10]
    # cities = list(map(lambda x: x[0].upper() + x[1:], cities))
    values = df['city, state'].value_counts().values[:10]

    by_city = sns.barplot(cities, values)
    by_city.tick_params(labelsize=30)
    plt.setp(by_city.get_xticklabels(), rotation=45)

    plt.title('Frequency by city', fontdict={'fontsize': 40})
    plt.ylabel('Frequency', fontdict={'fontsize': 30})
    plt.show()

    #2 Frequency by City (3 special day removed)
    pop_list = [3059393, 3629114, 1886011, 12150996, 2956746, 1849898, 4944332, 8608208, 843168, 5502379, 1510516,
                741318,
                1362416, 1723634, 3281212, 1664496, 2374203, 1758210, 5429524, 215304, 1368035, 18351295, 3629114,
                1249442, 5121892,
                183012, 1487483, 2150706, 56204, 1065219]
    pop_dict = dict(zip(list(df['city, state'].value_counts()[:30].keys()), pop_list))
    mask1 = (df['month'] == '7') & (df['day'] == '4')
    mask2 = (df['month'] == '12') & (df['day'] == '31')
    mask3 = (df['month'] == '1') & (df['day'] == '1')

    mask = ((1 - mask1) * (1 - mask2) * (1 - mask3)).astype(bool)
    # mask = (1-mask1).astype(bool)

    df2 = df[mask]

    temp = (list(df2['city, state'].value_counts()[:30].keys()), [0] * 30)
    pop_dict2 = dict(zip(*temp))
    for city in pop_dict.keys():
        if city in pop_dict2.keys():
            pop_dict2[city] = pop_dict[city]

    pop_dict2['spokane, wa'] = 573493

    pop_list2 = list(pop_dict2.values())
    # remove July 4, December 31 and January 1st


    # %8
    # remove July 4

    plt.figure(figsize=(16, 16), dpi=100)

    cities = df2['city, state'].value_counts().keys()[:10]
    # cities = list(map(lambda x: x[0].upper() + x[1:], cities))
    values = df2['city, state'].value_counts().values[:10]

    by_city = sns.barplot(cities, values)
    by_city.tick_params(labelsize=30)
    plt.setp(by_city.get_xticklabels(), rotation=45)

    plt.title('Frequency by city (Jul 4 / Dec 31 / Jan 1 Removed)', fontdict={'fontsize': 40})
    plt.ylabel('Frequency', fontdict={'fontsize': 30})
    plt.show()


    #3  Frequency (Normalized by Urban Population)
    plt.figure(figsize=(16, 16), dpi=100)

    cities = df['city, state'].value_counts().keys()[:30]
    # cities = list(map(lambda x: x[0].upper() + x[1:], cities))
    values = df['city, state'].value_counts().values[:30]
    values = values / np.array(pop_list)

    city_dict = {}
    for i in range(30):
        city_dict[cities[i]] = values[i]

    # combine phoenix & mesa, portland & vancouver
    city_dict['phoenix, az'] += city_dict['mesa, az']
    city_dict['portland, or'] += city_dict['vancouver, wa'] * pop_list[(cities == 'vancouver, wa').argmax()] / pop_list[(cities == 'portland, or').argmax()]
#KeyError: 'vancouver, wa'

    city_dict = dict(sorted(city_dict.items(), key=lambda x: x[1], reverse=True))

    del city_dict['vancouver, wa'], city_dict['mesa, az']

    # by_city = sns.barplot(cities, values)
    by_city = sns.barplot(list(city_dict.keys())[:10], list(city_dict.values())[:10])
    by_city.tick_params(labelsize=30)
    plt.setp(by_city.get_xticklabels(), rotation=45)

    plt.title('Frequency by city (Normalized)', fontdict={'fontsize': 40})
    plt.ylabel('Frequency (times / population)', fontdict={'fontsize': 30})
    plt.show()

    #4 Frequency (Normalized by Urban Population, 3 special days are removed)
    plt.figure(figsize=(16, 16), dpi=100)


    cities = df2['city, state'].value_counts().keys()[:30]
    # cities = list(map(lambda x: x[0].upper() + x[1:], cities))
    values = df2['city, state'].value_counts().values[:30]
    values = values / np.array(pop_list2)

    # ValueError: operands could not be broadcast together with shapes (30,) (31,)

    city_dict = {}
    for i in range(30):
        city_dict[cities[i]] = values[i]

    # combine phoenix & mesa, portland & vancouver
    city_dict['phoenix, az'] += city_dict['mesa, az']
    city_dict['portland, or'] += city_dict['vancouver, wa'] * pop_list2[(cities == 'vancouver, wa').argmax()] / \
                                 pop_list2[(cities == 'portland, or').argmax()]

    city_dict = dict(sorted(city_dict.items(), key=lambda x: x[1], reverse=True))

    # del city_dict['vancouver, wa'], city_dict['mesa, az']

    # by_city = sns.barplot(cities, values)
    by_city = sns.barplot(list(city_dict.keys())[:10], list(city_dict.values())[:10])
    by_city.tick_params(labelsize=30)
    plt.setp(by_city.get_xticklabels(), rotation=45)

    plt.title('Frequency by city (Normalized, Jul 4/Dec 31/Jan 1 Removed)', fontdict={'fontsize': 40})
    plt.ylabel('Frequency (times / population)', fontdict={'fontsize': 30})
    plt.show()


def show_freq_by_date(df):
    plt.figure(figsize=(16, 16), dpi=100)

    dt = df['datetime'].value_counts().keys()[:50]
    values = df['datetime'].value_counts().values[:50]

    by_dt = sns.barplot(list(dt), values)
    plt.setp(by_dt.get_xticklabels(), rotation=45)

    plt.title('Frequency by Specific Date and Time')
    plt.ylabel('Frequency')
    plt.show()

    # %5 date with year

    plt.figure(figsize=(16, 16), dpi=100)

    dt = []
    for date in df['datetime']:
        dt.append(date.date())

    df['date'] = dt

    dt = df['date'].value_counts().keys()[:10]
    values = df['date'].value_counts().values[:10]

    by_dt = sns.barplot(dt, values)
    by_dt.tick_params(labelsize=30)
    plt.setp(by_dt.get_xticklabels(), rotation=45)

    plt.title('Frequency by Date (with Year)', fontdict={'fontsize': 40})
    plt.ylabel('Frequency', fontdict={'fontsize': 30})
    plt.show()

    # %6 date without year

    plt.figure(figsize=(16, 16), dpi=100)

    dt = []
    for date in df['datetime']:
        d = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][
                date.month - 1] + ' ' + str(100 + date.day)[1:]
        # d = str(100 + date.month)[1:] + '-' + str(100+date.day)[1:]
        dt.append(d)

    df['date w/o year'] = dt

    dt = df['date w/o year'].value_counts().keys()[:10]
    values = df['date w/o year'].value_counts().values[:10]

    by_dt = sns.barplot(dt, values)
    by_dt.tick_params(labelsize=30)
    plt.setp(by_dt.get_xticklabels(), rotation=45)

    plt.title('Frequency by Date (without Year)', fontdict={'fontsize': 40})
    plt.ylabel('Frequency', fontdict={'fontsize': 30})
    plt.show()

    months = df['month']
    months = pd.Series(months).value_counts()

    months_ = months.keys()
    values = months.values

    plt.figure(figsize=(16, 16), dpi=100)
    by_m = sns.barplot(months_, values)
    by_m.tick_params(labelsize=20)
    plt.setp(by_m.get_xticklabels(), rotation=45)

    plt.title('Frequency by Month', fontdict={'fontsize': 30})
    plt.ylabel('Frequency', fontdict={'fontsize': 20})
    plt.show()


    days = df['day']
    days = pd.Series(days).value_counts()

    days_ = days.keys()
    values = days.values

    plt.figure(figsize=(16, 16), dpi=100)
    by_d = sns.barplot(days_, values)
    by_d.tick_params(labelsize=20)
    plt.setp(by_d.get_xticklabels(), rotation=45)

    plt.title('Frequency by Day', fontdict={'fontsize': 30})
    plt.ylabel('Frequency', fontdict={'fontsize': 20})
    plt.show()


    hours = df['time']


    hours = pd.Series(hours).value_counts()

    hours_ = hours.keys()
    values = hours.values

    plt.figure(figsize=(16, 16), dpi=100)
    by_h = sns.barplot(hours_, values)
    by_h.tick_params(labelsize=20)
    plt.setp(by_h.get_xticklabels(), rotation=45)

    plt.title('Frequency by Time', fontdict={'fontsize': 30})
    plt.ylabel('Frequency', fontdict={'fontsize': 20})
    plt.show()





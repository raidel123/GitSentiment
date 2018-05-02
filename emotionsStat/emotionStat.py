#!/usr/bin/env python

import sys
import os
import pandas as pd
import json
import sqlite3 as sqlite
from texttable import Texttable
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import norm


# get main project path (in case this file is compiled alone)

if os.name == 'nt':
    # Windows
    context = os.getcwd().split('\\')
else:
    # Ubuntu
    context = os.getcwd().split('/')

if context[-1] == 'emotionsStat':
    context = '/'.join(context[:-1])
else:
    context = os.getcwd()

db_location = context + '/sentimentAnalysis/whole_database_new.db'
db_connection = sqlite.connect(db_location)

# Paper: Section 3.1A
# assume table is a list of dictionaries

# get data from table
# import to pandas
# use pandas for displaying statistical data, and display bar graph
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.describe.html
def EmotionsProject():

    print "Emotions Average/proportion score per project:\n"

    projectEmotion = {}
    top6 = []

    df = pd.read_sql_query("SELECT project_name, sentiment_pos, sentiment_neg FROM commit_sentiments;", db_connection)

    for index, row in df.iterrows():
        if row['project_name'] in projectEmotion:
            projectEmotion[row['project_name']].append(float(row['sentiment_pos']) + float(row['sentiment_neg']))
        else:
            projectEmotion[row['project_name']] = [float(row['sentiment_pos']) + float(row['sentiment_neg'])]

    for key in sorted(projectEmotion,  key=lambda k: len(projectEmotion[k]), reverse=True)[:6]:
        print 'mean:', norm.stats(projectEmotion[key], moments='ms')
        print 'mean:', stats.tmean(projectEmotion[key])
        print 'std dev:', stats.tstd(projectEmotion[key])
        top6.append([key, reduce(lambda x, y: x + y, projectEmotion[key]) / len(projectEmotion[key]), len(projectEmotion[key])])

    print "Top 6\n"

    t = Texttable()
    t.add_rows([['Project', 'Emotion Score Average', 'Commits']] + top6)
    print t.draw()

    # objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
    objects = [val[0] for val in top6]
    y_pos = np.arange(len(objects))
    performance = [val[1] for val in top6]

    colors = ['g', 'g', 'g', 'g', 'g', 'g']
    plt.bar(y_pos, performance, align='center', alpha=0.5, color=colors)
    plt.xticks(y_pos, objects)
    plt.ylabel('Emotion score average')
    plt.title('Fig 1. Emotion Score Average Per Project')

    plt.show()

    return top6

    # TODO: Create matplot for these stats

# TODO
# Paper: Section 3.1B, proportion of comment emotion types per project
# assume table is a list of dictionaries
# get data from table
# import to pandas
# use pandas for displaying statistical data using bar graph
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.describe.html
def EmotionsProjectProportion():
    print "Emotions Average/proportion score per project:\n"

    projectEmotion = {}
    # projectEmotion = {'negative':0, 'neutral':0, 'positive':0}
    top6 = []

    df = pd.read_sql_query("SELECT project_name, sentiment_pos, sentiment_neg FROM commit_sentiments;", db_connection)

    for index, row in df.iterrows():
        if row['project_name'] not in projectEmotion:
            projectEmotion[row['project_name']] = {'negative':[], 'neutral':[], 'positive':[]}

        emotion = float(row['sentiment_pos']) + float(row['sentiment_neg'])
        if emotion < 1.0:
            projectEmotion[row['project_name']]['negative'].append(emotion)
        elif emotion > 1.0:
            projectEmotion[row['project_name']]['positive'].append(emotion)
        else:
            projectEmotion[row['project_name']]['neutral'].append(emotion)

    for key in sorted(projectEmotion,  key=lambda k: (len(projectEmotion[k]['negative']) + len(projectEmotion[k]['neutral']) + len(projectEmotion[k]['positive'])), reverse=True)[:6]:

        neg_val = float(len(projectEmotion[key]['negative'])) / float(len(projectEmotion[key]['negative']) + len(projectEmotion[key]['neutral']) + len(projectEmotion[key]['positive']))
        neut_val = float(len(projectEmotion[key]['neutral'])) / float(len(projectEmotion[key]['negative']) + len(projectEmotion[key]['neutral']) + len(projectEmotion[key]['positive']))
        pos_val = float(len(projectEmotion[key]['positive'])) / float(len(projectEmotion[key]['negative']) + len(projectEmotion[key]['neutral']) + len(projectEmotion[key]['positive']))

        '''
        print 'neg:', neg_val
        print 'neut:', neut_val
        print 'pos:', pos_val

        if len(projectEmotion[key]['negative']) != 0:
            neg_val = reduce(lambda x, y: x + y, projectEmotion[key]['negative']) / len(projectEmotion[key]['negative'])

        if len(projectEmotion[key]['neutral']) != 0:
            net_val = reduce(lambda x, y: x + y, projectEmotion[key]['neutral']) / len(projectEmotion[key]['neutral'])

        if len(projectEmotion[key]['positive']) != 0:
            pos_val = reduce(lambda x, y: x + y, projectEmotion[key]['positive']) / len(projectEmotion[key]['positive'])
        '''

        top6.append([key, neg_val, neut_val, pos_val])


    print "Top 6\n"

    t = Texttable()
    t.add_rows([['Project', 'Negative', 'Neutral', 'Positive']] + top6)
    print t.draw()

    objects = [val[0] for val in top6]
    y_pos = np.arange(len(objects))

    neg_avg = [val[1] for val in top6]
    neutral_avg = [val[2] for val in top6]
    pos_avg = [val[3] for val in top6]

    p3 = plt.bar(y_pos, pos_avg, align='center')
    p2 = plt.bar(y_pos, neutral_avg, align='center', bottom=pos_avg)
    p1 = plt.bar(y_pos, neg_avg, align='center', bottom=neutral_avg)

    plt.xticks(y_pos, objects)
    plt.ylabel('Emotion score average')
    plt.title('Fig 2. Proportion of positive, neutral and negative commit comments per project')
    plt.legend((p1[0], p2[0], p3[0]), ('Negative', 'Neutral', 'Positive'))

    plt.show()

    return top6

    # TODO: Create matplot for these stats

# Paper: Section 3.2
# assume table is a list of dictionaries
# get data from table
# use pandas for displaying statistical data, and dosplay table
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.describe.html
# --------------------------------------------------------------
# | Language    |  Commits   |     Mean    |   Stand. Dev.     |
# --------------------------------------------------------------

def EmotionsProgLang():
    print "Emotions program language"

    projectLang = {}
    top6 = []

    df = pd.read_sql_query("SELECT project_language, sentiment_pos, sentiment_neg FROM commit_sentiments;", db_connection)

    for index, row in df.iterrows():
        if row['project_language'] in projectLang:
            projectLang[row['project_language']].append(float(row['sentiment_pos']) + float(row['sentiment_neg']))
        else:
            projectLang[row['project_language']] = [float(row['sentiment_pos']) + float(row['sentiment_neg'])]

    for key in sorted(projectLang,  key=lambda k: len(projectLang[k]), reverse=True)[:6]:
        top6.append([key, reduce(lambda x, y: x + y, projectLang[key]) / len(projectLang[key])])

    print "Top 6\n"

    t = Texttable()
    t.add_rows([['Language', 'Emotion Score Average']] + top6)
    print t.draw()

    objects = [val[0] for val in top6]
    y_pos = np.arange(len(objects))
    performance = [val[1] for val in top6]

    colors = ['g', 'g', 'g', 'g', 'g', 'g']
    plt.bar(y_pos, performance, align='center', alpha=0.5, color=colors)
    plt.xticks(y_pos, objects)
    plt.ylabel('Emotion score average')
    plt.title('Fig 2. Proportion of positive, neutral and negative commit comments per project')

    plt.show()

    return top6

    # TODO: Create matplot for these stats


# Paper: Section 3.3A
def EmotionsDayofWeek():
    print "Emotions day and time of week\n"
    # Emotion based on day of the week: Mon - Sun
    # Emotion based on time of the day:
        # [1] Morning:      6:00 - 12:00
        # [2] Afternoon:    12:00 - 18:00
        # [3] Evening:      18:00 - 23:00
        # [4] Night:        23:00 - 6:00

    # --------------------------------------------------------------
    # | Weekday     |   Commits   |     Mean    |   Stand. Dev.     |
    # --------------------------------------------------------------

    # --------------------------------------------------------------
    # | Time of Day |   Commits   |    Mean    |   Stand. Dev.     |
    # --------------------------------------------------------------

    DayofWeek = {}
    top6 = []

    df = pd.read_sql_query("SELECT commit_sha, sentiment_pos, sentiment_neg FROM commit_sentiments;", db_connection)

    for index, row in df.iterrows():

        datetime_object = datetime.strptime(row['commit_sha'], '%Y-%m-%d %H:%M:%S')
        day = datetime_object.strftime('%A')

        if day in DayofWeek:
            DayofWeek[day].append(float(row['sentiment_pos']) + float(row['sentiment_neg']))
        else:
            DayofWeek[day] = [float(row['sentiment_pos']) + float(row['sentiment_neg'])]

    for key in sorted(DayofWeek,  key=lambda k: len(DayofWeek[k]), reverse=True):
        top6.append([key, reduce(lambda x, y: x + y, DayofWeek[key]) / len(DayofWeek[key])])

    print "Top 6\n"

    t = Texttable()
    t.add_rows([['Weekday', 'Emotion Score Average']] + top6)
    print t.draw()

    objects = [val[0] for val in top6]
    y_pos = np.arange(len(objects))
    performance = [val[1] for val in top6]

    colors = ['g', 'g', 'g', 'g', 'g', 'g']
    plt.bar(y_pos, performance, align='center', alpha=0.5, color=colors)
    plt.xticks(y_pos, objects)
    plt.ylabel('Emotion score average')
    plt.title('Fig 2. Proportion of positive, neutral and negative commit comments per project')

    plt.show()

    return top6

# Paper: Section 3.3B
def EmotionsTimeofDay():
    print "Emotions and times of day\n"

    # This package might be helpful in mapping countries to continents
    # https://pypi.org/project/incf.countryutils/

    # box plot of the continent distribution

    # ------------------------------------------------
    # | Continents  |    Mean    |   Stand. Dev.     |
    # ------------------------------------------------

    TimeofDay = {}
    top6 = []

    df = pd.read_sql_query("SELECT commit_sha, sentiment_pos, sentiment_neg FROM commit_sentiments;", db_connection)

    for index, row in df.iterrows():

        datetime_object = datetime.strptime(row['commit_sha'], '%Y-%m-%d %H:%M:%S')
        hour = datetime_object.strftime('%H')
        hour = int(hour)
        # print hour

        if hour >= 6 and hour < 12:
            hour_key = 'Morning'
        elif hour >= 12 and hour < 18:
            hour_key = 'Afternoon'
        elif hour >= 18 and hour < 23:
            hour_key = 'Evening'
        else:
            hour_key = 'Night'


        if hour_key in TimeofDay:
            TimeofDay[hour_key].append(float(row['sentiment_pos']) + float(row['sentiment_neg']))
        else:
            TimeofDay[hour_key] = [float(row['sentiment_pos']) + float(row['sentiment_neg'])]

    for key in sorted(TimeofDay,  key=lambda k: len(TimeofDay[k]), reverse=True):
        top6.append([key, reduce(lambda x, y: x + y, TimeofDay[key]) / len(TimeofDay[key])])

    print "Top 6\n"

    t = Texttable()
    t.add_rows([['Weekday', 'Emotion Score Average']] + top6)
    print t.draw()

    objects = [val[0] for val in top6]
    y_pos = np.arange(len(objects))
    performance = [val[1] for val in top6]

    colors = ['g', 'g', 'g', 'g', 'g', 'g']
    plt.bar(y_pos, performance, align='center', alpha=0.5, color=colors)
    plt.xticks(y_pos, objects)
    plt.ylabel('Emotion score average')
    plt.title('Fig 2. Proportion of positive, neutral and negative commit comments per project')

    plt.show()

    return top6

# TODO
# 3.4 emotion and team distribution
def EmotionsTeamDistribution():
    print "Emotions and project approval\n"

    TimeofDay = {}
    top6 = []

    df = pd.read_sql_query("SELECT location FROM commit_sentiments;", db_connection)
    print df

    '''
    for index, row in df.iterrows():

        datetime_object = datetime.strptime(row['commit_sha'], '%Y-%m-%d %H:%M:%S')
        hour = datetime_object.strftime('%H')
        hour = int(hour)
        # print hour

        if hour >= 6 and hour < 12:
            hour_key = 'Morning'
        elif hour >= 12 and hour < 18:
            hour_key = 'Afternoon'
        elif hour >= 18 and hour < 23:
            hour_key = 'Evening'
        else:
            hour_key = 'Night'


        if hour_key in TimeofDay:
            TimeofDay[hour_key].append(float(row['sentiment_pos']) + float(row['sentiment_neg']))
        else:
            TimeofDay[hour_key] = [float(row['sentiment_pos']) + float(row['sentiment_neg'])]

    for key in sorted(TimeofDay,  key=lambda k: len(TimeofDay[k]), reverse=True):
        top6.append([key, reduce(lambda x, y: x + y, TimeofDay[key]) / len(TimeofDay[key])])

    print "Top 6\n"

    t = Texttable()
    t.add_rows([['Weekday', 'Emotion Score Average']] + top6)
    print t.draw()

    return top6
    '''

if __name__ == "__main__":
    print "Emotion statistics processing here!!"
    EmotionsProject()
    EmotionsProjectProportion()
    #EmotionsProgLang()
    #EmotionsDayofWeek()
    #EmotionsTimeofDay()

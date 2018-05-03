#!/usr/bin/env python


'''
@author: Raidel Hernandez
'''

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

    print "Average Emotion Score per Project:\n"

    projectEmotion = {}
    top6 = []

    df = pd.read_sql_query("SELECT project_name, sentiment_pos, sentiment_neg FROM commit_sentiments;", db_connection)

    for index, row in df.iterrows():
        if row['project_name'] in projectEmotion:
            projectEmotion[row['project_name']].append(float(row['sentiment_pos']) + float(row['sentiment_neg']))
        else:
            projectEmotion[row['project_name']] = [float(row['sentiment_pos']) + float(row['sentiment_neg'])]

    for key in sorted(projectEmotion,  key=lambda k: len(projectEmotion[k]), reverse=True)[:6]:
        commits = len(projectEmotion[key])
        mean = stats.tmean(projectEmotion[key])
        std_dev = stats.tstd(projectEmotion[key])
        wilcoxon_test = stats.wilcoxon(projectEmotion[key])

        if wilcoxon_test[1] < 0.002:
            wilcoxon_test = '< 0.002'
        # print 'mean:', mean
        # print 'std dev:', std_dev
        # print 'Wilcoxon p-value:', wilcoxon_test    # Get p-value
        top6.append([key, commits, mean, std_dev, wilcoxon_test])

    print "Top 6\n"

    t = Texttable()
    t.add_rows([['Project', 'Commits:', 'Mean', 'Stand. Dev.', 'p-value']] + top6)
    print t.draw()

    objects = [val[0] for val in top6]
    y_pos = np.arange(len(objects))
    performance = [val[2] for val in top6]

    colors = ['b', 'b', 'b', 'b', 'b', 'b']
    plt.bar(y_pos, performance, align='center', alpha=0.5, color=colors, width = 0.35)
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
    print "Proportion of Emotion scores per project:\n"

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

        top6.append([key, neg_val, neut_val, pos_val])


    print "Proportion of positive, neutral and negative commit comments per project\n"

    t = Texttable()
    t.add_rows([['Project', 'Negative', 'Neutral', 'Positive']] + top6)
    print t.draw()

    objects = [val[0] for val in top6]
    y_pos = np.arange(len(objects))

    neg_avg = [val[1] for val in top6]
    neutral_avg = [val[2] for val in top6]
    pos_avg = [val[3] for val in top6]

    p3 = plt.bar(y_pos, pos_avg, align='center', width = 0.35, color='b')
    p2 = plt.bar(y_pos, neutral_avg, align='center', bottom=pos_avg, color='g', width = 0.35)
    p1 = plt.bar(y_pos, neg_avg, align='center', bottom=neutral_avg, color='r', width = 0.35)

    plt.xticks(y_pos, objects)
    plt.title('Fig 2. Proportion of positive, neutral and negative commit comments per project')
    plt.legend((p1[0], p2[0], p3[0]), ('Negative', 'Neutral', 'Positive'))

    plt.show()

    return top6

# Paper: Section 3.2
# assume table is a list of dictionaries
# get data from table
# use pandas for displaying statistical data, and dosplay table
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.describe.html
# --------------------------------------------------------------
# | Language    |  Commits   |     Mean    |   Stand. Dev.     |
# --------------------------------------------------------------

def EmotionsProgLang():
    print "Emotions and Programming Language"

    projectLang = {}
    top6 = []

    df = pd.read_sql_query("SELECT project_language, sentiment_pos, sentiment_neg FROM commit_sentiments;", db_connection)

    for index, row in df.iterrows():
        if row['project_language'] in projectLang:
            projectLang[row['project_language']].append(float(row['sentiment_pos']) + float(row['sentiment_neg']))
        else:
            projectLang[row['project_language']] = [float(row['sentiment_pos']) + float(row['sentiment_neg'])]

    for key in sorted(projectLang,  key=lambda k: len(projectLang[k]), reverse=True):

        if key == 'C' or key == 'C++' or key == 'Java' or key == 'Python' or key == 'JavaScript':
            commits = len(projectLang[key])
            mean = stats.tmean(projectLang[key])
            std_dev = stats.tstd(projectLang[key])
            wilcoxon_test = stats.wilcoxon(projectLang[key])[1]

            if wilcoxon_test < 0.002:
                wilcoxon_test = '< 0.002'

            # print 'mean:', mean
            # print 'std dev:', std_dev
            # print 'Wilcoxon p-value:', wilcoxon_test    # Get p-value
            top6.append([key, commits, mean, std_dev, wilcoxon_test])

    # print "Top 6\n"

    t = Texttable()
    t.add_rows([['Project', 'Commits:', 'Mean', 'Stand. Dev.', 'p-value']] + top6)
    print t.draw()

    objects = [val[0] for val in top6]
    y_pos = np.arange(len(objects))
    performance = [val[2] for val in top6]

    colors = ['b', 'b', 'b', 'b', 'r']
    plt.bar(y_pos, performance, align='center', alpha=0.5, color=colors)
    plt.xticks(y_pos, objects)
    plt.ylabel('Emotion score average')
    plt.title('Fig 3. Emotions score average grouped by programming language')

    plt.show()

    return top6

    # TODO: Create matplot for these stats


# Paper: Section 3.3A
def EmotionsDayofWeek():
    print "Emotions, Day of Week\n"
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
        commits = len(DayofWeek[key])
        mean = stats.tmean(DayofWeek[key])
        std_dev = stats.tstd(DayofWeek[key])
        wilcoxon_test = stats.wilcoxon(DayofWeek[key])

        if wilcoxon_test[1] < 0.002:
            wilcoxon_test = '< 0.002'
        # print 'mean:', mean
        # print 'std dev:', std_dev
        # print 'Wilcoxon p-value:', wilcoxon_test    # Get p-value
        top6.append([key, commits, mean, std_dev, wilcoxon_test])

    # print "Top 6\n"

    t = Texttable()
    t.add_rows([['Project', 'Commits:', 'Mean', 'Stand. Dev.', 'p-value']] + top6)
    print t.draw()

    objects = [val[0] for val in top6]
    y_pos = np.arange(len(objects))
    performance = [val[2] for val in top6]

    colors = ['b', 'b', 'b', 'b', 'b', 'b']
    plt.bar(y_pos, performance, align='center', alpha=0.5, color=colors)
    plt.xticks(y_pos, objects)
    plt.ylabel('Emotion score average')
    plt.title('Fig 4. Emotion score average of commi comments grouped by weekday')

    plt.show()

    return top6

# Paper: Section 3.3B
def EmotionsTimeofDay():
    print "Emotions, Time of Day\n"

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
        commits = len(TimeofDay[key])
        mean = stats.tmean(TimeofDay[key])
        std_dev = stats.tstd(TimeofDay[key])
        wilcoxon_test = stats.wilcoxon(TimeofDay[key])

        if wilcoxon_test[1] < 0.002:
            wilcoxon_test = '< 0.002'
        # print 'mean:', mean
        # print 'std dev:', std_dev
        # print 'Wilcoxon p-value:', wilcoxon_test    # Get p-value
        top6.append([key, commits, mean, std_dev, wilcoxon_test])

    # print "Top 6\n"

    t = Texttable()
    t.add_rows([['Project', 'Commits:', 'Mean', 'Stand. Dev.', 'p-value']] + top6)
    print t.draw()

    objects = [val[0] for val in top6]
    y_pos = np.arange(len(objects))
    performance = [val[2] for val in top6]

    colors = ['b', 'b', 'b', 'b', 'b', 'b']
    plt.bar(y_pos, performance, align='center', alpha=0.5, color=colors)
    plt.xticks(y_pos, objects)
    plt.ylabel('Emotion score average')
    plt.title('Fig 5. Emotion score average of commit comments grouped by time of the day')

    plt.show()

    return top6


# TODO
# 3.4 emotion and team distribution
def EmotionsTeamDistribution():
    print "Emotions and project approval\n"

    TimeofDay = {}
    top6 = []

    df = pd.read_sql_query("SELECT project_name, sentiment_pos, sentiment_neg, location FROM commit_sentiments;", db_connection)

    df = df

    print df


def paperStats():
    df = pd.read_sql_query("SELECT DISTINCT(project_language) FROM commit_sentiments;", db_connection)
    print df

if __name__ == "__main__":
    print "Emotion statistics processing here!!\n"
    #EmotionsProject()
    #EmotionsProjectProportion()
    #EmotionsProgLang()
    #EmotionsDayofWeek()
    #EmotionsTimeofDay()
    # EmotionsProject()
    EmotionsTeamDistribution()

    paperStats()

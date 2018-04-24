#!/usr/bin/env python

import sys
import os
import pandas as pd

# Paper: Section 3.2
# assume table is a list of dictionaries
def EmotionsProgLang(table):
    print "Emotions program language"

    # key = language, value = [commits, mean, std. dev.]
    language_emotion = {}

    # get data from table (figure out format)
    # import to pandas if possible
    # use pandas for displaying statistical data, and dosplay table
    # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.describe.html
    # --------------------------------------------------------------
    # | Language    |  Commits   |     Mean    |   Stand. Dev.     |
    # --------------------------------------------------------------

# Paper: Section 3.3
def EmotionsTimeofWeek():
    print "Emotions day and time of week"
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

# Paper: Section 3.4
def EmotionsTeamDistribution():
    print "Emotions and team distribution"

    # This package might be helpful in mapping countries to continents
    # https://pypi.org/project/incf.countryutils/

    # box plot of the continent distribution

    # ------------------------------------------------
    # | Continents  |    Mean    |   Stand. Dev.     |
    # ------------------------------------------------

'''
# 3.5 emotion in project approval
def EmotionsProjectApproval():
    print "Emotions and project approval"
'''

if __name__ == "__main__":
    print "Emotion statistics processing here!!"

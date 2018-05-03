#!/usr/bin/env python



import os
import sys

# local imports setup
sys.path.append(os.getcwd() + "/utils")
sys.path.append(os.getcwd() + "/repoAnalysis")
sys.path.append(os.getcwd() + "/emotionsStat")
sys.path.append(os.getcwd() + "/sentimentAnalysis")

# db table parsing script inside utils directory
import bsonparser as bsonparse
import emotionStat as es
import analyze_results as ra

def CreateEmotionGraphs():
    es.EmotionsProject()
    es.EmotionsProjectProportion()
    es.EmotionsProgLang()
    es.EmotionsDayofWeek()
    es.EmotionsTimeofDay()

if __name__ == "__main__":

    # TODO: this is the main file, call necessary functions

    # Show all the graphs created by Raidel,
    # graphs are similar to those presented in the assigned paper.
    # CreateEmotionGraphs()
    ra.analyze()

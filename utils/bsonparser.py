import os
import bson
import csv
# import sqlite3
# import pandas as pd

# from pymongo import MongoClient
from bson.json_util import loads

# get main project path (in case this file is compiled alone)
cwd = os.getcwd().split('/')
if cwd[-1] == 'utils':
    cwd = '/'.join(cwd[:-1])
else:
    cwd = os.getcwd()

dump_location = cwd + '/dump/msr14/'
bson_ext = '.bson'

# collection names (parameter types) can be found here: http://ghtorrent.org/mongo.html
def GetDBTable(collection_name):

    # Open the database file containing collection name in parameter.
    # How to download the dataset and where to put it can be found on
    # the README.
    with open(dump_location + collection_name + bson_ext,'rb') as f:
        # read the db table file and decode using bson
        # may need to read the file in chunks (check results)
        commit_comments = bson.decode_all( f.read() )

        # TODO remove prints, provided to look at the data that was obtained
        print commit_comments[0], '\n'            # dictionary, print single comment
        print commit_comments[0].keys(), '\n'     # dictionary, print single comment keys
        print commit_comments[0].values(), '\n'   # dictionary, print single comment values

        # returns a list of dictionary (each dictionary is a single comments info)
        # Schemas for each dictionary in the list can be found at: http://ghtorrent.org/mongo.html)
        return commit_comments

def CommentsTabletoCSV(table):

    with open('comments_table.csv','wb') as f:

        w = csv.writer(f)
        w.writerow(['commit_id','body'])

        for comment in table:
            w.writerow([comment['commit_id'].encode('utf-8'), comment['body'].encode('utf-8')])

if __name__ == "__main__":

    # example run obtaining data for commit_comments collection(table) name
    comments_table = GetDBTable('commit_comments')

    # CommentsTabletoCSV(comments_table)

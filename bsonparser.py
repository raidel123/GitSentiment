import os
import bson
import csv
# import sqlite3
# import pandas as pd

# from pymongo import MongoClient
from bson.json_util import loads

dump_location = os.getcwd() + '/dump/msr14/'
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

        print commit_comments[0], '\n'            # dictionary, print single comment
        print commit_comments[0].keys(), '\n'     # dictionary, print single comment keys
        print commit_comments[0].values(), '\n'   # dictionary, print single comment values

        # return is a dictionary (schemas can be found in documentation url fields: http://ghtorrent.org/mongo.html)
        return commit_comments

def TabletoCSV(table):

    with open('comments_table.csv','wb') as f:
        w = csv.writer(f)
        w.writerow(['commit_id','body'])

        for comment in table:
            w.writerow([comment['commit_id'].encode('utf-8'), comment['body'].encode('utf-8')])

if __name__ == "__main__":

    # example run obtaining data for commit_comments collection(table) name
    comments_table = GetDBTable('commit_comments')

    TabletoCSV(comments_table)

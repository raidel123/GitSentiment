import os
import sys

# local imports setup
sys.path.append(os.getcwd() + "/utils")

# db table parsing script inside utils directory
import bsonparser as bsonparse

if __name__ == "__main__":

    # example run obtaining data for commit_comments collection(table) name
    comments_table = bsonparse.GetDBTable('commit_comments')
    for comment in comments_table:
        if 'commit_id' in comment:
            print comment['commit_id']
            break   # just print 1 value for testing

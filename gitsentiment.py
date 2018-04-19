import os
import sys

# local imports setup
sys.path.append(os.getcwd() + "/utils")
sys.path.append(os.getcwd() + "/repoAnalysis")
sys.path.append(os.getcwd() + "/emotionsStat")

# db table parsing script inside utils directory
import bsonparser as bsonparse

if __name__ == "__main__":

    # TODO: this is the main file, call necessary functions



    # code below this line is for testing purposes

    # example run obtaining data for commit_comments collection(table) name
    comments_table = bsonparse.GetDBTable('commit_comments')
    repos = bsonparse.GetDBTable('repos')

    '''
    for comment in comments_table:
        if 'commit_id' in comment:
            print comment['commit_id']
            break   # just print 1 value for testing
    '''

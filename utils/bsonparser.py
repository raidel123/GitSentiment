import os
import bson
import json

from bson.json_util import loads

# get main project path (in case this file is compiled alone)
context = os.getcwd().split('/')
if context[-1] == 'utils':
    context = '/'.join(context[:-1])
else:
    context = os.getcwd()

dump_location = context + '/dump/msr14/'
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
        print 'Printing table keys for: %s\n' % collection_name
        # print commit_comments[0], '\n'            # dictionary, print single comment
        print commit_comments[0].keys(), '\n'     # dictionary, print single comment keys
        # print commit_comments[0].values(), '\n'   # dictionary, print single comment values

        # returns a list of dictionary (each dictionary is a single comments info)
        # Schemas for each dictionary in the list can be found at: http://ghtorrent.org/mongo.html)
        return commit_comments

def CommentsTabletoJSON(table):

    # creates a list of dictionaries for each commit comment in db table,
    # each dictionary inside the list contains a field (key) for ( commit_id, body ).
    commenttojson = []
    for comment in table:
        info = {'commit_id': comment['commit_id'].encode('utf-8'),
                'body': comment['body'].encode('utf-8')}
        commenttojson.append(info)


    with open('comments_table.json','wb') as f:
        json.dump(commenttojson, f)

# filename of json file to input as parameter
def RetrieveJSONTable(filename):
    with open(filename,'rb') as f:
        return json.load(f)

if __name__ == "__main__":

    # example run obtaining data for commit_comments collection(table) name
    comments_table = GetDBTable('commit_comments')

    # function call below used to create a json file in current directory
    # CommentsTabletoJSON(comments_table)

    # example on how to retrieve json data from a file
     rtable = RetrieveJSONTable(context + '/test/comments_table.json')
     print rtable[0]    # print only the first index of the table for testing

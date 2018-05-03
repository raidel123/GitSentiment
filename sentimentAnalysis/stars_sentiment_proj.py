import db_utils
import json
import nltk
import sqlite3 as sqlite
import subprocess as sub
import shlex

import urllib

import senti_strength_sentiment

if __name__ == "__main__":
	
	# retrieves the result from the query and then formats into a dictionary
	# that will be dumped to be parsed by SentiStrength

	query = """SELECT projects.name, login
						 FROM projects
						 INNER JOIN users on projects.owner_id = users.id"""

	urls = dict()

	for row in db_utils.do_my_query(query).fetchall():
		urls[row[0]] = "https://api.github.com/repos/"+row[1]+"/"+row[0]
		

	counts = dict()
	total_sentiment = dict()

	with sqlite.connect('./whole_database_new.db') as con:
		con.text_factory = str
		cur = con.cursor() # get the current spot for executing
		cur.execute("""SELECT sentiment_pos, sentiment_neg, project_name FROM commit_sentiments""")
		rows = cur.fetchall()

		for row in rows:
			project_name = row[2]

			sent = int(row[0]) + int(row[1])

			#print(sent)

			if project_name in counts:
				counts[project_name] += 1
			else:
				counts[project_name] = 1

			if project_name in total_sentiment:
				total_sentiment[project_name] += sent
			else:
				total_sentiment[project_name] = sent

	print counts
	print total_sentiment

	avg = dict()

	for key in total_sentiment:
		avg[key] = float(total_sentiment[key])/float(counts[key])

	print(avg)

	stars_count = dict()

	content = list()

	with open("./stars.txt") as f:
	    content = f.readlines()

	print(content)

	i = 0

	for key in total_sentiment:
		print key,
		print avg[key],
		print content[i],

		i += 1
		


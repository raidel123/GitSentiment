import db_utils
import json
import nltk
import sqlite3 as sqlite

import senti_strength_sentiment

if __name__ == "__main__":
	
	# retrieves the result from the query and then formats into a dictionary
	# that will be dumped to be parsed by SentiStrength

	query = """SELECT commit_comments.id, sha, body, projects.name, projects.language, commit_comments.created_at, users.login, users.email, users.name FROM commit_comments
			INNER JOIN commits on commit_comments.id = commits.id
			INNER JOIN projects on commits.project_id = projects.id
			INNER JOIN users on commits.author_id = users.id"""

	# dict for storing the data need for SentiStrength analysis

	l = list()
	d = dict()

	for row in db_utils.do_my_query(query).fetchall():
		

		project_name = row[3]

		if project_name in d:
			d[project_name] += 1
		else:
			d[project_name] = 1

	# stores all of this in ss_ready.json so that it can be processed on a Windows machine
	# to be able to be processed by SentiStrength

	dict_proj = dict()

	for key in d.keys():
		if d[key] > 200:
			dict_proj[key] = d[key]

	with open('project_names.json', 'w') as fp:
		json.dump(l, fp)
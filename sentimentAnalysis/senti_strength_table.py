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
			INNER JOIN users on commits.author_id = users.id LIMIT 1000"""

	# dict for storing the data need for SentiStrength analysis

	l = list()

	for row in db_utils.do_my_query(query).fetchall():
		
		ccid = row[0]
		sha = row[1]
		body = row[2]
		project_name = row[3]
		language = row[4]
		cc_created_at = row[5]
		commenter_login = row[6]
		commenter_email = row[7]
		#commenter_

		pos, neg = senti_strength_sentiment.RateSentiment(body)

		print({"comment_id": ccid, 
				  "sha": sha,
				  "body": body,
				  "project_name": project_name,
				  "pos_sentiment": pos[0],
				  "neg_sentiment": neg[0], # need negative sign
				  "cc_created_at": cc_created_at,
				  "project_language": language})

	# stores all of this in ss_ready.json so that it can be processed on a Windows machine
	# to be able to be processed by SentiStrength

	print(l)
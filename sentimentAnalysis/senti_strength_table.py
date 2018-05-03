import db_utils
import json
import nltk
import sqlite3 as sqlite

import senti_strength_sentiment

if __name__ == "__main__":
	
	# retrieves the result from the query and then formats into a dictionary
	# that will be dumped to be parsed by SentiStrength

	query = """SELECT commit_comments.id, 
					  body,
					  commit_comments.created_at, 
					  sha,
					  projects.name, 
					  projects.language,
					  users.email,
					  users.login,
					  users.location
						 FROM commit_comments
			INNER JOIN commits on commit_comments.id = commits.id
			INNER JOIN projects on commits.project_id = projects.id
			INNER JOIN users on commit_comments.user_id = users.id"""

	# dict for storing the data need for SentiStrength analysis

	l = list()

	for row in db_utils.do_my_query(query).fetchall():
		
		ccid = row[0]
		body = row[1]
		created_at = row[2]
		sha = row[3]
		project_name = row[4]
		language = row[5]
		email = row[6]
		login = row[7]
		loc = row[8]

		pos = ""
		neg = ""

		with sqlite.connect('./database_sentiments.db') as con:
			cur = con.cursor() # get the current spot for executing		
			cur.execute("SELECT sentiment_pos, sentiment_neg FROM commit_sentiments_store WHERE commit_comment_id =?", (ccid,))
			rows = cur.fetchall()
			pos = rows[0][0]
			neg = rows[0][1]

		with sqlite.connect('./whole_database_new.db') as con:
			con.text_factory = str
			cur = con.cursor() # get the current spot for executing
			cur.execute("""INSERT INTO commit_sentiments
				(commit_comment_id, 
				 commit_comment_body,
				 created_at,
				 commit_sha,
				 project_name,
				 project_language,
				 commenter_email,
				 commenter_login,
				 location,
				 sentiment_pos, 
				 sentiment_neg)
				 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
				(ccid, body, created_at, sha, project_name, language, email, login, loc, pos, neg)) # execute insert to add the score and name
			con.commit() # commit the query


	print(row)
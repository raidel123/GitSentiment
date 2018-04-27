import db_utils
import json
import nltk
import sqlite3 as sqlite

from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('punkt')
nltk.download('vader_lexicon')

if __name__ == "__main__":
	
	# retrieves the result from the query and then formats into a dictionary
	# that will be dumped to be parsed by SentiStrength

	query = """SELECT commit_comments.id, sha, body, projects.name FROM commit_comments
			INNER JOIN commits on commit_comments.id = commits.id
			INNER JOIN projects on commits.project_id = projects.id
			INNER JOIN users on commits.author_id = users.id"""

	# dict for storing the data need for SentiStrength analysis

	l = list()

	sid = SentimentIntensityAnalyzer()

	classifier = SentimentIntensityAnalyzer()

	for row in db_utils.do_my_query(query).fetchall():
		
		ccid = row[0]
		sha = row[1]
		body = row[2]
		project_name = row[3]

		sent_compound = classifier.polarity_scores(body)['compound']

		l.append({"comment_id": ccid, 
				  "sha": sha,
				  "body": body,
				  "project_name": project_name,
				  "sentiment": sent_compound})

	# stores all of this in ss_ready.json so that it can be processed on a Windows machine
	# to be able to be processed by SentiStrength

	with open('nltk_vader_sentiments.json', 'w') as fp:
		json.dump(l, fp)
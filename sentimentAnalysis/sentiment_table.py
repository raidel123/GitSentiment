import db_utils
import json
import sqlite3 as sqlite

import senti_strength_sentiment

if __name__ == "__main__":

	query = """SELECT commit_comments.id, body FROM commit_comments"""

	l = list()

	#for row in db_utils.do_my_query(query).fetchall():
	#	ccid = row[0]
	#	body = row[1].strip()

	#	pos, neg = senti_strength_sentiment.RateSentiment(body)

	#	with sqlite.connect('./database_sentiments.db') as con:
	#		con.text_factory = str
	#		cur = con.cursor() # get the current spot for executing
	#		cur.execute("""INSERT INTO commit_sentiments_store 
	#			(commit_comment_id, commit_comment_body, sentiment_pos, sentiment_neg) VALUES (?, ?, ?, ?)""", 
	#			(ccid, body, pos, neg)) # execute insert to add the score and name
	#		con.commit() # commit the query

	
	with sqlite.connect('./whole_database.db') as con:	
		cur = con.cursor() # get the current spot for executing		
		cur.execute("SELECT count(*) FROM commit_sentiments")
		rows = cur.fetchall()

    	print(rows)

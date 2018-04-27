import db_utils
import json
import sqlite3 as sqlite

import senti_strength_sentiment

if __name__ == "__main__":

	query = """SELECT commit_comments.id, body FROM commit_comments LIMIT 100"""

	l = list()

	for row in db_utils.do_my_query(query).fetchall():
		ccid = row[0]
		body = row[1].strip()

		print(row)

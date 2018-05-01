import db_utils
import json
import sqlite3 as sqlite

if __name__ == "__main__":

	with sqlite.connect('./whole_database_new.db') as con:	
		cur = con.cursor() # get the current spot for executing		
		cur.execute("SELECT count(*) FROM commit_sentiments")
		rows = cur.fetchall()

    	print(rows)

"""TABLE
				commit_sentiments (commit_comment_id int,
									commit_comment_body int,
									created_at timestamp,
									commit_sha varchar(40),
									project_name varchar(255),
									project_language varchar(255),
									committer_email varchar(255),
									committer_login varchar(255),
									location varchar(255),
									sentiment_pos int,
									sentiment_neg int)"""
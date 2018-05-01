import sqlite3 as sqlite

conn = sqlite.connect('./whole_database.db')
print("Opened database successfully!")

conn.execute("""CREATE TABLE
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
									sentiment_neg int)""")

conn.execute("""CREATE TABLE IF NOT EXISTS
				commit_sentiments_store (commit_comment_id int,
										 commit_comment_body varchar(255),
										 sentiment_pos int,
										 sentiment_neg int)""")



print("Table created successfully!")

conn.close()
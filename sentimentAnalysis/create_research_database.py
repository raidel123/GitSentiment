import sqlite3 as sqlite

conn = sqlite.connect('./database_sentiments.db')
print("Opened database successfully!")

conn.execute("""CREATE TABLE IF NOT EXISTS
				commit_sentiments (commit_comment_id int,
									commit_comment_body int,
									created_at timestamp,
									commit_sha varchar(40),
									commenter_login varchar(40),
									project_name varchar(255),
									sentiment_pos int,
									sentiment_neg int,
									commenter_email varchar(255),
									commenter_name varchar(255))""")

conn.execute("""CREATE TABLE IF NOT EXISTS
				commit_sentiments_store (commit_comment_id int,
										 commit_comment_body varchar(255),
										 sentiment_pos,
										 sentiment_neg)""")

print("Table created successfully!")

conn.close()
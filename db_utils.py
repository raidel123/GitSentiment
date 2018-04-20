import MySQLdb
import creds

def do_my_query(query):

	# db connection

	db = MySQLdb.connect(host=creds.creds['h'],    # your host, usually localhost
					 user=creds.creds['u'],        # your username
					 passwd=creds.creds['p'],      # your password
					 db=creds.creds['d'])          # name of the data base

	cur = db.cursor()

	# execute the passed in query

	cur.execute(query)

	# closes the db connection

	db.close()

	# returns the result of the db call
	
	return cur
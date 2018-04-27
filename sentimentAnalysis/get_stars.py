import db_utils
import json
import urllib

if __name__ == "__main__":
	query = "SELECT login FROM users LIMIT 1000"

	l = list()

	for row in db_utils.do_my_query(query).fetchall():
		login = row[0]

		url = "https://api.github.com/users/"+login+"/starred?page=0&per_page=1000"
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		print data
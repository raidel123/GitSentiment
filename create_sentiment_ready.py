import db_utils
import json

if __name__ == "__main__":
	
	# retrieves the result from the query and then formats into a dictionary
	# that will be dumped to be parsed by SentiStrength

	query = """SELECT commit_comments.id, sha, body, projects.name FROM commit_comments
			INNER JOIN commits on commit_comments.id = commits.id
			INNER JOIN projects on commits.project_id = projects.id
			INNER JOIN users on commits.author_id = users.id"""

	# dict for storing the data need for SentiStrength analysis

	l = list()

	for row in db_utils.do_my_query(query).fetchall():
		
		ccid = row[0]
		sha = row[1]
		body = row[2]
		project_name = row[3]

		l.append({"comment_id": ccid, 
				  "sha": sha,
				  "body": body,
				  "project_name": project_name})

	# stores all of this in ss_ready.json so that it can be processed on a Windows machine
	# to be able to be processed by SentiStrength

	with open('ss_ready.json', 'w') as fp:
		json.dump(l, fp)

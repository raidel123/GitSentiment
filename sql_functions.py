import db_utils

if __name__ == "__main__":
	
	# retrieves the result from the query and then formats into a dictionary
	# that will be dumped to be parsed by SentiStrength

	query = """SELECT commit_id, body, commit_comments.id, sha, projects.name, users.login FROM commit_comments
			INNER JOIN commits on commit_comments.id = commits.id
			INNER JOIN projects on commits.project_id = projects.id
			INNER JOIN users on commits.author_id = users.id"""

	for row in db_utils.do_my_query(query).fetchall():
		print row
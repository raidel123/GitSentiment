"""
PyGitHub(github) is a Python (2 and 3) library to access the GitHub API v3. 
This library enables you to manage GitHub resources such as repositories, user profiles, and organizations 
in your Python applications.
"""
from github import *
from Users import Users

"""
will be used to determine quality of code
"""
from pylint.lint import Run

"""
easy/safe way to create temporary files
needed for pylint analyzation (will create temp file of user code to analyze)
"""
import tempfile

"""
Used to hide stdout of pylint command
"""
import sys, os

"""
wrapper for database connection
"""
from DB import Database

"""
Store login credentials in separate file
Obtain personal access code by following steps here: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/

OR 

simply use your github username and password and put variables (USER:PASSWORD) in data.py (included in .gitignore)
"""
try:
    from data import PERSONAL_ACCESS_TOKEN
except  ImportError:
    try:
        from data import USER, PASSWORD
    except:
        raise ImportError('check to see if you have a data.py in repoAnalysis directory')


"""
Attempt to authenticate user with personal access token
Github() initialization does not throw error on its own
    * so attempt simple api call for some test user
    * if BadCredentials
        * attempt to instantiate g with USER and PASSWORD instead
        * if that fails with BadCredentials, then terminate
Finally, check to see if github APIv3 is up, terminate if not
"""
def authenticate():
    g = Github(PERSONAL_ACCESS_TOKEN)

    try:
        g.get_user("test")
    except BadCredentialsException:
        try:
            g = Github(USER, PASSWORD)
        except BadCredentialsException:
            print "error with credentials"
            exit()

    if g.get_api_status().status != "good":
        print "github APIv3 is down"
        exit()

    return g

"""
TODO: retrieve users from SQL database and create array of Users objects initializing them with data from db
"""
def retrieve_users(db):
    user_list_str = db.get('Users', 'commentor_login, sentiment_score', 100)
    users = []
    for u in user_list_str:
        users.append(Users(u[0], u[1]))
    return users
    

"""
TODO: establish connection with Andrew's database
"""
def connect_to_db(f):
    db = Database()
    db.open(f)
    return db

"""
determine code quality of file temp with pylint 
params: temporaryfile
ret: float
"""
def get_code_quality_py(temp):
    # temporarily hide stdout, stderr b/c pylint's Run will print there no matter what
    _stdout = sys.stdout
    _stderr = sys.stderr
    null = open(os.devnull, 'wb')
    sys.stdout = sys.stderr = null

    # run pylint on temp file
    results = Run([temp.name], exit=False)

    # restore stdout
    sys.stdout = _stdout
    sys.stderr = _stderr
    return results.linter.stats['global_note']

"""
go through all top level documents within projects and run them through language appropriate linters
then average score for that user
"""
def examine_user_files(user, git_user):
    for repo in git_user.get_repos():
        if repo.language == "Python":
            for fs in repo.get_dir_contents('/'):
                if fs.name.endswith(".py"):
                     with tempfile.NamedTemporaryFile() as temp:
                        # write string of decoded file to a temp file so pylint can read from it
                        temp.write(fs.decoded_content)
                        temp.flush()
                        user.add_quality_score(get_code_quality_py(temp))
                        temp.close()
                   

    

if __name__ == '__main__':
    g = authenticate()
    
    #TODO: read userid from SQL database to be added by andrew
    db = connect_to_db('temp.sql')
    users = retrieve_users(db)

    for u in users:
        git_user = g.get_user(u.username)
        examine_user_files(u, git_user)
        print u.username, u.qualityAverage, u.qualityScore


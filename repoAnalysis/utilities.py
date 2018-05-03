"""
Store login credentials in separate file
Obtain personal access code by following steps here:
https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/

OR

simply use your github username and password and put variables (USER:PASSWORD)
in data.py (included in .gitignore)
"""
try:
    from data import PERSONAL_ACCESS_TOKEN
except ImportError:
    try:
        from data import USER, PASSWORD
    except:
        print "unable to import github credentials"

"""
Languages in which we can analyze (determined by the linters installed)
"""
VALID_LANGUAGES = ["Python", "C++", "JavaScript", "Ruby"]

"""
retrieve users from SQL database and create array of Users objects initializing them with data from db
@param db Established Database object
"""
from Users import Users

def retrieve_users(db, table, attributes, limit=None):
    user_list_str = db.get(table, attributes, limit)
    users = []
    for user in user_list_str:
        temp_user = Users(**user)
        flag = True
        for u in users:
            if u.username == temp_user.username:
               u.add_sentiment_score(temp_user.sentiment)
               flag = False
        if flag:
            users.append(Users(**user))
    return users


"""
Attempt to establish connection with database
@param f Path to sqlite file
"""
from DB import Database

def connect_to_db(f):
    try:
        connected_db = Database(f)
    except ValueError:
        print "{0} not found!".format(f)
        exit()
    return connected_db


"""
PyGitHub(github) is a Python (2 and 3) library to access the GitHub API v3.
This library enables you to manage GitHub resources such as repositories,
user profiles, and organizations in your Python applications.

Attempt to authenticate user with personal access token
Github() initialization does not throw error on its own
    * so attempt simple api call for some test user
    * if BadCredentials
        * attempt to instantiate g with USER and PASSWORD instead
        * if that fails with BadCredentials, then terminate
Finally, check to see if github APIv3 is up, terminate if not
"""
from github import Github, BadCredentialsException

def authenticate():
    try:
        github = Github(PERSONAL_ACCESS_TOKEN)
    except NameError:
        try:
            github = Github(USER, PASSWORD)
        except BadCredentialsException:
            print "error with credentials"
            exit()

    try:
        github.get_user("test")
    except BadCredentialsException:
        try:
            github = Github(USER, PASSWORD)
        except BadCredentialsException:
            print "error with credentials"
            exit()

    if github.get_api_status().status != "good":
        print "github APIv3 is down"
        exit()

    return github


"""
examine a Github users repositories, searching for their most used language
@params git_user Github user object
@ret string most common language used
"""
from collections import Counter

def get_most_used_language(git_user):
    try:
        return Counter([repo.language for repo in git_user.get_repos()]).most_common(1)[0][0]
    except IndexError:
        return None

"""
@params temp Name of NamedTemporaryFile
@ret int Number of lines in file
"""
def get_num_lines(temp):
    return sum(1 for line in open(temp))

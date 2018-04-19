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
subprocess for humans (needed to invoke pylint)
"""
import delegator

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
def retrieve_users():
    pass

"""
TODO: establish connection with Andrew's database
"""
def connect_to_db():
    pass

"""
TODO: analyze all of the user's repositories, and determine code quality by folloing measures:
    * ratio of comments to code
    * readme complexity
then deterimne score
"""
def determine_code_quality(user):
    for repo in user.get_repos():
        if repo.language == "Python":
            for fs in repo.get_dir_contents('/'):
                if fs.name.endswith(".py"):
                    with tempfile.NamedTemporaryFile() as temp:
                        temp.write(fs.decoded_content)
                        temp.flush()
                        #c = delegator.run("pylint " + temp.name)
                        results = Run([temp.name], exit=False,)
                        # print results.linter.stats
                        # pylint_stdout, pylint_stderr = lint.py_run(f.name , return_std=True)
                        # print pylint_stderr.getvalue()
                        temp.close()

    pass

if __name__ == '__main__':
    g = authenticate()
    
    #TODO: read userid from SQL database to be added by andrew
    
    user = g.get_user("raidel123")
    repo = user.get_repo("UnixShell")
    f = repo.get_file_contents("/myls.c")
    
    determine_code_quality(user)
    #print f.decoded_content 


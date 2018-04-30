from utilities import *

"""
determine code quality of file temp with pylint 
@params temp TemporarFile name created by examine_user_files
@ret float Code quality score determine by PyLint
"""
from pylint.lint import Run
import sys
import os
def get_code_quality_py(temp):
    # temporarily hide stdout, stderr b/c pylint's Run will print there no matter what
    _stdout = sys.stdout
    _stderr = sys.stderr
    null = open(os.devnull, 'wb')
    sys.stdout = sys.stderr = null

    # run pylint on temp file
    results = Run([temp], exit=False)

    # restore stdout
    sys.stdout = _stdout
    sys.stderr = _stderr
    return results.linter.stats['global_note']

"""
will determine the code quality by examining ratio of linter warnings to length of code
@params temp Name of NamedTemporaryFile to be analyzed
@params linter Name of linter command line utility to run
@ret float Code quality socre (if no warnings, return a perfect score)
"""
from subprocess import PIPE, Popen
def get_code_quality_rb(temp):
    proc = Popen(["standard", temp], stdout=PIPE, stderr=PIPE)
    warning_output = proc.stdout.read()
    num_lines = get_num_lines(temp)
    try:
        return float(num_lines) / warning_output.count('\n')
    except ZeroDivisionError:
        return 10


def get_code_quality_cpp(temp):
    proc = Popen(["python", "cpplint.py", temp], stdout=PIPE, stderr=PIPE)
    warning_output = proc.stdout.read()
    num_lines = get_num_lines(temp)
    try:
        return float(num_lines) / warning_output.count('\n')
    except ZeroDivisionError:
        return 10

"""
will determine the code quality by examining ratio of linter warnings to length of code
ruby linter lists the number of warnings so we need to use regex to get this amount
@params temp Name of NamedTemporaryFile to be analyzed
@ret float Code quality socre (if no warnigs, return a perfect score)
"""
import re
def get_code_quality_js(temp):
    proc = Popen(["excellent", temp], stdout=PIPE, stderr=PIPE)
    warning_output = proc.stdout.read()
    num_warnings = re.search("Found (.*) warnings.", warning_output).group(1)
    num_lines = get_num_lines(temp)
    try:
        return float(num_lines) / int(num_warnings)
    except ZeroDivisionError:
        return 10


"""
easy/safe way to create temporary files
needed for pylint analyzation (will create temp file of user code to analyze)
"""
import tempfile
"""
go through all top level documents within projects and run them through language appropriate linters
then average score for that user
@param user Users object which will keep track of individual users quality score
@param git_user Authenticated GitHub user needed to get repo information
"""
def examine_user_files(user, git_user):
    if user.language not in VALID_LANGUAGES:
        return -1
    for repo in git_user.get_repos():
        if repo.language in VALID_LANGUAGES and repo.language == user.language:
            for _file in repo.get_dir_contents('/'):

                if _file.name.endswith(".py") and repo.language == "Python":
                    with tempfile.NamedTemporaryFile(suffix='.py') as temp:
                        # write string of decoded file to a temp file so pylint can read from it
                        temp.write(_file.decoded_content)
                        temp.flush()
                        user.add_quality_score(get_code_quality_py(temp.name))
                        temp.close()

                elif _file.name.endswith(".js") and repo.language == "JavaScript":
                    with tempfile.NamedTemporaryFile(suffix='.js') as temp:
                        temp.write(_file.decoded_content)
                        temp.flush()
                        user.add_quality_score(get_code_quality_js(temp.name))
                        temp.close()

                elif _file.name.endswith(".cpp") and repo.language == "C++":
                    with tempfile.NamedTemporaryFile(suffix='.cpp') as temp:
                        temp.write(_file.decoded_content)
                        temp.flush()
                        user.add_quality_score(get_code_quality_cpp(temp.name))
                        temp.close()

                elif _file.name.endswith(".rb") and repo.language == "Ruby":
                    with tempfile.NamedTemporaryFile(suffix='.rb') as temp:
                        temp.write(_file.decoded_content)
                        temp.flush()
                        user.add_quality_score(get_code_quality_rb(temp.name))
                        temp.close()

def main():
    github = authenticate()

    #TODO: read userid from SQL database to be added by andrew
    sentiment_db = connect_to_db('temp.sql')
    users = retrieve_users(sentiment_db, 'Users', 'commentor_login, sentiment_score')

    results_db = connect_to_db('results.sql')

    """
    loop over every user object found in database and update their code quality information in
    retsults database
    """
    for user in users:
        git_user = github.get_user(user.username)
        user.language = get_most_used_language(git_user)
        examine_user_files(user, git_user)
        print "adding {0}, {1}, {2}, {3} to database".format(user.username, user.language, user.sentiment,
                                                             user.qualityAverage)
        param = "{0}, {1}, {2}, {3}".format(user.username, user.language, user.sentiment, user.qualityAverage)
        results_db.write('Users', "commentor_login, language, sentiment_score, quality", "?, ?, ?, ?", (user.username,
                                                 user.language, user.sentiment, user.qualityAverage))

if __name__ == '__main__':
    main()

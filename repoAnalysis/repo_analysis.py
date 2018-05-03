from utilities import retrieve_users, authenticate, connect_to_db,\
                      get_num_lines, get_most_used_language, VALID_LANGUAGES
from github import UnknownObjectException, GithubException, RateLimitExceededException
from time import sleep
"""
determine code quality of file temp with pylint 
@params temp TemporarFile name created by examine_user_files
@ret float Code quality score determine by PyLint
"""
from pylint.lint import Run
import sys
import os
def get_code_quality_py(temp, command=None):
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
    try:
        return results.linter.stats['global_note']
    except KeyError:
        return 0

"""
will determine the code quality by examining ratio of linter warnings to length of code
ruby linter lists the number of warnings so we need to use regex to get this amount
@params temp Name of NamedTemporaryFile to be analyzed
@ret float Code quality score (if no warnigs, return a perfect score)
""" 
from subprocess import PIPE, Popen
def get_code_quality(temp, command):
    num_lines = get_num_lines(temp)
    proc = Popen(command, stdout=PIPE, stderr=PIPE)
    warning_output = proc.stdout.read()
    try:
        return float(num_lines) / warning_output.count('\n')
    except ZeroDivisionError:
        return 0

def handle_file_writing(quality_function, suffix, _file, user, command):
    with tempfile.NamedTemporaryFile(suffix=suffix) as temp:
        # dont attempt to analyze file if too large
        try:
            content = _file.decoded_content
            if sys.getsizeof(content) > 15000:
                temp.close()
                return 0
        except AssertionError:
            temp.close()
            return
        except GithubException:
            temp.close()
            return
        temp.write(content)
        temp.flush()
        command.append(temp.name)
        user.add_quality_score(quality_function(temp.name, command))
        temp.close()

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
    for repo in git_user.get_repos():
        if repo.language == user.language and repo.language in VALID_LANGUAGES:
            repoContents = repo.get_dir_contents('/')
            if len(repoContents) <= 10:
                for _file in repoContents:
                    if _file.name.endswith(".py") and repo.language == "Python":
                        handle_file_writing(
                            get_code_quality_py, '.py', _file, user, [])

                    elif _file.name.endswith(".js") and repo.language == "JavaScript":
                        handle_file_writing(
                            get_code_quality, '.js', _file, user, ["standard"])

                    elif _file.name.endswith(".cpp") and repo.language == "C++":
                        handle_file_writing(
                            get_code_quality, '.cpp', _file, user, ["python", "cpplint.py"])

                    elif _file.name.endswith(".rb") and repo.language == "Ruby":
                        handle_file_writing(
                            get_code_quality, '.rb', _file, user, ["excellent"])
                    

def main():
    github = authenticate()

    #TODO: read userid from SQL database to be added by andrew
    sentiment_db = connect_to_db('../sentimentAnalysis/whole_database_new.db')
    users = retrieve_users(sentiment_db, 'commit_sentiments', 'commenter_login, sentiment_pos, sentiment_neg')

    results_db = connect_to_db('results.sql')
    existing_users = results_db.get('Users', 'commenter_login')

    """
    loop over every user object found in database and update their code quality information in
    retsults database
    """
    for user in users:
        try:
            # let's not redo work we already completed
            if user.username in existing_users:
                continue
            try:
                git_user = github.get_user(user.username)
            except UnknownObjectException:
                continue 
            user.language = get_most_used_language(git_user)
            if not user.language or user.language not in VALID_LANGUAGES:
                continue
            
            examine_user_files(user, git_user)
            print "adding {0}, {1}, {2}, {3} to database".format(user.username, user.language, user.sentiment,
                                                                user.qualityAverage)
            results_db.write('Users', "commenter_login, language, sentiment_score, quality", "?, ?, ?, ?", 
                            (user.username, user.language, user.sentimentAverage, user.qualityAverage))
        except RateLimitExceededException:
            print "need to wait"
            sleep(3600)
        except GithubException:
            continue
        except Exception:
            continue

if __name__ == '__main__':
    main()

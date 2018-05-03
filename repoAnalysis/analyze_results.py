from scipy.stats.stats import pearsonr
from DB import Database
from Users import Users
from utilities import retrieve_users, connect_to_db, VALID_LANGUAGES
import matplotlib.pyplot as plt

def get_language_results(users, lang):
    qualityScores = [user.qualityAverage for user in users if user.language == lang]
    sentimentScores = [user.sentiment for user in users if user.language == lang]
    return qualityScores, sentimentScores
        
def print_graph(axisTitle, data):
    plt.figure()
    plt.boxplot(data)
    plt.ylabel(axisTitle)
    plt.show()

def analyze():
    database_connection = connect_to_db('results.sql')
    users = retrieve_users(database_connection, 'Users', 'commenter_login, language, sentiment_score, quality')
    print len(users)
    # remove all users with 0.0 qualityAverage as it means we were unable to get a score for some reason
    users = [u for u in users if u.qualityAverage != 0.0]
    print len(users)
    for lang in VALID_LANGUAGES:
        qualityScores, sentimentScores = get_language_results(users, lang)
        print "{0} {1}: {2}".format(lang, len(qualityScores), pearsonr(sentimentScores, qualityScores))
        print_graph(lang+" Code Quality", qualityScores)
        print_graph(lang+" Average Sentiment", sentimentScores)

if __name__ == '__main__':
    main()

from scipy.stats.stats import pearsonr
from DB import Database
from Users import Users
from utilities import retrieve_users, connect_to_db, VALID_LANGUAGES

def get_language_results(users):
    qualityScores = dict()
    sentimentScores = dict()
    for lang in VALID_LANGUAGES:
        qualityScores.update(lang, (user.qualityAverage for user in users if user.language == lang))
        sentimentScores.update(lang, (user.sentiment for user in users if user.language == lang))
    return qualityScores, sentimentScores
        

def main():
    database_connection = connect_to_db('results.sql')
    users = retrieve_users(database_connection, 'Users', 'commentor_login, language, sentiment_score, quality')
    qualityScores, sentimentScores = get_language_results(users)
    """
    TODO: get pearson coefficient
    """


    pass

if __name__ == '__main__':
    main()

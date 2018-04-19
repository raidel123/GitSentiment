"""
Will be initialized from sql database of users with their sentiment score and username
will make keeping track of a particular user and their relevant data for easy evaluation
"""
class Users:
    def __init__(self, username, sentiment):
        self.username = username
        self.sentiment = sentiment
        self.qualityScore = 0
    
    def add_quality_score(self, score):
        self.qualityScore += score
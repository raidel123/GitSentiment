"""
Will be initialized from sql database of users with their sentiment score and username
will make keeping track of a particular user and their relevant data for easy evaluation
"""
class Users:
    def __init__(self, **kwargs):
        self.username = kwargs.get('commentor_login', 0.0)
        self.sentiment = kwargs.get('sentiment_score', 0.0)
        self.qualityScore = 0
        self.qualityAverage = kwargs.get('quality', 0.0)
        self.dataCount = 0
        self.language = kwargs.get('language', "")
        self.pearson_correlation = 0.0
        self.pearson_significance = 0.0
    
    def add_quality_score(self, score):
        self.qualityScore += score
        self.dataCount += 1
        self.qualityAverage = self.qualityScore/self.dataCount

"""
Will be initialized from sql database of users with their sentiment score and username
will make keeping track of a particular user and their relevant data for easy evaluation
"""
class Users:
    def __init__(self, **kwargs):
        self.username = kwargs.get('commenter_login', 'test')
        self.sentiment = kwargs.get(
            'sentiment_pos', kwargs.get('sentiment_score', 0)) + kwargs.get('sentiment_neg', 0)
        self.sentimentAverage = 0
        self.qualityScore = 0
        self.qualityAverage = kwargs.get('quality', 0.0)
        self.dataCount = 0
        self.commentCount = 0
        self.language = kwargs.get('language', "")        

    def add_sentiment_score(self, score):
        self.sentiment += score
        self.commentCount += 1
        self.sentimentAverage = self.sentiment / self.commentCount
    def add_quality_score(self, score):
        self.qualityScore += score
        self.dataCount += 1
        self.qualityAverage = self.qualityScore/self.dataCount
    
    def __eq__(self, other):
        return self.username == other.username

    def __hash__(self):
        return hash(('username', self.username))

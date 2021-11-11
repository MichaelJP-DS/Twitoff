from flask_sqlalchemy import SQLAlchemy

# Create a DB Object

DB = SQLAlchemy()

# Make a User table by creating a User class

class User(DB.Model):
    '''Creates a User Table with SQLAlchemy'''

    #id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    #username column
    username = DB.Column(DB.String, nullable=False)

    newest_tweet_id = DB.Column(DB.BigInteger)
    # We don't need a tweets attribute b/c this is 
    # automatically being added by the backref in the tweet model
    def __repr__(self):
        return f'<User: {self.username}>'

# Make a Tweet table by creating a tweet class

class Tweet(DB.Model):
    '''Creates a User Table with SQLAlchemy'''

    #id column
    id = DB.Column(DB.BigInteger, primary_key=True)

    #text column
    text = DB.Column(DB.Unicode(300)) #unicode allows for multiple data types

    #vect column
    vect = DB.Column(DB.PickleType, nullable=False)
    
    # Create a relationship between a tweet and a user
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    
    # Finalize Relationship making sure it goes both ways
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f'<Tweet: {self.text}>'
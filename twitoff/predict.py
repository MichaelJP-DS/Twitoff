
from sklearn.linear_model import LogisticRegression
import numpy as np
from twitoff.models import Tweet, User
from .twitter import vectorize_tweet

def predict_user(user0_name, user1_name, hypo_tweet_text):
    '''Take in two usernames, query for the tweet vectorizations
    for the two users, compile the vectorizations into an X matrix
    vectorize the hypothetical tweet text generate and return a prediction'''

    # Query two users
    user0 = User.query.filter(User.username == user0_name).one()
    user1 = User.query.filter(User.username == user1_name).one()

    # Get the tweet vectorizations for the two Users
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Combine the vectors into an X matrix

    X = np.vstack([user0_vects, user1_vects])

    # Generate labes for y vector

    y = np.concatenate([np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    # Build and Fit Model
    log_reg = LogisticRegression().fit(X, y)

    # Vectorize hypothetical tweet
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # Return the predicted label:(0, 1)
    return log_reg.predict(hypo_tweet_vect.reshape(1, -1))




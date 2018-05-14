import sys
import os
import time
import tweepy
import csv

VERSION="0.1.1"

# pip install -r requirements.txt

# Visit https://apps.twitter.com to create a key

# Hard Coded Credentials, although set to None if unknown
CONSUMER_KEY_DEFAULT = None
CONSUMER_SECRET_DEFAULT = None

# Name of environment variables
ENVIRONMENT_NAME_FOR_CONSUMER_KEY = "TWITTER_API_CONSUMER_KEY"
ENVIRONMENT_NAME_FOR_CONSUMER_SECRET = "TWITTER_API_CONSUMER_SECRET"

consumer_key = os.getenv(ENVIRONMENT_NAME_FOR_CONSUMER_KEY, CONSUMER_KEY_DEFAULT)
consumer_secret = os.getenv(ENVIRONMENT_NAME_FOR_CONSUMER_SECRET, CONSUMER_SECRET_DEFAULT)

if not consumer_key : print( "%ERROR, please specify the consumer key in the environment as " + ENVIRONMENT_NAME_FOR_CONSUMER_KEY)
if not consumer_secret : print( "%ERROR, please specify the consumer secret in the environment as " + ENVIRONMENT_NAME_FOR_CONSUMER_SECRET)
if not consumer_key or not consumer_secret : sys.exit(1)

if len(sys.argv) < 2 :
    print("%Error, please list one or more Twitter screen names, separated by spaces")
    sys.exit(1)

OUTPUT_FILENAME = time.strftime("tweets-%Y-%m-%d_%H-%M-%S.csv")

# Authenticate our app
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth)



TWITTER_MAX_COUNT = 200

# As of this writing, 2018-05-13, the rate limite is 1500 per 15 minute window
# see https://developer.twitter.com/en/docs/basics/rate-limits.html
RUNNNING_API_COUNT = 0

def getPublicTweets(username, max_id=None):
    global RUNNNING_API_COUNT
    RUNNNING_API_COUNT += 1
    return api.user_timeline(username, count=TWITTER_MAX_COUNT, max_id=max_id)


def getNewMaxId(lastTweetResponse):
    global RUNNNING_API_COUNT
    RUNNNING_API_COUNT += 1
    return lastTweetResponse[len(lastTweetResponse) - 1].id - 1


# carraige returns and linefeeds really seem to confuse Excel, so we change them to spaces
translateTable = str.maketrans("\r\n", "  ")

TOTAL_TWEETS = 0

fieldnames = ["AuthorId", "AuthorName", "ScreenName", "FriendCount", "FollowersCount",
              "TweetId", "TweatCreated", "TweetText", "TweetSource", "Retweeted", "Favorited",
              "PossiblySensitiveContent"]
with open(OUTPUT_FILENAME, 'w', newline='') as csvfile:
    tweetwriter = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_ALL)
    tweetwriter.writerow(fieldnames)

    for index, screenName in enumerate(sys.argv):
        if index == 0: continue
        print("Processing @" + screenName + "  ", end='', flush=True)

        USER_TWEETS=0

        public_tweets = getPublicTweets(screenName)

        while len(public_tweets) > 0:

            print(".", end='', flush=True)

            for tweet in public_tweets:
                USER_TWEETS += 1
                tweetwriter.writerow([
                    tweet.author.id_str,
                    tweet.author.name,
                    "@" + tweet.author.screen_name,
                    tweet.author.friends_count,
                    tweet.author.followers_count,
                    tweet.id,
                    tweet.created_at,
                    tweet.text.translate(translateTable),
                    tweet.source,
                    tweet.retweet_count,
                    tweet.favorite_count,
                    tweet.possibly_sensitive if hasattr(tweet, "possibly_sensitive") else "null"
                ])

            nextMaxId = getNewMaxId(public_tweets)
            public_tweets = getPublicTweets(screenName, nextMaxId)

        print("  " + str(USER_TWEETS) + " tweets")
        TOTAL_TWEETS += USER_TWEETS
        print("  (" + str(RUNNNING_API_COUNT) + " API calls so far)")

if RUNNNING_API_COUNT >= 1500 :
    print("%WARNING, so data might be lost due to rate limiting (1500 API calls per 15 minute window);")
    print("          see https://developer.twitter.com/en/docs/basics/rate-limits.html")

print( "%INFORMATION, contents were written to " + OUTPUT_FILENAME)
print( "              ( " + str(TOTAL_TWEETS) + " total tweets )")
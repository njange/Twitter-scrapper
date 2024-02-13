import tweepy
import csv
import datetime

# Store API credentials securely in a separate file (e.g., credentials.py)
from credentials import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

# Authenticate with Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# Twitter account to get tweets from
twitter_account = 'StateHouseKenya'

# Define start date as January 1st, 2020
start_date = datetime.datetime(2020, 1, 1)

# Get tweets iteratively with pagination to avoid rate limits
max_tweets = 20 # Maximum tweets retrieved per API call
all_tweets = []

# Keep track of the oldest tweet retrieved so far
oldest_tweet_id = None

while True:
    try:
        tweets = api.user_timeline(screen_name=twitter_account, count=max_tweets, tweet_mode='extended', since_id=oldest_tweet_id)
        if not tweets:  # No more tweets to retrieve
            break

        # Reverse chronological order, newest tweets first
        all_tweets.extend(reversed(tweets))

        # Update oldest tweet ID for next iteration
        oldest_tweet_id = tweets[-1].id_str - 1

        # Check if we reached the start date
        if tweets[0].created_at < start_date:
            break

    except tweepy.TweepyException as e:
        # Handle errors gracefully, e.g., log the error and sleep for a while
        print("Error:", e)
        break

# Open CSV file in write mode with proper encoding
with open('statehouse_tweets.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['ID', 'Date', 'Tweet', 'Username', 'Retweets', 'Likes'])  # Write header

    # Write tweets to the CSV file, including additional information
    for tweet in all_tweets:
        writer.writerow([
            tweet.id_str,
            tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            tweet.full_text.replace('\n', ' '),
            tweet.user.screen_name,
            tweet.retweet_count,
            tweet.favorite_count
        ])

print("Downloaded", len(all_tweets), "tweets from StateHouseKenya.")

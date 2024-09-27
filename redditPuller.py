import os
import praw
import time
import csv
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get sensitive data from the environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_agent = os.getenv("USER_AGENT")

# Set up the Reddit client using the credentials from the .env file
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Specify the subreddit you want to pull the top post from
subreddit_name = "offmychest"  # Replace with the subreddit you want
subreddit = reddit.subreddit(subreddit_name)

# Get the top post of the day
top_post = next(subreddit.top(time_filter="day", limit=1))

csv_filename = f"{subreddit_name}_top_posts.csv"

# Open the CSV file for writing
csv_filename = f"{subreddit_name}_top_posts.csv"

# Open the CSV file for writing
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row, including a column for word count
    writer.writerow(['Title', 'Post Text', 'Word Count'])

    # Fetch the top posts of the day
    for submission in subreddit.top(time_filter="day", limit=10):  # Adjust the limit as needed
        if submission.is_self:  # Check if the post is a text-based post
            title = submission.title
            post_text = submission.selftext

            # Calculate the word count for the post
            word_count = len(post_text.split())

            # Write the title, post text, and word count to the CSV file
            writer.writerow([title, post_text, word_count])
            print(f"Added post: {title} (Word Count: {word_count})")
        else:
            print(f"Skipping non-text post: {submission.title}")
        
        # Sleep for 1 second to avoid rate limiting
        time.sleep(1)

print(f"CSV file '{csv_filename}' has been created.")

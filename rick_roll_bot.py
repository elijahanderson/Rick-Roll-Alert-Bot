# Rick Roll Bot - warns reddit users if a comment links to "Never Gonna Give You Up" by Rick Astley on Youtube
#
# By Eli Anderson
#
# Last edited 7.28.17
#


# praw is a tool that makes interacting with reddit much easier.
#


import praw

# time module is used so the bot won't go crazy

import time
import os


# Login the bot into reddit


def authenticate() :
    print('Authenticating...')
    reddit = praw.Reddit('RickRoll', user_agent='rick_roll_bot_test v0.1')
    print('Authenticated as ' + str(reddit.user.me()))
    return reddit


def run_bot(reddit, comments_replied_to2) :

    # Loop through the comments in all recent posts in all subreddits

    for comment in reddit.subreddit('all').comments(limit=None) :

        # check if youtube link is in any of those comments and comment has already been replied to

        if ('https://www.youtube.com/watch?v=dQw4w9WgXcQ' in comment.body or 'https://www.youtube.com/watch?v=6_b7RDuLwcI' in comment.body) and comment.id not in comments_replied_to2:

            print('Comment containing Rick Roll found!!')

            # Fetch username of author of the comment to be replied to
            username = comment.author.name

            # Go through user's recent comment history, record number of times that bastard Rick Rolls someone
            #
            # Loop through the comments
            rick_roll_count = 0

            for comment_hist in reddit.redditor(username).comments.new(limit=None) :

                # Find where they link the Rick Roll

                if 'https://www.youtube.com/watch?v=6_b7RDuLwcI' in comment_hist.body or 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' in comment_hist.body:
                    rick_roll_count += 1

            # Reply via comment
            #
            # If the user has a tendency to Rick Roll often, call them out on it

            if rick_roll_count > 5 :
                comment.reply('**WARNING --** If you click on that link, you\'ll be Rick Rolled!\n\n' +
                              '/u/' + username + ' has some explaining to do... they\'ve Rick Rolled on ' +
                              str(rick_roll_count) + ' other occasions!\n\n' +
                              '^^This is a bot reply. If you don\'t like it, just downvote and if it gets enough downvotes I\'ll gladly get rid of it.')
            else :
                comment.reply('**WARNING --** If you click on that link, you\'ll be Rick Rolled!\n\n' +
                              '^^This is a bot reply. If you don\'t like it, just downvote and if it gets enough downvotes I\'ll gladly get rid of it.')

            print('Replied to ' + comment.id)

            # Add comment ID to replied to list
            comments_replied_to2.append(comment.id)

            # Save comment ID to comments_replied_to2.txt (the 'a' means I am appending to the file)

            with open('comments_replied_to2.txt', 'a') as file:
                file.write(comment.id + '\n')

    # Sleep for ten seconds

    print('Sleeping for 10 seconds...')
    time.sleep(10)

# Save the comments that have been replied to in the past so the bot doesn't reply to same comments the after each time
# it is run
#
# Uses .txt file to store the comment IDs


def get_saved_comments() :

    # If .txt file with comment IDs doesnt exist, create one and return a blank array

    if not os.path.isfile('comments_replied_to2.txt') :
        comments_replied_to2 = []

    else :
        with open('comments_replied_to2.txt', 'r') as file :

            # Read contents of the file
            comments_replied_to2 = file.read()

            # split() by new line
            comments_replied_to2 = comments_replied_to2.split('\n')

            # Filter out the empty string at end of the .txt file
            # filter() filters out the first argument from the second argument
            # comments_replied_to = filter('', comments_replied_to)

    return comments_replied_to2

reddit = authenticate()

# To prevent spam, create list of comments already replied to

comments_replied_to2 = get_saved_comments()
print(comments_replied_to2)

# To automatically reply to comments, a while loop is used

while True :
    run_bot(reddit, comments_replied_to2)
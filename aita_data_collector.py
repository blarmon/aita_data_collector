import time
import random

import config
from get_submissions_between import submissions_pushshift_praw

# todo hook up to aws probably....  something along those lines.  we'll see.  have the ability to write out json or sql tho
# TODO.  group by the number of comments!  small medium and large

reddit = config.reddit_config
subreddit = reddit.subreddit('AmITheAsshole')

def check_valid_submission(created, length):
    # todo not already in the database
    # todo has a body (not deleted)
    days_old = abs((time.time() - created))
    print(created)
    print(days_old)
    if length >= 100 and days_old > 5:
        return True
    return False


if __name__ == '__main__':

    two_years_back = 1483228800
    rand_time = random.randint(two_years_back, int(time.time()))
    rand_submissions = submissions_pushshift_praw(reddit, 'AmItheAsshole', rand_time, limit=5)
    print(rand_submissions)
    print(reddit.auth.limits)
    for sub in rand_submissions:
        print(sub)
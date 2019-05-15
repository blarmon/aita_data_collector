import time
import random
import re
from collections import defaultdict

import config
from get_submissions_between import submissions_pushshift_praw

# todo hook up to aws probably....  something along those lines.  we'll see.  have the ability to write out json or sql tho
# TODO.  group by the number of comments!  small medium and large

reddit = config.reddit_config
subreddit = reddit.subreddit('AmITheAsshole')

def valid_submission(sub_body, comments):
    if sub_body == '[deleted]' or sub_body == '[removed]' or comments < 5:
        return False
    return True

def generate_submission_data(submission_id):
    submission = reddit.submission(id=submission_id)

    if not valid_submission(submission.selftext, submission.num_comments):
        return None

    aita_dict = defaultdict(int)

    # try:
    submission.comments.replace_more(limit=None)
    # except AssertionError as e:
    #     logger.log_error(time.time(), e, 'replace_more', write_lock)
    #     time_to_reset = reddit.auth.limits['reset_timestamp'] - time.time()
    #     time.sleep(time_to_reset)
    #     q.put(comment)
    #     return

    highest_rated_comment_body = None
    highest_comment_score = float('-inf')
    highest_rated_comment_author = None
    highest_rated_comment_author_id = None

    for comment in submission.comments.list():
        matcher = aita_regex.search(comment.body)
        if matcher:
            aita_dict[matcher.group(1)] += 1
            if comment.score > highest_comment_score:
                highest_comment_score = comment.score
                highest_rated_comment_body = comment.body
                highest_rated_comment_author = comment.author.name

    #todo, convert created date to a more standard datetime I think.
    aita_dict['total_votes'] = sum([v for v in aita_dict.values()])
    aita_dict['submission_id'] = submission_id
    aita_dict['submission_num_comments'] = submission.num_comments
    aita_dict['created'] = submission.created_utc
    aita_dict['edited'] = submission.edited
    aita_dict['score'] = submission.score
    aita_dict['body'] = submission.selftext
    aita_dict['title'] = submission.title
    aita_dict['upvote_ratio'] = submission.upvote_ratio
    aita_dict['highest_comment_score'] = highest_comment_score
    aita_dict['highest_rated_comment_body'] = highest_rated_comment_body
    aita_dict['highest_rated_comment_author'] = highest_rated_comment_author
    aita_dict['highest_rated_comment_author_id'] = highest_rated_comment_author_id


    return aita_dict


# TODO FINISH THIS NEXT :)  THEN MOVE ONTO YOUR LOGGING AND DATA FUNCTIONS
# todo threading after that?  yee


if __name__ == '__main__':

    aita_regex = re.compile(r'(YTA|NTA|ESH|NAH|INFO)')

    two_years_back = 1483228800
    rand_time = random.randint(two_years_back, int(time.time()) - 604800)
    rand_submissions = submissions_pushshift_praw(reddit, 'AmItheAsshole', rand_time, limit=1)

    for sub in rand_submissions:
        print(generate_submission_data('b4r6bd'))
    print(reddit.auth.limits)
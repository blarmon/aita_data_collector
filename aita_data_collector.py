import time
import random
import re
import threading

import config
from get_submissions_between import submissions_pushshift_praw
from write_out_data import write_csv, get_max_date

# todo hook up to aws probably....  something along those lines.  we'll see.  have the ability to write out json or sql tho
# TODO.  group by the number of comments!  small medium and large

reddit = config.reddit_config
subreddit = reddit.subreddit('AmITheAsshole')

def valid_submission(sub_body):
    if sub_body == '[deleted]' or sub_body == '[removed]':
        return False
    return True

def generate_submission_data(submission_id):
    submission = reddit.submission(id=submission_id)

    if not valid_submission(submission.selftext):
        return None

    aita_dict = {'YTA': 0, 'NTA': 0, 'ESH': 0, 'NAH': 0, 'INFO': 0}

    try:
        submission.comments.replace_more(limit=None)
    except AssertionError as e:
        # todo ADD MORE TO LOGGER, LIKE SUBMISSION ID.  WE CAN TRY THESE SUBMISSIONS AGAIN LATER :)
        # logger.log_error(time.time(), e, 'replace_more', write_lock)
        # time_to_reset = reddit.auth.limits['reset_timestamp'] - time.time()
        # time.sleep(time_to_reset)
        # q.put(comment)
        # todo should raise an error instead of returning None I think?
        return None

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
                highest_rated_comment_author = comment.author.name if comment.author else "N/A"
                highest_rated_comment_author_id = comment.author.id if comment.author else "N/A"
                # TODO highest rated comment VOTE!!!

    total_votes = sum([v for v in aita_dict.values()])

    #todo, convert created date to a more standard datetime I think.
    aita_dict['collected_datetime'] = time.time()
    aita_dict['total_votes'] = total_votes
    aita_dict['submission_id'] = submission_id
    aita_dict['submission_num_comments'] = submission.num_comments
    aita_dict['created_datetime'] = submission.created_utc
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
    write_lock = threading.Lock()

    max_date = get_max_date()
    if not max_date:
        max_date = 1483228800
    else:
        max_date += 1

    submissions = submissions_pushshift_praw(reddit=reddit, subreddit='AmItheAsshole', start=max_date, end=time.time(), limit=1, extra_query="")

    for sub in submissions:
        data = generate_submission_data(sub)
        if data:
          write_csv(data, write_lock)

    print(reddit.auth.limits)
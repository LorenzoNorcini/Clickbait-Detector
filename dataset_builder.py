import praw
import cPickle as pickle
import random

def download_reddit_news_data(save_to_file=True, file_name="NTRD", split=True):

    reddit = praw.Reddit(client_id='*', client_secret="*",
                         password='*', user_agent='*',
                         username='*')

    print "loggin to Reddit as " + str(reddit.user.me())

    titles = {
        "0": [],
        "1": []
    }

    print "\nLoading titles from file"

    with open('clickbait.dat') as f:
        titles["1"] = f.read().splitlines()

    with open('news.dat') as f:
        titles["0"] = f.read().splitlines()

    print "Downloading \'controversial\' submissions from r/savedyouaclick ..."
    for submission in reddit.subreddit('savedyouaclick').controversial('year'):
        t = submission.title
        titles["1"].append(t.split('|')[0])

    print "Downloading \'controversial\' submissions from r/news ..."
    for submission in reddit.subreddit('news').controversial('year'):
        titles["0"].append(submission.title)

    print "Downloading \'controversial\' submissions from r/inthenews ..."
    for submission in reddit.subreddit('inthenews').controversial('year'):
        titles["0"].append(submission.title)

    print "Downloading \'hot\' submissions from r/savedyouaclick ..."
    for submission in reddit.subreddit('savedyouaclick').hot(limit=None):
        t = submission.title
        titles["1"].append(t.split('|')[0])

    print "Downloading \'hot\' submissions from r/news ..."
    for submission in reddit.subreddit('news').hot(limit=None):
        titles["0"].append(submission.title)

    print "Downloading \'hot\' submissions from r/inthenews ..."
    for submission in reddit.subreddit('inthenews').hot(limit=None):
        titles["0"].append(submission.title)

    print "Downloading \'new\' submissions from r/savedyouaclick ..."
    for submission in reddit.subreddit('savedyouaclick').new():
        t = submission.title
        titles["1"].append(t.split('|')[0])

    print "Downloading \'new\' submissions from r/news ..."
    for submission in reddit.subreddit('news').new():
        titles["0"].append(submission.title)

    print "Downloading \'new\' submissions from r/inthenews ..."
    for submission in reddit.subreddit('inthenews').new():
        titles["0"].append(submission.title)

    print "Downloading \'top\' submissions from r/savedyouaclick ..."
    for submission in reddit.subreddit('savedyouaclick').top('all'):
        t = submission.title
        titles["1"].append(t.split('|')[0])

    print "Downloading \'top\' submissions from r/news ..."
    for submission in reddit.subreddit('news').top('all'):
        titles["0"].append(submission.title)

    print "Downloading \'top\' submissions from r/inthenews ...\n"
    for submission in reddit.subreddit('inthenews').top('all'):
        titles["0"].append(submission.title)

    if split:
        random.shuffle(titles["0"])
        random.shuffle(titles["1"])

        tr_size_0 = int(len(titles["0"])*.85)
        v_size_0 = int(len(titles["0"])*.1)
        te_size_0 = int(len(titles["0"])*.05)
        tr_size_1 = int(len(titles["1"])*.85)
        v_size_1 = int(len(titles["1"])*.1)
        te_size_1 = int(len(titles["1"])*.05)

        titles = {
            "train": {
                "0": titles["0"][:tr_size_0],
                "1": titles["1"][:tr_size_1]
            },
            "validation": {
                "0": titles["0"][tr_size_0+1:tr_size_0+v_size_0],
                "1": titles["1"][tr_size_1+1:tr_size_1+v_size_1],
            },
            "test": {
                "0": titles["0"][tr_size_0+v_size_0+1:tr_size_0+v_size_0+te_size_0],
                "1": titles["1"][tr_size_1+v_size_1+1:tr_size_1+v_size_1+te_size_1],
            }
        }

    if save_to_file:
        with open(file_name, 'wb') as f:
            pickle.dump(titles, f)
    else:
        return titles

"""Twitter consumer key and secret for Olipy

If you write a program based on Olipy, you can use these keys
instead of registering a brand new application with Twitter.

You will still need to get an access token for each Twitter account
you plan to use with your Olipy program.
"""
TWITTER_CONSUMER_KEY = "LeRTMqHlCzvWv4jpwDxIzQ"
TWITTER_CONSUMER_SECRET = "Q4fdZc4uAxl5g0ufSpgXieK5sSu4C91xc7w4U7Sh5fk"

from alphabet import Alphabet

try:
    import twitter
except Exception, e:
    twitter = None

if twitter:
    class Twitter(twitter.Twitter):
        """Simple wrapper around the python-twitter library for Olipy.

        https://github.com/bear/python-twitter    
        """
        def __init__(self, twitter_token, twitter_secret):
            oauth = twitter.OAuth(
                twitter_token, twitter_secret,
                TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
            super(Twitter, self).__init__(auth=oauth)

def pad(s, destination_size=None):
    """Pad a string using different whitespace characters to stop Twitter
    from thinking two tweets are the same.

    Will try to add 10% whitespace to the string.
    """
    if not destination_size:
        destination_size = min(len(s) + max(len(s)*0.1, 5), 140)
    padding = ''
    for i in range(len(s), destination_size):
        padding += Alphabet.random_whitespace()
    return s + padding

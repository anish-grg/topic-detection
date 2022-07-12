import tweepy
import pandas as pd
from app.settings import CONSUMER_API_KEY, CONSUMER_API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

def get_tweepy_api():
    """
    Prepare and return Tweepy API
    """
    auth = tweepy.OAuthHandler(CONSUMER_API_KEY, CONSUMER_API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth, wait_on_rate_limit=True, retry_count=10, retry_delay=3)

def get_luminaries():
    import os 
    print('***** WORKING DIRECTORY ****', os.getcwd())
    equity_seed = pd.read_csv('/app/files/equity_seed.csv', header=None)
    equity_seed.columns = ['handle']
    lumin_list = list(equity_seed['handle'])
    return lumin_list
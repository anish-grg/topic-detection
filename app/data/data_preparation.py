import pandas as pd 
from datetime import datetime
from data.twitter import get_luminaries, get_tweepy_api
from app.utils import month_dict, day_of_week
import pytz
import tweepy

# column names for dataframe
col_names = ['tweet_text', 'tweet_id', 'created_at', 'tweet_yr', 'tweet_mo', 'tweet_mo_nbr',
    'tweet_day', 'tweet_hr','tweet_day_of_week','tweet_dow_nbr', 'tweet_date', 'is_extended_tweet',
    'is_retweet', 'is_quote_tweet', 'url_count', 'hashtag_count', 'lang',
    'user_id', 'screen_name', 'link_to_tweet', 'followers_count',
    'friends_count', 'user_created_at', 'user_statuses_count', 'user_tweets_per_day',
    'user_age_days', 'retweet_count', 'favorite_count', 'rechecked_time']

def process_lumin_tweet(status,is_retweeted):
    try:
        status = status._json
    except AttributeError as error:
        pass
    
    #tweet_data = {}
    tweet_data = pd.DataFrame(columns = [col_names])
    try:
        tweet_text = (status["extended_tweet"]["full_text"]).strip().replace('\n', ' ').replace('\r', '').replace(',', '').replace(u'’', u"'")
        is_extended=True
    except KeyError:
        tweet_text = (status["full_text"]).strip().replace('\n', ' ').replace('\r', '').replace(',', '').replace(u'’', u"'")
        is_extended=False
        
    tweet_id = str(status["id"])
    created_at = status["created_at"]
    tweet_yr = created_at[-4:-1]+created_at[-1]
    tweet_mo = created_at[4:7]
    tweet_mo_nbr = month_dict[tweet_mo]
    tweet_day = created_at[8:10]
    tweet_day_of_week = created_at[0:3]
    tweet_dow_nbr = day_of_week[tweet_day_of_week]
    tweet_hr = created_at[11:13]
    s = "-"
    seq = (tweet_yr, tweet_mo_nbr, tweet_day)
    tweet_date = s.join(seq)
    is_extended_tweet = is_extended
    is_retweet = is_retweeted
    is_quote_tweet = hasattr(status, "quoted_status")
    lang = status["lang"]
    
    if is_extended:
        url_count = len(status["extended_tweet"]["entities"]["urls"])
        hashtag_count = len(status["extended_tweet"]["entities"]["hashtags"])
    else:
        url_count = len(status["entities"]["urls"])
        hashtag_count = len(status["entities"]["hashtags"])
    
    user_json = status["user"]
    
    user_id = str(user_json["id"])
    screen_name = user_json["screen_name"]
    link_to_tweet = "https://twitter.com/{}/status/{}".format(tweet_data["screen_name"], status["id"])
    followers_count = user_json["followers_count"]
    friends_count = user_json["friends_count"]
    user_created_at = user_json["created_at"]
    user_statuses_count = user_json["statuses_count"]
    user_age_days = ((datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.strptime(user_json['created_at'], "%a %b %d %H:%M:%S %z %Y")).days)

    try:
        tweets_per_day = user_json['statuses_count'] / user_age_days
    except ZeroDivisionError:
        tweets_per_day = 0
    user_tweets_per_day = tweets_per_day
    user_age_days = user_age_days
    
    retweet_count = status["retweet_count"]
    favorite_count = status["favorite_count"]
    rechecked_time = ((datetime.utcnow().replace(tzinfo=pytz.utc)))
    
    tweet_list = [tweet_text,
                  tweet_id,
                  created_at,
                  tweet_yr,
                  tweet_mo,
                  tweet_mo_nbr,
                  tweet_day,
                  tweet_hr,
                  tweet_day_of_week,
                  tweet_dow_nbr,
                  tweet_date,
                 is_extended_tweet,
                 is_retweet,
                 is_quote_tweet,
                 url_count,
                 hashtag_count,
                 lang,
                 user_id,
                 screen_name,
                 link_to_tweet,
                 followers_count,
                 friends_count,
                 user_created_at,
                 user_statuses_count,
                 user_tweets_per_day,
                 user_age_days,
                 retweet_count,
                 favorite_count,
                 rechecked_time]

    return tweet_list

def export_tweet_dataframe():
    # get API object
    api = get_tweepy_api()
    count = 0
    tweet_df = pd.DataFrame(columns=col_names) 
    lumin_list = get_luminaries()

    for lumin in lumin_list:
        temp_list=[]
        # print(lumin, count)
        count+=1
        tweets = []
        try:
            tweets = api.user_timeline(
                screen_name=lumin, 
                # getting last 10 tweets 
                count=10,
                include_rts = False,
                # Tweet mode extended necessary to keep full_text 
                # otherwise only the first 140 words are extracted
                tweet_mode = 'extended'
                )
        except tweepy.TweepError:
            print('Protected tweets cannot be accessed')

        all_tweets = []
        all_tweets.extend(tweets)
            
        for tweet in all_tweets:
            temp_list.append(process_lumin_tweet(tweet,is_retweeted=False))

        df = pd.DataFrame(temp_list, columns=col_names)
        tweet_df = pd.concat([tweet_df, df])
        # print("N of tweets downloaded", len(all_tweets))
    
    tweet_df.to_csv("app/files/sample_lumin_last_10_tweets.csv")
    print('Sample Tweets exported succesfully!')

def text_processing():
     #lowercase the text strings and remove punctuation
    # store in a new column
    df['processed'] = df['tweet_text'].apply(lambda x: re.sub(r'[^\w\s]',' ', x.lower()))  #\w [a-zA-Z0-9_] \s [ \t\n\r\f\v]
    
    # numerical feature engineering
    # total length of sentence
    df['length'] = df['processed'].apply(lambda x: len(x))
    # get number of words
    df['words'] = df['processed'].apply(lambda x: len(x.split(' ')))
    df['words_not_stopword'] = df['processed'].apply(lambda x: len([t for t in x.split(' ') if t not in stopWords]))
    # get the average word length
    df['avg_word_length'] = df['processed'].apply(lambda x: np.mean([len(t) for t in x.split(' ') if t not in stopWords]) if len([len(t) for t in x.split(' ') if t not in stopWords]) > 0 else 0)
    # get the sum(map(text.count, string.punctuation))/len(text)
    df['punctuationRatio'] = df['tweet_text'].apply(lambda x: sum(map(x.count, string.punctuation))/len(x))
    df['commas'] = df['tweet_text'].apply(lambda x: x.count(','))

    return(df)  # return a dataframe for now
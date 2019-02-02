import tweepy
import json
import logging
from datetime import datetime, timedelta
from email.utils import parsedate_tz

#override tweepy.StreamListener to add logic to on_data
class TwitterStreamListenner(tweepy.StreamListener):
    sync = None
    logger = None

    def to_datetime(self, datestring):
        time_tuple = parsedate_tz(datestring.strip())
        dt = datetime(*time_tuple[:6])
        return dt - timedelta(seconds=time_tuple[-1])
    
    def __init__(self, sync, logger):
       self.sync = sync         
       self.logger = logger

    def on_data(self, data):
        json_data = json.loads(data)    

        parsed_data = {
            'id'         : None,
            'data'       : None,
            'usuario'    : None,
            'texto'      : None,
            'location'   : None,
            'lang'       : None,
            'geo'        : None,
            'coordinates': None,
            'place'      : None,
            'hashtags'   :   [],
            'urls'       :   [],
            'user_mentions': [],  
            'retweeted'  : None,
            'quoted'     : None   
        }

        parsed_data['id']       = json_data['id']
        parsed_data['data']     = json_data['created_at']
        parsed_data['usuario']  = json_data['user']['screen_name']            

        if 'extended_tweet' in json_data:
            parsed_data['texto'] = json_data['extended_tweet']['full_text']
        else:
            parsed_data['texto'] = json_data['text']

        if 'retweeted_status' in json_data:
            parsed_data['retweeted'] = True
        else:
            parsed_data['retweeted'] = False

        if 'quoted_status' in json_data:
            parsed_data['quoted'] = True
        else:
            parsed_data['quoted'] = False


        parsed_data['location'] = json_data['user']['location']
        parsed_data['lang']     = json_data['lang']
        parsed_data['geo']      = json_data['geo']
        parsed_data['coordinates'] = json_data['coordinates']
        parsed_data['place']    = json_data['place']
        parsed_data['hashtags'] = json_data['entities']['hashtags']
        parsed_data['urls']     = json_data['entities']['urls']
        parsed_data['user_mentions'] = json_data['entities']['user_mentions']

        self.logger.debug(parsed_data)   

        created_at = self.to_datetime(parsed_data['data'])
        hour = int(created_at.hour)
        day  = int(created_at.weekday())

        if ( ( day >= 0 ) & ( day < 5) ):
            if ( ( ( hour >= 7 ) & ( hour < 10) ) |
                ( ( hour >= 17 ) & ( hour < 20) ) ) :
                self.sync.persist(parsed_data)
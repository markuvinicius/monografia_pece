import tweepy
import json
import logging

#override tweepy.StreamListener to add logic to on_data
class TwitterStreamListenner(tweepy.StreamListener):
    sync = None
    logger = None
    
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
        self.sync.persist(parsed_data)
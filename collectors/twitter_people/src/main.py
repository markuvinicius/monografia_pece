import tweepy
import json
from pymongo import MongoClient

class TwitterSync(object):

    def persist(self,document):
        pass

class MongoTwitterSync(TwitterSync):    
    database = None
    collection = None

    def __init__(self,host,port,bucket,collection):
        client     = MongoClient(host, port)         
        self.database   = client[bucket]
        self.collection = collection

        print('bucket = ' + bucket)               
        print('collection = ' + collection)

    def persist(self,document):        
        print('document = ' + str(document))
        document_id = self.database[self.collection].insert_one(document).inserted_id
        print('document id - ' + str(document_id))
        return document_id
        


#override tweepy.StreamListener to add logic to on_data
class TwitterStreamListenner(tweepy.StreamListener):
    sync = None
    

    def __init__(self, sync):
       self.sync = sync         

    def on_data(self, data):
        json_data = json.loads(data)    

        parsed_data = {
            'id'      : None,
            'data'    : None,
            'usuario' : None,
            'texto'   : None,
            'location': None,
            'lang'    : None,
            'geo'     : None,
            'coordinates': None,
            'place'   : None,
            'hashtags': [],
            'urls'    : [],
            'user_mentions': [],  
            'retweeted' : None,
            'quoted'  : None   
        }

        parsed_data['id'] = json_data['id']
        parsed_data['data'] = json_data['created_at']
        parsed_data['usuario'] = json_data['user']['screen_name']            

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
        parsed_data['lang'] = json_data['lang']
        parsed_data['geo'] = json_data['geo']
        parsed_data['coordinates'] = json_data['coordinates']
        parsed_data['place'] = json_data['place']
        parsed_data['hashtags'] = json_data['entities']['hashtags']
        parsed_data['urls'] = json_data['entities']['urls']
        parsed_data['user_mentions'] = json_data['entities']['user_mentions']

        print('+++++++++++++++++++++++++++')
        print(parsed_data)

        self.sync.persist(parsed_data)
            

#twitter_oauth_autentication
def tw_oauth(authfile):
    with open(authfile, "r") as f:
        ak = f.readlines()
    f.close()

    auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n", ""), ak[1].replace("\n", ""))
    auth1.set_access_token(ak[2].replace("\n", ""), ak[3].replace("\n", ""))
    return tweepy.API(auth1)


#main collector execution
if __name__ == "__main__":
    auth = tw_oauth('../config/tw_auth.k')

    mongo_sync = MongoTwitterSync('mongo',27017,'landing_zone','people_data')    
    listener = TwitterStreamListenner(mongo_sync)
    myStream = tweepy.Stream(auth=auth.auth, listener=listener)    


    follow = ['2735996796',
              '78682416',
              '76710878',
              '107185590',
              '339261594',
              '63542310',
              '153033613',
              '138075168',
              '385206072',
              '33535408',
              '728331254840602625',
              '34604337',
              '21087358',
              '327548721',
              '63459107',
              '132245890',
              '551433766',
              '861714397',
              '861720824',
              '861654906',
              '861605592',
              '281105655',
              '76713550',
              '861646484',
              '861589262',
              '76931509',
              '76714080',
              '36859263'
              ]
 
    myStream.filter(follow=follow, languages=['pt'])    
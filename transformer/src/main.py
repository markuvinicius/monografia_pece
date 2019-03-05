# encoding=utf8
import sys
import csv
from pymongo import MongoClient

origin_mongo_uri="mongodb://collector:collector123@ds145639.mlab.com:45639/landing_zone"
target_mongo_uri="mongodb://app:nodeapp01@ds249824.mlab.com:49824/labeling_zone"
 
def get_data(collection):          
     mongoClient = MongoClient(origin_mongo_uri)     
     db = mongoClient.landing_zone
     collection = db[collection]     
     tweets = collection.find({'$and': [ {'retweeted':False}, {'quoted':False},{'lang':"pt"},
                                         {'$or': [ 
                                             {'texto':{'$regex':u'acidente'}},                                             
                                             {'texto':{'$regex':u'colisao'}},
                                             {'texto':{'$regex':u'colisão'}},
                                             {'texto':{'$regex':u'capotamento'}},
                                             {'texto':{'$regex':u'batida'}},                        
                                             {'texto':{'$regex':u'trânsito'}},
                                             {'texto':{'$regex':u'choque'}},
                                             {'texto':{'$regex':u'engavetamento'}},
                                             {'texto':{'$regex':u'motoqueiro'}},
                                             {'texto':{'$regex':u'motocicleta'}},
                                             {'texto':{'$regex':u'sinistro'}},
                                             {'texto':{'$regex':u'desastre'}},
                                             {'texto':{'$regex':u'incidente'}},
                                             {'texto':{'$regex':u'veículo'}}
                                        ]}]})                                             
     return tweets

def dump_data(new_collection, data):     
     count = 1
     posts = []
     for item in data:          
          print("Transformando post %s" % count)

          """
          tweet = { 
               "id"       : item['id'],
               "data"     : item['data'],
               "usuario"  : item['usuario'],
               "retweeted": item['retweeted'],
               "quoted"  : item['quoted'],
               "lang"    : item['lang'],
               "texto"   : item['texto']
          }
          """
          tweet = item

          posts.append(tweet)
          count = count+1

     if len(posts)>0:     
          mongoClient = MongoClient(target_mongo_uri)     
          db = mongoClient.labeling_zone
          collection = db[new_collection]
          return collection.insert_many(posts)
     else:
          print("Sem documentos para inserir")
          return None               
             
if __name__ == "__main__":
     #reload(sys)
     #sys.setdefaultencoding('utf8')

     if len(sys.argv) == 3:
         collection      = sys.argv[1]   
         new_collection  = sys.argv[2]      
         
         data = get_data(collection)         
         insert = dump_data(new_collection,data)

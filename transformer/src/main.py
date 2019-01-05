# encoding=utf8
import sys
import csv
from pymongo import MongoClient
 
def get_data(collection):          
     mongoClient = MongoClient('192.168.0.47',27017)     
     db = mongoClient.landing_zone
     collection = db[collection]     
     tweets = collection.find({"retweeted":False,
                               "quoted":False,
                               "lang":"pt"
                              })

     return tweets

def dump_data(new_collection, data):     
     count = 1
     posts = []
     for item in data:          
          print("Transformando post %s" % count)

          tweet = { 
               "id"       : item['id'],
               "data"     : item['data'],
               "usuario"  : item['usuario'],
               #"retweeted": item['retweeted'],
               #"quoted"  : item['quoted'],
               #"lang"    : item['lang'],
               "texto"   : item['texto']
          }
          posts.append(tweet)
          count = count+1
          
     mongoClient = MongoClient('mongodb://app:nodeapp01@ds249824.mlab.com:49824/labeling_zone')     
     db = mongoClient.labeling_zone
     collection = db[new_collection]
     result = collection.insert_many(posts)

     return result   
          
             
if __name__ == "__main__":
     reload(sys)
     sys.setdefaultencoding('utf8')

     if len(sys.argv) == 3:
         collection      = sys.argv[1]   
         new_collection  = sys.argv[2]      
         
         data = get_data(collection)         
         insert = dump_data(new_collection,data)

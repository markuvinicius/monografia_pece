from TwitterSync import TwitterSync
from pymongo import MongoClient
from urllib.parse import quote_plus
import logging

class MongoTwitterSync(TwitterSync):    
	database = None
	collection = None
	logger = None

	def __init__(self, host, port, database, logger=None, user=None, password=None, collection=None ):
		self.logger = logger
		if  ( user is None ) | (password is None) | ( (user == "") & (password == "") ) :          
			uri = "mongodb://%s:%s" % (host, port)
		else:    
			uri = "mongodb://%s:%s@%s:%s/%s" % (quote_plus(user), quote_plus(password), host, port,database)

		client = MongoClient(uri)
		self.database   = client[database]
		self.collection = collection
            
	def persist(self,document):        
		self.logger.debug('Inserindo Documento : ' + str(document))        
		document_id = self.database[self.collection].insert_one(document).inserted_id
		self.logger.info('document_id - ' + str(document_id))
        
		return document_id

import abc
import xapian

import common 

CONFIG = common.getConfig()

class BaseIndexer(abc.ABC):
    database:xapian.WritableDatabase=None

    def __init__(self):
        self.database = xapian.WritableDatabase(CONFIG["DEFAULT"]["index.dir"], xapian.DB_CREATE_OR_OPEN)

    @abc.abstractmethod
    def index(self, document)->bool:
        pass
    
    def new_batch( self):
        self.database.begin_transaction()
    
    def save_batch(self):
        self.database.commit_transaction()
    
    def cancel_batch(self):
        self.database.cancel_transaction()
    
    def finish(self):
        self.database.flush()
        self.database.close()
        del self.database

class BaseSearcher(abc.ABC):
    database:xapian.Database=None
    def __init__(self):
        self.database = xapian.Database(CONFIG["DEFAULT"]["index.dir"])

    @abc.abstractmethod
    def search(self, query_string, offset, limit)->list:
        pass

    def finish(self):
        self.database.close()
        del self.database

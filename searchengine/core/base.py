import abc
import xapian

import config 

class BaseIndexer(abc.ABC):
    database:xapian.WritableDatabase=None

    def __init__(self):
        self.database = xapian.WritableDatabase(config.INDEX_DIR, xapian.DB_CREATE_OR_OPEN)

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
        self.database = xapian.Database(config.INDEX_DIR)

    @abc.abstractmethod
    def search(self, query, offset, limit)->list:
        pass

    def finish(self):
        self.database.close()
        del self.database

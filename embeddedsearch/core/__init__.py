import abc
import xapian

import config 

class BaseIndexer(abc.ABC):
    database:xapian.WritableDatabase=None

    def __init__(self):
        self.database = xapian.WritableDatabase(config.INDEX_PATH, xapian.DB_CREATE_OR_OPEN)
        self.database.begin_transaction()

    @abc.abstractmethod
    def index(self, document)->bool:
        pass
    
    def dispose(self):
        self.database.commit_transaction()
        self.database.flush()
        self.database.close()
        del self.database

class BaseSearcher(abc.ABC):
    database=None
    def __init__(self):
        self.database = xapian.Database(config.INDEX_PATH)
    
    @abc.abstractmethod
    def search(self, query, offset, limit)->list:
        pass

    def dispose(self):
        self.database.close()
        del self.database

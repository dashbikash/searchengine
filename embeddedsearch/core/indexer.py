import json
import zlib
import xapian

import config as cfg
from .pbutil import article_pb_marshal

def index_document(unique_id,document)->bool:
    db = xapian.WritableDatabase(cfg.INDEX_PATH, xapian.DB_CREATE_OR_OPEN)
    enquire = xapian.Enquire(db)
    
    query = xapian.Query(unique_id)
    enquire.set_query(query)
    matches = enquire.get_mset(0, 1)
    if matches.size() > 0:
        return False
    
    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("english")
    indexer.set_stemmer(stemmer)
    xapian_doc = xapian.Document()
    xapian_doc.set_data(article_pb_marshal(document))
    indexer.set_document(xapian_doc)
    
    indexer.index_text(document["headline"],1,"H")
    indexer.index_text(document["category"],1,"C")
    indexer.index_text(document["short_description"],1,"S")
    indexer.index_text(document["authors"],1,"A")
    xapian_doc.add_term(unique_id)  # Add the unique identifier as a term
    # Add the document to the database.
    db.add_document(xapian_doc)
    return True

import xapian
import xxhash

import config as cfg
from core import BaseIndexer
from .pbutil import article_pb_marshal
import pyonmttok

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
    
    indexer.index_text(document["category"],1,"C")

    content_text="\n".join([document["headline"],document["short_description"],document["authors"]])
    indexer.index_text(content_text,2,"Z")


    xapian_doc.add_term(unique_id)  # Add the unique identifier as a term
    # Add the document to the database.
    db.add_document(xapian_doc)
    return True


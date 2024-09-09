import json
import xapian

import config as cfg
from .pbutil import doc_pb_serialize

def index_document(unique_id,document)->bool:
    db = xapian.WritableDatabase(cfg.INDEX_PATH, xapian.DB_CREATE_OR_OPEN)
    enquire = xapian.Enquire(db)
    
    query = xapian.Query(unique_id)
    enquire.set_query(query)
    matches = enquire.get_mset(0, 1)
    if matches.size() > 0:
        print(f"Document with ID {unique_id} already exists. Skipping indexing.")
        return False
    
    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("english")
    indexer.set_stemmer(stemmer)
    xapian_doc = xapian.Document()
    xapian_doc.set_data(doc_pb_serialize(document))
    indexer.set_document(xapian_doc)
    index_text=[document[key] for key in document.keys()]
    indexer.index_text("\n".join(index_text))
    xapian_doc.add_term(unique_id)  # Add the unique identifier as a term
    # Add the document to the database.
    db.add_document(xapian_doc)
    return True

import json
import xapian

import config as cfg

def index_document(unique_id,document):
    db = xapian.WritableDatabase(cfg.INDEX_PATH, xapian.DB_CREATE_OR_OPEN)
    enquire = xapian.Enquire(db)
    
    query = xapian.Query(unique_id)
    enquire.set_query(query)
    matches = enquire.get_mset(0, 1)
    if matches.size() > 0:
        print(f"Document with ID {unique_id} already exists. Skipping indexing.")
        return
    
    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("english")
    indexer.set_stemmer(stemmer)
    doc = xapian.Document()
    doc.set_data(json.dumps(document).encode('utf8'))
    indexer.set_document(doc)
    indexer.index_text(doc.get_data())

    doc.add_term(unique_id)  # Add the unique identifier as a term
    # Add the document to the database.
    db.add_document(doc)

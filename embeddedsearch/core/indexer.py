import json
import xapian

import config

def index_document(document):
    database = xapian.WritableDatabase(config.INDEX_PATH, xapian.DB_CREATE_OR_OPEN)

    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("english")
    indexer.set_stemmer(stemmer)
    doc = xapian.Document()
    doc.set_data(json.dumps(document).encode('utf8'))
    indexer.set_document(doc)
    indexer.index_text(json.dumps(document).encode('utf8'))

    # Add the document to the database.
    database.add_document(doc)

import csv
import json
import sys

import xxhash
from core.indexer import index_document
from core.searcher import search_documents

from core import pbutil


document_data = [
    {'id': 1, 'title': 'Document 1', 'content': 'This is the content of document One'},
    {'id': 2, 'title': 'Document 2', 'content': 'This is the content of document Two'},
    {'id': 3, 'title': 'Document 3', 'content': 'This is the content of document Three'},
]

# for document in document_data:
#     index_document(document)


def index_news():
    with open('tests/news.csv', mode ='r') as file:    
       csvFile = csv.DictReader(file)
       for idx,lines in enumerate(csvFile):
            print("%d: [OK] %s"%(idx,lines["links"]))
            index_document(xxhash.xxh64_hexdigest(lines["links"]),lines)

if len(sys.argv) > 1:
    if sys.argv[1] == 'i':
        print("Indexing .")
        index_news()
    if sys.argv[1] == 's':    
        query_string = sys.argv[2]
        result = search_documents(query_string)
        if "data" in result.keys() :
            for doc in result["data"]:
                print(pbutil.doc_pb_deserialize(doc))
else:
    print("No command line argument provided.")






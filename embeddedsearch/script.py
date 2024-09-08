import csv
import json
import sys

import xxhash
from core.indexer import index_document
from core.searcher import search_documents
import langdetect


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
       for lines in csvFile:
            print("[OK] "+lines["links"])
            index_document(xxhash.xxh64_hexdigest(lines["links"]),lines)

if len(sys.argv) > 1:
    if sys.argv[1] == 'i':
        print("Indexing .")
        index_news()
    if sys.argv[1] == 's':    
        query_string = sys.argv[2]
        result = search_documents(query_string)
        for doc in result["data"]:
            item=json.loads(doc.decode("utf-8"))
            print(item)
            print(langdetect.detect(item["short_description"]))
else:
    print("No command line argument provided.")






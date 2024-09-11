import csv
import json
import sys
import time

import xxhash
from core.indexer import index_document
from core.searcher import search_documents

from core import pbutil
import urllib.request
import os
import time

def index_news():
    if not os.path.exists('/tmp/news.csv'):
        urllib.request.urlretrieve("https://gitlab.com/mrdash/datasets/-/raw/main/news_category.csv?ref_type=heads&inline=false", "/tmp/news.csv")

    with open('/tmp/news.csv', mode ='r') as file:
        csvFile = csv.DictReader(file)
        count=0
        start_time = time.time()
        for line in csvFile:
            if index_document(xxhash.xxh64_hexdigest(line["link"]),line):
                print("[\u2713] %s"%(line["link"]))
                count+=1
            else:
                print("[x] %s"%(line["link"]))
        print("Total documents indexed: %d" % count)
        print("Total time taken: %d" % (start_time-time.time()))



def search_news():
    query_string = sys.argv[2]
    result = search_documents(query_string)
    if "data" in result.keys() :
        for doc in result["data"]:
            print(pbutil.article_pb_unmarshal(doc))

if len(sys.argv) > 1:
    if sys.argv[1] == 'i':
        print("Indexing...")
        index_news()
    if sys.argv[1] == 's':
        search_news() 
        
else:
    print("No command line argument provided.")






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
        limit=int(sys.argv[2]) if len(sys.argv)==3 else  0
        start_time = time.time()
        for line in csvFile:
            if (limit==0 or count<limit) and index_document(xxhash.xxh64_hexdigest(line["link"]),line):
                print("[\033[92m\u2713\033[00m] %s"%(line["link"]))
                count+=1
            elif limit>0 and count>=limit:
                break
            else:
                print("[\033[91mx\033[00m] %s"%(line["link"]))
        print("Total documents indexed: %d" % count)
        print("Total time taken: %d" % (time.time()-start_time))



def search_news():
    query_string = sys.argv[2]
    result = search_documents(query_string)
    if "data" in result.keys() :
        for doc in result["data"]:
            print(doc)


if len(sys.argv) > 1:
    if sys.argv[1] == 'i':
        print("Indexing...")
        index_news()
    if sys.argv[1] == 's':
        search_news() 
        
else:
    print("No command line argument provided.")






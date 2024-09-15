import csv
import sys
import time

import urllib.request
import os
import time
from core.news_engine import NewsIndexer,NewsSearcher


TEXT_RED = '\033[91m'
TEXT_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

def index_news():
    
    if not os.path.exists('/tmp/news.csv'):
        print("Downloading news dataset...")
        urllib.request.urlretrieve("https://gitlab.com/mrdash/datasets/-/raw/main/news_category.csv?ref_type=heads&inline=false", "/tmp/news.csv")

    print("Indexing news dataset...")
    indexer=NewsIndexer()
    with open('/tmp/news.csv', mode ='r') as file:
        csvFile = csv.DictReader(file)
        count=0
        limit=int(sys.argv[2]) if len(sys.argv)==3 else  0
        start_time = time.time()
        for line in csvFile:
            if (limit==0 or count<limit) and indexer.index(line):
                print("["+TEXT_GREEN+"\u2713"+RESET_COLOR+"] %s"%(line["link"]))
                count+=1
            elif limit>0 and count>=limit:
                break
            else:
                print("["+TEXT_RED+"x"+RESET_COLOR+"] %s"%(line["link"]))
        indexer.done()
        print("Documents indexed: %d" % count)
        print("Time taken: %d" % (time.time()-start_time))



def search_news():
    searcher =NewsSearcher()
    query_string = sys.argv[2]
    result = searcher.search(query_string)
    searcher.done()
    if "data" in result.keys() :
        for doc in result["data"]:
            print(doc)


if len(sys.argv) > 1:
    if sys.argv[1] == 'i':
        index_news()
    if sys.argv[1] == 's':
        search_news() 
        
else:
    print("No command line argument provided.")






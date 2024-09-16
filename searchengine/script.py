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
        print("Downloading news...")
        urllib.request.urlretrieve("https://gitlab.com/mrdash/datasets/-/raw/main/news_category.csv?ref_type=heads&inline=false", "/tmp/news.csv")

    print("Indexing news...")
    indexer=NewsIndexer()
    with open('/tmp/news.csv', mode ='r') as file:
        csvFile = csv.DictReader(file)
        count=0
        limit=int(sys.argv[2]) if len(sys.argv)==3 else  0
        start_time = time.time()
        batch_reset=True
        batch_size=2500
        for i,line in enumerate(csvFile):
            if batch_reset:
                indexer.new_batch()
                batch_reset=False
            if (limit==0 or count<limit) and indexer.index(line):
                count+=1
                print("["+TEXT_GREEN+"\u2713"+RESET_COLOR+"] %s"%(line["link"]))
                
            elif limit>0 and count>=limit:
                break
            else:
                print("["+TEXT_RED+"x"+RESET_COLOR+"] %s"%(line["link"]))
            
            if i%batch_size==0:
                indexer.save_batch()
                batch_reset=True
            
        if not batch_reset:
            indexer.save_batch()

        indexer.finish()
        print("Documents indexed: %d" % count)
        print("Time taken: %d" % (time.time()-start_time))


def search_news():
    searcher =NewsSearcher()
    query_string = sys.argv[2]
    page=int(sys.argv[3]) if len(sys.argv)==4 else 1
    result = searcher.search(query_string, (page-1)*10, 10)
    searcher.finish()
    if "data" in result.keys() :
        for i,doc in enumerate( result["data"]):
            print("[%d] %s" % (i+1,doc))


if len(sys.argv) > 1:
    if sys.argv[1] == 'i':
        index_news()
    if sys.argv[1] == 's':
        search_news() 
        
else:
    print("No command line argument provided.")






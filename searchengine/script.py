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
        batch_count=0
        batch_size=2000
        
        for line in csvFile:
            if (limit==0 or count<limit) and indexer.index(line):
                if batch_count==0: indexer.new_batch()
                print("["+TEXT_GREEN+"\u2713"+RESET_COLOR+"] %s"%(line["link"]))
                count+=1
                batch_count+=1
            elif limit>0 and count>=limit:
                break
            else:
                print("["+TEXT_RED+"x"+RESET_COLOR+"] %s"%(line["link"]))
            
            if batch_count>=batch_size:
                batch_count=0
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
        print("Estimated: %s" % result["estimated"])
        for i,doc in enumerate( result["data"]):
            print("[%d] %s" % (i+1,doc))


if len(sys.argv) > 1:
    if sys.argv[1] == 'i':
        index_news()
    if sys.argv[1] == 's':
        search_news() 
        
else:
    print("No command line argument provided.")






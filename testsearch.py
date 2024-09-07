import sys
from embeddedsearch.core.searcher import search_documents


query_string = sys.argv[1]
result = search_documents(query_string)
for doc in result["data"]:
    print(doc.decode("utf-8")+"\n")
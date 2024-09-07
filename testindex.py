import csv

from embeddedsearch.core.indexer import index_document


document_data = [
    {'id': 1, 'title': 'Document 1', 'content': 'This is the content of document One'},
    {'id': 2, 'title': 'Document 2', 'content': 'This is the content of document Two'},
    {'id': 3, 'title': 'Document 3', 'content': 'This is the content of document Three'},
]

# for document in document_data:
#     index_document(document)

with open('tests/news.csv', mode ='r') as file:    
       csvFile = csv.DictReader(file)
       for lines in csvFile:
            print(lines["links"])
            index_document(lines)


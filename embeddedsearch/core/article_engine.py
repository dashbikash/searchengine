import xapian
import xxhash
from core import BaseIndexer,BaseSearcher
from .pbutil import article_pb_marshal,article_pb_unmarshal
import pyonmttok
from datetime import datetime
import pb.documents_pb2 as pb

class ArticleIndexer(BaseIndexer):
    def __init__(self):
        super().__init__()
        self._tokenizer=pyonmttok.Tokenizer("conservative", joiner_annotate=True)

    def index(self, document)->bool:
        unique_id = xxhash.xxh3_64_hexdigest(document["link"])
        
        
        if self._document_exists(unique_id):
            return False

        indexer = xapian.TermGenerator()
        stemmer = xapian.Stem("english")
        indexer.set_stemmer(stemmer)
        xapian_doc = xapian.Document()
        xapian_doc.set_data(article_pb_marshal(document))
        indexer.set_document(xapian_doc)
        
        indexer.index_text(document["category"],1,"C")

        content_text="\n".join([document["headline"],document["short_description"],document["authors"]])
        indexer.index_text(content_text,2,"Z")

        for token in self._tokenize(content_text):
            self.database.add_spelling(token)

        xapian_doc.add_term(unique_id)  # Add the unique identifier as a term
        # Add the document to the database.
        self.database.add_document(xapian_doc)
        return True
    
    def _document_exists(self, unique_id):
        enquire = xapian.Enquire(self.database)
        query = xapian.Query(unique_id)
        enquire.set_query(query)
        matches = enquire.get_mset(0, 1)
        return True if matches.size() > 0 else False
        
    
    def _tokenize(self, text:str)->list:
        return self._tokenizer.tokenize(text)[0]


class ArticleSearcher(BaseSearcher):
    def __init__(self):
        super().__init__()
        pass

    def search(self, query="", offset=0, limit=10):
        result={}
        try:
            self.database.reopen()

            # Parse the query string to produce a Xapian::Query object.
            query_parser = xapian.QueryParser()
            query_parser.set_database(self.database)

            query_parser.set_stemmer(xapian.Stem("english"))
            query_parser.set_stemming_strategy(xapian.QueryParser.STEM_SOME)

            query_parser.add_prefix("category", "C")

            # Set the query parser flags to enable OR operator
            query_parser.set_default_op(xapian.Query.OP_OR)
            
            flags= xapian.QueryParser.FLAG_DEFAULT | xapian.QueryParser.FLAG_SPELLING_CORRECTION
            query_parsed = query_parser.parse_query(query, flags)
            
            print("Parsed query: %s" % str(query_parsed))

            print("Corrected query: %s" % str(query_parser.get_corrected_query_string()))
            
            # Start an enquire session.
            enquire = xapian.Enquire(self.database)
            enquire.set_query(query_parsed)
            matches = enquire.get_mset(offset, limit)

            # Display the results.
            print ("%i results found." % matches.get_matches_estimated())
            print ("Results 1-%i:" % matches.size())
            if matches.size()>0:
                result["data"]=[ article_pb_unmarshal(m.document.get_data()) for m in matches]
                result["estimated"]=matches.get_matches_estimated()
                result["offset"]=offset
                result["limit"]=limit
        finally:
            return result



def article_pb_marshal(article):
    pb_article = pb.Article()
    if 'link' in article.keys() : pb_article.link=article['link']
    if 'category' in article.keys() : pb_article.category = article['category']
    if 'headline' in article.keys() : pb_article.headline = article['headline']
    if 'short_description' in article.keys() : pb_article.short_description = article['short_description']
    if 'authors' in article.keys() : pb_article.authors=article['authors']
    pb_article.date = datetime.strptime(article['date'], '%Y-%m-%d')
    return pb_article.SerializeToString()
    

def article_pb_unmarshal(article_serialized):
    pb_article = pb.Article()
    pb_article.ParseFromString(article_serialized)
    article = {
        "link": pb_article.link,
        "category": pb_article.category,
        "headline": pb_article.headline,
        "short_description": pb_article.short_description,
        "authors": pb_article.authors,
        "date": pb_article.date.ToDatetime().strftime('%Y-%m-%d')
    }
    return article
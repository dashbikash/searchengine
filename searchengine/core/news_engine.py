import json
import xapian
import xxhash
from core.base import BaseIndexer,BaseSearcher
import pyonmttok
from datetime import datetime
import common
import pb.documents_pb2 as pb

LOG=common.getLogger(__name__)

class NewsIndexer(BaseIndexer):
    
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
        xapian_doc.set_data(news_pb_marshal(document))
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


class NewsSearcher(BaseSearcher):
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
            
            LOG.info("Parsed query: %s" % str(query_parsed))
 
            LOG.info("Corrected query: %s" % str(query_parser.get_corrected_query_string()))
            
            # Start an enquire session.
            enquire = xapian.Enquire(self.database)
            enquire.set_query(query_parsed)
            matches = enquire.get_mset(offset, limit)

            # Display the results.
            
            # LOG.disabled("%i results found." % matches.get_matches_estimated())
            # LOG.disabled("Results 1-%i:" % matches.size())
            if matches.size()>0:
                result["data"]=[ news_pb_unmarshal(m.document.get_data()) for m in matches]
                result["estimated"]=matches.get_matches_estimated()
                result["offset"]=offset
                result["limit"]=limit
        finally:
            return result



def news_pb_marshal(news):
    pb_news = pb.DummyNews(link=news['link'],category=news['category'],headline=news['headline'],short_description=news['short_description'],authors=news['authors'],date=datetime.strptime(news['date'], '%Y-%m-%d'))
    # if 'link' in news.keys() : pb_news.link=news['link']
    # if 'category' in news.keys() : pb_news.category = news['category']
    # if 'headline' in news.keys() : pb_news.headline = news['headline']
    # if 'short_description' in news.keys() : pb_news.short_description = news['short_description']
    # if 'authors' in news.keys() : pb_news.authors=news['authors']
    # pb_news.date = datetime.strptime(news['date'], '%Y-%m-%d')
    
    return pb_news.SerializeToString()
    # return json.dumps(news).encode('utf-8')
    

def news_pb_unmarshal(news_serialized):
    pb_news = pb.DummyNews()
    pb_news.ParseFromString(news_serialized)
    news = {
        "link": pb_news.link,
        "category": pb_news.category,
        "headline": pb_news.headline,
        "short_description": pb_news.short_description,
        "authors": pb_news.authors,
        "date": pb_news.date.ToDatetime().strftime('%Y-%m-%d')
    }
    return news
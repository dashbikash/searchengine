import xapian
import xxhash
from core.base import BaseIndexer,BaseSearcher
import tiktoken
from datetime import datetime
import common
import pb.documents_pb2 as pb

LOG=common.getLogger(__name__)

class NewsIndexer(BaseIndexer):
    
    def __init__(self):
        super().__init__()
        self._tokenizer=tiktoken.get_encoding("cl100k_base")

    def index(self, document)->bool:
        unique_id = xxhash.xxh3_128_hexdigest(document["link"])

        if self._document_exists(unique_id):
            return False

        term_generator = xapian.TermGenerator()
        term_generator.set_stemmer(xapian.Stem("english"))
        term_generator.set_stemming_strategy(xapian.TermGenerator.STEM_SOME)
        xapian_doc = xapian.Document()
        xapian_doc.set_data(news_pb_marshal(document))
        term_generator.set_document(xapian_doc)
        
        term_generator.index_text(document["category"],1,"C")
        term_generator.index_text(document["headline"])
        term_generator.index_text(document["short_description"])
        term_generator.index_text(document["authors"])

        for token in self._tokenize("\n".join([document["headline"],document["short_description"]])):
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
        
        return [self._tokenizer.decode_single_token_bytes(t) for t in  self._tokenizer.encode(text)]


class NewsSearcher(BaseSearcher):
    def __init__(self):
        super().__init__()
        pass

    def search(self, query_string="", offset=0, limit=10):
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
            
            flags = (
                xapian.QueryParser.FLAG_DEFAULT |
                xapian.QueryParser.FLAG_SPELLING_CORRECTION|
                xapian.QueryParser.FLAG_PHRASE
            )
            query_parsed = query_parser.parse_query(query_string, flags)
            
            LOG.info("Parsed query: %s" % str(query_parsed))
            LOG.info("Corrected query: %s" % str(query_parser.get_corrected_query_string()))
            
            # Start an enquire session.
            enquire = xapian.Enquire(self.database)
            enquire.set_weighting_scheme(xapian.TfIdfWeight())
            enquire.set_query(query_parsed)
            matches = enquire.get_mset(offset, limit)

            # Display the results.
            LOG.info("Estimated records %i " % matches.get_matches_estimated())

            if matches.size()>0:
                result["data"]=[ news_pb_unmarshal(m.document.get_data()) for m in matches]
                result["estimated"]=matches.get_matches_estimated()
                result["offset"]=offset
                result["limit"]=limit
        except Exception as e:
            LOG.error("Error searching: %s" % str(e))
        finally:
            return result



def news_pb_marshal(news):
    
    return pb.DummyNews(link=news['link'],category=news['category'],headline=news['headline'],short_description=news['short_description'],authors=news['authors'],date=datetime.strptime(news['date'], '%Y-%m-%d')).SerializeToString()
    # return json.dumps(news).encode('utf-8')
    

def news_pb_unmarshal(news_serialized):
    pb_news = pb.DummyNews()
    pb_news.ParseFromString(news_serialized)

    return {
        "link": pb_news.link,
        "category": pb_news.category,
        "headline": pb_news.headline,
        "short_description": pb_news.short_description,
        "authors": pb_news.authors,
        "date": pb_news.date.ToDatetime().strftime('%Y-%m-%d')
    }
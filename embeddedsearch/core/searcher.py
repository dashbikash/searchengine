
import xapian


import config as cfg
from .pbutil import article_pb_unmarshal

def search_documents(query_string, offset=0, limit=10):
    result={}
    try:
        database = xapian.Database(cfg.INDEX_PATH)
        database.reopen()

        # Parse the query string to produce a Xapian::Query object.
        query_parser = xapian.QueryParser()
        query_parser.set_database(database)

        query_parser.set_stemmer(xapian.Stem("english"))
        query_parser.set_stemming_strategy(xapian.QueryParser.STEM_SOME)

        query_parser.add_prefix("category", "C")

        # Set the query parser flags to enable OR operator
        query_parser.set_default_op(xapian.Query.OP_OR)
        
        flags= xapian.QueryParser.FLAG_DEFAULT | xapian.QueryParser.FLAG_SPELLING_CORRECTION
        query = query_parser.parse_query(query_string, flags)
        
        print("Parsed query: %s" % str(query))

        print("Corrected query: %s" % str(query_parser.get_corrected_query_string()))
        
        # Start an enquire session.
        enquire = xapian.Enquire(database)
        enquire.set_query(query)
        matches = enquire.get_mset(offset, limit)

        

        # Display the results.
        print ("%i results found." % matches.get_matches_estimated())
        print ("Results 1-%i:" % matches.size())
        if matches.size()>0:
            result["data"]=[ article_pb_unmarshal(m.document.get_data()) for m in matches]
            result["total"]=matches.get_matches_estimated()
            result["offset"]=offset
            result["limit"]=limit
    finally:
        return result
    


import xapian


import config as cfg

def search_documents(query_string, offset=0, limit=20):
    database = xapian.Database(cfg.INDEX_PATH)
    database.reopen()
    # Start an enquire session.
    enquire = xapian.Enquire(database)

    # Combine the rest of the command line arguments with spaces between
    # them, so that simple queries don't have to be quoted at the shell
    # level.

    # Parse the query string to produce a Xapian::Query object.
    qp = xapian.QueryParser()
    stemmer = xapian.Stem("english")
    qp.set_stemmer(stemmer)
    qp.set_database(database)
    qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME_FULL_POS)
    query = qp.parse_query(query_string)
    print ("Parsed query is: %s" % str(query))

    # Find the top 10 results for the query.
    enquire.set_query(query)
    matches = enquire.get_mset(offset, limit)

    # Display the results.
    print ("%i results found." % matches.get_matches_estimated())
    print ("Results 1-%i:" % matches.size())

    result={}
    
    result["data"]=[m.document.get_data() for m in matches]
    result["total"]=matches.get_matches_estimated()
    result["offset"]=offset
    result["limit"]=limit

    return result
    # for m in matches:
    #     print ("%i: %i%% docid=%i [%s]" % (m.rank + 1, m.percent, m.docid, m.document.get_data()))

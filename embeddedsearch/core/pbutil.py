# link,headline,category,short_description,authors,date
# https://www.huffpost.com/entry/covid-boosters-uptake-us_n_632d719ee4b087fae6feaac9,Over 4 Million Americans Roll Up Sleeves For Omicron-Targeted COVID Boosters,U.S. NEWS,Health experts said it is too early to predict whether demand would match up with the 171 million doses of the new boosters the U.S. ordered for the fall.,"Carla K. Johnson, AP",2022-09-23

from datetime import datetime
import pb.documents_pb2 as pb

def article_pb_marshal(article):
    pb_article = pb.Article()
    pb_article.link=article['link']
    pb_article.category = article['category']
    pb_article.headline = article['headline']
    pb_article.short_description = article['short_description']
    pb_article.authors=article['authors']
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


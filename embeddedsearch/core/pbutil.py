# {'category': 'WELLNESS', 'headline': 'Bye-Bye Retirement, Hello Life!', 'links': 'https://www.huffingtonpost.com/entry/byebye-retirementhello-li_us_5b9dccd0e4b03a1dcc8d0cec', 'short_description': 'What if there is no retirement? What if we don\'t wait until 65 to enjoy life and connect with our passions? What if the so called "Act 2" when retirees find their dream jobs doing what they love to do actually happens now when we are in our 20s, 30s and 40s?', 'keywords': 'byebye-retirementhello-li'}
import pb.documents_pb2 as pb

def doc_pb_serialize(document):
    pb_doc = pb.Document()
    pb_doc.category = document['category']
    pb_doc.headline = document['headline']
    pb_doc.links=document['links']
    pb_doc.short_description = document['short_description']
    pb_doc.keywords=document['keywords']
    return pb_doc.SerializeToString()

def doc_pb_deserialize(document_serialized):
    pb_doc = pb.Document()
    pb_doc.ParseFromString(document_serialized)
    document = {
        'category': pb_doc.category,
        'headline': pb_doc.headline,
        'links': pb_doc.links,
        'short_description': pb_doc.short_description,
        'keywords': pb_doc.keywords
    }
    return document


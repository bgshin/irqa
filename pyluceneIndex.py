import jnius_config

cpath ='./lib/luceneInterface.jar'
jnius_config.set_classpath(cpath)

from jnius import autoclass
import json

Stack = autoclass('java.util.Stack')
luceneInterface = autoclass('luceneInterface')

index="./index/"
stopwords="./stopwords.txt"

luceneInterface.makeIndexWriter(index, stopwords)

with open('./data/documents.json') as data_file:
    data = json.load(data_file)

    for d in data:
        print d['doc_id'], len(d['text'])
        if len(d['text'])>30000:
            luceneInterface.indexDoc(d['doc_id'], "contents",  d['text'][0:30000].encode("utf-8"))
        else:
            luceneInterface.indexDoc(d['doc_id'], "contents",  d['text'].encode("utf-8"))

luceneInterface.writer.close()


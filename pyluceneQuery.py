import jnius_config

cpath ='./lib/luceneInterface.jar'
jnius_config.set_classpath(cpath)

from jnius import autoclass
import json

luceneInterface = autoclass('luceneInterface')

index="./index/"
stopwords="./stopwords.txt"

answercount=0
questioncount=0

with open('./data/questions.json') as data_file:
    qustions = json.load(data_file)
    questioncount=len(qustions)

    for q in qustions:
        print q['question'], ":", q['doc_id']
        docs = luceneInterface.query(index, stopwords, q['question'], 5)
        if docs.size()==0:
            continue

        queryanswer = docs.get(0).get("docid")
        goldanswer = q['doc_id'].encode("utf-8")

        if queryanswer==goldanswer:
            answercount = answercount+1


print questioncount,answercount
print answercount/(questioncount*1.0)*100



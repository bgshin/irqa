from whoosh.index import create_in
from whoosh.fields import *
import argparse


def indexFiles(indexpath):
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    ix = create_in(indexpath, schema)
    writer = ix.writer()
    writer.add_document(title=u"First document", path=u"/a",
                        content=u"This is the first document we've added!")
    writer.add_document(title=u"Second document", path=u"/b",
                        content=u"The second one is even more interesting!")
    writer.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("datapath")
    parser.add_argument("indexpath")
    args = parser.parse_args()

    indexFiles(args.indexpath)

    print args.datapath, args.indexpath


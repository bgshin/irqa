from whoosh.qparser import QueryParser
import whoosh.index as index
import argparse

def query(indexpath):
    ix = index.open_dir(indexpath)

    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse("first")
        results = searcher.search(query)
        print results[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("indexpath")
    args = parser.parse_args()

    query(args.indexpath)
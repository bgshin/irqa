from whoosh.qparser import QueryParser
import whoosh.index as index
from whoosh.fields import *
from whoosh import qparser

import argparse
import os
import time
import logging


class Timer(object):
    def __init__(self, name=None, logger=None):
        self.logger = logger
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        if self.logger is None:
            if self.name:
                print '[%s]' % self.name,
            print 'Elapsed: %s' % (time.time() - self.tstart)

        else:
            if self.name:
                self.logger.info("[%s] Elapsed: %s" % (self.name, (time.time() - self.tstart)))
            else:
                self.logger.info('Elapsed: %s' % (time.time() - self.tstart))


def get_section(rawtxt, tag1, tag2):
    rexp1 = "%s([\\S\\s]*?)%s" % (tag1, tag2)
    re_exp = re.compile(rexp1, re.DOTALL)
    section = []
    for m in re_exp.finditer(rawtxt):
        section.append(m.group(1))

    return section

def get_section2(rawtxt, tag1, tag2):
    rexp1 = "(%s[\\S\\s]*?%s)" % (tag1, tag2)
    re_exp = re.compile(rexp1, re.DOTALL)
    section = []
    for m in re_exp.finditer(rawtxt):
        section.append(m.group(1))

    return section


def query(indexpath):
    ix = index.open_dir(indexpath)

    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse("test")
        results = searcher.search(query)
        print results[0]


def batch_query(querypath, indexpath):
    ix = index.open_dir(indexpath)

    with open(querypath, 'r') as fh:
        with open('output.txt', 'w') as out_file:
            rawdata = fh.read()
            document = get_section2(rawdata, "<top>", "</top>")
            for d in document:
                topicnum = get_section(d, "<num> Number:", "<title>")[0].strip(" ").strip("\n")
                title = get_section(d, "<title>", "<desc>")[0].strip(" ").strip("\n")
                desc = get_section(d, "<desc>", "<narr>")[0].replace("Description:","").strip(" ")
                narr = get_section(d, "<narr>", "</top>")[0].replace("Narrative:","").strip(" ")

                print topicnum, title, desc, narr

                with ix.searcher() as searcher:
                    parser = qparser.QueryParser("content", schema=ix.schema,
                                 group=qparser.OrGroup)

                    query = parser.parse(desc+" "+title)

                    # query = QueryParser("content", ix.schema)
                    results = searcher.search(query, limit=1000)
                    print results[0]
                    print results[1]
                    # return

                    for i in range(1000):
                        out_file.write("%s\tQ0\t%s\t%s\t%s\t jack\n" % (topicnum, results[i].values()[1], results[i].rank+1, results[i].score))

                    # return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("querypath")
    parser.add_argument("indexpath")
    args = parser.parse_args()

    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)

    with Timer("indexing", logger):
        batch_query(args.querypath, args.indexpath)
    # query(args.indexpath)
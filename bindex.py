from whoosh.index import create_in
from whoosh.fields import *
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


def index_files(indexpath):
    schema = Schema(title=TEXT(stored=False), path=ID(stored=True), content=TEXT(stored=False))
    ix = create_in(indexpath, schema)
    writer = ix.writer()
    writer.add_document(title=u"First document", path=u"/a",
                        content=u"This is the first document we've added!")
    writer.add_document(title=u"Second document", path=u"/b",
                        content=u"The second one is even more interesting!")
    writer.commit()


def get_section(rawtxt, tag):
    rexp1 = "<%s>([\\S\\s]*?)</%s>" % (tag, tag)
    re_exp = re.compile(rexp1, re.DOTALL)
    section = []
    for m in re_exp.finditer(rawtxt):
        section.append(m.group(1))

    return section


def get_text(rawtext):
    text = get_section(rawtext, "TEXT")
    if len(text) == 0:
        text = get_section(rawtext, "DATELINE")
        if len(text) == 0:
            text = get_section(rawtext, "GRAPHIC")
            if len(text) == 0:
                text = get_section(rawtext, "CORRECTION")
                if len(text) == 0:
                    text = get_section(rawtext, "HEADLINE")

    return text


def batch_index(datapath, indexpath):
    schema = Schema(headline=TEXT(stored=False), path=ID(stored=True), content=TEXT(stored=False))

    ix = create_in(indexpath, schema)
    writer = ix.writer()

    num_index=0
    num_scan=0


    for root, dirs, files in os.walk(datapath):
        for f in files:
            fname = os.path.join(root, f)
            with open(fname, 'r') as fh:
                rawdata = fh.read()
                document = get_section(rawdata, "DOC")
                for d in document:
                    num_scan = num_scan+1
                    docid = get_section(d, "DOCNO")
                    if len(docid) == 0:
                        docid = get_section(d, "DOCID")

                    if len(docid) == 0:
                        continue

                    docid_add = docid[0].strip(" ")

                    text = get_text(d)
                    if len(text) == 0:
                        text_add = ""
                    else:
                        text_add = text[0]

                    headlines = get_section(d, "HEADLINE")
                    if len(headlines) == 0:
                        headlines_add = ""
                    else:
                        headlines_add = headlines[0]

                    print docid_add
                    writer.add_document(headline=unicode(headlines_add, errors='replace'),
                                        path=unicode(docid_add, errors='replace'),
                                        content=unicode(text_add, errors='replace'))
                    num_index = num_index+1

    writer.commit()
    print 'scanned=%d\nindexed=%d' % (num_scan, num_index)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("datapath")
    parser.add_argument("indexpath")
    args = parser.parse_args()
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)

    with Timer("indexing", logger):
        batch_index(args.datapath, args.indexpath)




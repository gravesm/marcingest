import pysolr
import sys
import conf
from marcingest import read, filters

def parse(record):
    doc = {}
    for field, handler in conf.FIELD_HANDLERS.items():
        if hasattr(handler, '__call__'):
            doc[field] = handler(record)
        else:
            doc[field] = handler
    return doc

def main():
    f = sys.argv[1]
    fp = open(f)
    solr = pysolr.Solr(conf.SOLR_URL)
    docs = map(parse, read(fp, filters.combined_filter))
    solr.delete(q="Institution:MIT AND DataType:('Paper Map' OR 'CD-ROM' OR 'DVD-ROM')")
    solr.add(docs)


if __name__ == '__main__':
    main()

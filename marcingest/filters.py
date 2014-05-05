from . import NSMAP

def datatype_filter(record):
    datatypes = record.xpath("marc:datafield[@tag='876']/marc:subfield[@code='k']",
                            namespaces=NSMAP)
    for datatype in datatypes:
        if datatype.text in ("MAP",):
            return True
    return False

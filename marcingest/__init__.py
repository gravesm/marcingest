from lxml import etree
from itertools import ifilter


MARC = "http://www.loc.gov/MARC21/slim"
MARCNS = "{{{0}}}".format(MARC)
NSMAP = {
    "marc": MARC,
}

_XPATHS = {
    "001": "marc:controlfield[@tag='001']",
    "008": "marc:controlfield[@tag='008']",
    "034_d": "marc:datafield[@tag='034']/marc:subfield[@code='d']/text()",
    "034_e": "marc:datafield[@tag='034']/marc:subfield[@code='e']/text()",
    "034_f": "marc:datafield[@tag='034']/marc:subfield[@code='f']/text()",
    "034_g": "marc:datafield[@tag='034']/marc:subfield[@code='g']/text()",
    "245": "marc:datafield[@tag=245]/marc:subfield/text()",
    "260_b": "marc:datafield[@tag='260']/marc:subfield[@code='b']",
    "500_a": "marc:datafield[@tag='500']/marc:subfield[@code='a']/text()",
    "650_a": "marc:datafield[@tag='650']/marc:subfield[@code='a']",
    "650_z": "marc:datafield[@tag='650']/marc:subfield[@code='z']",
    "876_k": "marc:datafield[@tag='876']/marc:subfield[@code='k']",
}

XPATHS = dict((k, etree.XPath(v, namespaces=NSMAP)) for k,v in _XPATHS.items())

def read(marcxml, record_filter=len):
    marc = etree.parse(marcxml)
    return ifilter(record_filter, marc.xpath("//marc:record", namespaces=NSMAP))

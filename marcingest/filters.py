from . import NSMAP

def datatype_filter(record):
    datatypes = record.xpath("marc:datafield[@tag='876']/marc:subfield[@code='k']",
                            namespaces=NSMAP)
    for datatype in datatypes:
        if datatype.text in ("MAP", "CDROM", "DVDROM",):
            return True
    return False

def location_filter(record):
    location = record.xpath("marc:datafield[@tag='876']/marc:subfield[@code='B']",
                            namespaces=NSMAP)
    return location[0].text in ("Map Room", "GIS Collection",)

def combined_filter(record):
    return datatype_filter(record) and location_filter(record)

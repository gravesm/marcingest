from . import XPATHS
import datetime
import re


########################
# Regular expression to extract parts of coordinate string from 034 field
#
# $1 = Hemisphere: Could be any of: +,-,N,S,E,W, or None
# $2 = Degrees
# $4 = Minutes
# $6 = Seconds
########################
_COORD_REGEX = re.compile("^([NSEW+-])?(\d{3}(\.\d*)?)(\d{2}(\.\d*)?)?(\d{2}(\.\d*)?)?",
                          re.IGNORECASE)

def datatype(record):
    xpath = XPATHS['876_k']
    mapping = {
        "MAP": "Paper Map",
        "CDROM": "CD-ROM",
        "DVDROM": "DVD-ROM",
    }
    for datatype in xpath(record):
        if datatype.text in ("MAP", "CDROM", "DVDROM"):
            return mapping[datatype.text]
    return "Unknown"

def theme_keywords(record):
    return _keywords(record, XPATHS['650_a'])

def theme_keywords_concat(record):
    return " ".join(theme_keywords(record))

def place_keywords(record):
    return _keywords(record, XPATHS['650_z'])

def place_keywords_concat(record):
    return " ".join(place_keywords(record))

def publisher(record):
    xpath = XPATHS['260_b']
    publisher = xpath(record)
    if publisher:
        return publisher[0].text.rstrip(",")

def layer_id(record):
    xpath = XPATHS['001']
    return "MIT.{0}".format(xpath(record)[0].text)

def location(record):
    xpath = XPATHS['001']
    return '{{"libRecord": "http://library.mit.edu/item/{0}"}}'.format(xpath(record)[0].text)

def name(record):
    xpath = XPATHS['001']
    return xpath(record)[0].text

def layer_display_name(record):
    xpath = XPATHS['245']
    return " ".join(xpath(record))

def content_date(record):
    xpath = XPATHS['008']
    date = xpath(record)[0].text[7:11]
    try:
        date = int(date)
        return datetime.date(date, 1, 1)
    except ValueError:
        pass

def abstract(record):
    xpath = XPATHS['500_a']
    return " ".join(xpath(record))

def min_x(record):
    xpath = XPATHS['034_d']
    coord = xpath(record)
    if coord:
        return _convert_coord(coord[0])

def min_y(record):
    xpath = XPATHS['034_g']
    coord = xpath(record)
    if coord:
        return _convert_coord(coord[0])

def max_x(record):
    xpath = XPATHS['034_e']
    coord = xpath(record)
    if coord:
        return _convert_coord(coord[0])

def max_y(record):
    xpath = XPATHS['034_f']
    coord = xpath(record)
    if coord:
        return _convert_coord(coord[0])

def center_x(record):
    west = min_x(record)
    east = max_x(record)
    if west is not None and east is not None:
        return west + abs(east - west) / 2

def center_y(record):
    south = min_y(record)
    north = max_y(record)
    if south is not None and north is not None:
        return south + abs(north - south) / 2

def area(record):
    west = min_x(record)
    east = max_x(record)
    south = min_y(record)
    north = max_y(record)
    if all(v is not None for v in (west, east, south, north)):
        return abs(east - west) * abs(north - south)

def half_height(record):
    north = max_y(record)
    south = min_y(record)
    if north is not None and south is not None:
        return abs(north - south) / 2

def half_width(record):
    east = max_x(record)
    west = min_x(record)
    if east is not None and west is not None:
        return abs(east - west) / 2

def _convert_coord(coordinate):
    parts = _COORD_REGEX.search(coordinate)
    if parts is None:
        return
    decimal = float(parts.group(2)) + float(parts.group(4) or 0) / 60 + float(parts.group(6) or 0) / 3600
    if parts.group(1) and parts.group(1) in "WSws-":
        decimal = -decimal
    return decimal

def _keywords(record, xpath):
    keywords = set()
    for keyword in xpath(record):
        keywords.add(keyword.text.rstrip(":;,. "))
    return list(keywords)

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from lxml.builder import ElementMaker
from marcingest import MARC


class M:
    E = ElementMaker(namespace=MARC)
    COLLECTION = E.collection
    RECORD = E.record
    DATAFIELD = E.datafield
    SUBFIELD = E.subfield
    CONTROLFIELD = E.controlfield

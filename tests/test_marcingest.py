from testing_utils import unittest, M
from cStringIO import StringIO
from lxml import etree
from marcingest import read, MARCNS

class TestMarcingest(unittest.TestCase):

    def test_read_returns_an_iterator_of_records(self):
        collection = M.COLLECTION(
            M.RECORD(
                M.DATAFIELD("Foo")
            ),
            M.RECORD(
                M.DATAFIELD("Bar")
            )
        )
        records = [r for r in read(StringIO(etree.tostring(collection)))]
        self.assertEqual(records[0].tag, "{0}record".format(MARCNS))
        self.assertEqual(len(records), 2)

    def test_read_filters_records(self):
        def filt(record):
            if record.get("type") == "dog":
                return False
            else:
                return True
        coll = M.COLLECTION(
            M.RECORD({"type": "dog"},
                M.DATAFIELD("Rover")
            ),
            M.RECORD({"type": "cat"},
                M.DATAFIELD("Lucy")
            )
        )
        records = [r for r in read(StringIO(etree.tostring(coll)), filt)]
        self.assertEqual(records[0].get("type"), "cat")
        self.assertEqual(len(records), 1)

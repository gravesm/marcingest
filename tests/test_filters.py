from testing_utils import unittest, M
from marcingest import filters as f

class TestFilters(unittest.TestCase):

    def test_datatype_filter_returns_false_for_unsupported_datatypes(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "876"},
                M.SUBFIELD("ATLAS", code="k")
            )
        )
        self.assertFalse(f.datatype_filter(record))

    def test_datatype_filter_returns_true_for_supported_datatypes(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "876"},
                M.SUBFIELD("MAP", code="k")
            )
        )
        self.assertTrue(f.datatype_filter(record))

    def test_location_filter_returns_false_for_unsupported_locations(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "876"}, M.SUBFIELD("Neverland", code="B"))
        )
        self.assertFalse(f.location_filter(record))

    def test_location_filter_returns_true_for_supported_locations(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "876"}, M.SUBFIELD("Map Room", code="B"))
        )
        self.assertTrue(f.location_filter(record))

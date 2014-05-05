from testing_utils import unittest, M
from marcingest import field_handlers as fh
import datetime

class TestFieldHandlers(unittest.TestCase):

    def test_datatype_maps_datatype(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "876"},
                M.SUBFIELD("MAP", code="k")
            )
        )
        self.assertEqual(fh.datatype(record), "Paper Map")

    def test__keywords_removes_duplicates(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "650"},
                M.SUBFIELD("FOO", code="a"),
                M.SUBFIELD("BAR", code="a")
            ),
            M.DATAFIELD({"tag": "650"},
                M.SUBFIELD("BAR", code="a")
            ),
            M.DATAFIELD({"tag": "650"},
                M.SUBFIELD("FOO", code="a")
            )
        )
        self.assertEqual(len(fh.theme_keywords(record)), 2)
        self.assertIn("FOO", fh.theme_keywords(record))
        self.assertIn("BAR", fh.theme_keywords(record))

    def test__keywords_strips_punctuation(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "650"},
                M.SUBFIELD("Foo;", code="a"),
                M.SUBFIELD("Bar,. ", code="a"),
                M.SUBFIELD("Baz. (Gaz):", code="a"),
            )
        )
        self.assertIn("Foo", fh.theme_keywords(record))
        self.assertIn("Bar", fh.theme_keywords(record))
        self.assertIn("Baz. (Gaz)", fh.theme_keywords(record))

    def test_publisher_removes_trailing_comma(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "260"},
                M.SUBFIELD("Pubiddypub,", code="b")
            )
        )
        self.assertEqual(fh.publisher(record), "Pubiddypub")

    def test_layer_id_returns_mit_id(self):
        record = M.RECORD(M.CONTROLFIELD({"tag": "001"}, "Catsenfield"))
        self.assertEqual(fh.layer_id(record), "MIT.Catsenfield")

    def test_location_returns_formatted_location(self):
        record = M.RECORD(M.CONTROLFIELD({"tag": "001"}, "Kittenshelf"))
        self.assertEqual(fh.location(record),
                         '{"libRecord": "http://library.mit.edu/item/Kittenshelf"}')

    def test_name_returns_name(self):
        record = M.RECORD(M.CONTROLFIELD({"tag": "001"}, "Fluffypants"))
        self.assertEqual(fh.name(record), "Fluffypants")

    def test_layer_display_name_concatenates_title_subfields(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "245"},
                M.SUBFIELD("This", code="a"),
                M.SUBFIELD("Is", code="b"),
                M.SUBFIELD("KITTENTOWN!")
            )
        )
        self.assertEqual(fh.layer_display_name(record), "This Is KITTENTOWN!")

    def test_content_date_returns_date(self):
        record = M.RECORD(M.CONTROLFIELD({"tag": "008"}, "0439028195532901"))
        self.assertIsInstance(fh.content_date(record), datetime.date)
        self.assertEqual(fh.content_date(record).year, 1955)

    def test_abstract_concatenates_note_fields(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "500"},
                M.SUBFIELD("Today I watched the birds outside.", code="a")
            ),
            M.DATAFIELD({"tag": "500"},
                M.SUBFIELD("I also vommed on the carpet.", code="a")
            )
        )
        self.assertEqual(fh.abstract(record),
                         "Today I watched the birds outside. I also vommed on the carpet.")

    def test__coord_regex_extracts_parts_of_single_coordinate(self):
        parts = fh._COORD_REGEX.search("N0451289")
        self.assertEqual(parts.group(1), "N")
        self.assertEqual(parts.group(2), "045")
        self.assertEqual(parts.group(4), "12")
        self.assertEqual(parts.group(6), "89")

    def test_min_x_returns_left_bounds_as_float(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "034"},
                M.SUBFIELD("W0733110", code="d")
            )
        )
        degrees = 73 + 31./60 + 10./3600
        self.assertAlmostEqual(fh.min_x(record), -degrees)

    def test_min_y_returns_bottom_bounds_as_float(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "034"},
                M.SUBFIELD("-023.234567", code="g")
            )
        )
        self.assertAlmostEqual(fh.min_y(record), -23.234567)

    def test_max_x_returns_right_bounds_as_float(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "034"},
                M.SUBFIELD("E17934.5678", code="e")
            )
        )
        degrees = 179 + 34.5678/60
        self.assertAlmostEqual(fh.max_x(record), degrees)

    def test_max_y_returns_top_bounds_as_float(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "034"},
                M.SUBFIELD("+0123456.789", code="f")
            )
        )
        degrees = 12 + 34./60 + 56.789/3600
        self.assertAlmostEqual(fh.max_y(record), degrees)

    def test_center_x_computes_center_of_x_axis(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "034"},
                M.SUBFIELD("W1000000", code="d"),
                M.SUBFIELD("W0500000", code="e")
            )
        )
        self.assertAlmostEqual(fh.center_x(record), -75.)

    def test_center_y_computes_center_of_y_axis(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "034"},
                M.SUBFIELD("0200000", code="f"),
                M.SUBFIELD("S0400000", code="g")
            )
        )
        self.assertAlmostEqual(fh.center_y(record), -10.)

    def test_area_computes_area_of_bounds(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "034"},
                M.SUBFIELD("W0200000", code="d"),
                M.SUBFIELD("E0200000", code="e"),
                M.SUBFIELD("S0200000", code="g"),
                M.SUBFIELD("N0200000", code="f")
            )
        )
        self.assertAlmostEqual(fh.area(record), 1600.)

    def test_half_height_computes_half_height_of_bounds(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "034"},
                M.SUBFIELD("S0123456", code="f"),
                M.SUBFIELD("S0223456", code="g")
            )
        )
        self.assertAlmostEqual(fh.half_height(record), 5.)

    def test_half_width_computes_half_width_of_bounds(self):
        record = M.RECORD(
            M.DATAFIELD({"tag": "034"},
                M.SUBFIELD("E0350000", code="e"),
                M.SUBFIELD("E0150000", code="d")
            )
        )
        self.assertAlmostEqual(fh.half_width(record), 10.)

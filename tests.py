import unittest
from geo import FileDistanceRunner

class GeoUnitTests(unittest.TestCase):

    df = None

    def setUp(self):
        self.df = FileDistanceRunner(src="res/cities.json")

    def test_p_to_p(self):
        """ Test that the distance between two known cities is still calculated correctly.
        """
        res = self.df.point_to_point('geneva', 'shanghai')
        self.assertAlmostEqual(9238.52173022, res)

    def test_dublin_five_hundred(self):
        """Which Cities are within 500Km of Dublin? - If this fails, then something has gone seriously wrong...
        """
        golden_value = [u'aberdeen', u'belfast', u'birmingham', u'cardiff', u'cork',\
                        u'douglas', u'dublin', u'edinburgh', u'glasgow', u'greenwich',\
                        u'leeds', u'liverpool', u'london', u'manchester']
        res = self.df.ranged_poi(500)
        self.assertEqual(res, golden_value)

    def test_set_home(self):
        """ Can the home location be updated from the default as expected?
        """
        target = "london"

        self.df.set_home(target)
        self.assertEqual(self.df.home, target)

    def test_london_500_miles(self):
        """What cities are within 500 miles of London? - Tests that using miles as a unit works as expected.
        """
        golden_value =  [u'aberdeen', u'amsterdam', u'antwerp', u'belfast', u'bern', \
                         u'birmingham', u'brussels', u'cardiff', u'cologne', u'cork', \
                         u'd%c3%bcsseldorf', u'douglas', u'dublin', u'edinburgh', u'frankfurt',\
                         u'geneva', u'glasgow', u'greenwich', u'hamburg', u'hanover', u'leeds',\
                         u'liverpool', u'london', u'luxembourg', u'lyon', u'manchester', \
                         u'nantes', u'paris', u'rotterdam', u'strasbourg', u'stuttgart',\
                         u'thehague', u'z%c3%bcrich']

        self.df.set_home("london")
        res =  self.df.ranged_poi(500, kilometer=False)
        self.assertEqual(golden_value, res)

    def test_range_fail(self):
        """Test that setting strings for distances raises a ValueError as intended.
        """
        with self.assertRaises(ValueError):
            self.df.ranged_poi("Hello")


if __name__ == "__main__":
    unittest.main()

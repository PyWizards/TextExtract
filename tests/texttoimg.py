import unittest
from TextExtractApi.TextExtract import TextExtractFunctions


class TestTextExtract(unittest.TestCase):

    def test_image_to_string(self):
        result, scale = TextExtractFunctions.image_to_string_only("MenuIcon.png", lang='eng')
        self.assertEqual(result,'Menu')

    def test_image_to_string_matched(self):
        result, match = TextExtractFunctions.image_to_string_matched("MenuIcon.png", expected_text='Menu', lang='eng')
        self.assertEqual(result,'Menu')

    def test_image_to_string_matched2(self):
        finalresult, scaled_results = TextExtractFunctions.image_to_string_matched("MenuIcon.png", expected_text='Menu',
                                                                               all_results=True)
        self.assertEqual(finalresult,['Menu', 100.0])
        self.assertEqual(len(scaled_results),6)
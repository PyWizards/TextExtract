import unittest
from TextExtractApi.TextExtract import TextExtractFunctions
from os import path

DATA_DIR = path.dirname(path.abspath(__file__))
TEST_JPEG = path.join(DATA_DIR, 'MenuIcon.png')

class TestAutomate(unittest.TestCase):

    def test_image_to_string(self):
        result, scale = TextExtractFunctions.image_to_string_only(TEST_JPEG, lang='eng')
        # assert result=='Menu',"Test Failed : Image to string not matched"
        self.assertEqual(result,'Menu',"Test Failed : Image to string not matched")

    def test_image_to_string_matched(self):
        result, match = TextExtractFunctions.image_to_string_matched(TEST_JPEG, expected_text='Menu', lang='eng')
        # assert result=='Menu',"Test Failed : Image to string matched with expected"
        self.assertEqual(result,'Menu',"Test Failed : Image to string matched with expected")

    def test_image_to_string_matched2(self):
        finalresult, scaled_results = TextExtractFunctions.image_to_string_matched(TEST_JPEG, expected_text='Menu',
                                                                               all_results=True)
        # assert finalresult==['Menu', 100.0],"Test Failed : Image to string matched withcd expected"
        # assert len(scaled_results)==6,"Test Failed : Image to String with all scalings"
        self.assertEqual(finalresult,['Menu', 100.0], "Test Failed : Image to string matched withcd expected")
        self.assertEqual(len(scaled_results),6, "Test Failed : Image to String with all scalings")
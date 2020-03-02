import pytest
from TextExtractApi.TextExtract import TextExtractFunctions
from os import path

DATA_DIR = path.join(path.dirname(path.abspath(__file__)), 'data')
TEST_JPEG = path.join(DATA_DIR, 'MenuIcon.png')

def test_image_to_string():
    result, scale = TextExtractFunctions.image_to_string_only(TEST_JPEG, lang='eng')
    assert result=='Menu',"Test Failed : Image to string not matched"

def test_image_to_string_matched():
    result, match = TextExtractFunctions.image_to_string_matched(TEST_JPEG, expected_text='Menu', lang='eng')
    assert result=='Menu',"Test Failed : Image to string matched with expected"

def test_image_to_string_matched2():
    finalresult, scaled_results = TextExtractFunctions.image_to_string_matched(TEST_JPEG, expected_text='Menu',
                                                                           all_results=True)
    assert finalresult==['Menu', 100.0],"Test Failed : Image to string matched withcd expected"
    assert len(scaled_results)==6,"Test Failed : Image to String with all scalings"

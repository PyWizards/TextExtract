import pytest
from TextExtractApi.TextExtract import TextExtractFunctions
import os

def test_image_to_string():
    result, scale = TextExtractFunctions.image_to_string_only("./test/MenuIcon.png", lang='eng')
    assert result=='Menu',"Test Failed : Image to string not matched"

def test_image_to_string_matched():
    result, match = TextExtractFunctions.image_to_string_matched("./test/MenuIcon.png", expected_text='Menu', lang='eng')
    assert result=='Menu',"Test Failed : Image to string matched with expected"

def test_image_to_string_matched2():
    finalresult, scaled_results = TextExtractFunctions.image_to_string_matched(".tests/MenuIcon.png", expected_text='Menu',
                                                                           all_results=True)
    assert finalresult==['Menu', 100.0],"Test Failed : Image to string matched with expected"
    assert len(scaled_results)==6,"Test Failed : Image to String with all scalings"

# from TextExtract.TextExtractApi.TextExtract import TextExtractFunctions
from TextExtractApi.TextExtract import TextExtractFunctions


result,scale=TextExtractFunctions.image_to_string_only("MenuIcon.png",lang='eng')
result,match=TextExtractFunctions.image_to_string_matched("MenuIcon.png",expected_text='Menu',lang='eng')
finalresult,scaled_results=TextExtractFunctions.image_to_string_matched("MenuIcon.png",expected_text='Menu',all_results=True)

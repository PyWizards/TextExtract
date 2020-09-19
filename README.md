[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

TextExtract :  
=======================
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/textextract)](https://pepy.tech/project/textextract)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![PyPI version](https://badge.fury.io/py/TextExtract.svg)](https://badge.fury.io/py/TextExtract)
![Python package](https://github.com/sam4u3/TextExtract/workflows/Python%20package/badge.svg?branch=master)
[![PyWizards](https://circleci.com/gh/PyWizards/TextExtract.svg?style=svg)](https://circleci.com/gh/Pywizards/TextExtract)

Overview :  
=======================  
  
TextExtract is a optimize version of Tesseract to provide better text recognition.
  
  
Features :  
==============================  
  
1) Extract text from any image  
2) Extract text which match expected text   
  
Installation :
==============================  
  
**Prerequisite :**  
  
- Python 3.6+ (https://www.python.org/downloads/)  
- Tesseract.exe file and DLLs('liblept177.dll','libtesseract400.dll','vcomp140.dll')  
- Tesseract version used is : tesseract 4.0.0-beta.3  
  
**Using pip :**  
  
`pip install TextExtract`  
  
Usage :  
==============================  
  
```python  
from TextExtractApi.TextExtract import TextExtractFunctions  
  
#Get single text without comparing text with expected  
result,scale=TextExtractFunctions.image_to_string_only("MenuIcon.png",lang='eng')
  
#Get texts from list of scaled images text with highest matching with expected text
result,match=TextExtractFunctions.image_to_string_matched("MenuIcon.png",expected_text='Menu',lang='eng')
  
#Get list of result with matches results  
finalresult,scaled_results=TextExtractFunctions.image_to_string_matched("MenuIcon.png",expected_text='Menu',all_results=True)

```  
  
**Contact Information :**  
  
[Email: sayarmendis26@gmail.com](mailto::sayarmendis26@gmail.com)

**Donation :**

If you have found my softwares to be of any use to you, do consider helping me pay my internet bills. This would encourage me to create many such softwares :)

<a href="https://www.instamojo.com/@sayarmendis26/" target="_blank"><img src="https://www.soldermall.com/images/pic-online-payment.jpg" alt="Donate via Instamojo" title="Donate via instamojo" /></a>

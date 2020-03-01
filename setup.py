# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    readme = f.read()

# with open(os.path.join(HERE, "LICENSE")) as f:
#     license = f.read()

setup(
    name='TextExtract',
    version='1.2.0',
    description='Tesseract Optimize is a optimize version of Tesseract to provide better text recognition.',
    long_description_content_type="text/markdown",
    long_description=readme,
    url="https://github.com/sam4u3/TextExtract",
    author='Sayar Mendis',
    author_email='sayarmendis26@gmail.com',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6'
    ],
    packages=find_packages(exclude=('tests', 'docs'))

)



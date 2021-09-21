from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='pylib',
    version='0.1',
#     packages=find_packages(),
    packages=['pylib'],                      # root folder of your package
    package_dir={'pylib': 'pylib'},      # directory which contains the python code
    long_description='Package to analyze cmd data',
    package_data={'pylib': ['data/*.csv']},  # directory which contains your csvs
)
import versioneer
#from setuptools import setup, find_packages
from distutils.core import setup

setup(
        name='qrl-chain-scrape',
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        description='QRL Chain Scrape utility',
        author='James Gordon',
        author_email='fr1t2@protonmail.com',
        #packages=['distutils', 'distutils.command'],
     )




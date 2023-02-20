import versioneer
#from setuptools import setup, find_packages
from setuptools import setup

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setup(
        name='qrl_chain_scrape',
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        description='QRL Chain Scrape utility',
        author='James Gordon',
        install_requires=requirements,
        author_email='fr1t2@protonmail.com',
        license='MIT'
        #packages=['distutils', 'distutils.command'],
     )

import configparser
import os

# Load the configuration file
config_file = os.path.join(os.path.dirname(__file__), 'config.ini.example')
config = configparser.ConfigParser()
config.read(config_file)

# Import the chainfunctions sub-module
from src.chainfunctions import *

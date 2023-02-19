""" grab block data from a local node for a given block and return it's data in an array """
import mysql.connector
import requests
import configparser
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler()) 



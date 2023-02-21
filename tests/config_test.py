"""unit tests for the config file"""
import pytest
import configparser
import os
import logging
import shutil

def test_config_file_opens():
    """see if the file opens"""
    try:
        config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
        config = configparser.ConfigParser() 
        config.read(config_file)  
    except:
        pytest.fail("Failed to open config file")

def test_example_config_file_opens():
    """ test that the example config file opens for comparison"""
    try:
        example_config_file = os.path.join(os.path.dirname(__file__), 'config.ini.example')
        ex_conf = configparser.ConfigParser()
        ex_conf.read(example_config_file)
    except:
        pytest.fail("Failed to open example config file")

def test_config_file_is_ini():
    """Check that ist is a vaild .ini file"""
    config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'qrl_chain_state', 'src', 'config.ini'))
    assert os.path.splitext(config_file)[1] == '.ini', "Config file is not named as a valid .ini file"


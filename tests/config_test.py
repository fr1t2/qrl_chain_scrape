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

def test_config_file_not_empty():
    """Ensure the file is not empty"""
    config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'qrl_chain_state', 'src', 'config.ini'))
    assert os.stat(config_file).st_size > 0, "Config file is empty"

def test_config_file_is_ini():
    """Check that ist is a vaild .ini file"""
    config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'qrl_chain_state', 'src', 'config.ini'))
    assert os.path.splitext(config_file)[1] == '.ini', "Config file is not named as a valid .ini file"

def test_all_sections_and_keys_are_present():
    """compares the example config with the user provided one"""

    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    example_config_file = os.path.join(os.path.dirname(__file__), 'config.ini.example')

    # copy config.ini.example to config.ini if it doesn't exist
    if not os.path.exists(config_file):
        shutil.copyfile(example_config_file, config_file)

    config = configparser.ConfigParser()
    config.read(config_file)
    ex_conf = configparser.ConfigParser()
    ex_conf.read(example_config_file)

    for section in ex_conf.sections():
        if section not in config:
            pytest.fail(f"Section [{section}] is missing from {config_file}")
        else:
            for key in ex_conf[section]:
                if key not in config[section]:
                    pytest.fail(f"Key {key} is missing from section [{section}] in {config_file}")
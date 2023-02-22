"""Test the src/price/coingecko.py file.

This file contains tests for the src/price/coingecko.py file.

Attributes:
    LAST_UPDATE (float): The last time the rate limit was checked.

TODO:
    * Add tests for the get_price() function.
    * Add tests for the compile_api_url function.
    * Add tests for the ping_api() function.
    * Add tests for the get_all_coins() function.
    * Add tests for the get_coin_data() function.
    * Add tests for the supported_denom() function.
    * Add tests for the price_history() function.
    * Add tests for the price_lookup() function.

"""

import logging
from unittest.mock import patch, MagicMock, mock_open

from requests.exceptions import RequestException
import pytest
import datetime

from src import config

from src.price import rate_limit
from src.price import compile_api_url
from src.price import ping_api
from src.price import get_all_coins
from src.price import supported_denom
from src.price import get_coin_data

LAST_UPDATE = datetime.datetime.now().timestamp()


import os
import shutil
from unittest.mock import patch, mock_open

def test_rate_limit():
    global LAST_UPDATE #pylint: disable="w0603"
    LAST_UPDATE = 0
    # get the rate limit time and calls from the config file
    rate_limit_time = config.getfloat("coingecko", "rate_limit_time")
    rate_limit_calls = config.getint("coingecko", "rate_limit_calls")


    # Check if function returns True when rate limit has not been reached
    # rate limit takes time of LAST_UPDATE and subtracts it from the current time to compare to the rate_limit_time / rate_limit_calls in config.ini
    # assert that given the correct time (now - last_update > rate_limit_time / rate_limit_calls) the function returns True
    # give the conditional paramater in seconds like datetime.datetime.now().timestamp() - 5.0
    assert rate_limit(0.0) is True # time is set to epoch of time, has been long enough for any rate limit to be reached
    assert rate_limit(datetime.datetime.now().timestamp - (rate_limit_time / rate_limit_calls)) is True # time is set to now - the time allowed between calls (rate_limit_time / rate_limit_calls), should return True


    # assert that given the incorrect time (now - last_update < rate_limit_time / rate_limit_calls) the function returns False
    assert rate_limit(datetime.datetime.now().timestamp - (rate_limit_time / rate_limit_calls) + 1) is False # time is set to now - the time allowed between calls (rate_limit_time / rate_limit_calls) + 1 second, should return False

    # Check if function raises a TypeError when input is invalid
    try:
        rate_limit("invalid")
    except TypeError:
        pass
    else:
        raise AssertionError("Error: function did not raise a TypeError")

    # Check if function raises a TypeError when RATE_LIMIT is invalid
    try:
        config.set("coingecko", "rate_limit_calls", "invalid")
        rate_limit(20.0)
    except TypeError:
        pass
    else:
        raise AssertionError("Error: function did not raise a TypeError")

    # Check if function returns False and prints an error message when an exception occurs
    assert not rate_limit(None)

def test_compile_api_url():
    # Test for free API usage
    config.set("coingecko", "api_key", "YOUR_API_KEY")
    assert compile_api_url("ping") == "https://api.coingecko.com/api/v3/ping"

    # Test for pro API usage with api key set in config.ini
    config.set("coingecko", "api_key", "1234567890")
    assert compile_api_url("ping") == "https://pro-coingecko.com/api/v3/ping?x_cg_pro_api_key=1234567890"

    # Test if function raises a TypeError when endpoint input is invalid
    try:
        compile_api_url(123)
    except TypeError:
        pass
    else:
        raise AssertionError("Error: function did not raise a TypeError")

    # Test if function returns None and prints an error message when api_url is None
    config.set("coingecko", "api_url", None)
    assert compile_api_url("ping") is None
    captured = pytest.capsys.readouterr()
    assert "Error: No 'api_url' value found in config.ini file." in captured.out

    # Test if function returns None and prints an error message when pro_api_url is None
    config.set("coingecko", "pro_api_url", None)
    assert compile_api_url("ping") is None
    captured = pytest.capsys.readouterr()
    assert "Error: No 'pro_api_url' value found in config.ini file." in captured.out

    # Test if function returns None and prints an error message when api_key is None
    config.set("coingecko", "api_key", None)
    assert compile_api_url("ping") is None
    captured = pytest.capsys.readouterr()
    assert "Error: No 'api_key' value found in config.ini file." in captured.out


@patch('src.price.requests')
def test_ping_api(mock_requests):
    # Create a mock response object
    mock_response = MagicMock()
    mock_response.status_code = 200

    # Configure the mock requests.get() method to return the mock response object
    mock_requests.get.return_value = mock_response

    # Test if function returns True when API is online
    assert ping_api() is True

    # Configure the mock requests.get() method to raise an exception
    mock_requests.get.side_effect = Exception("Error")

    # Test if function returns False when API is offline
    config.set("coingecko", "api_url", "https://httpstat.us/404")
    assert ping_api() is False

    # Test if function returns False when API is offline
    config.set("coingecko", "pro_api_url", "https://httpstat.us/404")
    assert ping_api() is False

def test_get_all_coins():
    # Test that the function returns a list of dictionaries
    coins_data = get_all_coins()
    assert isinstance(coins_data, list)
    assert all(isinstance(item, dict) for item in coins_data)

    # Test that the returned dictionaries have the expected keys
    expected_keys = {"id", "symbol", "name"}
    assert all(expected_keys.issubset(set(coin.keys())) for coin in coins_data)

    # Test that the returned list is not empty
    assert len(coins_data) > 0

def test_get_coin_data():
    # Mock response from the Coingecko API
    mock_response = {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"}

    # Patch requests.get to return a MagicMock object with a json() method
    with patch("requests.get") as mock_get:
        mock_get.return_value = MagicMock()
        mock_get.return_value.json.return_value = mock_response

        # Call the function with a mock coin ID
        coin_data = get_coin_data("bitcoin")

        # Assert that the function returns a non-empty dictionary
        assert isinstance(coin_data, dict)
        assert bool(coin_data)


@patch("price.get_coin_data")
def test_supported_denom(mock_get_coin_data):
    # Set up mock response data
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "tickers": ["aed", "ars", "aud", "bch", "btc", "cad", "chf", "clp", "cny", "czk", "dkk", "dot", "eos", "eth", "eur", "gbp", "hkd", "huf", "idr", "ils", "inr", "jpy", "krw", "kwd", "lkr", "ltc", "mmk", "mxn", "myr", "ngn", "nok", "nzd", "php", "pkr", "pln", "rub", "sar", "sek", "sgd", "thb", "try", "twd", "uah", "usd", "vef", "vnd", "xag", "xau", "xdr", "xlm", "xrp", "zar"],
    }

    # Assign mock response to get_coin_data function
    mock_get_coin_data.return_value = mock_response

    # Call the function with a valid coin_id
    result = supported_denom("bitcoin")

    # Assert that the response is a list and not empty
    assert isinstance(result, list)
    assert len(result) > 0

    # Call the function with an invalid coin_id
    with pytest.raises(Exception):
        supported_denom("invalid_coin_id")

    # Call the function with an error in get_coin_data
    mock_get_coin_data.side_effect = Exception("Error getting coin data")
    with pytest.raises(Exception):
        supported_denom("bitcoin")

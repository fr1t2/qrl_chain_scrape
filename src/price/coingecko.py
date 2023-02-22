""" collection of API functions for the coingecko API 

functions:
    ping_api()
    get_all_coins()
    get_coin_data()

    supported_denom()
    price_history()
    price_lookup()
    rate_limit()
    get_coingecko_price(coin)

"""

# pull from the coingecko_api.py file

import datetime
import logging

import requests

from src import config


# full pro api link https://pro-coingecko.com/api/v3/ping?x_cg_pro_api_key=api_key

# get the config values from the config.ini file
api_url = config.get('coingecko', 'api_url')
pro_api_url = config.get('coingecko', 'pro_api_url')
api_key = config.get('coingecko', 'api_key')

# set the last update time to now
LAST_UPDATE = datetime.datetime.now().timestamp()


# check it api_key is not 'YOUR_API_KEY' or blank in the config.ini file (config) 
#
# if it is not set then use the free API URL
# if it is set then use the pro API URL

if api_key != "YOUR_API_KEY" and api_key is not None:
    API_URL = pro_api_url
    PRO_API = True
    print("Using pro API URL")
else:
    API_URL = api_url
    PRO_API = False
    print("Using free API URL")


def compile_api_url(endpoint):
    """ Function to compile the correct API url depending if we need to add an API key or not

    Args:
        endpoint (str): The API endpoint to use.

    Returns:
        str: The full API URL to use.

    Example:
        # free api usage
        >>> compile_api_url("ping")
        "https://api.coingecko.com/api/v3/ping"

        # pro api usage with api key set in config.ini
        >>> compile_api_url("ping")
        "https://pro-api.coingecko.com/api/v3/ping?x_cg_pro_api_key=api_key"

    """
    if PRO_API:
        logging.info('Using pro API URL: %s%s?x_cg_pro_api_key=%s' % (API_URL, endpoint, api_key))
        response = API_URL + endpoint + "?x_cg_pro_api_key=" + api_key
    else:
        logging.info('Using free API URL: %s%s' % (API_URL, endpoint))
        response = api_url + endpoint # using the free api, only need the endpoint
    return response



def ping_api():
    """Ping the Coingecko API to check if it is up and running.

    Returns:
        bool: True if the API is up and running, False if not.

    Example:
        >>> ping_api()
        {
          "gecko_says": "(V3) To the Moon!"
        }
    """
    # handle any errors that the api may give us
    try:
        response = requests.get(compile_api_url("ping"))
    except requests.exceptions.RequestException as request_error:
        logging.error(request_error)
        raise Exception("Error pinging API") from request_error

    return not response.status_code != 200


def get_all_coins():
    """Get a list of all coins from the Coingecko API.

    Returns:
        list of dict: A list of dictionaries containing information about each coin.

    Example:
        >>> get_all_coins()
        [
            {
                "id": "bitcoin",
                "symbol": "btc",
                "name": "Bitcoin"
            },
            {
                "id": "ethereum",
                "symbol": "eth",
                "name": "Ethereum"
            },
            ...
        ]
    """
    # handle any errors that the api may give us
    try:
        response = requests.get(compile_api_url("coins/list"))
    except requests.exceptions.RequestException as request_error:
        logging.error(request_error)
        raise Exception("Error getting all coins from API") from request_error # raise the error from the requests library
    # return the json response
    return response.json()


def get_coin_data(coin_id):
    """Get data from a given coin from the Coingecko API.

    Makes an API call to the coingecko API to get data about a coin using this API endpoint:
    https://www.coingecko.com/api/documentations/v3/coins/get_coins__id_
    
    Args:
        coin_id (str): The ID of the coin to get information about.

    Returns:
        dict: A dictionary containing data about the coin.

    Example:
        >>> get_coin_info("bitcoin")
        {
          "id": "bitcoin",
          "symbol": "btc",
          "name": "Bitcoin",
          "asset_platform_id": null,
          "platforms": {
            "": ""
          },
          "detail_platforms": {
          [...]
    """
    try:
        response = requests.get(compile_api_url("coins/%s" % coin_id))
        response.raise_for_status()
    except requests.exceptions.RequestException as request_error:
        logging.error(request_error)
        raise Exception("Error getting coin info from API") from request_error # raise the error from the requests library
    except Exception as request_error:
        logging.error(request_error)
        raise

    # return the json response
    return response.json()

def supported_denom(coin_id):
    """Get a list of supported denominations for a coin from the Coingecko API.

    using the response data from the get_coin_data() function we can get the supported denominations for a coin.

    Args:
        coin_id (str): The ID of the coin to get information about.

    Returns:
        list of str: A list of supported denominations for a coin.

    Example:
        >>> supported_denom("bitcoin")
        ["aed", "ars", "aud", "bch", ...]

    raises:
        Exception: If an error occurs while getting the supported denominations.

    """
    try:
        # get the coin data from the API
        coin_data = get_coin_data(coin_id)
        # get the supported denominations from the API response
        supported_denomination = coin_data["tickers"]
        # if the coin is not found in the API response
        if supported_denom is None:
            raise Exception("Coin not found in API response")
        # return the list of supported denominations
        return supported_denomination
    except (KeyError, AttributeError, TypeError) as coin_data_error:
        logging.error(coin_data_error)
        raise Exception("Error getting supported denominations") from coin_data_error

def price_history(coin_id, date=None, localization=False):
    """ Get the price history of a coin from the Coingecko API.

    Using the API endpoint: https://www.coingecko.com/api/documentations/v3#/coins/coin_id/history
    to collect the historical data for a coin on a given day in all currencies.

    Example request URL for this command in the coingecko API
    https://api.coingecko.com/api/v3/coins/bitcoin/history?date=20-02-2023&localization=false


    Args:
        coin_id (str): The ID of the coin to get information about (bitcoin).
        date (str): The date for the price history for eg: 20-02-2023. Defaults to today if None.
        localization (bool): Whether or not to localize the prices. Defaults to False.

    Returns:
        dict: A dictionary containing the price history for the coin on a date given.

    Example:
        >>> price_history("bitcoin", "20-02-2023")
        {
          "id": "bitcoin",
          "symbol": "btc",
          "name": "Bitcoin",
          "image": {
            "thumb": "https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png?1547033579",
            "small": "https://assets.coingecko.com/coins/images/1/small/bitcoin.png?1547033579"
          },
          "market_data": {
            "current_price": {
              "aed": 89196.88770764416,
              "ars": 4656153.985875782,
              ...
            },
            "market_cap": {
                "aed": 1580120000000.0,
                "ars": 82900000000000.0,
                ...
            },
            "total_volume": {
                "aed": 123650382415.91557,
                "ars": 6454655938534.384,
                ...
            }
            },
            "last_updated": "2021-02-20T09:42:02.000Z"
        }

    Raises:
        ValueError: If an invalid date format is passed in by the user.
        ValueError: If the response from the API does not contain the expected data format.
        Exception: If an error occurs while getting the price history.

    """
    if date is not None:
        try:
            datetime.datetime.strptime(date, "%d-%m-%Y")
        except ValueError as date_error:
            raise ValueError("Incorrect date format, should be dd-mm-yyyy") from date_error
    else:
        date = datetime.datetime.today().strftime("%d-%m-%Y")

    try:
        # Build API request URL
        url = compile_api_url(f"coins/{coin_id}/history?date={date}&localization={localization}")

        # Send API request and get response
        response = requests.get(url)
        response_json = response.json()

        # Check if the response is in JSON format and contains the expected data
        if "market_data" not in response_json:
            raise ValueError("Unexpected API response format: missing 'market_data' field")
        if "current_price" not in response_json["market_data"]:
            raise ValueError("Unexpected API response format: missing 'current_price' field")

        # Extract and return the price history
        coin_history = response_json["market_data"]["current_price"]
        return coin_history

    except (ValueError, requests.exceptions.RequestException) as coin_history_error:
        logging.error(coin_history_error)
        raise Exception("Error getting price history from API") from coin_history_error




def price_lookup(coin_id, currency, days="max", interval="daily"):
    """ get the price for a given coin from the coingecko API for a given denomination.

        example call: https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=max&interval=daily

        Args:
            coin_id (str): The ID of the coin to get information about (bitcoin).
            currency (str): The currency to get the price in (usd).
            days (str): The number of days to get the price history for (max, 1, 10, 200...). Defaults to max.
            interval (str): The interval to get the price history for (daily, hourly, minutely). Defaults to daily.

        Returns:
            dict: A dictionary containing the price history for the coin matching the currency given for the number of days specified (default: max).

        Example:
            >>> price_lookup("bitcoin", "usd", "max", "daily")
            {
                "prices": [
                    [ 1613795200000,  46922.0 ],
                    [ 1613881600000,  47064.0 ],
                    [ ... ],

                ],
                "market_caps": [
                    [ 1613795200000,  883000000.0 ],
                    [ 1613881600000,  885000000.0 ],
                    [ ... ],
                ],
                "total_volumes": [
                    [ 1613795200000,  461000000.0 ],
                    [ 1613881600000,  463000000.0 ],
                    [ ... ],
                ]
            }
        Raises:
            ValueError: If an invalid currency is passed in by the user.
            ValueError: If the response from the API does not contain the expected data format.
            Exception: If an error occurs while getting the price lookup.
        """
    # Build API request URL
    url = compile_api_url(f"coins/{coin_id}/market_chart?vs_currency={currency}&days={days}&interval={interval}")

    # Send API request and get response
    response = requests.get(url)
    response_json = response.json()
    # Check if the response is in JSON format and contains the expected data
    if "prices" not in response_json:
        raise ValueError("Unexpected API response format: missing 'prices' field")
    if "market_caps" not in response_json:
        raise ValueError("Unexpected API response format: missing 'market_caps' field")
    if "total_volumes" not in response_json:
        raise ValueError("Unexpected API response format: missing 'total_volumes' field")

    # Extract and return the price lookup
    coin_lookup = {
        "prices": response_json["prices"],
        "market_caps": response_json["market_caps"],
        "total_volumes": response_json["total_volumes"],
    }
    return coin_lookup



def rate_limit(time_of_request):
    """Check if the rate limit has been reached.

    Args:
        time_of_request (float): The time of the request in Unix seconds.

    Returns:
        bool: True if the rate limit has not been reached, False otherwise.

    Raises:
        TypeError: If the time_of_request is not a float.
        TypeError: If the rate_limit_calls is not a float or an integer.
    """
    if not isinstance(time_of_request, float):
        raise TypeError("time_of_request must be a float")
    
    rate_limit_calls = config.getfloat("coingecko", "rate_limit_calls", fallback=10.0) # 10 calls per minute
    
    if not isinstance(rate_limit_calls, (int, float)):
        raise TypeError("rate_limit_calls must be a float or an integer")
    
    global LAST_UPDATE #pylint: disable="w0603
    try:
        if time_of_request - LAST_UPDATE > 60 / rate_limit_calls:
            LAST_UPDATE = datetime.datetime.now().timestamp()
            return True
        return False
    except Exception as general_error:
        print(f"Error occurred: {general_error}")
        return False

#def get_coingecko_price(coin):
#    """ """
    
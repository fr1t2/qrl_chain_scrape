""" using the API found here https://www.coingecko.com/en/api/documentation, collect the
available daily price of a coin id for all days available. I will store the results
in a database for future lookups
"""
import json
import time
import datetime
import mysql.connector
import requests

from src import config

import os
#import configparser

LAST_UPDATE = time.time()

# Load configuration from file
#config = configparser.ConfigParser()
#config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
#print(os.path.join(os.path.dirname(__file__), 'config.ini'))  
print(config.get('pricedb', 'user'))
db_user = config.get('pricedb', 'user')
db_password = config.get('pricedb', 'password')
db_host = config.get('pricedb', 'host')
db_name = config.get('pricedb', 'database')

def cg_get_all_coins():
    """Get a list of supported coins from the Coingecko API.

    Returns:
        list of dict: A list of dictionaries containing information about each coin.

    Example:
        >>> cg_get_all_coins()
        [{"id": "bitcoin", "symbol": "btc"}, {"id": "ethereum", "symbol": "eth"}]
    """
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=false"
    try:
        response = requests.get(url)
        response.raise_for_status() # raise an exception for 4xx or 5xx status codes
    except requests.exceptions.RequestException as request_error:
        print(f"Error while fetching data from Coingecko: {request_error}")
        return []
    coin_list_response = response.json()
    if not isinstance(coin_list_response, list):
        print("Error: Invalid response format from Coingecko API")
        return []
    return coin_list_response

def cg_supported_denominations(coin_id):
    """Get a list of supported denominations for a coin from the Coingecko API.

    Args:
        coin_id (str): The ID of the coin to get supported denominations for.

    Returns:
        list of str: A list of supported denominations for the coin.

    Example:
        >>> cg_supported_denominations("bitcoin")
        ["usd", "eur", "jpy"]
    """
    print(coin_id)
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for non-2xx status codes.
        coin_data = response.json()
    except (requests.exceptions.RequestException, json.JSONDecodeError) as request_error:
        print(f"Error retrieving data for {coin_id}: {request_error}")
        return None
    denominations = []
    try:
        current_prices = coin_data["market_data"]["current_price"]
        for denomination in current_prices.keys():
            denominations.append(str(denomination))
    except KeyError as request_error:
        print(f"Error parsing data for {coin_id}: {request_error}")
        return None
    return denominations

def connect_to_db(data_base = 'address_report1'):
    """Connect to the database and return the connection object.

    Args:
        db_name (str): The name of the database to connect to.

    Returns:
        MySQLConnection: A MySQL connection object.

    Example:
        >>> cnx = connect_to_db("mydatabase")
    """
    cnx = mysql.connector.connect(user=db_user, \
                                  password=db_password, \
                                  host=db_host, \
                                  database=db_name)

    return cnx

def db_create(new_db):
    """Check if database exists and if not, create it"""
    cnx = connect_to_db()
    mycursor = cnx.cursor(buffered=True)
    mycursor.execute("SHOW DATABASES")
    rows = mycursor.fetchall()
    if (new_db,) not in rows:
        # Create the database if it doesn't exist
        print(f"Creating {new_db} database...")
        mycursor.execute(f"CREATE DATABASE IF NOT EXISTS `{new_db}`")
        print(f"{new_db} database created")
    cnx.close()


def db_create_tables(supported_denominations, coin_id_response):
    """Create tables in the databases for each denomination of the coins in coin_list.

    Args:
        denominations (list of str): The list of supported denominations.
        coin_list (list of dict): The list of supported coins.

    Returns:
        None

    Example:
        >>> denominations = ["usd", "eur", "jpy"]
        >>> coin_list = [{"id": "bitcoin", "symbol": "btc"}, {"id": "ethereum", "symbol": "eth"}]
        >>> db_create_tables(denominations, coin_list)
    """
    db_create("address_report1")
    cnx = connect_to_db()
    mycursor = cnx.cursor(buffered=True)
    mycursor.execute("CREATE TABLE IF NOT EXISTS `coin_info` \
                      (coin_id VARCHAR(255), symbol VARCHAR(255), \
                      name VARCHAR(255), PRIMARY KEY (symbol))")
    cnx.close()
    create_table_values = ""
    for denomination in supported_denominations:
        create_table_values += f"`{denomination}` DECIMAL(20,8), "
    create_table_values = create_table_values[:-2]
    for supported_coin in coin_id_response:
        coin_symbol = supported_coin["symbol"][0:63]
        cnx = connect_to_db()
        mycursor = cnx.cursor(buffered=True)
        mycursor.execute(f'CREATE TABLE IF NOT EXISTS `{coin_symbol}` \
                          ({create_table_values}, date_stamp VARCHAR(255), \
                          PRIMARY KEY (date_stamp))')
        cnx.close()

def cg_price_history(coin_id, date):
    """Get the price history for a coin on a given day from the Coingecko API.

    Args:
        coin_id (str): The ID of the coin to get the price history for.
        date (str): The date to get the price history for in dd-mm-yyyy

    Returns:
        dict: A dictionary containing the price history for the coin on the given day.

    Example:
        >>> cg_price_history("bitcoin", "01-01-2021"){'prices': [[1609459200000, 28983.56777061452]], \
                                                      'market_caps': [[1609459200000, 541831712.0]],  \
                                                      'total_volumes': [[1609459200000, 0.0]]} 
    """
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/history?date={date}'
    retry = True
    while retry:
        try:
            cg_data = requests.get(url)
            # check if the request was successful
            if cg_data.status_code != 200:
                raise requests.exceptions.RequestException(
                    f"Error: {cg_data.status_code} - {cg_data.reason}"
                )
            retry = False
        except requests.exceptions.RequestException as request_error:
            print(request_error)
            print("Retrying...")
            time.sleep(1)
    return cg_data.json()

def cg_price_lookup(coin_id, denomination):
    """Get the current price for a coin in a given denomination from the Coingecko API.

    Args:
        coin_id (str): The ID of the coin to get the price for.
        denomination (str): The denomination to get the price in.

    Returns:
        float: The current price of the coin in the given denomination. in a dictionary
        {"prices": [[timestamp, price], [timestamp, price], ...], \
         "market_caps": [[timestamp, market_cap], [timestamp, market_cap], ...], \
         "total_volumes": [[timestamp, total_volume], [timestamp, total_volume], ... ]}

    Example:
        >>> cg_price_lookup("bitcoin", "usd")
        48590.58
    """
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={denomination}&days=max&interval=daily'
    retry = True
    while retry:
        try:
            cg_data = requests.get(url)
            # check if the request was successful
            if cg_data.status_code != 200:
                raise requests.exceptions.RequestException(f"Request error: {cg_data.status_code}")
            coin_id_response = json.loads(cg_data.text)
            retry = False
        except (requests.exceptions.RequestException, json.JSONDecodeError) as request_error:
            print(f'Error in cg_price_lookup for coin_id={coin_id}, \
                    denomination={denomination}: {request_error}')
            print(f"Retrying in 5 seconds...")
            time.sleep(5)
    return coin_id_response

def coin_price_insert(coin_symbol, denomination, price_data):
    """
    Inserts price data for a coin and denomination into the corresponding table in the database.

    This function inserts price data into a table whose name is generated by concatenating the
    given coin symbol and denomination with an underscore. The price data is obtained from the
     cg_price_lookup function and is represented by a dictionary containing the keys "prices",
     "market_caps", and "total_volumes". Each key's value is a list of tuples, where each tuple
      represents a data point with a timestamp and a value.

    Parameters:
    - coin_symbol (str): The symbol or ID of the coin for which to insert price data.
    - denomination (str): The denomination in which to record the price data.
    - price_data (dict): A dictionary containing the price data to insert.

    Returns:
    - None

    The function establishes a connection to the database and inserts each price data point into
     the corresponding table. If a price data point for the given timestamp already exists in the
     table but differs from the new value, the function updates the table instead of inserting a new row.
    """
    print(f'Check for {coin_symbol} : {denomination} price data in database for a given day')
    cnx = connect_to_db()
    mycursor = cnx.cursor(buffered=True)
    for price in price_data["prices"]:
        timestamp = price[0]
        mycursor.execute(f'SELECT {denomination}, date_stamp FROM {coin_symbol} WHERE date_stamp = %s', (timestamp,))
        result_row = mycursor.fetchone()
        if result_row:
            if result_row[0] is None:
                mycursor.execute(f'UPDATE {coin_symbol} SET {denomination} = %s WHERE date_stamp = %s', (price[1], timestamp)) # price[1] is the price
                cnx.commit()
                continue
            if timestamp > (time.time() * 1000) - (3 * 24 * 60 * 60 * 1000): # 3 days in milliseconds
                continue # if timestamp is less than 3 days ago we trust the old data, continue
            current_price = price[1] # price[1] is the price
            found_price = result_row[0] # result_row[0] is the price in the database
            current_price_str = str(current_price) # convert the price to a string
            found_price_str = str(found_price) # convert the price in the database to a string
            if '.' in current_price_str and '.' in found_price_str:
                current_price_str = "{:.{}f}".format(   # Round to the same number of decimal places as found_price
                    float(current_price_str),
                    len(found_price_str.split('.')[-1]) # Number of decimal places in found_price
                )
            if found_price_str != current_price_str and current_price_str != 'None':
                # Update the database with the new price
                mycursor.execute(f'INSERT INTO {coin_symbol} ({denomination}, date_stamp) VALUES (%s, %s) \
                                   ON DUPLICATE KEY UPDATE {denomination} = %s',
                                   (current_price_str, timestamp, current_price_str))
                cnx.commit()
        elif result_row is None: # if the timestamp is not in the database, we need to insert a new row
            current_price = price[1] # price[1] is the price
            todays_timestamp = int(datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000) # get the timestamp for today at 00:00:00
            timestamp = min(timestamp, todays_timestamp) # if the timestamp is greater than today, set it to today at 00:00:00
            mycursor.execute(f'INSERT INTO {coin_symbol} (date_stamp, {denomination}) VALUES (%s, %s) ON DUPLICATE KEY UPDATE {denomination} = %s', (timestamp, current_price, current_price))
            cnx.commit()
    mycursor.close() # close the cursor
    cnx.close() # close the connection








def coin_info_insert(coin_symbol, coin_name, coin_id):
    """Insert coin data into the database for a given coin and denomination.

    Args:
        coin_id (str): The ID of the coin to insert data for.
        coin_symbol (str): The symbol of the coin to insert data for.
        coin_name (str): The name of the coin to insert data for.

    Returns:
        None

    Example:
        >>> coin_info_insert("bitcoin", "Bitcoin", "BTC")
    """
    cnx = connect_to_db()
    mycursor = cnx.cursor(buffered=True)
    try:
        mycursor.execute("UPDATE coin_info SET coin_id=%s, name=%s WHERE symbol=%s",
                         (coin_id, coin_name, coin_symbol))
        if mycursor.rowcount == 0:
            mycursor.execute("INSERT INTO coin_info (coin_id, symbol, name) \
                              VALUES (%s, %s, %s)", (coin_id, coin_symbol, coin_name))
        cnx.commit()
    except mysql.connector.errors.IntegrityError as mysql_error:
        print(mysql_error)
        cnx.rollback()
    cnx.close()

def cg_rate_limit(time_of_request):
    """Check the time between API calls and rate limit the requests to avoid a block.
    Each call to the API should happen after this function returns True.

    Args:
        time_of_request (float): The Unix timestamp of the request.

    Returns:
        bool: True if the rate limit has passed and the request can be made, False otherwise.

    Example:
        >>> cg_rate_limit(time.time())
        True
    """
    rate_limit = 60 # seconds
    calls_allowed_in_period = 10 # number of calls allowed in rate_limit time frame
    global LAST_UPDATE # use the global LAST_UPDATE variable #pylint: disable=global-statement
    if (time_of_request - LAST_UPDATE) >= (rate_limit / calls_allowed_in_period):
        LAST_UPDATE = time.time()
    else:
        time_to_wait = (rate_limit / calls_allowed_in_period) - (time_of_request - LAST_UPDATE)
        time.sleep(time_to_wait)
        return cg_rate_limit(time.time()) if time_to_wait > 0 else False
    return True

#def coin_check(symbol):
#    """Check whether data for a given coin is up to date.
#
#    This function queries the database for the last entered timestamp for the given coin and 
#    checks if the data is less than or equal to 86400 seconds (1 day) old. If the data is up 
#    to date, it returns a list with two elements:
#    The first element is True, and the second element is the timestamp of the last data entry. 
#    If the data is not up to date or an error occurs, it returns a list with two elements: 
#    the first element is False, and the second element is the timestamp of the last data entry.
#
#    Args:
#        symbol (str): The symbol of the coin to check.
#
#    Returns:
#        A list with two elements: the first element is a boolean indicating whether the data is up to date, and the
#        second element is the timestamp of the last data entry.
#
#    Example:
#        >>> coin_check('BTC')
#        cur: 1645093196 - last: 1645093195 = True
#        [True, 1645093195]
#    """
#    up_to_date = [False, 0]  # initialize to default value
#    last_timestamp = 0  # initialize to default value
#    try:
#        cnx = connect_to_db()
#        mycursor = cnx.cursor(buffered=True)
#        mycursor.execute("SELECT date_stamp FROM " + symbol + " ORDER BY date_stamp DESC LIMIT 1")
#        result = mycursor.fetchone()
#        if result is not None:
#            last_timestamp = result[0]
#            current_time = int(time.time())
#            if (int(current_time) - (int(last_timestamp)/1000)) <= 86400:
#                up_to_date = [True, last_timestamp]
#    except: #pylint: disable=W0702
#        up_to_date = [False, last_timestamp]  # initialize to default value
#    cnx.close()
#    return up_to_date
def coin_check(symbol):
    """Check whether data for a given coin is up to date.

    This function queries the database for the last entered timestamp for the given coin and
    checks if the data is less than or equal to 86400 seconds (1 day) old. If the data is up
    to date, it returns a list with two elements:
    The first element is True, and the second element is the timestamp of the last data entry.
    If the data is not up to date or an error occurs, it returns a list with two elements:
    the first element is False, and the second element is the timestamp of the last data entry.

    Args:
        symbol (str): The symbol of the coin to check.

    Returns:
        A list with two elements: the first element is a boolean indicating whether the data is up to date, and the
        second element is the timestamp of the last data entry.

    Example:
        >>> coin_check('BTC')
        cur: 1645093196 - last: 1645093195 = True
        [True, 1645093195]
    """
    up_to_date = [False, 0]  # initialize to default value
    last_timestamp = 0  # initialize to default value
    try:
        cnx = connect_to_db()
        mycursor = cnx.cursor(buffered=True)
        query = "SELECT date_stamp FROM %s ORDER BY date_stamp DESC LIMIT 1"
        mycursor.execute(query, (symbol,))
        result = mycursor.fetchone()
        if result is not None:
            last_timestamp = result[0]
            current_time = int(time.time())
            if (int(current_time) - (int(last_timestamp)/1000)) <= 86400:
                up_to_date = [True, last_timestamp]
    except: #pylint: disable=W0702
        up_to_date = [False, last_timestamp]  # initialize to default value
    cnx.close()
    return up_to_date


def historical_data_collection():
    """
    Collect all historical data from the API and store price for all denomination found.
    """
    denominations = []
    supported_coins = []
    # the coinlist.json file is in the same directory as this file, open it
    script_path = os.path.abspath(__file__)
    coinlist_path = os.path.join(os.path.dirname(script_path), 'price', 'coinlist.json') 
    with open(coinlist_path, "r", encoding="utf-8") as coinlist_file: 
        supported_coins = json.load(coinlist_file)
    if cg_rate_limit(time.time()):
        denominations = cg_supported_denominations(supported_coins[0]["id"])
    db_create_tables(denominations, supported_coins)
    for supported_coin in supported_coins:
        print(f'Check if up to date {supported_coin["symbol"]}')
        is_up_to_date = coin_check(supported_coin["symbol"])
        if is_up_to_date[0]:
            continue
        coin_info_insert(supported_coin["symbol"], supported_coin["name"], supported_coin["id"]) #pylint: disable=E1121
        for denom in denominations:
            #print(denom)
            if cg_rate_limit(time.time()):
                curent_lookup = cg_price_lookup(supported_coin["id"], denom)
                coin_price_insert(supported_coin["symbol"], denom, curent_lookup)

if __name__ == "__main__":
    #time how long the command takes to execute
    start_time = time.time()
    historical_data_collection()
    # print in condensed time, if hours print in hh:mm:ss, if minutes print in mm:ss, if seconds print in ss
    if (time.time() - start_time) > 3600:
        print(f'done in: {datetime.timedelta(seconds=time.time() - start_time)}')
    elif (time.time() - start_time) > 60:
        print(f'done in: {round((time.time() - start_time)/60, 2)} minutes')
    else:
        print(f'done in: {round(time.time() - start_time, 2)} seconds')
    #
    # print(f'done in: {datetime.timedelta(seconds=time.time() - start_time)}')
    # print(f'done in: {time.time() - start_time} seconds or {round((time.time() - start_time)/60, 2)} minutes')
""" file contains helper functions for the database.

"""
import logging
from config import config

# check for MySQLdb module
try:
    import mysql.connector
except ImportError:
    logging.error('MySQLdb module not found. Please install it with: pip3 install MySQL-python')
    raise


def connect():
    """ Connect to the database and return the connection object.

    :return: the connection object
    """
    logging.info('Connecting to database...')

# handle any errors that might occur while connecting to the database
    try:
        connection = mysql.connector.connect(
            host=config['chaindb']['host'],
            port=config['chaindb']['port'],
            user=config['chaindb']['user'],
            password=config['chaindb']['password'],
            database=config['chaindb']['database']
        )
        logging.info('Connected to database.')

    except mysql.connector.Error as err:
        logging.error('Could not connect to database: {}'.format(err))
        raise

    return connection # return the connection object


def get_cursor(connection):
    """ Get a cursor object from the connection object.

    :param connection: the connection object
    :return: the cursor object
    """
    # handle any errors that might occur while getting the cursor
    try:
        cursor = connection.cursor()
    except mysql.connector.Error as err:
        logging.error('Could not get cursor: {}'.format(err))
        raise

    return cursor # return the cursor object


# check for a given database in the server
def check_database_exists(connection, database):
    """ Check if a database exists.

    :param connection: the connection object
    :param database: the database to check
    :return: True if the database exists, False otherwise
    """
    cursor = get_cursor(connection)
    cursor.execute('SHOW DATABASES')
    databases = [row[0] for row in cursor.fetchall()]
    return database in databases


# create the given database if it doesn't exist, do nothing if it does
def create_database(connection, database):
    """ Create a database.

    :param connection: the connection object
    :param database: the database to create
    :return: True if the database was created, False otherwise
    """
    if not check_database_exists(connection, database):
        # handle any errors that might occur while creating the database
        try:
            cursor = get_cursor(connection)
            cursor.execute('CREATE DATABASE {}'.format(database))
            logging.info('Database {} created.'.format(database))

        except mysql.connector.Error as err:
            logging.error('Could not create database: {}'.format(err))
            raise

        return True
    else:
        logging.info('Database {} already exists.'.format(database))
        return False



# check for a given table in the database.


#create the given table if it doesn't exist in the given database, do nothing if it does






def execute_query(connection, query, params=None):
    """ Execute a query on the database.

    :param connection: the connection object
    :param query: the query to execute
    :param params: the parameters to use in the query
    :return: the cursor object
    """
    cursor = get_cursor(connection)
    if params is None:
        cursor.execute(query)
    else:
        # handle multiple parameters
        if isinstance(params, tuple):
            cursor.execute(query, params)
        # handle single parameter
        else:
            cursor.execute(query, (params,))

    return cursor # return the cursor object so we can fetch the results


def execute_query_many(connection, query, params):
    """ Execute a query on the database with multiple parameters.

    :param connection: the connection object
    :param query: the query to execute
    :param params: the parameters to use in the query
    :return: the cursor object
    """
    cursor = get_cursor(connection)
    cursor.executemany(query, params)
    return cursor # return the cursor object so we can fetch the results


def fetch_one(cursor):
    """ Fetch one row from the cursor.

    :param cursor: the cursor object
    :return: the row
    """
    return cursor.fetchone() # return the row


def fetch_all(cursor):
    """ Fetch all rows from the cursor.

    :param cursor: the cursor object
    :return: the rows
    """
    return cursor.fetchall() # return the rows


def commit(connection):
    """ Commit the changes to the database.

    :param connection: the connection object
    """
    connection.commit()


def close_connection(connection):
    """ Close the connection to the database.

    :param connection: the connection object
    """
    connection.close()
    logging.info('Connection to database closed.')


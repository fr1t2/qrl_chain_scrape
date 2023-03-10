""" file contains helper functions for the database.

"""
import logging

# check for MySQLdb module
try:
    import mysql.connector
except ImportError:
    logging.error('MySQLdb module not found. Please install it with: pip3 install MySQL-python')
    raise

from src import config

CONFIG_FILE = config.get_config()

print(CONFIG_FILE.get('pricedb', 'host'))

def connect(database=None):
    """
    Connects to the database and returns the connection object.

    Args:
        database (str): The name of the database to connect to.

    Returns:
        connection: The connection object representing the connection to the database.

    Raises:
        mysql.connector.Error: If the connection to the database could not be established.
    """
    logging.info('Connecting to database...')

    if database is None:
        database = CONFIG_FILE.get('chaindb', 'database')
        logging.info('No database given, using default database: {}'.format(database))

    try:
        connection = mysql.connector.connect(
            host=CONFIG_FILE.get(database, 'host'),
            port=CONFIG_FILE.get(database, 'port', fallback=3306),
            user=CONFIG_FILE.get(database, 'user'),
            password=CONFIG_FILE.get(database, 'password'),
            database=database
        )
        logging.info('Connected to database {}.'.format(database)) # log the database name

    except mysql.connector.Error as err:
        logging.error('Could not connect to database: {}'.format(err))
        raise

    return connection # return the connection object

def get_cursor(connection=None):
    """
    Returns a cursor object from the connection object.

    Args:
        connection: The connection object representing the connection to the database.

    Returns:
        cursor: The cursor object associated with the connection object.

    Raises:
        Exception: If the cursor could not be obtained from the connection object.
    """
    if connection is None:
        connection = connect() # get a connection object if one is not given

    try:
        cursor = connection.cursor(buffered=True)
    except mysql.connector.Error as err:
        logging.error('Could not get cursor: {}'.format(err))
        raise Exception('Could not get cursor: {}'.format(connection.json()['error'])) # raise an exception if the request fails

    return cursor # return the cursor object



# check for a given database in the server
def check_database_exists(connection, database, cursor=None):
    """ Check if a database exists.

        :param connection: the connection object to the database
        :param database: the name of the database to check
        :param cursor: the cursor object to use to execute the query, defaults to None
        :return: True if the database exists, False otherwise
    """
    # get a cursor if one is not given
    if cursor is None:
        cursor = get_cursor(connection)

    # get a list of all the databases
    cursor.execute('SHOW DATABASES')

    # check if the given database is in the list of databases
    databases = [row[0] for row in cursor.fetchall()] # get a list of all the databases
    #check if given database is in the list of databases
    if database in databases:
        return True
    else:
        return False


# create the given database if it doesn't exist, do nothing if it does
def create_database(connection, database, cursor=None):
    """ Create a database.

        :param connection: the connection object to the database
        :param database: the name of the database to create
        :param cursor: the cursor object to use to execute the query, defaults to None
        :return: True if the database was created, False otherwise
    """
    # get a cursor if one is not given
    if cursor is None:
        cursor = get_cursor(connection)

    if not check_database_exists(connection, database, cursor):
        # handle any errors that might occur while creating the database
        try:
            cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(database))
            logging.info('Database {} created.'.format(database))
            response = True

        except mysql.connector.Error as err:
            logging.error('Could not create database: {}'.format(err))
            raise Exception('Could not create database: {}'.format(connection.json()['error'])) from err

    else:
        logging.info('Database {} already exists.'.format(database))
        response = False

    return response # return True if the database was created, False otherwise


# check for a given table in the database.
def check_table_exists(connection, table, database=None, cursor=None):
    """ Check if a table exists.

    :param connection: the connection object
    :param table: the table to check
    :param database: the database to check the table in
    :return: True if the table exists, False otherwise
    """
    # get a cursor if one is not given
    if cursor is None:
        cursor = get_cursor(connection)

    # get a list of all the tables in the given database
    if database is None:
        cursor.execute('SHOW TABLES LIKE %s', (table,))
    else:
        cursor.execute('SHOW TABLES IN {} LIKE %s'.format(database), (table,))

    # check if the given table is in the list of tables
    tables = [row[0] for row in cursor.fetchall()] # get a list of all the tables
    #check if given table is in the list of tables
    if table in tables:
        return True
    else:
        return False


def create_table_if_not_exists(connection, table, values, database=None, cursor=None):
    """Create a table if it doesn't already exist.

    Args:
        - connection: a MySQL database connection object
        - table: the name of the table to be created
        - values: a list of strings containing the column names and their data types, e.g. ["id INTEGER", "name TEXT"]
        - database: (optional) the name of the database in which to create the table
        - cursor: (optional) a MySQL cursor object

    Returns:
        None

    Example usage:

        ```
        import mysql.connector

        # Establish a database connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password"
        )

        # Create a new table called "users" with columns "id" and "name"
        create_table_if_not_exists(connection, "users", ["id INTEGER", "name TEXT"])
        ```

    """
    # add a check for the connection being NoneType 
    if connection is None:
        try:
            connection = connect() # get a connection object if one is not given
        except Exception as err:
            logging.error('Could not connect to database: {}'.format(err))
            raise Exception('Could not connect to database: {}'.format(connection.json()['error'])) from err

    # get a cursor if one is not given
    if cursor is None:
        cursor = connection.cursor()

    if database is None:
        database = ""

    try:
        cursor.execute('CREATE TABLE IF NOT EXISTS {}.{} ({})'.format(database, table, ", ".join(values)))
    except mysql.connector.Error as err:
        logging.error('Could not create table: {}'.format(err))
        raise Exception('Could not create table: {}'.format(connection.json()['error'])) from err


def describe_table(connection, table, database, cursor):
    """Get a list of the column names in a table.

    Args:
        - connection: a MySQL database connection object
        - table: the name of the table to describe
        - database: (optional) the name of the database containing the table
        - cursor: a MySQL cursor object

    Returns:
        A list of strings representing the column names in the table.

    Example usage:

        ```
        import mysql.connector

        # Establish a database connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password"
        )

        # Get the column names in the "users" table
        columns = describe_table(connection, "users")
        ```

    """
    if database is None:
        try:
            cursor.execute('DESCRIBE {}'.format(table))
        except mysql.connector.Error as err:
            logging.error('Could not describe table: {}'.format(err))
            raise Exception('Could not describe table: {}'.format(connection.json()['error'])) from err
    else:
        try:
            cursor.execute('DESCRIBE {}.{}'.format(database, table))
        except mysql.connector.Error as err:
            logging.error('Could not describe table: {}'.format(err))
            raise Exception('Could not describe table: {}'.format(connection.json()['error'])) from err
    return [row[0] for row in cursor.fetchall()]


def add_new_column_to_table(connection, table, new_values, database, cursor):
    """Add a new column to a MySQL table.
    
    Args:
        connection (mysql.connector.connection_cext.CMySQLConnection): A MySQL database connection object.
        table (str): The name of the table to add a column to.
        new_values (str): A string containing the column name and data type, e.g. "email VARCHAR(255)".
        database (str, optional): The name of the database the table belongs to.
        cursor (mysql.connector.cursor_cext.CMySQLCursor, optional): A MySQL database cursor object.
        
    Raises:
        Exception: If the table cannot be altered, raises an exception with an error message.

    Returns:
        None.
    """
    if database is None:
        try:
            cursor.execute(f'ALTER TABLE {table} ADD COLUMN {new_values}')
        except mysql.connector.Error as err:
            logging.error('Could not alter table: {}'.format(err))
            raise Exception('Could not alter table: {}'.format(connection.json()['error'])) from err
    else:
        try:
            cursor.execute(f'ALTER TABLE {database}.{table} ADD COLUMN {new_values}')
        except mysql.connector.Error as err:
            logging.error('Could not alter table: {}'.format(err))
            raise Exception('Could not alter table: {}'.format(connection.json()['error'])) from err


def create_table(connection, table, values, database=None, cursor=None):
    """Create a new MySQL table.
    
    Args:
        connection (mysql.connector.connection_cext.CMySQLConnection): A MySQL database connection object.
        table (str): The name of the new table to create.
        values (list): A list of strings representing the column names and data types, e.g. ["id INTEGER", "name TEXT"].
        database (str, optional): The name of the database the new table should belong to.
        cursor (mysql.connector.cursor_cext.CMySQLCursor, optional): A MySQL database cursor object.
        primary_key (tuple, optional): A tuple representing the primary key column(s) and data type(s), e.g. ("id", "INTEGER").
        foreign_key (tuple, optional): A tuple representing the foreign key column, the table it references, and the referenced column, e.g. ("customer_id", "customers", "id").
        
    Raises:
        Exception: If the table already exists and cannot be altered, raises an exception with an error message.
        
    Returns:
        bool: Returns True if the table was successfully created or altered, and False if the table already exists with the same values.
    """
    if cursor is None:
        cursor = get_cursor(connection)

    if not check_table_exists(connection, table, database, cursor):
        create_table_if_not_exists(connection, table, values, database, cursor)
        logging.info('Table {} created.'.format(table))
        response = True
    else:
        logging.info('Table {} already exists.'.format(table))
        columns = describe_table(connection, table, database, cursor)
        if columns == values:
            logging.info('Table {} already exists with the same values.'.format(table))
            response = False
        else:
            logging.info('Table {} already exists with different values.'.format(table))
            new_values = [value for value in values if value not in columns]
            new_values = ', '.join(new_values)
            add_new_column_to_table(connection, table, new_values, database, cursor)
            logging.info('Table {} updated with new values: {}'.format(table, new_values))
            response = True

    return response




#
##--------------------------------------------------------------------------------------------------------------------------------------------------#
#
## create the given table if it doesn't exist in the given database, do nothing if it does exist
#def create_table1(connection, table, values, database=None, cursor=None):
#    """
#    Creates the given table in the specified database using the provided values for rows and columns.
#    If the table already exists in the database with the same values, it does nothing and returns False.
#    If the table already exists in the database with different values, it updates the table to include the new values
#    while keeping any existing data and returns True.
#
#    Args:
#        connection (object): A connection object to a MySQL database.
#        table (str): The name of the table to create.
#        values (str): A string of comma-separated values for the rows and columns in the format 'column1 datatype1, column2 datatype2'.
#        database (str, optional): The name of the database to use. Defaults to None, which means the table will be created in the default database.
#        cursor (object, optional): A cursor object for the database. Defaults to None, which means a new cursor will be created.
#
#    Returns:
#        bool: True if the table was created or updated, False if the table already exists with the same values.
#
#    Raises:
#        Exception: If there is an error creating or updating the table.
#
#    Examples:
#
#        # Create a table with columns id and name
#        create_table(connection, "customers", "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255)")
#
#        # Create a table with columns id, name, and age in a specific database
#        create_table(connection, "customers", "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT", database="mydatabase")
#    """
#    if cursor is None:
#        cursor = get_cursor(connection)
#
#    if not check_table_exists(connection, table, database, cursor):
#        try:
#            # create the table in the given database if one is given using the values given for rows and columns
#            if database is None:
#                # catch any issues with the cursor.execute statement and log them   
#                try:
#                    cursor.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(table, values))
#                except mysql.connector.Error as err:
#                    logging.error('Could not create table: {}'.format(err))
#                    raise Exception('Could not create table: {}'.format(connection.json()['error'])) from err # raise an exception if the request fails
#            else:
#                try:
#                    cursor.execute('CREATE TABLE IF NOT EXISTS {}.{} ({})'.format(database, table, values))
#                except mysql.connector.Error as err:
#                    logging.error('Could not create table: {}'.format(err))
#                    raise Exception('Could not create table: {}'.format(connection.json()['error'])) from err
#
#            logging.info('Table {} created.'.format(table))
#            response = True # return True if the table was created
#
#        except mysql.connector.Error as err:
#            logging.error('Could not create table: {}'.format(err))
#            raise Exception('Could not create table: {}'.format(connection.json()['error'])) from err# raise an exception if the request fails
#
#    else:
#        logging.info('Table {} already exists.'.format(table))
#        # check that the values for the rows and columns are the same as the values given
#        if database is None:
#            try:
#                cursor.execute('DESCRIBE {}'.format(table))
#            except mysql.connector.Error as err:
#                logging.error('Could not describe table: {}'.format(err))
#                raise Exception('Could not describe table: {}'.format(connection.json()['error'])) from err
#        else:
#            try:
#                cursor.execute('DESCRIBE {}.{}'.format(database, table))
#            except mysql.connector.Error as err:
#                logging.error('Could not describe table: {}'.format(err))
#                raise Exception('Could not describe table: {}'.format(connection.json()['error'])) from err
#
#        # get the values for the rows and columns
#        columns = [row[0] for row in cursor.fetchall()] # get a list of all the columns for the table
#        # check if the values for the rows and columns are the same as the values given
#        if columns == values:
#            logging.info('Table {} already exists with the same values.'.format(table))
#            response = False # return False if the table already exists with the same values
#        else:
#            logging.info('Table {} already exists with different values.'.format(table))
#            # append the table to include the new values while keeping any data in the database
#            # get the new values into a list to avoid duplicate columns if the table already exists
#            new_values = [value for value in values if value not in columns] # get the new values
#            new_values = ', '.join(new_values) # convert the list to a string
#            # append the table to include the new values while keeping any data in the database
#            if database is None:
#                try:
#                    cursor.execute(f'ALTER TABLE {table} ADD COLUMN {new_values}')
#                except mysql.connector.Error as err:
#                    logging.error('Could not alter table: {}'.format(err))
#                    raise Exception('Could not alter table: {}'.format(connection.json()['error'])) from err
#            else:
#                try:
#                    cursor.execute(f'ALTER TABLE {database}.{table} ADD COLUMN {new_values}')
#                except mysql.connector.Error as err:
#                    logging.error('Could not alter table: {}'.format(err))
#                    raise Exception('Could not alter table: {}'.format(connection.json()['error'])) from err
#
#            logging.info('Table {} updated with new values: {}'.format(table, new_values))
#            response = True # return True if the table was updated
#
#    return response # return True if the table was created, False otherwise

####################
## Lookup Functions
####################
# get the last modified time in unix sec from a given table, any row and any column
def get_last_modified_table_time(connection, table, database=None, cursor=None):
    """Get the last modified time in unix sec from a given table, any row and any column.

    Args:
        connection (object): A connection object for the database.
        table (str): The name of the table.
        database (str, optional): The name of the database. Defaults to None.
        cursor (object, optional): A cursor object for the database. Defaults to None.

    Returns:
        int: The last modified time in unix sec.

    Raises:
        Exception: If there is an error getting the last modified time.
    """

    if cursor is None:
        cursor = get_cursor(connection)

    #fetch the last modified row in the table using the last_modified column
    if database is None:
        try:
            cursor.execute('SELECT last_modified FROM {} ORDER BY last_modified DESC LIMIT 1'.format(table))
        except mysql.connector.Error as err:
            logging.error('Could not get last modified: {}'.format(err))
            raise Exception('Could not get last modified: {}'.format(connection.json()['error'])) from err
    else:
        try:
            cursor.execute('SELECT last_modified FROM {}.{} ORDER BY last_modified DESC LIMIT 1'.format(database, table))
        except mysql.connector.Error as err:
            logging.error('Could not get last modified: {}'.format(err))
            raise Exception('Could not get last modified: {}'.format(connection.json()['error'])) from err

    # get the last modified time in unix sec
    last_modified = cursor.fetchone()[0]
    return last_modified # return the last modified time in unix sec



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


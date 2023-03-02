"""test the file located at src/db/dbhelper.py and all of the functions there"""

#import logging
#import mysql.connector
#import pytest
#import unittest
#from unittest import mock
#from src import config
#
#from src.db import connect
#from src.db import get_cursor
#from src.db import check_database_exists
#from src.db import create_database
#from src.db import check_table_exists
#from src.db import describe_table
#from src.db import add_new_column_to_table
#from src.db import create_table
#from src.db import create_table_if_not_exists
#from src.db import get_last_modified_table_time
#from src.db import execute_query
#from src.db import execute_query_many
#from src.db import fetch_one
#from src.db import fetch_all
#from src.db import commit
#from src.db import close_connection






# We want to create a test database for the functions outlined to work. 
# We will create a test database and test tables to test the functions in this file 
# We will use the pytest framework to run the tests
# this database will be destroyed at the end of the testing process
# we will use the src.db.connect() function to connect to the database
# we will use the src.db.get_cursor() function to get a cursor object
# using these two functions we can create the test database and test tables
# we will use the src.db.check_database_exists() function to check if the database exists
# we will use the src.db.create_database() function to create the database
# we will use the src.db.check_table_exists() function to check if the table exists
# we will use the src.db.create_table() function to create the test tables
# we will use the src.db.describe_table() function to describe the table
# we will use the src.db.add_new_column_to_table() function to add a new column to the table
# we will use the src.db.create_table_if_not_exists() function to create a table if it does not exist
# we will use the src.db.close_connection() function to close the connection to the database




## test the create database function
#def test_create_database_and_connect():
#    # test both the connect and create database functions at the same time
#    # test that the function returns a connection object
#    assert isinstance(connect(), mysql.connector.MySQLConnection) == True # test that the function returns a connection object
#
#    # create the test database
#    create_database('test_db')
#
#    # connect to the test database
#    connect('test_db')
#
#    # test that the function returns a connection object with the correct database
#    assert connect('test_db').database == 'test_db' # test that the function returns a connection object with the correct database
#
#    # test that the function returns a connection object with the correct host
#    assert connect('test_db').host == 'localhost' # test that the function returns a connection object with the correct host
#
#    # test that the function returns a connection object with the correct port
#    assert connect('test_db').port == '3306' # test that the function returns a connection object with the correct port
#
#    # test that the function returns a connection object with the correct user
#    assert connect('test_db').user == 'qrl' # test that the function returns a connection object with the correct user
#
#
#
#
#
#
## test the get_cursor function
#def test_get_cursor():
#
#
#
#
## test ther check_database_exists function
#def test_check_database_exists():
#    # test that the function returns true if the database exists
#    assert check_database_exists('qrl_chain_scrape') == True
#
#    # test that the function returns false if the database does not exist
#    assert check_database_exists('some_database_that_does_not_exist') == False
#
## test the check_table_exists function
#def test_check_table_exists():
#    # test that the function returns true if the table exists
#    assert check_table_exists('qrl_chain_scrape', 'block') == True
#
#    # test that the function returns false if the table does not exist
#    assert check_table_exists('qrl_chain_scrape', 'some_table_that_does_not_exist') == False













"""
@pytest.mark.database
class TestConnect(unittest.TestCase):
    @mock.patch('src.db.connect')
    @mock.patch('src.config.get')
    def test_connect_successful(self, mock_config_get, mock_mysql_connect):
        mock_config_get.return_value = ''

        mock_mysql_connect.return_value = mock.MagicMock()

        result = connect()

        self.assertIsInstance(result, mysql.connector.MySQLConnection)
        self.assertTrue(mock_config_get.called)
        self.assertTrue(mock_mysql_connect.called)
        mock_mysql_connect.assert_called_once_with(
            host='some_value',
            port='3306',
            user='some_value',
            password='some_value',
            database='test_db'
        )

    @mock.patch('src.db.connect')
    @mock.patch('src.config.get')
    def test_connect_raises_error(self, mock_config_get, mock_mysql_connect):
        mock_config_get.return_value = 'localhost, 3306, qrl, blockchain, chaindb'
        mock_mysql_connect.side_effect = mysql.connector.Error()

        with self.assertRaises(mysql.connector.Error):
            connect(database='mysql')

        self.assertTrue(mock_config_get.called)
        self.assertTrue(mock_mysql_connect.called)

@patch('mysql.connector.connect')
@patch('src.db.dbhelper.config')
def test_connect_successful(mocked_config, mocked_connect):
    # configure the mock to return expected values for the config.get calls
    mocked_config.get.side_effect = ['localhost', '3306', 'qrl', 'blockchain', 'chaindb']
    mocked_connection = MagicMock() # create a mock connection object
    mocked_connect.return_value = mocked_connection # return the connection object

    # call the connect function and check that the correct arguments were used
    connection = connect() # call the connect function without specifying a database

    mocked_config.get.assert_has_calls([
        call('chaindb', 'database'),
        call('chaindb', 'host'),
        call('chaindb', 'port'),
        call('chaindb', 'user'),
        call('chaindb', 'password'),
    ]) # check that the correct arguments were used

    mocked_connect.assert_called_once_with( # check that the correct arguments were used
        database='qrl_chain_scrape',
        host='localhost',
        port='3306',
        user='qrl',
        password='blockchain'
    )

    assert connection == mocked_connection # check that the correct connection object was returned



@patch('src.config')
@patch('mysql.connector.connect')
def test_connect_successful1(mocked_connect, mocked_config):
    # should return the connection object from mysql.connector.connect if successful
    mocked_config.get.side_effect = ['localhost', '3306', 'qrl', 'blockchain']
    mocked_connection = Mock()
    mocked_connect.return_value = mocked_connection

    connection = connect('chaindb')

    print(connection)

#    mocked_config.get.assert_called_once_with('chaindb', 'host')
#    mocked_config.get.assert_called_once_with('chaindb', 'port')
#    mocked_config.get.assert_called_once_with('chaindb', 'qrl')
#    mocked_config.get.assert_called_once_with('chaindb', 'blockchain')
    #
#    mocked_connect.assert_called_once_with(
#        host='localhost',
#        port='3306',
#        user='qrl',
#        password='blockchain',
#        database='chaindb'
#    )


@patch('src.config')
@patch('mysql.connector.connect')
def test_connect_with_default_database(mocked_connect, mocked_config):
    mocked_config.get.return_value = 'some_value'
    mocked_connection = Mock()
    mocked_connect.return_value = mocked_connection

    connection = connect()

    mocked_config.get.assert_called_once_with('chaindb', 'database')
    mocked_connect.assert_called_once_with(
        host='some_value',
        port='some_value',
        user='some_value',
        password='some_value',
        database='some_value',
    )

    assert connection == mocked_connection


@patch('src.config')
@patch('mysql.connector.connect')
def test_connect_failure(mocked_connect, mocked_config):
    mocked_config.get.return_value = 'some_value'
    mocked_connect.side_effect = Exception('some error message')

    with pytest.raises(Exception):
        connect(database='my_database')

    mocked_config.get.assert_called_once_with('my_database', 'host')
    mocked_config.get.assert_called_once_with('my_database', 'port')
    mocked_config.get.assert_called_once_with('my_database', 'user')
    mocked_config.get.assert_called_once_with('my_database', 'password')
    mocked_connect.assert_called_once_with(
        host='some_value',
        port='some_value',
        user='some_value',
        password='some_value',
        database='my_database',
    )


def test_get_cursor():
    # Set up a mock connection object
    conn_mock = MagicMock()

    # Set up a mock cursor object
    cursor_mock = MagicMock()
    conn_mock.cursor.return_value = cursor_mock

    with patch('connect', return_value=conn_mock):
        cursor = get_cursor()

    # Ensure that the cursor was obtained from the connection object
    conn_mock.cursor.assert_called_once_with()

    # Ensure that the cursor is returned
    assert cursor is cursor_mock


@patch('mysql.connector.connect')
def test_check_database_exists(mock_connect):
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value = mock_cursor

    # Mock the execute method of the cursor
    mock_cursor.execute.return_value = None

    # Call the function with a database name that exists using mock
    exists = check_database_exists(mock_connect, 'testdb')

    # Assert that the connect and cursor methods were called with the correct arguments
    mock_connect.assert_called_once_with(
        host='localhost',
        port=3306,
        user='testuser',
        password='testpass'
    )
    mock_connect.return_value.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'testdb'")

    # Assert that the function returned True since the database exists
    assert exists is True

    # Call the function with a database name that does not exist
    mock_cursor.execute.side_effect = mysql.connector.Error()
    exists = check_database_exists(mock_connect, 'nonexistentdb')

    # Assert that the connect and cursor methods were called with the correct arguments
    mock_connect.assert_called_with(
        host='localhost',
        port=3306,
        user='testuser',
        password='testpass'
    )
    mock_connect.return_value.cursor.assert_called_with()
    mock_cursor.execute.assert_called_with("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'nonexistentdb'")

    # Assert that the function returned False since the database does not exist
    assert exists is False

@patch('mysql.connector.connect')
def test_check_table_exists(mocked_connect):
    mocked_cursor = MagicMock()
    mocked_connect.return_value.cursor.return_value = mocked_cursor

    # Mock the execute method of the cursor
    mocked_cursor.execute.return_value = None

    # Call the function with a table name that exists using mock
    exists = check_table_exists('test_table', mocked_connect)

    # Assert that the connect and cursor methods were called with the correct arguments
    mocked_connect.assert_called_once_with(database='my_database')
    mocked_connect.return_value.cursor.assert_called_once()
    mocked_cursor.execute.assert_called_once_with("SHOW TABLES LIKE 'test_table'")

    # Assert that the function returned True since the table exists
    assert exists is True

    # Call the function with a table name that does not exist
    mocked_cursor.execute.side_effect = mysql.connector.Error()
    exists = check_table_exists('nonexistent_table', mocked_connect)

    # Assert that the connect and cursor methods were called with the correct arguments
    mocked_connect.assert_called_with(database='my_database')
    mocked_connect.return_value.cursor.assert_called_with()
    mocked_cursor.execute.assert_called_with("SHOW TABLES LIKE 'nonexistent_table'")

    # Assert that the function returned False since the table does not exist
    assert exists is False




def test_describe_table(self):
    # Create a mock cursor object
    cursor = Mock()

    # Call the function with the mock cursor object
    describe_table(None, "users", None, cursor)

    # Check that the execute method was called with the correct SQL query
    cursor.execute.assert_called_once_with(
        "DESCRIBE users"
    )

    # Create a mock cursor object
    cursor = Mock()

    # Call the function with the mock cursor object and a non-existent table name
    with self.assertRaises(Exception):
        describe_table(None, "nonexistent_table", None, cursor)

    # Check that the execute method was not called
    cursor.execute.assert_not_called()

    # Create a mock cursor object
    cursor = Mock()

    # Create a mock description object
    description = [("id", "int", "NO", "PRI", None, ""),
                   ("name", "varchar(255)", "NO", "", None, ""),
                   ("email", "varchar(255)", "NO", "UNI", None, ""),
                   ("created_at", "timestamp", "NO", "", "CURRENT_TIMESTAMP", "")]

    # Set the return value of the fetchall method to the mock description object
    cursor.fetchall.return_value = description

    # Call the function with the mock cursor object
    result = describe_table(None, "users", None, cursor)

    # Check that the result matches the mock description object
    self.assertEqual(result, description)



class TestAddNewColumnToTable:
    def test_add_new_column_to_table(self):
        # Create a mock cursor object
        cursor = Mock()

        # Call the function with the mock cursor object
        add_new_column_to_table(None, "users", "new_column INT", None, cursor)

        # Check that the execute method was called with the correct SQL query
        cursor.execute.assert_called_once_with("ALTER TABLE users ADD COLUMN new_column INT")

    def test_add_new_column_to_table_with_database(self):
        # Create a mock cursor object
        cursor = Mock()

        # Call the function with the mock cursor object
        add_new_column_to_table(None, "users", "new_column INT", "my_database", cursor)

        # Check that the execute method was called with the correct SQL query
        cursor.execute.assert_called_once_with("ALTER TABLE my_database.users ADD COLUMN new_column INT")

    def test_add_new_column_to_table_error(self):
        # Create a mock cursor object that raises an exception
        cursor = Mock()
        cursor.execute.side_effect = mysql.connector.Error()

        # Call the function with the mock cursor object, and ensure it raises an exception
        with pytest.raises(Exception):
            add_new_column_to_table(None, "users", "new_column INT", None, cursor)




class TestDBHelper(unittest.TestCase):

    def test_create_table(self):
        with patch('mysql.connector.connect') as mock_connect:
            with patch('mysql.connector.cursor') as mock_cursor:
                cursor = MagicMock()
                mock_cursor.return_value = cursor
                create_table(None, 'users', ['id INTEGER', 'name TEXT'])
                cursor.execute.assert_called_with('CREATE TABLE users (id INTEGER, name TEXT)')

    def test_create_table_if_not_exists(self):
        with patch('mysql.connector.connect') as mock_connect:
            with patch('mysql.connector.cursor') as mock_cursor:
                cursor = MagicMock()
                mock_cursor.return_value = cursor
                create_table_if_not_exists(None, 'users', ['id INTEGER', 'name TEXT'])
                cursor.execute.assert_called_with('CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)')





## Test the connect function
#def test_connect():
#
#    # Test with no database given
#    with patch.object(mysql.connector, 'connect', return_value=MagicMock()) as mock_connect:
#        with patch.object(db.config, 'get', return_value='testdb') as mock_config:
#            db.connect()
#            mock_config.assert_called_with('chaindb', 'database')
#        mock_connect.assert_called_with(
#            host=db.config.get('testdb', 'host'),
#            port=db.config.get('testdb', 'port'),
#            user=db.config.get('testdb', 'user'),
#            password=db.config.get('testdb', 'password'),
#            database='testdb'
#        )
#
#    # Test with database given
#    with patch.object(mysql.connector, 'connect', return_value=MagicMock()) as mock_connect:
#        db.connect('testdb')
#        mock_connect.assert_called_with(
#            host=db.config.get('testdb', 'host'),
#            port=db.config.get('testdb', 'port'),
#            user=db.config.get('testdb', 'user'),
#            password=db.config.get('testdb', 'password'),
#            database='testdb'
#        )
#
#    # Test for exception handling
#    with pytest.raises(mysql.connector.Error):
#        with patch.object(mysql.connector, 'connect', side_effect=mysql.connector.Error()) as mock_connect:
#            db.connect('testdb')
#            mock_connect.assert_called_with(
#                host=db.config.get('testdb', 'host'),
#                port=db.config.get('testdb', 'port'),
#                user=db.config.get('testdb', 'user'),
#                password=db.config.get('testdb', 'password'),
#                database='testdb'
#            )
#
## Test the get_cursor function
#def test_get_cursor():
#
#    # Test with a valid connection
#    connection = MagicMock()
#    with patch.object(connection, 'cursor', return_value=Mock()) as mock_cursor:
#        db.get_cursor(connection)
#        mock_cursor.assert_called_with(buffered=True)
#
#    # Test for exception handling
#    with pytest.raises(Exception):
#        connection = MagicMock(json=Mock(return_value={'error': 'test error'}))
#        with patch.object(connection, 'cursor', side_effect=mysql.connector.Error()) as mock_cursor:
#            db.get_cursor(connection)
#
## Test the check_database_exists function
#def test_check_database_exists():
#    # Test with a valid database
#    connection = MagicMock()
#    cursor = MagicMock()
#    cursor.fetchall.return_value = [('testdb',)]
#    assert db.check_database_exists(connection, 'testdb', cursor) is True
#    cursor.execute.assert_called_with('SHOW DATABASES')
#
#    # Test with an invalid database
#    cursor.fetchall.return_value = [('otherdb',)]
#    assert db.check_database_exists(connection, 'testdb', cursor) is False
#
#    # Test with no cursor given
#    with patch.object(db, 'get_cursor', return_value=Mock()) as mock_get_cursor:
#        with patch.object(connection, 'cursor', return_value=cursor) as mock_cursor:
#            with patch.object(cursor, 'execute', side_effect=mysql.connector.Error()) as mock_execute:
#                with pytest.raises(mysql.connector.Error):
#                    db.check_database_exists(connection, 'testdb')
#                    mock_get_cursor.assert_called_once_with(connection)
#

"""
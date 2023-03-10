# test each database funciton from the ./dbhelper.py file
# run this file with: python3 -m unittest database_test.py
# or: python3 -m unittest discover -s . -p "database_test.py"

import src
from src import db, config

from src.db import dbhelper



# Test the connect function and open a connections to the database
connection = dbhelper.connect('pricedb')
cursor = dbhelper.get_cursor(connection)

db_check = dbhelper.check_database_exists(connection, 'address_report1', cursor)
print(db_check)


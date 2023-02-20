import sys
import os

# Add the path to the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you should be able to import the modules from the project
from qrl_chain_scrape import config
from chainfunctions.block import get_chain_height

height = get_chain_height()

print(f'height: {height}') # height: 0
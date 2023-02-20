from qrl_chain_scrape import config
from chainfunctions.block import get_chain_height

height = get_chain_height()

print(f'height: {height}') # height: 0
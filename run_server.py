import argparse
import numpy as np
from server import *
from game import Game


parser = argparse.ArgumentParser(description =
                    ''' 
                        Multi agent war simulation
                    ''')

parser.add_argument("port", type = int, help = "enter a valid port for the server to listen to")
parser.add_argument("--grid_size", type = int, default = 100, help = "grid size (must be an integer)")
parser.add_argument("--num_agents", type = int, default = 200, help = "number of agents in each team")
parser.add_argument("--num_teams", type = int, default = 2, help = "number of teams")
parser.add_argument("--num_episodes", type = int, default = 20, help = "number of episodes")

args = parser.parse_args()

start_server(port = args.port, grid_size = args.grid_size, 
                num_agents = args.num_agents, num_teams = args.num_teams,
                num_episodes = args.num_episodes)
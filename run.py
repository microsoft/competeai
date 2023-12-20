from SocioSim.simul import Simulation

import os
import yaml
import argparse

# parse the argument
parser = argparse.ArgumentParser()
parser.add_argument('name', type=str)
args = parser.parse_args()

# create a log folder
log_path = f"./logs/{args.name}"
if not os.path.exists(log_path):
    os.makedirs(log_path)

config_path = os.path.join('SocioSim', 'examples', 'restaurant.yaml')

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)
    config['log_path'] = log_path
    Simul = Simulation.from_config(config)
    Simul.run()
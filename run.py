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
# if exist, delete it
if os.path.exists(log_path):
    os.system(f"rm -rf {log_path}")
if not os.path.exists(log_path):
    os.makedirs(log_path)

config_path = os.path.join('SocioSim', 'examples', 'group.yaml')
relationship_path = os.path.join('SocioSim', 'relationship.yaml')

with open(relationship_path, 'r') as f:
    relationship = yaml.safe_load(f)

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)
    config['exp_name'] = args.name
    config['relationship'] = relationship
    Simul = Simulation.from_config(config)
    Simul.run()
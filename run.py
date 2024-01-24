"""
    Pipeline for running the simulation.
"""
from SocioSim.simul import Simulation
from SocioSim.utils import analysis, aggregate

import os
import yaml
import argparse

# parse the argument
parser = argparse.ArgumentParser()
parser.add_argument('name', type=str)
args = parser.parse_args()

# create a log folder
log_path = f"./logs/{args.name}"

# if not os.path.exists(log_path):
#     os.makedirs(log_path)
#     os.makedirs(f"{log_path}/fig")

# config_path = os.path.join('SocioSim', 'examples', 'group_v2.yaml')
# relationship_path = os.path.join('SocioSim', 'relationship.yaml')

# with open(relationship_path, 'r') as f:
#     relationship = yaml.safe_load(f)

# with open(config_path, 'r') as f:
#     config = yaml.safe_load(f)
#     config['exp_name'] = args.name
#     config['relationship'] = {}  # FIXME
#     Simul = Simulation.from_config(config)
#     Simul.run()
    
# # analysis the data
# aggregate('./logs', field='similar_proportion' )

analysis(log_path, field='customer_flow_with_annotation')



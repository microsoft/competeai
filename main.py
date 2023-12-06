from dataclasses import dataclass

import os
import yaml

@dataclass
class Step:
    agent_name: str
    task_name: str

# TODO: unify the config process
class Process:
    # read the steps from config file and build topology of the process
    def __init__(self, config):
        self.config = config
        self.steps = []
        self.curr_step = 0
        self.is_parerllel = False

    def get_process(self, name):
        with open('./config/competition.yaml', 'r') as file:
            data = yaml.safe_load(file)
        
    
    def get_next_step(self):
        pass
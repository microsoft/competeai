from typing import List

from ..config import Configurable
from ..message import Message, MessagePool
from ..agent import Player
from ..utils import PromptTemplate, get_data_from_database, \
                    send_data_to_database, PORT_MAP

import pandas as pd
import json


class Scene(Configurable):
    
    type_name = "scene"
    
    def __init__(self, message_pool: MessagePool, players: List[Player], **kwargs):
        """
        Initialize a scene
        
        Parameters:
            message_pool (MessagePool): The message pool for the scene
            players (List[Player]): The players in the scene
        """
        super().__init__(message_pool=message_pool, players=players, **kwargs)
        # All scenes share a common message pool, prompt assembler and output parser
        self.message_pool = message_pool
        self.players = players
        self.num_of_players = len(players)

        self.invalid_step_retry = 3
        
        self._curr_player_idx = 0
        self._curr_process_idx = 0
    
    # TODO: 根据需求组装更复杂的prompt
    def add_new_prompt(self, player_name, scene_name, step_name):
        # If the prompt template exists, render it and add it to the message pool
        if PromptTemplate([scene_name, step_name]).content:
            data = get_data_from_database(step_name, PORT_MAP['player_name'])
            prompt_template = PromptTemplate([scene_name, step_name])
            prompt = prompt_template.render(data=data)
            # convert str:prompt to Message:prompt
            turn = self.message_pool.last_message.turn + 1  # TODO: parallel run will confuse this?
            message = Message(agent_name=player_name, content=prompt, visible_to=player_name, turn=turn)
            self.message_pool.append(message)
    
    def parse_output(self, player_name, output, to_db):  
        if to_db:
            send_data_to_database(data=output, agent_name=player_name)
        
        # TODO: short output
        message = Message(agent_name='System', 
                          content=output, 
                          visible_to=player_name, 
                          turn=self.message_pool.last_message.turn + 1)
        self.message_pool.append_message(message)
    
    def log_table(self, data, column_name):
        # Try to read the CSV file if it exists, else create an empty DataFrame
        csv_file = f'{self.log_file}.csv'  # TODO: log_file
        try:
            df = pd.read_csv(csv_file)
        except FileNotFoundError:
            df = pd.DataFrame()

        # Check if the 'name' column exists in the DataFrame
        if 'name' not in df.columns:
            df['name'] = data.keys()
            df[column_name] = data.values()
        else:
            # Ensure the order of 'name' in the DataFrame and the data are the same
            # This assumes that the 'name' values in data are already present in the DataFrame
            ordered_values = [data[name] for name in df['name']]
            df[column_name] = ordered_values

        # Print the table and save it to CSV
        print(df)
        df.to_csv(csv_file, index=False)
    
    def is_terminal(self):
        pass
    
    def get_curr_player(self):
        return self.player[self._curr_player_idx]
    
    def get_curr_process(self):
        return self.processes[self._curr_process_idx]
        
    def step(self):
        pass

    def run(self):
        """
        Main function, automatically assemble input and parse output to run the scene
        """
        while not self.is_terminal():
            self.step()
        
        self.final_actions()
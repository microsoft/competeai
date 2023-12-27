from typing import List

from ..config import Configurable
from ..message import Message, MessagePool
from ..agent import Player
from ..utils import PromptTemplate, get_data_from_database, \
                    send_data_to_database, NAME2PORT, DELIMITER

import json


class Scene(Configurable):
    def __init__(self, players: List[Player], id: int, type_name: str, log_path: str, **kwargs):
        """
        Initialize a scene
        
        Parameters:
            message_pool (MessagePool): The message pool for the scene
            players (List[Player]): The players in the scene
        """
        super().__init__(players=players, id=id, type_name=type_name, **kwargs)
        # All scenes share a common message pool, prompt assembler and output parser
        self.id = id
        self.players = players
        
        self.log_path = f'{log_path}/{self.type_name}_{self.id}'
        self.message_pool = MessagePool(log_path=self.log_path)
        
        self.num_of_players = len(players)
        self.invalid_step_retry = 3
        
        self._curr_turn = 0  # for message turn
        self._curr_player_idx = 0
        self._curr_process_idx = 0
    
    # TODO: 根据需求组装更复杂的prompt
    def add_new_prompt(self, player_name, scene_name=None, step_name=None, data=None, from_db=False):
        # If the prompt template exists, render it and add it to the message pool
        prompt = None
        if scene_name and step_name:
            if PromptTemplate([scene_name, step_name]).content:
                prompt_template = PromptTemplate([scene_name, step_name])
                if from_db:
                    data = get_data_from_database(step_name, NAME2PORT[player_name])
                prompt = prompt_template.render(data=data)
        elif isinstance(data, str) and data != "None":
            prompt = data
        else:
            raise ValueError("Prompt not found")
            
        # convert str:prompt to Message:prompt
        message = Message(agent_name='System', content=prompt, 
                            visible_to=player_name, turn=self._curr_turn)
        self.message_pool.append_message(message)
    
    def parse_output(self, output, player_name, step_name, to_db=False):  
        if to_db and output != "None":  # TODO: better code
            send_data_to_database(output, step_name, NAME2PORT[player_name])
            
        def shorten_text(text):
            delimiter_idx = text.find(DELIMITER)
            if delimiter_idx != -1:
                return text[:delimiter_idx].strip()
            else:
                return text
        # The previous message to the player may have some format details, we need to remove it
        last_message = self.message_pool.get_last_message_system_to_player(player_name)
        if last_message:
            last_message.content = shorten_text(last_message.content)
            
        message = Message(agent_name=player_name, content=output, 
                            visible_to=player_name, turn=self._curr_turn)
        self.message_pool.append_message(message)
        
        try:
            parsed_ouput = json.loads(output)
            return parsed_ouput
        except:
            return None
    
    @classmethod
    def action_for_next_scene(self, data):
        return
            
    
    def is_terminal(self):
        pass
    
    def terminal_action(self):
        pass
    
    def get_curr_player(self):
        return self.players[self._curr_player_idx]
    
    def get_curr_process(self):
        return self.processes[self._curr_process_idx]
        
    def step(self, data=None):
        pass

    def run(self, previous_scene_data=None):
        """
        Main function, automatically assemble input and parse output to run the scene
        """
        # data can from previous scene or previous process
        data = previous_scene_data
        while not self.is_terminal():
            data = self.step(data)
        
        self.terminal_action()
        
        return data
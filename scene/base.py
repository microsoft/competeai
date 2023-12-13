from typing import List

from ..config import Configurable
from ..message import MessagePool
from ..agent import Player
from ..utils import *

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
        # TODO 这两个解析器应该在哪里实现？以及如何初始化
        self.prompt_assembler = None
        self.output_parser = None

        self.invalid_step_retry = 3
        
        self._curr_player_idx = 0
        self._curr_process_idx = 0
        
    def get_curr_player(self):
        return self.player[self._curr_player_idx]
    
    def get_curr_process(self):
        return self.processes[self._curr_process_idx]
        
    def step(self):
        curr_process = self.get_curr_process()
        curr_player = self.get_curr_player()

        # TODO: invalid step retry
        prompts = self.prompt_assembler.prompt_assemble(curr_player, self.name, curr_process['name'])
        output = curr_player(prompts)
        self.output_parser.parse(curr_player, output)
        
        self._curr_player_idx += 1
        # need customize the get next process function
        
        is_terminal = False
        return is_terminal

    def run(self):
        """
        Main function, automatically assemble input and parse output to run the scene
        """
        while self.step():
            pass
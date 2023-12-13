from base import Scene
from interface_database import *
from ..agent import Agent
from ..utils import *

 
processes = [
    {"name": "daybook", "from_db": True, "to_db": False},
    {"name": "rule", "from_db": True, "to_db": False},
    {"name": "basic_info", "from_db": True, "to_db": True},
    {"name": "menu", "from_db": True, "to_db": True},
    {"name": "chef", "from_db": True, "to_db": True},
    {"name": "ads", "from_db": True, "to_db": True},
]

class RestaurantDesign(Scene):
    def __init__(self):
        super().__init__()
        self.processes = processes
        self._curr_process_idx = 0
        
        self.player_names = []
        self._curr_player_idx = 0
        
    
    def get_curr_player(self):
        return self.player_names[self._curr_player_idx]
    
    def get_curr_process(self):
        return self.processes[self._curr_process_idx]
        
    # interactive step design
    def step(self):
        curr_process = self.get_curr_process()
        curr_player = self.get_curr_player()

        # TODO: invalid step retry
        prompts = self.prompt_assembler.prompt_assemble(curr_player, self.name, curr_process['name'])
        output = curr_player(prompts)
        self.output_parser.parse(curr_player, output)

        
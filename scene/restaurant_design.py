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
    
    type_name = "restaurant_design"
    
    def __init__(self, message_pool, players, **kwargs):
        super().__init__(message_pool=message_pool, players=players, **kwargs)
        self.processes = processes
        self.prompt_assembler = PromptAssembler(message_pool)
        self.output_parser = OutputParser()
        
    def step(self):
        curr_process = self.get_curr_process()
        curr_player = self.get_curr_player()

        # TODO: invalid step 
        prompts = self.prompt_assembler.prompt_assemble(curr_player, self.type_name, curr_process['name'])
        output = curr_player(prompts)
        self.output_parser.parse(curr_player, output)

        
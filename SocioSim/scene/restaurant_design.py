from typing import List
from .base import Scene
from ..agent import Player
from ..utils import PORT_MAP, BASE_PORT, get_data_from_database

 
processes = [
    {"name": "daybook", "from_db": True, "to_db": False},
    {"name": "rule", "from_db": False, "to_db": False},
    {"name": "basic_info", "from_db": True, "to_db": True},
    {"name": "menu", "from_db": True, "to_db": True},
    {"name": "chef", "from_db": True, "to_db": True},
    {"name": "ads", "from_db": True, "to_db": True},  # bug
]


class RestaurantDesign(Scene):
    
    type_name = "restaurant_design"
    
    def __init__(self, players: List[Player], id: int, log_path: str, **kwargs):
        super().__init__(players=players, id=id, log_path=log_path,  
                                type_name=self.type_name, **kwargs)
        self.processes = processes
        
        self.port = BASE_PORT + id
        self.day = 0
        
        for player in players:
            PORT_MAP[player.name] = self.port
    
    def is_terminal(self):
        return self._curr_process_idx == len(self.processes)
    
    def terminal_action(self):
        basic_info = get_data_from_database("basic_info", self.port)
        restaurant_name = basic_info[0]["name"]
        PORT_MAP[restaurant_name] = self.port
        
    def move_to_next_player(self):
        self._curr_player_idx = 0  # In restaurant design, only one player
    
    def move_to_next_process(self):
        self._curr_process_idx += 1
    
    # function: prepare the config: player, process for next step
    # more complex process and player sequence
    def prepare_for_next_step(self):
        self.move_to_next_player()
        self.move_to_next_process()
        self._curr_turn += 1
    
    def step(self):
        curr_process = self.get_curr_process()
        curr_player = self.get_curr_player()
        
        if not (curr_process['name'] == 'daybook' and self.day == 0):
            # LLM can not simulate the whole process automatically, it needs prompt to guide
            self.add_new_prompt(player_name=curr_player.name, 
                                scene_name=self.type_name, 
                                step_name=curr_process['name'], 
                                from_db=curr_process['from_db'])

        observation = self.message_pool.get_visible_messages(agent_name=curr_player.name, turn=self._curr_turn)
        
        for i in range(self.invalid_step_retry):
            try:
                output = curr_player(observation)
                break
            except Exception as e:
                print(f"Attempt {i + 1} failed with error: {e}")
        else:
            raise Exception("Invalid step retry arrived at maximum.")
        
        self.parse_output(output, curr_player.name, curr_process['name'], curr_process['to_db'])
        self.prepare_for_next_step()
        
        

        
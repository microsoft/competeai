from typing import List
from .base import Scene
from ..agent import Player
from ..globals import NAME2PORT, PORT2NAME, BASE_PORT
from ..utils import PromptTemplate, get_data_from_database, log_table
                     
 
processes = [
    {"name": "daybook", "from_db": False, "to_db": False},
    {"name": "rule", "from_db": False, "to_db": False},
    {"name": "basic_info", "from_db": True, "to_db": True},
    {"name": "menu", "from_db": True, "to_db": True},
    {"name": "chef", "from_db": True, "to_db": True},
    {"name": "ads", "from_db": True, "to_db": True},
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
            NAME2PORT[player.name] = self.port
    
    def is_terminal(self):
        return self._curr_process_idx == len(self.processes)
    
    def terminal_action(self):
        basic_info = get_data_from_database("basic_info", self.port)
        restaurant_name = basic_info[0]["name"]
        NAME2PORT[restaurant_name] = self.port
        PORT2NAME[self.port] = restaurant_name
        self.day += 1
        self._curr_process_idx = 0
    
    @classmethod
    def action_for_next_scene(cls, data=None):
        ports = set(NAME2PORT.values())
        res = {}
        for port in ports:
            data = get_data_from_database("show", port=port)
            restaurant = data["name"]
            data = data.values()
            today_offering = PromptTemplate([cls.type_name, "today_offering"]).render(data=data)
            dish_score = get_data_from_database("score", port=port)
            res[restaurant] = {"today_offering": today_offering, "dish_score": dish_score}
        
        return res
        
    def move_to_next_player(self):
        self._curr_player_idx = 0  # In restaurant design, only one player
    
    def move_to_next_process(self):
        self._curr_process_idx += 1
    
    def prepare_for_next_step(self):
        self.move_to_next_player()
        self.move_to_next_process()
        self._curr_turn += 1
    
    def step(self, input=None):
        curr_process = self.get_curr_process()
        curr_player = self.get_curr_player()
        
        if curr_process['name'] == 'daybook' and self.day == 0:
            pass
        elif curr_process['name'] == 'daybook' and self.day != 0:
            daybook = get_data_from_database("daybook", port=self.port)
            daybook = daybook[self.day-1]
            rival_info = daybook["rival_info"]
            daybook = {k: v for k, v in daybook.items() if k != "rival_info"}
            comment = get_data_from_database("last_comment", port=self.port)
            data = [self.day, daybook, comment, rival_info] 
            self.add_new_prompt(player_name=curr_player.name, 
                                scene_name=self.type_name, 
                                step_name=curr_process['name'], 
                                data=data)
            log_table(self.log_file, daybook, f"day{self.day}") # log
        else:
            self.add_new_prompt(player_name=curr_player.name, 
                                scene_name=self.type_name, 
                                step_name=curr_process['name'], 
                                from_db=curr_process['from_db'])
        # text observation
        observation_text = self.message_pool.get_visible_messages(agent_name=curr_player.name, turn=self._curr_turn)
        # vision observation
        observation_vision = None # TODO
        
        for i in range(self.invalid_step_retry):
            try:
                output = curr_player(observation_text, observation_vision)
                break
            except Exception as e:
                print(f"Attempt {i + 1} failed with error: {e}")
        else:
            raise Exception("Invalid step retry arrived at maximum.")
        
        self.parse_output(output, curr_player.name, curr_process['name'], curr_process['to_db'])
        self.prepare_for_next_step()
        
        return
        
        

        
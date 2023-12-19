from .base import Scene
from ..utils import PORT_MAP, get_data_from_database

 
processes = [
    {"name": "daybook", "from_db": True, "to_db": False},
    {"name": "rule", "from_db": True, "to_db": False},
    {"name": "basic_info", "from_db": True, "to_db": True},
    {"name": "menu", "from_db": True, "to_db": True},
    {"name": "chef", "from_db": True, "to_db": True},
    {"name": "ads", "from_db": True, "to_db": True},
]

# TODO：明天上午的目标：成功运行restaurant_design

class RestaurantDesign(Scene):
    
    type_name = "restaurant_design"
    
    def __init__(self, message_pool, players, **kwargs):
        super().__init__(message_pool=message_pool, players=players, **kwargs)
        self.processes = processes
        self.port = PORT_MAP[self.players[0].name]
        self.day = 0
    
    def is_terminal(self):
        return self._curr_process_idx == len(self.processes)
    
    def terminal_action(self):
        basic_info = get_data_from_database("basic_info")
        restaurant_name = basic_info[0]["name"]
        PORT_MAP[restaurant_name] = self.port
    
    def step(self):
        curr_process = self.get_curr_process()
        curr_player = self.get_curr_player()
        
        if curr_process['name'] == 'daybook' and self.day == 0:
            pass
        else:
            # LLM can not simulate the whole process automatically, it needs prompt to guide
            self.add_new_prompt(curr_player.name, self.type_name, curr_process['name'])

        observation = self.message_pool.get_visible_messages(agent_name=curr_player.name)
        
        for i in range(self.invalid_step_retry):
            try:
                output = curr_player(observation)
                break
            except Exception as e:
                print(f"Attempt {i + 1} failed with error: {e}")
        else:
            raise Exception("Invalid step retry arrived at maximum.")
        
        self.parse_output(curr_player, output, curr_process['to_db'])
        
        # TODO: more complex process and player sequence
        self._curr_process_idx += 1
        self._curr_player_idx = (self._curr_player_idx + 1) % self.num_of_players
        

        
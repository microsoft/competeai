from typing import List
from .base import Scene
from ..agent import Player
from ..message import MessagePool
from ..image import Image
from ..globals import NAME2PORT, PORT2NAME, BASE_PORT, image_pool
from ..utils import PromptTemplate, get_data_from_database, \
                    log_table, combine_images, convert_img_to_base64
   
import os                  
 
EXP_NAME = None
 
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
    
    def __init__(self, players: List[Player], id: int, exp_name: str, **kwargs):
        super().__init__(players=players, id=id, type_name=self.type_name, **kwargs)
        global EXP_NAME
        EXP_NAME = exp_name
        
        self.processes = processes
        self.port = BASE_PORT + id
        
        self.log_path = f"./logs/{exp_name}/{self.type_name}_{self.port}"
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
            
        self.message_pool = MessagePool(log_path=f'{self.log_path}/message')
        
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
            menu = data["menu"]
            restaurant = data["name"]
            today_offering = PromptTemplate([cls.type_name, "today_offering"]).render(data=data.values())
            dish_score = get_data_from_database("score", port=port)
            res[restaurant] = {"today_offering": today_offering, "dish_score": dish_score}
            
            # Menu image
            dish_ids = [d["id"] for d in menu]
            folder_path = f"./logs/{EXP_NAME}/{cls.type_name}_{port}"
            img_paths = [f"{folder_path}/menu_{id}.png" for id in dish_ids]
            img_base64_menu = combine_images(input_paths=img_paths, output_path=f"{folder_path}/menu.png")
            img_menu = Image(owner=restaurant, content=img_base64_menu, description="menu")
            image_pool.append_image(img_menu)
            # Restaurant image
            img_base64_r = convert_img_to_base64(f"{folder_path}/basic_info_1.png")
            img_r = Image(owner=restaurant, content=img_base64_r, description="basic_info")
            image_pool.append_image(img_r)
            
            image_pool.print()
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
            log_table(f'{self.log_path}/data', daybook, f"day{self.day}") # log
        else:
            self.add_new_prompt(player_name=curr_player.name, 
                                scene_name=self.type_name, 
                                step_name=curr_process['name'], 
                                from_db=curr_process['from_db'])
        # text observation
        observation_text = self.message_pool.get_visible_messages(agent_name=curr_player.name, turn=self._curr_turn)
        # vision observation
        r_name = PORT2NAME[self.port] if self.port in PORT2NAME else None
        observation_vision = image_pool.get_visible_images(restaurant_name=r_name, step_name=curr_process['name'])
        
        for i in range(self.invalid_step_retry):
            try:
                output = curr_player(observation_text, observation_vision)
                self.parse_output(output, curr_player.name, curr_process['name'], curr_process['to_db'])
                break
            except Exception as e:
                print(f"Attempt {i + 1} failed with error: {e}")
        else:
            raise Exception("Invalid step retry arrived at maximum.")
        
        self.prepare_for_next_step()
        
        return
        
        

        
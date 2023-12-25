from typing import List
from .base import Stage
from ..agent import Player

 
processes = [
    {"name": "order", "from_db": False, "to_db": False},
    {"name": "comment", "from_db": False, "to_db": False},
]

class Dine(Stage):
    
    type_name = "dine"
    
    def __init__(self, players: List[Player], id: int, log_path: str, **kwargs):
        super().__init__(players=players, id=id, log_path=log_path,  
                                type_name=self.type_name, **kwargs)
        self.processes = processes
        
        self.day = 1
    
    def is_terminal(self):
        return self._curr_process_idx == len(self.processes)
    
    def move_to_next_player(self):
        self._curr_player_idx = 0  # In restaurant design, only one player
    
    def move_to_next_process(self):
        self._curr_process_idx += 1
    
    def prepare_for_next_step(self):
        self.move_to_next_player()
        self.move_to_next_process()
        self._curr_turn += 1
    
    # interactive step design
    def step(self, input=None):
        curr_player = self.get_curr_player()
        curr_process = self.get_curr_process()
        output = None
        
        # pre-process
        if curr_process['name'] == 'order':
            for k in input.keys():
                # add all today offerings to message pool
                self.add_new_prompt(player_name=curr_player.name, 
                                scene_name=self.type_name, 
                                step_name=curr_process['name'], 
                                data=input[k]['today_offering'])
            # add order prompt
            self.add_new_prompt(player_name=curr_player.name, 
                                scene_name=self.type_name, 
                                step_name=curr_process['name'], 
                                from_db=curr_process['from_db'])
        elif curr_process['name'] == 'comment':
            # add dish score and comment prompt
            self.add_new_prompt(player_name=curr_player.name,
                                scene_name=self.type_name,
                                step_name=curr_process['name'],
                                data=input)

        observation = self.message_pool.get_visible_messages(agent_name=curr_player.name, turn=self._curr_turn)
        
        for i in range(self.invalid_step_retry):
            try:
                output = curr_player(observation)
                parsed_ouput = self.parse_output(output, curr_player.name, curr_process['name'], curr_process['to_db'])
                break
            except Exception as e:
                print(f"Attempt {i + 1} failed with error: {e}")
        else:
            raise Exception("Invalid step retry arrived at maximum.")
        
        # post-process
        if curr_process['name'] == 'order':
            restaurant = parsed_ouput['restaurant_name']
            dishes = parsed_ouput['dishes']
            dish_score = input[restaurant]['dish_score']
            
            prompt = ''
            for dish in dishes:
                # check if the dish is in the restaurant
                if dish in dish_score[restaurant].keys():
                    score = dish_score[restaurant][dish]
                    prompt += f"\n{dish}: {score}"
                output = prompt
                
        self.prepare_for_next_step()
        
        return output
        
        
        
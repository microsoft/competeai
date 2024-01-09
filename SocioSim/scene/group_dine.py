from typing import List
from .base import Scene
from ..agent import Player
from ..message import MessagePool
from ..globals import NAME2PORT, PORT2NAME, image_pool
from ..utils import log_table, get_data_from_database, send_data_to_database

import numpy as np
     
EXP_NAME = None

# 增加一轮让每个人内心先做一个选择？
processes = [
    {"name": "group_order", "from_db": False, "to_db": False},
    {"name": "group_comment", "from_db": False, "to_db": False},
]

class GroupDine(Scene):
    
    type_name = "group_dine"
    
    def __init__(self, players: List[Player], id: int, exp_name: str, **kwargs):
        super().__init__(players=players, id=id, type_name=self.type_name, **kwargs)
        
        global EXP_NAME
        EXP_NAME = exp_name
        
        self.processes = processes
        self.log_path = f"./logs/{exp_name}/{self.type_name}_{id}"
        self.message_pool = MessagePool(log_path=self.log_path)
        
        self.day = 1
        self.dishes = None
        self.process_start = True # a flag to indicate adding new prompt
        self.process_end = False  # a flag to indicate move to next process
    
    @classmethod
    def action_for_next_scene(cls, data):
        restaurant_list = []
        daybooks = {}
        comments = {}
        num_of_customer = {}
        infos = {}
        rival_infos = {}
        customer_choice = {}

        for value in PORT2NAME.values():
            restaurant_list.append(value)
            comments[value] = []
            daybooks[value] = {}
            num_of_customer[value] = 0
            infos[value] = ''
            rival_infos[value] = ''
            
        for d in data:
            agent_name = next(iter(d))
            d = d[agent_name]
            day = d["day"]
            r_name = d["restaurant"]
            
            # record customer choice
            customer_choice[agent_name] = r_name
            
            # construct comment
            if "comment" in d:
                comment = {"day": day, "name": agent_name, "score": d["score"], "content":  d["comment"]}
                comments[r_name].append({"type": "add", "data": comment})
                
            # construct daybook
            dishes = d["dishes"]
            num_of_customer[r_name] += 1
            for dish in dishes:
                if not dish in daybooks[r_name]:
                    daybooks[r_name][dish] = 0
                daybooks[r_name][dish] += 1
                
        # log customer choice
        log_path = f'./logs/{EXP_NAME}/{cls.type_name}'  # FIXME
        log_table(log_path, customer_choice, f"day{day}")

        for key in comments:
            send_data_to_database(comments[key], "comment", port=NAME2PORT[key])
        
        # construct whole daybook  
        for r_name in restaurant_list:
            show = get_data_from_database("show", port=NAME2PORT[r_name])
            info = f"Restaurant: {r_name} \nNumber of customers: {num_of_customer[r_name]}\n Customer Comments: {show['comment']} \nMenu: {show['menu']}\n "
            infos[r_name] = info
        
        for key in daybooks:
            for r_name in restaurant_list:
                if r_name != key:
                    rival_infos[key] += infos[r_name]
            daybook = {"dishes": daybooks[key], "num_of_customer": num_of_customer[key], "rival_info": rival_infos[key]}
            
            print(f'debugging-daybook: {daybook}')
            
            daybooks[key] = {"type": "add", "data": daybook}

        # send comments and daybooks to database
        for key in daybooks:
            send_data_to_database(daybooks[key], "daybook", port=NAME2PORT[key])
        
        return
        
    def is_terminal(self):
        return self._curr_process_idx == len(self.processes)

    def terminal_action(self):
        # message pool 只留最后一个
        summary = self.message_pool.last_message
        summary.content = f"Day{self.day} experience: {summary.content}"
        self.message_pool.compress_last_turn(summary)
        
        self.day += 1
        self._curr_turn += 1
        self._curr_process_idx = 0
        self.group_chosen = False
    
    def move_to_next_player(self):
        self._curr_player_idx = (self._curr_player_idx + 1) % self.num_of_players

    def move_to_next_process(self):
        # In group order, check if choose restaurant
        if self.process_end:
            self._curr_process_idx += 1
            
            self.process_end = False
            self.process_start = True
            
    def prepare_for_next_step(self):
        self.move_to_next_player()
        self.move_to_next_process()
    
    # interactive step design
    def step(self, input=None):        
        curr_player = self.get_curr_player()
        curr_process = self.get_curr_process()
        result = None
        
        # pre-process
        if self.process_start:
            if curr_process['name']  == "group_order":
                self.r_info = input
                for k in input.keys():
                    # add all today offerings to message pool
                    self.add_new_prompt(player_name='all', 
                                    data=input[k]['today_offering'])
                # add order prompt
                self.add_new_prompt(player_name='all', 
                                    scene_name=self.type_name, 
                                    step_name=curr_process['name'], 
                                    from_db=curr_process['from_db'])
            elif curr_process['name'] == "group_comment":
                # add dish score and comment prompt
                self.add_new_prompt(player_name='all',
                                    scene_name=self.type_name,
                                    step_name=curr_process['name'],
                                    data=input)
            self.process_start = False

        # text observation
        observation_text = self.message_pool.get_visible_messages(agent_name=curr_player.name, turn=self._curr_turn)
        # vision observation, get two restaurant images for showing
        # observation_vision = image_pool.get_visible_images(restaurant_name="All")
        if curr_process['name'] == 'group_order':
            observation_vision = image_pool.get_visible_images(restaurant_name="All")
        else:
            observation_vision = []
        
        for i in range(self.invalid_step_retry):
            try:
                output = curr_player(observation_text, observation_vision)
                parsed_ouput = self.parse_output(output, curr_player.name, curr_process['name'], curr_process['to_db'])
                break
            except Exception as e:
                print(f"Attempt {i + 1} failed with error: {e}")
        else:
            raise Exception("Invalid step retry arrived at maximum.")
        
        # post-process
        if curr_process['name'] == 'group_order':
            if parsed_ouput and 'restaurant' in parsed_ouput:
                restaurant = parsed_ouput['restaurant']
                dish_score = self.r_info[restaurant]['dish_score']
                self.dishes = parsed_ouput['dishes']
                
                prompt = ''
                for dish in self.dishes:
                    # check if the dish is in the restaurant
                    if dish in dish_score.keys():
                        score = dish_score[dish]
                        prompt += f"\n{dish}: {score}"
                    result = prompt
                
                self._curr_player_idx = -1
                
                self.process_end = True

        if curr_process['name'] == "group_comment":
            if parsed_ouput and 'comment' in parsed_ouput:
                dine_info = parsed_ouput
                dine_info['dishes'] = self.dishes
                dine_info['day'] = self.day
                customer_name = self.players[0].name
                dine_info = {customer_name: dine_info}
                result = dine_info
                
                self.process_end = True
                
        self.prepare_for_next_step()
        
        return result
        
        
        
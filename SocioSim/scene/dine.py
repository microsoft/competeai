from base import Stage
from ..agent import Agent
from SocioSim.SocioSim.message import Message

 
processes = [
    {"name": "order", "from_db": False, "to_db": True},
    {"name": "comment", "from_db": False, "to_db": True},
]


class Dine(Stage):
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
    
    def get_prompt(self, process: str, from_db: bool):
        """
        process (str): the name of the process
        from_db (bool): whether the prompt needs to get data from the database
        """
        if from_db:
            data = self.get_data_from_db(endpoint=process)
            prompt = self.generate_prompt(prompt_template=process, input=data)
        else:
            prompt = self.generate_prompt(prompt_template=process)
            
        return prompt
        
    # interactive step design
    def step(self):
        curr_player = self.get_curr_player()
        curr_process = self.get_curr_process()
        
        prompt = self.get_prompt(process=curr_process['name'], from_db=curr_process['from_db'])
        message = Message(agent_name='System', content=prompt, visible_to=curr_player, turn=self.message_pool.last_turn + 1)
        self.message_pool.append_message(message)
        
        is_valid = True
        for i in range(self.invalid_step_retry):
            response = self.step(curr_player)

            if curr_process['to_db']:
                is_valid = self.send_data_to_db(endpoint=curr_process['name'], data=response)
                
            if is_valid:
                message = Message(agent_name=curr_player, content=response, visible_to=curr_player, turn=self.message_pool.last_turn + 1)
                self.message_pool.append_message(message)
                break
        
        self._curr_process_idx += 1
        
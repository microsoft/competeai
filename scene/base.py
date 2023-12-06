from ..message import MessagePool

class Scene():
    def __init__(self, message_pool=None):
        self.process = None
        # All scenes share a common message pool
        self.message_pool = message_pool
        self.invalid_step_retry = 3
        
    def get_data_from_db(self, base_url='http://localhost:', port='8000', endpoint=None):
        pass
    
    def send_data_to_db(self, base_url='http://localhost:', port='8000', endpoint=None):
        pass
    
    def generate_prompt(self, prompt_template=None, input=None):
        pass
    
    def step(self):
        # get history messages from message pool
        # add prompt to the last message
        pass

    def run(self):
        """
        Main function, automatically assemble input and parse output to run the scene
        """
        while self.step():
            pass
from ..message import Message, MessagePool

class OutputParser():
    """
    Parse the output of LLM, Json format; add compact information to message_pool; send data to database
    """
    def __init__(self, message_pool: MessagePool):
        self.message_pool = message_pool
    
    def send_data_to_db(self, data):
        pass
    
    def parse(self, agent_name, output):
        # First parse output
        data = output # TODO parse output preliminarily
        short_text = output
        
        # TODO: Error handle
        self.send_data_to_db(data=data)
        
        message = Message(agent_name='System', content=short_text, visible_to=agent_name, turn=self.message_pool.last_turn + 1)
        
        self.message_pool.append_message(message)
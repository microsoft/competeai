from ..prompt_template import PromptTemplate

class PromptAssembler():
    def __init__(self, agent_name: str, message_pool=None, database=None, scene_name=None, step_name=None):
        self.agent_name = agent_name
        self.message_pool = message_pool
        self.database = database
        self.scene_name = scene_name
        self.step_name = step_name
    
    def get_data_from_db(self, base_url='http://localhost:', port='8000', endpoint=None):
        pass
    
    def get_prompt_template(self):
        return PromptTemplate(self.scene_name, self.step_name).get()
    
    def prompt_template_render(self, prompt_template=None, data=None):
        """
        prompt_template (str): the name of the prompt template
        data (dict): the input data for the prompt template
        """
        pass
    
    def prompt_assemble(self):
        """
        prompt_template (str): the name of the prompt template
        input (dict): the input data for the prompt template
        """
        data = self.get_data_from_db()
        prompt_template = self.get_prompt_template()
        prompt = self.prompt_template_render(prompt_template=prompt_template, data=data)
        
        
from ..prompt_template import PromptTemplate
from ..message import Message, MessagePool, SYSTEM_NAME

END_OF_MESSAGE = "<EOS>"
BASE_PROMPT = f"The messages always end with the token {END_OF_MESSAGE}."


# 该组装器运行在整个模拟运行过程中，init初始化时只能传入供全局使用的config, message_pool
class PromptAssembler():
    def __init__(self, config: Config, message_pool: MessagePool):
        self.config = config
        self.message_pool = message_pool
    
    def get_data_from_db(self, base_url='http://localhost:', port='8000', endpoint=None):
        pass
    
    def get_prompt_template(self, first_dir, second_dir):
        return PromptTemplate(first_dir, second_dir).get()
    
    def prompt_template_render(self, prompt_template=None, data=None):
        """
        prompt_template (str): the name of the prompt template
        data (dict): the input data for the prompt template
        """
        pass
    
    def prompt_assemble(self, agent_name, scene_name, step_name):
        """
        prompt_template (str): the name of the prompt template
        input (dict): the input data for the prompt template
        """
        global_prompt = self.config['background'] if 'background' in self.config else ''
        role_desc = self.config[agent_name]['role_desc']
        
        # Merge the role description and the global prompt as the system prompt for the agent
        if global_prompt:  # Prepend the global prompt if it exists
            system_prompt = f"{global_prompt.strip()}\n{BASE_PROMPT}\n\nYour name is {agent_name}.\n\nYour role:{role_desc}"
        else:
            system_prompt = f" Your name is {agent_name}.\n\nYour role:{role_desc}\n\n{BASE_PROMPT}"
            
        all_messages = [(SYSTEM_NAME, system_prompt)]
        
        data = self.get_data_from_db(step_name)
        prompt_template = self.get_prompt_template(scene_name, step_name)
        prompt = self.prompt_template_render(prompt_template=prompt_template, data=data)
        
        # convert str:prompt to Message:prompt
        turn = self.message_pool.last_turn + 1  # FIXME
        message = Message(agent_name=self.agent_name, content=prompt, visible_to=self.agent_name, turn=turn)
        self.message_pool.append(message)
        
        # get all visible message
        history_messages = self.message_pool.get_visible_messages(agent_name=agent_name, turn=turn)
        
        for msg in history_messages:
            if msg.agent_name == SYSTEM_NAME:
                all_messages.append((SYSTEM_NAME, msg.content))
            else:  # non-system messages are suffixed with the end of message token
                all_messages.append((msg.agent_name, f"{msg.content}{END_OF_MESSAGE}"))

        # request_msg是一个很好的设计，它用于规定llm最后生成的格式，但是不加入message_pool，不消耗未来的tokens
        # if request_msg:
        #     all_messages.append((SYSTEM_NAME, request_msg.content))
        # else:  # The default request message that reminds the agent its role and instruct it to speak
        #     all_messages.append((SYSTEM_NAME, f"Remember your role: {role_desc} Now you speak, {agent_name}.{END_OF_MESSAGE}"))
        
        
        
        
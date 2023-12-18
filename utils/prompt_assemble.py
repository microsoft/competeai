from ..message import Message, MessagePool, SYSTEM_NAME
from ..simul import PORT_MAP
from .prompt_template import PromptTemplate
from .database import get_data_from_db

END_OF_MESSAGE = "<EOS>"
BASE_PROMPT = f"The messages always end with the token {END_OF_MESSAGE}."


class PromptAssembler():
    def __init__(self, message_pool: MessagePool):
        self.message_pool = message_pool
    
    def assemble(self, player, scene_name, step_name):
        """
        prompt_template (str): the name of the prompt template
        input (dict): the input data for the prompt template
        """
        player_name = player.name
        role_desc = player.role_desc
        global_prompt = player.global_prompt
        
        # Merge the role description and the global prompt as the system prompt for the agent
        if global_prompt:  # Prepend the global prompt if it exists
            system_prompt = f"{global_prompt.strip()}\n{BASE_PROMPT}\n\nYour name is {player_name}.\n\nYour role:{role_desc}"
        else:
            system_prompt = f" Your name is {player_name}.\n\nYour role:{role_desc}\n\n{BASE_PROMPT}"
            
        all_messages = [(SYSTEM_NAME, system_prompt)]
        
        # If the prompt template exists, render it and add it to the message pool
        if PromptTemplate([scene_name, step_name]).content:
            data = get_data_from_db(step_name, PORT_MAP['player_name'])  # TODO: how to transmit 'port' to here?
            prompt_template = PromptTemplate([scene_name, step_name])
            prompt = prompt_template.render(data=data)
            # convert str:prompt to Message:prompt
            turn = self.message_pool.last_turn + 1  # FIXME
            message = Message(agent_name=player_name, content=prompt, visible_to=player_name, turn=turn)
            self.message_pool.append(message)
        
        # get all visible message
        history_messages = self.message_pool.get_visible_messages(agent_name=player_name, turn=turn)
        
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
        
        return all_messages
        
        
        
        
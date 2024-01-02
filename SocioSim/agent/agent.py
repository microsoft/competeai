from typing import List, Union
import re
from tenacity import RetryError
import logging
import uuid
from abc import abstractmethod
import asyncio

from .backends import IntelligenceBackend, load_backend
from ..image import Image
from ..message import Message, SYSTEM_NAME
from ..config import AgentConfig, Configurable, BackendConfig

# A special signal sent by the player to indicate that it is not possible to continue the conversation, and it requests to end the conversation.
# It contains a random UUID string to avoid being exploited by any of the players.
SIGNAL_END_OF_CONVERSATION = f"<<<<<<END_OF_CONVERSATION>>>>>>{uuid.uuid4()}"


class Agent(Configurable):
    """
        An abstract base class for all the agents in the chatArena environment.
    """
    @abstractmethod
    def __init__(self, name: str, agent_type: str, role_desc: str, global_prompt: str = None, *args, **kwargs):
        """
        Initialize the agent.

        Parameters:
            name (str): The name of the agent.
            role_desc (str): Description of the agent's role.
            global_prompt (str): A universal prompt that applies to all agents. Defaults to None.
        """
        super().__init__(name=name, role_desc=role_desc, global_prompt=global_prompt, **kwargs)
        self.name = name
        self.agent_type = agent_type
        self.role_desc = role_desc
        if global_prompt and agent_type in global_prompt.keys():
            self.global_prompt = global_prompt[agent_type]


class Player(Agent):
    """
    The Player class represents a player in the chatArena environment. A player can observe the environment
    and perform an action (generate a response) based on the observation.
    """

    def __init__(self, name: str, role_desc: str, backend: Union[BackendConfig, IntelligenceBackend],
                 global_prompt: str = None, **kwargs):
        """
        Initialize the player with a name, role description, backend, and a global prompt.

        Parameters:
            name (str): The name of the player.
            role_desc (str): Description of the player's role.
            backend (Union[BackendConfig, IntelligenceBackend]): The backend that will be used for decision making. It can be either a LLM backend or a Human backend.
            global_prompt (str): A universal prompt that applies to all players. Defaults to None.
        """

        if isinstance(backend, BackendConfig):
            backend_config = backend
            backend = load_backend(backend_config)
        elif isinstance(backend, IntelligenceBackend):
            backend_config = backend.to_config()
        else:
            raise ValueError(f"backend must be a BackendConfig or an IntelligenceBackend, but got {type(backend)}")

        assert name != SYSTEM_NAME, f"Player name cannot be {SYSTEM_NAME}, which is reserved for the system."

        # Register the fields in the _config
        super().__init__(name=name, role_desc=role_desc, backend=backend_config,
                         global_prompt=global_prompt, **kwargs)

        self.backend = backend

    def to_config(self) -> AgentConfig:
        return AgentConfig(
            name=self.name,
            role_desc=self.role_desc,
            backend=self.backend.to_config(),
            global_prompt=self.global_prompt,
        )

    def act(self, observation_text: List[Message], observation_vision: List[Image]=[]) -> str:
        """
        Take an action based on the observation (Generate a response), which can later be parsed to actual actions that affect the game dyanmics.

        Parameters:
            observation (List[Message]): The messages that the player has observed from the environment.

        Returns:
            str: The action (response) of the player.
        """ 
        try:
            response = self.backend.query(agent_name=self.name, agent_type=self.agent_type, role_desc=self.role_desc,
                                          history_messages=observation_text, global_prompt=self.global_prompt,
                                          images=observation_vision, request_msg=None)
        except RetryError as e:
            err_msg = f"Agent {self.name} failed to generate a response. Error: {e.last_attempt.exception()}. Sending signal to end the conversation."
            logging.warning(err_msg)
            response = SIGNAL_END_OF_CONVERSATION + err_msg

        return response

    def __call__(self, observation_text: List[Message], observation_vision: List[Image]) -> str:
        return self.act(observation_text, observation_vision)

    async def async_act(self, observation: List[Message]) -> str:
        """
        Async version of act(). This is used when you want to generate a response asynchronously.

        Parameters:
            observation (List[Message]): The messages that the player has observed from the environment.

        Returns:
            str: The action (response) of the player.
        """
        try:
            response = self.backend.async_query(agent_name=self.name, role_desc=self.role_desc,
                                                history_messages=observation, global_prompt=self.global_prompt,
                                                request_msg=None)
        except RetryError as e:
            err_msg = f"Agent {self.name} failed to generate a response. Error: {e.last_attempt.exception()}. Sending signal to end the conversation."
            logging.warning(err_msg)
            response = SIGNAL_END_OF_CONVERSATION + err_msg

        return response

    def reset(self):
        """
        Reset the player's backend in case they are not stateless.
        This is usually called at the end of each episode.
        """
        self.backend.reset()
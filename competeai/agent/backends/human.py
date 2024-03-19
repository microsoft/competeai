# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
# Source Attribution:
# The majority of this code is derived from the following sources:
# - Chatarena GitHub Repository: https://github.com/Farama-Foundation/chatarena

from .base import IntelligenceBackend
from ...config import BackendConfig


# An Error class for the human backend
class HumanBackendError(Exception):
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        super().__init__(f"Human backend requires a UI to get input from {agent_name}.")


class Human(IntelligenceBackend):
    stateful = False
    type_name = "human"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_config(self) -> BackendConfig:
        return BackendConfig(backend_type=self.type_name)

    def query(self, agent_name: str, **kwargs) -> str:
        raise HumanBackendError(agent_name)

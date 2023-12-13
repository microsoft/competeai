import json
import yaml
import copy
from abc import abstractmethod

from .utils import AttributedDict


class Config(AttributedDict):
    """
    Config class to manage the configuration of the games.
    The class has a few useful methods to load and save the config.
    """

    # convert dict to Config recursively
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = init_config(value)  # convert dict to Config recursively
            # convert list of dict to list of Config recursively
            elif isinstance(value, list) and len(value) > 0:
                self[key] = [init_config(item) if isinstance(item, dict) else item for item in value]

    def save(self, path: str):
        # save config to file
        if 'json' in path:
            with open(path, "w") as f:
                json.dump(self, f, indent=4)
        elif 'yaml' in path:
            with open(path, "w") as f:
                yaml.safe_dump(self, f, indent=4)

    @classmethod
    def load(cls, path: str):
        # load config from file
        if 'json' in path:
            with open(path, "r") as f:
                config = json.load(f)
        elif 'yaml' in path:
            with open(path, "r") as f:
                config = yaml.safe_load(f)
        return cls(config)

    def deepcopy(self):
        # get the config class so that subclasses can be copied in the correct class
        config_class = self.__class__
        # make a deep copy of the config
        return config_class(copy.deepcopy(self))


class Configurable:
    """
    Configurable is an interface for classes that can be initialized with a config.
    """

    def __init__(self, **kwargs):
        self._config_dict = kwargs

    @classmethod
    def from_config(cls, config: Config):
        return cls(**config)

    def to_config(self) -> Config:
        # Convert the _config_dict to Config
        return Config(**self._config_dict)

    def save_config(self, path: str):
        self.to_config().save(path)


class SceneConfig(Config):
    """
    TODO SceneConfig contains
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # check if the env_type field is specified
        if "scene_type" not in self:
            raise ValueError("The scene_type field is not specified")


class BackendConfig(Config):
    """
    BackendConfig contains a backend_type field to indicate the name of the backend.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # check if the backend_type field is specified
        if "backend_type" not in self:
            raise ValueError("The backend_type field is not specified")


class AgentConfig(Config):
    """
    AgentConfig contains role_desc and backend fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # check if the role_desc field is specified
        if "role_desc" not in self:
            raise ValueError("The role_desc field is not specified")
        # check if the backend field is specified
        if "backend" not in self:
            raise ValueError("The backend field is not specified")
        # Make sure the backend field is a BackendConfig
        if not isinstance(self["backend"], BackendConfig):
            raise ValueError("The backend field must be a BackendConfig")


class SimulConfig(Config):
    """
    SimulConfig contains a list of AgentConfig.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # check if the players field is specified and it is List[AgentConfig]
        if "players" not in self:
            raise ValueError("The players field is not specified")
        if not isinstance(self["players"], list):
            raise ValueError("The players field must be a list")
        for player in self["players"]:
            if not isinstance(player, AgentConfig):
                raise ValueError("The players field must be a list of AgentConfig")

        # check if scene field is specified and it is SceneConfig
        if "scenes" not in self:
            raise ValueError("The scene field is not specified")
        if not isinstance(self["scene"], list):
            raise ValueError("The scene field must be a list")
        for scene in self["scene"]:
            if not isinstance(scene, SceneConfig):
                raise ValueError("The scene field must be a list of sceneConfig")


# Initialize with different config class depending on whether the config is for scene or backend
def init_config(config: dict):
    if not isinstance(config, dict):
        raise ValueError("The config must be a dict")

    # check if the config is for scene or backend
    if "env_type" in config:
        return SceneConfig(config)
    elif "backend_type" in config:
        return BackendConfig(config)
    elif "role_desc" in config:
        return AgentConfig(config)
    elif "players" in config:
        return SimulConfig(config)
    else:
        return Config(config)

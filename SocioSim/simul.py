from dataclasses import dataclass
from typing import Union, List
from concurrent.futures import ThreadPoolExecutor

from .config import SimulConfig
from .message import MessagePool
from .agent import Player
from .scene import load_scene, Scene

from .utils import NAME2PORT


# 该类负责全局的模拟过程
# 并行化运行scene，推进simulation进行.

class Simulation:
    def __init__(self, scenes: List[Scene]):
        self.scenes = scenes   
        self.curr_scene_idx = 0

    def get_curr_scene(self):
        # TODO: graph search
        return self.scenes[self.curr_scene_idx]
    
    def step(self, data):
        """
        Run one step of the simulation
        """
        current_scene = self.get_curr_scene()
        
        # Parallel run scenes & check if all scenes are finished
        max_number_parallel = 6
        with ThreadPoolExecutor(max_workers=max_number_parallel) as executor:
            futures = [executor.submit(scene.run(data)) for scene in current_scene]
            # Optionally, wait for all scenes to finish and get their results
            results = [future.result() for future in futures]
        
        next_scene_data = current_scene[0].get_data_for_next_scene()
        self.curr_scene_idx += 1
        
        return next_scene_data
    
    def run(self):
        """
        Main function, run the simulation
        """
        previous_scene_data = None
        while True:  # TODO
            res = self.step(previous_scene_data)
            previous_scene_data = res
    
    @classmethod
    def from_config(cls, config: Union[str, dict, SimulConfig]):
        """
        create an simul from a config
        """
        # If config is a path, load the config
        if isinstance(config, str):
            config = SimulConfig.load(config)
        if isinstance(config, dict):
            config = SimulConfig(config)

        global_prompt = config.get("global_prompt", None)
        database_port = config.get("database_port_base", None)
        log_path = config.get("log_path", None)

        # fill the port map, not a universal code  
        for scene_config in config.scenes:
            if scene_config['scene_type'] == 'restaurant_design':
                for player in scene_config['players']:
                    NAME2PORT[player] = database_port
                    database_port += 1
        
        # Create the players
        players = []
        for player_config in config.players:
            # Add public_prompt to the player config
            if global_prompt is not None:
                player_config["global_prompt"] = global_prompt

            player = Player.from_config(player_config)
            players.append(player)

        # Check that the player names are unique
        player_names = [player.name for player in players]
        assert len(player_names) == len(set(player_names)), "Player names must be unique"

        # Create scenes and decide their order
        scenes = []
        for scene_config in config.scenes:
            same_scene = []
            scene_config['log_path'] = log_path
            for i, player in enumerate(scene_config['players']):   
                scene_config['id'] = i
                # a single player or a group of players
                if isinstance(player, str):
                    assert player in player_names, f"Player {player} is not defined"
                    scene_config["players"] = [players[player_names.index(player)]]
                    scene = load_scene(scene_config)
                elif isinstance(player, list):
                    assert all(p in player_names for p in player), f"Player {player} is not defined"
                    scene_config["players"] = [players[player_names.index(p)] for p in player]
                    scene = load_scene(scene_config)
                same_scene.append(scene)
            scenes.append(same_scene)

        return cls(scenes)
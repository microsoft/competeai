from dataclasses import dataclass

import os
import yaml

@dataclass
class Step:
    agent_name: str
    task_name: str

# 该类负责全局的模拟过程
# 初始化config, message_pool, database, backend，为scene和每个scene构建多个实例
# 并行化运行scene，推进simulation进行
# 根据实际情况继续改进...
class Simulation:
    # read the steps from config file and build topology of the process
    def __init__(self, config):
        self.config = config
        self.steps = []

    def get_process(self, name):
        with open('./config/competition.yaml', 'r') as file:
            data = yaml.safe_load(file)
        
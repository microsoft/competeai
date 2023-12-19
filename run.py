import os
from SocioSim.simul import Simulation

config_path = os.path.join('SocioSim', 'examples', 'restaurant.yaml')
Simul = Simulation.from_config(config_path)
Simul.run()
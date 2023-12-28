from .prompt_template import PromptTemplate
from .database import *
from .dall_e import generate_picture
from .log import log_table

NAME2PORT = {}
PORT2NAME = {}
BASE_PORT = 9000
DELIMITER = "<<FORMAT>>"
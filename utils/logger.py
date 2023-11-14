import datetime
from enum import Enum

import utils.config

# Level
class Level(Enum):
    RESET = "\033[0m"
    ERROR = "\033[91m"
    INFO = "\033[92m"
    WARNING = "\033[93m"
    DEBUG = "\033[94m"

class Logger:
    def __init__(self, loglevel:Level, content:str):
        self.loglevel = loglevel
        self.content = content
        self.output()
    
    def output(self):
        try:
            if utils.config.Config().read_config()['bot'][1]['debug'] == True or self.loglevel != Level.DEBUG:
                print(f"{self.loglevel.value}[{datetime.datetime.now()}] -> {self.content} \033[0m")
        except:
            print(f"{self.loglevel.value}[{datetime.datetime.now()}] -> {self.content} \033[0m")


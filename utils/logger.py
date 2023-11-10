import datetime
from enum import Enum

# Color
class Color(Enum):
    RESET = "\033[0m"
    ERROR = "\033[91m"
    INFO = "\033[92m"
    WARNING = "\033[93m"
    DEBUG = "\033[94m"

class Logger:
    def __init__(self, loglevel:Color, content:str):
        self.loglevel = loglevel
        self.content = content
    
    def output(self):
        print(f"{self.loglevel.value}[{datetime.datetime.now()}] -> {self.content} \033[0m")


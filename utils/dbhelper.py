from utils.config import *
import sqlite3

# Workspace
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir,'..'))

class DBHelper():
    def __init__(self):
        self.db_enabled = read_config()['database'][0]['db_enabled']
        if self.db_enabled:
            self.conn = sqlite3.connect(read_config()['database'][1]['db_name'])
            self.cursor = self.conn.cursor()
        else:
            pass
        self.return_db_status()
    def return_db_status(self):
        return self.db_enabled
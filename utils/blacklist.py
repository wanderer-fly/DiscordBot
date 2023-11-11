from utils.config import *
from utils.dbhelper import *
from utils.logger import *
import sqlite3

# Workspace
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir,'..'))

class Blacklist:
    def __init__(self, db_helper: DBHelper):
        self.db_helper = db_helper
        if self.db_helper.db_enabled:
            self.table_name = 'blacklist'

            query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
            result = self.db_helper.cursor.execute(query, (self.table_name,)).fetchone()
            
            if not result:
                Logger(Color.WARNING, f"Table {self.table_name} is not exist, creating a new one...")
                self.init_db()
            Logger(Color.INFO, "Blacklist enabled")
    
    def init_db(self): # if not self.db_helper.db_enabled 这个函数不会被执行，所以不需要判断
        self.db_helper.cursor.execute('''
            CREATE TABLE IF NOT EXISTS blacklist (
                user_id TEXT PRIMARY KEY
            )
        ''')
        self.db_helper.conn.commit()

    def check_user(self, user_id) -> bool:
        if not self.db_helper.db_enabled:
            Logger(Color.WARNING, "Database not enabled, ignoring this request")
            return False
        else:
            try:
                query = f"SELECT COUNT(*) FROM {self.table_name} WHERE user_id = ?"
                result = self.db_helper.cursor.execute(query, (user_id,)).fetchone()
                count = result[0]
                
                # if `count` >  0, the user is in blacklist
                if count > 0:
                    return True
                else:
                    return False
            except Exception as e:
                print(e)
                return False
    
    def add_user(self, user_id) -> bool:
        if not self.db_helper.db_enabled:
            Logger(Color.WARNING, "Database not enable, ignoring this request")
            return False
        else:
            try:
                query = f"INSERT INTO {self.table_name} (user_id) VALUES (?)"
                self.db_helper.cursor.execute(query, (user_id,))
                self.db_helper.conn.commit()
                return True
            except Exception as e:
                print(e)
                return False

    def del_user(self, user_id) -> bool:
        if not self.db_helper.db_enabled:
            Logger(Color.WARNING, "Database not enable, ignoring this request")
            return False
        else:
            try:
                query = f"DELETE FROM {self.table_name} WHERE user_id = ?"
                r = self.db_helper.cursor.execute(query, (user_id,))
                self.db_helper.conn.commit()
                return True
            except Exception as e:
                print(e)
                return False
    

from enum import Enum

from utils.dbhelper import *

from discord.ext import commands

class User(Enum):
    ACCESS = 1
    ADMIN = 2
    SUPERADMIN = 3
    OWNER = 4

    def get_permission_value(dbhelper: DBHelper, user_id: str) -> int:
        return 10
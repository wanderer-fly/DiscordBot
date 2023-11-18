from enum import Enum

from utils.dbhelper import *
from utils import db

from discord.ext import commands


class Permission(Enum):
    ACCESS = 1
    ADMIN = 2
    SUPERADMIN = 3
    OWNER = 4

    def get_permission_value(user_id: str) -> int:
        if not db.return_db_status():
            return 10 # if database not enabled, return 10 as the highest permission
        else:
            query = f"SELECT COUNT(*) FROM permission WHERE user_id = ?"
            return 
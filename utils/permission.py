from enum import Enum

from utils.dbhelper import *
from utils import db

from discord.ext import commands


class User(Enum):
    ACCESS = 1
    ADMIN = 2
    SUPERADMIN = 3
    OWNER = 4

    def get_permission_value(user_id: str) -> int:
        return 1
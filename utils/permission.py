from enum import Enum

class User(Enum):
    ACCESS = 1
    ADMIN = 2
    SUPERADMIN = 3
    OWNER = 4

    def get_premission_value(user_id):
        return 10
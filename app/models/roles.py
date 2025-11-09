from enum import Enum


class RoleEnum(str, Enum):
    USER = "user"
    OPERATOR = "operator"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"

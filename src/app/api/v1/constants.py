from enum import Enum


class Prefixes(str, Enum):
    employees = "employees"
    projects = "projects"
    users = "users"


class Tags(str, Enum):
    employees = "Employees"
    projects = "Projects"
    users = "Users"

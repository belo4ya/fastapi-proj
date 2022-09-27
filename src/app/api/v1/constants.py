from enum import Enum


class Prefixes(str, Enum):
    employees = "employees"
    projects = "projects"
    users = "users"


class Tags(str, Enum):
    employees = "Employees"
    projects = "Projects"
    users = "Users"


class UserRoles(str, Enum):
    # users
    employee = "employee"
    manager = "manager"
    project_owner = "project_owner"
    project_manager = "project_manager"
    hr_manger = "hr_manger"
    tech_support = "tech_support"

    # service
    admin = "admin"


class SSORoles(str, Enum):
    pass


class ProjectStatuses(str, Enum):
    active = "active"
    finished = "finished"

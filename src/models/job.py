from dataclasses import dataclass


@dataclass
class Job:
    id: int
    user_id: int
    title: str
    description: str
    salary_from: str
    salary_to: str
    is_active: bool


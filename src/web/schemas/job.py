from typing import Optional

from pydantic import BaseModel, Field


class JobCreateSchema(BaseModel):

    title: Optional[str] = Field(description="Название вакансии")
    description: Optional[str] = Field(description="Описание вакансии")
    salary_from: Optional[str] = Field(description="Зарплата от")
    salary_to: Optional[str] = Field(description="Зарплата до")
    is_active: bool = Field(default=True, description="Флаг активности")


class JobSchema(BaseModel):

    id: int = Field(description="Идентификатор вакансии")
    user_id: int = Field(description="Идентификатор пользователя")


class JobUpdateSchema(BaseModel):

    id: int = Field(description="Идентификатор вакансии")
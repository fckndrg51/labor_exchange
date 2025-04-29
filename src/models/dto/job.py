from typing import Optional

from pydantic import BaseModel, Field


class JobUpdateDto(BaseModel):

    title: Optional[str] = Field(description="Название вакансии")
    description: Optional[str] = Field(description="Описание вакансии")
    salary_from: Optional[str] = Field(description="Зарплата от")
    salary_to: Optional[str] = Field(description="Зарплата до")
    is_active: bool = Field(description="Флаг активности")


class JobCreateDto(JobUpdateDto):

    user_id: int = Field(description="Идентификатор пользователя")
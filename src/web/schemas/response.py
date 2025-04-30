from typing import Optional

from pydantic import BaseModel, Field


class ResponseCreateSchema(BaseModel):

    job_id: int = Field(description="Идентификатор вакансии")
    message: Optional[str] = Field(description="Рекомендательное письмо")


class ResponseSchema(BaseModel):

    id: int = Field(description="Идентификатор отклика")
    user_id: int = Field(description="Идентификатор пользователя")
    job_id: int = Field(description="Идентификатор вакансии")
    message: Optional[str] = Field(description="Сопроводительное письмо")


class ResponseUpdateSchema(BaseModel):

    id: int = Field(description="Идентификатор отклика")
    message: Optional[str] = Field(description="Сопроводительное письмо")
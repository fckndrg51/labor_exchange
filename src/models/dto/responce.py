from pydantic import BaseModel, Field

class ResponseUpdateDto(BaseModel):

    message: str = Field(description="Сопроводительное письмо")

class ResponseCreateDto(BaseModel):

    job_id: int = Field(description="Идентификатор вакансии")
    user_id: int = Field(description="Идентификатор пользователя")
    message: str = Field(description="Сопроводительное письмо")
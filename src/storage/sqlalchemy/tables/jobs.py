from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


from storage.sqlalchemy.client import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, comment="Идентификатор вакансии")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), comment="Идентификатор пользователя"
    )

    # добавьте ваши колонки сюда
    title: Mapped[str] = mapped_column(comment="Название вакансии")
    description: Mapped[str] = mapped_column(comment="Описание вакансии")
    salary_from: Mapped[str] = mapped_column(comment="Зарплата от")
    salary_to: Mapped[str] = mapped_column(comment="Зарплата до")
    is_active: Mapped[bool] = mapped_column(default=True, comment="Активна ли вакансия")
    created_at: Mapped[datetime] = mapped_column(comment="Время создания записи", default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="jobs")  # noqa
    responses: Mapped["Response"] = relationship(back_populates="job")  # noqa

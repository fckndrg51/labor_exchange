from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from interfaces import IRepositoryAsync
from models import Job as JobModel
from models import Response as ResponseModel
from storage.sqlalchemy.tables import Job
from models.dto.job import JobCreateDto, JobUpdateDto
from exception.repository_exception import NotFoundError



class UserRepository(IRepositoryAsync):
    def __init__(self, session: Callable[..., AbstractContextManager[Session]]):
        self.session = session

    async def create(self, job_create_dto: JobCreateDto) -> JobModel:
        async with self.session() as session:
            job = Job(
                user_id=job_create_dto.user_id,
                title=job_create_dto.title,
                description=job_create_dto.description,
                salary_from=job_create_dto.salary_from,
                salary_to=job_create_dto.salary_to,
                is_active=job_create_dto.is_active,
            )
            session.add(job)
            await session.commit()
            await session.refresh(job)

        return self.to_job_model(job, include_relations=False)

    async def retrieve(self, include_relations: bool = False, **kwargs) -> JobModel:
        async with self.session() as session:
            query = select(Job).filter_by(**kwargs).limit(1)
            if include_relations:
                query = query.options(selectinload(Job.responses))
            res = await session.execute(query)
            job_from_db = res.scalars().first()

        return self.to_job_model(job_from_db, include_relations=include_relations)

    async def retrieve_many(self, limit: int = 100, skip: int = 0, include_relations: bool = False) -> list[JobModel]:
        async with self.session() as session:
            query = select(Job).limit(limit).offset(skip)
            if include_relations:
                query = query.options(selectinload(Job.responses))
            res = await session.execute(query)
            jobs_from_db = res.scalars().all()

        return [self.to_job_model(job, include_relations=include_relations) for job in jobs_from_db]

    async def update(self, id: int, job_update_dto: JobUpdateDto) -> JobModel:
        async with self.session() as session:
            res = await session.execute(select(Job).filter_by(id=id))
            job_from_db = res.scalars().first()

            if not job_from_db:
                raise NotFoundError("Вакансия", id)

            job_from_db.title = job_update_dto.title or job_from_db.title
            job_from_db.description = job_update_dto.description or job_from_db.description
            job_from_db.salary_from = job_update_dto.salary_from if job_update_dto.salary_from is not None else job_from_db.salary_from
            job_from_db.salary_to = job_update_dto.salary_to if job_update_dto.salary_to is not None else job_from_db.salary_to
            job_from_db.is_active = job_update_dto.is_active if job_update_dto.is_active is not None else job_from_db.is_active

            session.add(job_from_db)
            await session.commit()
            await session.refresh(job_from_db)

        return self.to_job_model(job_from_db, include_relations=False)

    async def delete(self, id: int) -> JobModel:
        async with self.session() as session:
            res = await session.execute(select(Job).filter_by(id=id))
            job_from_db = res.scalars().first()

            if not job_from_db:
                raise NotFoundError("Вакансия", id)

            await session.delete(job_from_db)
            await session.commit()

        return self.to_job_model(job_from_db, include_relations=False)

    def to_job_model(self, job_from_db: Job, include_relations: bool = False) -> JobModel:
        if not job_from_db:
            return None

        responses = []
        if include_relations and hasattr(job_from_db, "responses"):
            responses = [
                ResponseModel(
                    id=resp.id,
                    job_id=resp.job_id,
                    user_id=resp.user_id,
                    message=resp.message,
                )
                for resp in job_from_db.responses
            ]

        return JobModel(
            id=job_from_db.id,
            user_id=job_from_db.user_id,
            title=job_from_db.title,
            description=job_from_db.description,
            salary_from=job_from_db.salary_from,
            salary_to=job_from_db.salary_to,
            is_active=job_from_db.is_active,
            responses=responses,
        )


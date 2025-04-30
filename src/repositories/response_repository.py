from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from interfaces import IRepositoryAsync
from models import Response as ResponseModel
from storage.sqlalchemy.tables import Response
from models.dto.responce import ResponseCreateDto, ResponseUpdateDto
from exception.repository_exception import NotFoundError


class ResponseRepository(IRepositoryAsync):
    def __init__(self, session: Callable[..., AbstractContextManager[Session]]):
        self.session = session

    async def create(self, response_create_dto: ResponseCreateDto) -> ResponseModel:
        async with self.session() as session:
            response = Response(
                user_id=response_create_dto.user_id,
                job_id=response_create_dto.job_id,
                message=response_create_dto.message
            )

            session.add(response)
            await session.commit()
            await session.refresh(response)

        return self.to_response_model(response_from_db=response)

    async def retrieve(self, **kwargs) -> ResponseModel:
        async with self.session() as session:
            query = select(Response).filter_by(**kwargs).limit(1)
            res = await session.execute(query)
            response_from_db = res.scalars().first()

        if not response_from_db:
            raise NotFoundError(entity_name="Отклик", entity_id=kwargs.get("id", 0))

        return self.to_response_model(response_from_db=response_from_db)

    async def retrieve_many(self, limit: int = 100, skip: int = 0) -> list[ResponseModel]:
        async with self.session() as session:
            query = select(Response).limit(limit).offset(skip)
            res = await session.execute(query)
            responses_from_db = res.scalars().all()

        return [self.to_response_model(response) for response in responses_from_db]

    async def update(self, id: int, response_update_dto: ResponseUpdateDto) -> ResponseModel:
        async with self.session() as session:
            query = select(Response).filter_by(id=id).limit(1)
            res = await session.execute(query)
            response_from_db = res.scalars().first()

            if not response_from_db:
                raise NotFoundError(entity_name="Отклик", entity_id=id)

            response_from_db.message = response_update_dto.message

            session.add(response_from_db)
            await session.commit()
            await session.refresh(response_from_db)

        return self.to_response_model(response_from_db=response_from_db)

    async def delete(self, id: int) -> ResponseModel:
        async with self.session() as session:
            query = select(Response).filter_by(id=id).limit(1)
            res = await session.execute(query)
            response_from_db = res.scalars().first()

            if not response_from_db:
                raise NotFoundError(entity_name="Отклик", entity_id=id)

            await session.delete(response_from_db)
            await session.commit()

        return self.to_response_model(response_from_db=response_from_db)

    def to_response_model(self, response_from_db: Response) -> ResponseModel:
        return ResponseModel(
            id=response_from_db.id,
            user_id=response_from_db.user_id,
            job_id=response_from_db.job_id,
            message=response_from_db.message,
        )

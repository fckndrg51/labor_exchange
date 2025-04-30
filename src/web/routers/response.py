from dataclasses import asdict
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.containers import RepositoriesContainer
from models.dto.responce import ResponseCreateDto, ResponseUpdateDto
from repositories import ResponseRepository
from web.schemas.response import ResponseCreateSchema, ResponseSchema, ResponseUpdateSchema
from exception.repository_exception import NotFoundError

router = APIRouter(prefix="/responses", tags=["responses"])


@router.get("")
@inject
async def read_responses(
    limit: int = 100,
    skip: int = 0,
    response_repository: ResponseRepository = Depends(Provide[RepositoriesContainer.response_repository]),
) -> list[ResponseSchema]:
    responses = await response_repository.retrieve_many(limit=limit, skip=skip)
    return [ResponseSchema(**asdict(r)) for r in responses]


@router.post("")
@inject
async def create_response(
    response_create_schema: ResponseCreateSchema,
    response_repository: ResponseRepository = Depends(Provide[RepositoriesContainer.response_repository]),
) -> ResponseSchema:
    dto = ResponseCreateDto(**response_create_schema.dict())
    response = await response_repository.create(dto)
    return ResponseSchema(**asdict(response))


@router.put("/{response_id}")
@inject
async def update_response(
    response_id: int,
    response_update_schema: ResponseUpdateSchema,
    response_repository: ResponseRepository = Depends(Provide[RepositoriesContainer.response_repository]),
) -> ResponseSchema:
    try:
        dto = ResponseUpdateDto(**response_update_schema.dict())
        updated = await response_repository.update(response_id, dto)
        return ResponseSchema(**asdict(updated))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{response_id}")
@inject
async def delete_response(
    response_id: int,
    response_repository: ResponseRepository = Depends(Provide[RepositoriesContainer.response_repository]),
) -> ResponseSchema:
    try:
        deleted = await response_repository.delete(response_id)
        return ResponseSchema(**asdict(deleted))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

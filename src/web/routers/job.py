from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_current_user
from dependencies.containers import RepositoriesContainer
from exception.repository_exception import NotFoundError
from models import User
from repositories import JobRepository
from web.schemas.job import JobSchema, JobCreateSchema, JobUpdateSchema
from models.dto.job import JobCreateDto, JobUpdateDto

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
@inject
async def read_jobs(
    limit: int = 100,
    skip: int = 0,
    job_repository: JobRepository = Depends(Provide[RepositoriesContainer.job_repository]),
) -> list[JobSchema]:
    job_models = await job_repository.retrieve_many(limit=limit, skip=skip, include_relations=True)
    return [JobSchema(**asdict(job)) for job in job_models]


@router.post("")
@inject
async def create_job(
    job_create_schema: JobCreateSchema,
    job_repository: JobRepository = Depends(Provide[RepositoriesContainer.job_repository]),
    current_user: User = Depends(get_current_user),
) -> JobSchema:
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

    job_create_dto = JobCreateDto(user_id=current_user.id, **job_create_schema.model_dump())
    job = await job_repository.create(job_create_dto)
    return JobSchema(**asdict(job))


@router.put("")
@inject
async def update_job(
    job_update_schema: JobUpdateSchema,
    job_repository: JobRepository = Depends(Provide[RepositoriesContainer.job_repository]),
    current_user: User = Depends(get_current_user),
) -> JobSchema:
    job = await job_repository.retrieve(id=job_update_schema.id)
    if not job or job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

    job_update_dto = JobUpdateDto(**job_update_schema.model_dump())
    try:
        updated_job = await job_repository.update(id=job_update_schema.id, job_update_dto=job_update_dto)
        return JobSchema(**asdict(updated_job))
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")


@router.delete("/{id}")
@inject
async def delete_job(
    id: int,
    job_repository: JobRepository = Depends(Provide[RepositoriesContainer.job_repository]),
    current_user: User = Depends(get_current_user),
) -> JobSchema:
    job = await job_repository.retrieve(id=id)
    if not job or job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

    try:
        deleted_job = await job_repository.delete(id)
        return JobSchema(**asdict(deleted_job))
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")

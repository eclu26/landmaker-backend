from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4

from app.database import get_session
from app.models.project import Project
from app.schemas.project import GetProjectResponse, CreateProjectRequest, CreateProjectResponse

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.get("/{project_id}", response_model=GetProjectResponse)
async def get_project(project_id: UUID, session: AsyncSession = Depends(get_session)) -> GetProjectResponse:
    result = await session.execute(
        select(Project).where(Project.id == project_id)
    )

    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return project

@router.post("/", response_model=CreateProjectResponse)
async def create_project(project: CreateProjectRequest, 
                         session: AsyncSession = Depends(get_session)) -> CreateProjectResponse:
    new_project = Project(
        id=uuid4(),
        name=project.name,
        description=project.description
    )

    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)

    return new_project
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4

from app.database import get_session
from app.models.project import Project
from app.schemas.project import GetProjectResponse, CreateProjectRequest, CreateProjectResponse
from app.functions.database import get_project_rq, create_project_rq

router = APIRouter(
    prefix="/api/v1/projects",
    tags=["Projects"]
)

@router.get("/{project_id}", response_model=GetProjectResponse)
async def get_project(project_id: UUID, session: AsyncSession = Depends(get_session)) -> GetProjectResponse:
    project = await get_project_rq(session, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return project

@router.post("/", response_model=CreateProjectResponse)
async def create_project(project: CreateProjectRequest, 
                         session: AsyncSession = Depends(get_session)) -> CreateProjectResponse:
    new_project = await create_project_rq(session, project.name, project.description)
    return new_project
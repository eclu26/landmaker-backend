from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_session
from app.schemas.project import GetProjectResponse, CreateProjectRequest, CreateProjectResponse
from app.functions.database import get_project_rq, create_project_rq
from app.functions.security import verify_jwt

router = APIRouter(
    prefix="/api/v1/projects",
    tags=["Projects"]
)

@router.get("/{project_id}", response_model=GetProjectResponse)
async def get_project(project_id: UUID, 
                      session: AsyncSession = Depends(get_session), 
                      user_id: UUID = Depends(verify_jwt)) -> GetProjectResponse:
    project = await get_project_rq(session, project_id, user_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return project

@router.post("/", response_model=CreateProjectResponse)
async def create_project(project: CreateProjectRequest, 
                         session: AsyncSession = Depends(get_session), 
                         user_id: UUID = Depends(verify_jwt)) -> CreateProjectResponse:
    new_project = await create_project_rq(session, user_id, project.name, project.description)
    return new_project
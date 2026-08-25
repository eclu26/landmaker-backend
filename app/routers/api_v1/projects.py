from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4

from app.database import get_session
from app.schemas.project import(
    GetProjectResponse, 
    CreateProjectRequest, 
    CreateProjectResponse, 
    GenerateHTMLRequest, 
    GenerateHTMLResponse
)
from app.functions.database import (
    get_project_rq, 
    get_projects_rq, 
    create_project_rq
)
from app.functions.s3 import save_new_html_rq
from app.functions.ai import generate_html
from app.functions.security import verify_jwt

router = APIRouter(
    prefix="/api/v1/projects",
    tags=["Projects"]
)

@router.post("/", response_model=CreateProjectResponse)
async def create_project(project: CreateProjectRequest, 
                         session: AsyncSession = Depends(get_session), 
                         user_id: UUID = Depends(verify_jwt)) -> CreateProjectResponse:
    new_project = await create_project_rq(session, user_id, project.name, project.description)
    return new_project

@router.get("/", response_model=list[GetProjectResponse])
async def get_projects(session: AsyncSession = Depends(get_session), user_id: UUID = Depends(verify_jwt)):
    return await get_projects_rq(session, user_id)

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

@router.post("/{project_id}/generate", response_model=GenerateHTMLResponse)
async def generate_project(project_id: UUID, body: GenerateHTMLRequest,
                      session: AsyncSession = Depends(get_session), 
                      user_id: UUID = Depends(verify_jwt)) -> GetProjectResponse:
    project = await get_project_rq(session, project_id, user_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    html = await generate_html(body.prompt, None)
    
    html_id = await save_new_html_rq(project_id, html)

    project.current_html = html_id
    await session.commit()
    await session.refresh(project)

    return GenerateHTMLResponse(
        html_id=html_id,
        html=html
    )


@router.post("/{project_id}/publish")
async def publish_project(project_id: UUID,
                      session: AsyncSession = Depends(get_session), 
                      user_id: UUID = Depends(verify_jwt)) -> dict:
    project = await get_project_rq(session, project_id, user_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    project.is_published = True
    await session.commit()
    await session.refresh(project)

    return {"detail":"Landing was published"}
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.project import Project
from app.schemas.project import GetProjectResponse
from app.functions.database import get_project
from app.functions.s3 import get_html

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

@router.get("/{project_id}", response_class=HTMLResponse)
async def get_project_html(project_id: UUID, session: AsyncSession = Depends(get_session)) -> HTMLResponse:
    project = await get_project(session, project_id)
    
    
    if project is None:
        raise HTTPException(status_code=404)
    else:
        current_html = GetProjectResponse.model_validate(project).current_html

    html_content = await get_html(project_id, current_html)

    return HTMLResponse(content=html_content)
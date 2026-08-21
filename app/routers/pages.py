from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.project import GetProjectResponse
from app.functions.database import get_project_non_admin_rq
from app.functions.s3 import get_html_rq

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

@router.get("/{project_id}", response_class=HTMLResponse)
async def get_project_html(project_id: UUID, session: AsyncSession = Depends(get_session)) -> HTMLResponse:
    project = await get_project_non_admin_rq(session, project_id)
    
    if project is None:
        raise HTTPException(
                    status_code=404,
                    detail="Project not found",
                )
    else:
        current_html = GetProjectResponse.model_validate(project).current_html

    if current_html is None:
        raise HTTPException(
                    status_code=404,
                    detail="Landing isn't published",
                )
    else:
        html_content = await get_html_rq(project_id, current_html)

    return HTMLResponse(content=html_content)
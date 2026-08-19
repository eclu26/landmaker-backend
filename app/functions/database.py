from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project

async def get_project(session: AsyncSession, project_id: UUID) -> Project | None:
    result = await session.execute(
        select(Project).where(Project.id == project_id)
    )

    return result.scalar_one_or_none()
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project

async def get_project_rq(session: AsyncSession, project_id: UUID) -> Project | None:
    result = await session.execute(
        select(Project).where(Project.id == project_id)
    )

    return result.scalar_one_or_none()

async def create_project_rq(session: AsyncSession, name: str, description: str) -> Project:
    new_project = Project(
        id=uuid4(),
        name=name,
        description=description
    )

    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)

    return new_project
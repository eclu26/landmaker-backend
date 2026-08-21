from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.user import User

async def get_projects_rq(session: AsyncSession, user_id: UUID) -> list[Project]:
    result = await session.execute(
        select(Project).where(Project.user_id == user_id)
    )

    return list(result.scalars().all())

async def get_project_rq(session: AsyncSession, project_id: UUID, user_id: UUID) -> Project | None:
    result = await session.execute(
        select(Project).where(Project.id == project_id, Project.user_id == user_id)
    )

    return result.scalar_one_or_none()

async def get_project_non_admin_rq(session: AsyncSession, project_id: UUID) -> Project | None:
    result = await session.execute(
        select(Project).where(Project.id == project_id)
    )

    return result.scalar_one_or_none()

async def create_project_rq(session: AsyncSession, user_id: UUID, name: str, description: str) -> Project:
    new_project = Project(
        id=uuid4(),
        user_id=user_id,
        name=name,
        description=description
    )

    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)

    return new_project

async def get_user_by_email_rq(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(
        select(User).where(User.email == email)
    )

    return result.scalar_one_or_none()

async def get_user_by_uuid_rq(session: AsyncSession, user_id: UUID) -> User | None:
    result = await session.execute(
        select(User).where(User.id == user_id)
    )

    return result.scalar_one_or_none()

async def create_user_rq(session: AsyncSession, email: str, password_hash: str) -> User:
    new_user = User(
        id=uuid4(),
        email=email,
        password_hash=password_hash
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user
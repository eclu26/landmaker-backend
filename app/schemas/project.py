from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class GetProjectResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: str | None
    current_html: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class CreateProjectRequest(BaseModel):
    name: str
    description: str | None = None

class CreateProjectResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: str | None

    model_config = {
        "from_attributes": True
    }
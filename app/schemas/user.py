from uuid import UUID

from pydantic import BaseModel

class CommonUserRequest(BaseModel):
    email: str
    password: str

class CreateUserResponse(BaseModel):
    id: UUID
    email: str

    model_config = {
        "from_attributes": True
    }

class AuthUserResponse(BaseModel):
    id: UUID
    email: str
    jwt: str
    
    model_config = {
        "from_attributes": True
    }
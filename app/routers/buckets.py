from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import boto3
from uuid import UUID

from app.settings import settings

s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{settings.s3_host}:{settings.s3_port}",
    aws_access_key_id=settings.s3_access_key,
    aws_secret_access_key=settings.s3_secret_key,
    region_name=settings.s3_region
)

router = APIRouter(
    prefix="/buckets",
    tags=["Buckets"]
)

@router.get("/{project_id}/get-html-by-uuid/{html_id}", response_class=HTMLResponse)
async def get_html_by_uuid(project_id: UUID, html_id: UUID) -> str:
    response = s3.get_object(
        Bucket=str(project_id),
        Key=f"htmls/{str(html_id)}.html"
    )

    #return response["Body"].read().decode("utf-8")
    return HTMLResponse(content=response["Body"].read().decode("utf-8"))
import boto3
from uuid import UUID, uuid4

from app.settings import settings

s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{settings.s3_host}:{settings.s3_port}",
    aws_access_key_id=settings.s3_access_key,
    aws_secret_access_key=settings.s3_secret_key,
    region_name=settings.s3_region
)

async def get_html_rq(project_id: UUID, html_id: UUID) -> str:
    response = s3.get_object(
        Bucket=settings.s3_bucket,
        Key=f"{str(project_id)}/htmls/{str(html_id)}.html"
    )

    return response["Body"].read().decode("utf-8")

async def save_new_html_rq(project_id: UUID, html: str) -> UUID:
    html_id = uuid4()

    s3.put_object(
        Bucket=settings.s3_bucket,
        Key=f"{project_id}/htmls/{html_id}.html",
        Body=html.encode("utf-8"),
        ContentType="text/html; charset=utf-8",
    )

    return html_id
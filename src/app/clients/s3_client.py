import logging
import os
from typing import Optional

import aioboto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, status

from core.config import settings

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class S3Client:
    def __init__(
        self,
        bucket_name: str,
        endpoint_url: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
    ):
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.session = aioboto3.Session()

    async def _get_client(self):
        return self.session.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            endpoint_url=self.endpoint_url,
        )

    async def upload_file(
        self, file_path: str, key: str, content_type: Optional[str] = None
    ):
        """Загрузить файл в S3."""
        try:
            async with await self._get_client() as s3_client:
                extra_args = {"ContentType": content_type} if content_type else {}
                await s3_client.upload_file(
                    Filename=file_path,
                    Bucket=self.bucket_name,
                    Key=key,
                    ExtraArgs=extra_args,
                )
                log.info("Файл %s загружен как %s", file_path, key)
                os.remove(file_path)
                return key
        except ClientError as e:
            log.error("Ошибка при загрузке файла %s: %s", file_path, e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при загрузке файла в S3",
            )

    async def delete_file(self, key: str):
        """Удалить файл из S3."""
        try:
            async with await self._get_client() as s3_client:
                await s3_client.delete_object(Bucket=self.bucket_name, Key=key)
                log.info("Файл %s удален из S3", key)
        except ClientError as e:
            log.error("Ошибка при удалении файла %s: %s", key, e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при удалении файла из S3",
            )

    async def delete_files(self, keys: list[str]):
        """Удалить файлы из S3 по списку ключей (URL)."""
        try:
            async with await self._get_client() as s3_client:
                await s3_client.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={"Objects": [{"Key": key} for key in keys]},
                )
                log.info("Файлы %s удалены из S3", keys)
        except ClientError as e:
            log.error("Ошибка при удалении файлов: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при удалении файлов из S3",
            )

    async def copy_file(
        self, source_bucket: str, source_key: str, destination_key: str
    ):
        """Скопировать файл внутри S3 между бакетами или по ключам."""
        try:
            async with await self._get_client() as s3_client:
                copy_source = {
                    "Bucket": source_bucket,
                    "Key": source_key,
                }
                await s3_client.copy_object(
                    CopySource=copy_source,
                    Bucket=self.bucket_name,
                    Key=destination_key,
                )
                log.info(
                    "Файл %s скопирован из %s в %s/%s",
                    source_key,
                    source_bucket,
                    self.bucket_name,
                    destination_key,
                )
                return destination_key
        except ClientError as e:
            log.error("Ошибка при копировании файла: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при копировании файла в S3",
            )


# Инициализация менеджера S3
s3_client = S3Client(
    bucket_name=settings.s3_client.bucket_name,
    endpoint_url=settings.s3_client.endpoint_url,
    aws_access_key_id=settings.s3_client.aws_access_key_id,
    aws_secret_access_key=settings.s3_client.aws_secret_access_key,
)

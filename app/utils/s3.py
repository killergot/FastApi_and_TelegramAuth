from typing import Tuple, Optional

import boto3
import io

from app.core.config import load_config, Config

def get_s3_client(config: Config):
    return boto3.client(
        's3',
        aws_access_key_id=config.s3.key_id,
        aws_secret_access_key=config.s3.secret,
        region_name=config.s3.region,
        endpoint_url=config.s3.endpoint
    )

config = load_config()
s3_client = get_s3_client(config)
# Инициализация S3 клиента
bucket_name = config.s3.bucket_name


# Функция загрузки файла
def upload_file_to_s3(
        file_content: bytes,
        original_name: str,
        group_number: str,
        subject: str
) -> str:
    # Формируем новое имя файла
    safe_group = group_number.replace('/', '_')
    safe_subject = subject.replace('/', '_')
    new_filename = f"{safe_group}_{safe_subject}_{original_name}"

    # Загружаем файл
    file_obj = io.BytesIO(file_content)
    s3_client.upload_fileobj(file_obj, bucket_name, new_filename)
    print(f"File {new_filename} uploaded to S3")
    return new_filename


# Функция получения файла
def download_file_from_s3(
        file_key: str,
        expected_group: Optional[str] = None,
        expected_subject: Optional[str] = None
) -> Tuple[str, bytes]:

    try:
        # Загружаем файл из S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        content = response['Body'].read()

        # Извлекаем оригинальное имя файла
        parts = file_key.split('_', 2)
        if len(parts) != 3:
            raise ValueError(f"Invalid file key format. Expected 'group_subject_filename', got '{file_key}'")

        group, subject, original_filename = parts

        # Валидация группы и предмета (если указаны)
        if expected_group and group != expected_group.replace('/', '_'):
            raise ValueError(f"Group mismatch. Expected '{expected_group}', got '{group}'")

        if expected_subject and subject != expected_subject.replace('/', '_'):
            raise ValueError(f"Subject mismatch. Expected '{expected_subject}', got '{subject}'")

        return original_filename, content

    except Exception as e:
        print(f"Download failed: {str(e)}")
        raise


# Функция удаления файла
def delete_file_from_s3(
        file_key: str
) -> bool:
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=file_key)
        print(f"File {file_key} deleted from S3")
        return True
    except Exception as e:
        print(f"Deletion failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Тестовые параметры
    test_bucket = config.s3.bucket_name
    test_group = "123"
    test_subject = "123"
    test_filename = "lecture_notes.pdf"

    # Создаем тестовый файл в S3
    test_key = f"{test_group.replace('/', '_')}_{test_subject.replace('/', '_')}_{test_filename}"
    s3_client.put_object(Bucket=test_bucket, Key=test_key, Body=b"Test content")

    try:
        # Загружаем файл с проверкой
        original_name, content = download_file_from_s3(
            s3_client,
            test_bucket,
            test_key,
            expected_group=test_group,
            expected_subject=test_subject
        )

        print(f"Downloaded file '{original_name}' with content: {content[:20]}...")

        # Проверяем, что имя восстановлено правильно
        assert original_name == test_filename
        print("Filename extraction test passed!")

    finally:
        # Удаляем тестовый файл
        s3_client.delete_object(Bucket=test_bucket, Key=test_key)
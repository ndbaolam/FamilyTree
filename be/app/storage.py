from minio import Minio
from minio.error import S3Error
import os
import io

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "minioheader")
BUCKET_NAME = "family-tree-avatars"
PUBLIC_MINIO_URL = os.getenv("PUBLIC_MINIO_URL", "http://localhost:9000")

class MinioClient:
    def __init__(self):
        # Determine if secure connection is needed (default false for local dev)
        secure = os.getenv("MINIO_SECURE", "false").lower() == "true"
        
        self.client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=secure
        )
        self.ensure_bucket()

    def ensure_bucket(self):
        try:
            if not self.client.bucket_exists(BUCKET_NAME):
                self.client.make_bucket(BUCKET_NAME)
                # Set policy to public read for simple avatar access
                policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": ["*"]},
                            "Action": ["s3:GetObject"],
                            "Resource": [f"arn:aws:s3:::{BUCKET_NAME}/*"]
                        }
                    ]
                }
                import json
                self.client.set_bucket_policy(BUCKET_NAME, json.dumps(policy))
                print(f"Bucket {BUCKET_NAME} created with public read policy.")
        except S3Error as e:
            print(f"Error ensuring bucket exists: {e}")

    def upload_file(self, file_content: bytes, file_name: str, content_type: str) -> str | None:
        try:
            # Wrap bytes in BytesIO
            data_stream = io.BytesIO(file_content)
            
            self.client.put_object(
                BUCKET_NAME,
                file_name,
                data_stream,
                length=len(file_content),
                content_type=content_type
            )
            # Return public URL
            return f"{PUBLIC_MINIO_URL}/{BUCKET_NAME}/{file_name}"
        except S3Error as e:
            print(f"Error uploading file: {e}")
            return None

# Initialize singleton
minio_client = MinioClient()

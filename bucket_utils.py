from google.cloud import storage
from google.cloud import storage
from google.api_core import exceptions
from google.api_core.retry import Retry
from builtins import str
from constants import PROJECT_ID,BUCKET_NAME
_MY_RETRIABLE_TYPES = [
    exceptions.TooManyRequests,  # 429
    exceptions.InternalServerError,  # 500
    exceptions.BadGateway,  # 502
    exceptions.ServiceUnavailable,  # 503
]

def is_retryable(exc):
    return isinstance(exc, _MY_RETRIABLE_TYPES)


my_retry_policy = Retry(predicate=is_retryable)

gcp_project = PROJECT_ID
gcp_bucket_name = BUCKET_NAME

storage_client = storage.Client(project=gcp_project)
bucket = storage_client.bucket(gcp_bucket_name)

def upload_to_bucket(local: str, user_id: str, doc_id: str, type: str,extension):
    destination = f"{user_id}/{doc_id}_{type}_{extension}.{extension}"
    bucket.blob(destination).upload_from_filename(local)

def download_from_bucket(user_id,doc_id,type,extension):
    blob = bucket.blob(f"{user_id}/{doc_id}_{type}_{extension}.{extension}")
    content = blob.download_as_bytes()
    return content
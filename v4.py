import datetime

from google.cloud import storage


def generate_download_signed_url_v4(bucket_name, blob_name):
    storage_client = storage.Client.from_service_account_json('gcplab-404301-18a6ad31e8c0.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method="GET",
    )

    return url

print(generate_download_signed_url_v4('my-test-bucket-5s', 'cloudtrail.json'))
# Imports the Google Cloud client library
import logging
from google.cloud import storage

# upload_blob("aucr", "test", "test2")


def implicit():
    """
    If you don't specify credentials when constructing the client, the
    client library will look for credentials in the environment.
    """
    storage_client = storage.Client()
    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    logging.info(buckets)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Upload a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    logging.info('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Download a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    logging.info(('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name)))

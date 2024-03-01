import os
import shutil
from collections.abc import Generator
from contextlib import closing
from typing import Union

import boto3
from botocore.exceptions import ClientError


class StorageConfig:
    """
    The StorageConfig class is used to configure the storage system.
    It can be configured to use either a local file system or Amazon S3.
    """

    def __init__(self):
        """
        Initializes a new instance of the StorageConfig class.
        """
        self.storage_type = None
        self.local_path = None
        self.s3_bucket_name = None
        self.s3_access_key = None
        self.s3_secret_key = None
        self.s3_endpoint = None
        self.s3_region = None

    @classmethod
    def local(cls, local_path: str):
        """
        Configures the storage system to use a local file system.

        Args:
            local_path (str): The path to the local directory to be used for storage.

        Returns:
            StorageConfig: A configured instance of the StorageConfig class.
        """
        conf = StorageConfig()
        conf.storage_type = 'local'
        conf.local_path = local_path

        return conf

    @classmethod
    def s3(cls, bucket_name: str, access_key: str, secret_key: str, endpoint: str, region: str):
        """
        Configures the storage system to use Amazon S3.

        Args:
            bucket_name (str): The name of the S3 bucket to be used for storage.
            access_key (str): The access key for the S3 service.
            secret_key (str): The secret key for the S3 service.
            endpoint (str): The endpoint for the S3 service.
            region (str): The region for the S3 service.

        Returns:
            StorageConfig: A configured instance of the StorageConfig class.
        """
        conf = StorageConfig()
        conf.storage_type = 's3'
        conf.s3_bucket_name = bucket_name
        conf.s3_access_key = access_key
        conf.s3_secret_key = secret_key
        conf.s3_endpoint = endpoint
        conf.s3_region = region

        return conf


class Storage:
    def __init__(self):
        self.storage_type: str = ''
        self.bucket_name: str = ''
        self.client = None
        self.folder: str = ''

    def init(self, conf: StorageConfig):
        self.storage_type = conf.storage_type
        if self.storage_type == 's3':
            self.bucket_name = conf.s3_bucket_name
            self.client = boto3.client(
                's3',
                aws_secret_access_key=conf.s3_secret_key,
                aws_access_key_id=conf.s3_access_key,
                endpoint_url=conf.s3_endpoint,
                region_name=conf.s3_region
            )
        else:
            self.folder = conf.local_path

    def save(self, filename, data):
        if self.storage_type == 's3':
            self.client.put_object(Bucket=self.bucket_name, Key=filename, Body=data)
        else:
            if not self.folder or self.folder.endswith('/'):
                filename = self.folder + filename
            else:
                filename = self.folder + '/' + filename

            folder = os.path.dirname(filename)
            os.makedirs(folder, exist_ok=True)

            with open(os.path.join(os.getcwd(), filename), "wb") as f:
                f.write(data)

    def load(self, filename: str, stream: bool = False) -> Union[bytes, Generator]:
        if stream:
            return self.load_stream(filename)
        else:
            return self.load_once(filename)

    def load_once(self, filename: str) -> bytes:
        if self.storage_type == 's3':
            try:
                with closing(self.client) as client:
                    data = client.get_object(Bucket=self.bucket_name, Key=filename)['Body'].read()
            except ClientError as ex:
                if ex.response['Error']['Code'] == 'NoSuchKey':
                    raise FileNotFoundError("File not found")
                else:
                    raise
        else:
            if not self.folder or self.folder.endswith('/'):
                filename = self.folder + filename
            else:
                filename = self.folder + '/' + filename

            if not os.path.exists(filename):
                raise FileNotFoundError("File not found")

            with open(filename, "rb") as f:
                data = f.read()

        return data

    def load_stream(self, filename: str) -> Generator:
        def generate(filename: str = filename) -> Generator:
            if self.storage_type == 's3':
                try:
                    with closing(self.client) as client:
                        response = client.get_object(Bucket=self.bucket_name, Key=filename)
                        for chunk in response['Body'].iter_chunks():
                            yield chunk
                except ClientError as ex:
                    if ex.response['Error']['Code'] == 'NoSuchKey':
                        raise FileNotFoundError("File not found")
                    else:
                        raise
            else:
                if not self.folder or self.folder.endswith('/'):
                    filename = self.folder + filename
                else:
                    filename = self.folder + '/' + filename

                if not os.path.exists(filename):
                    raise FileNotFoundError("File not found")

                with open(filename, "rb") as f:
                    while chunk := f.read(4096):  # Read in chunks of 4KB
                        yield chunk

        return generate()

    def download(self, filename, target_filepath):
        if self.storage_type == 's3':
            with closing(self.client) as client:
                client.download_file(self.bucket_name, filename, target_filepath)
        else:
            if not self.folder or self.folder.endswith('/'):
                filename = self.folder + filename
            else:
                filename = self.folder + '/' + filename

            if not os.path.exists(filename):
                raise FileNotFoundError("File not found")

            shutil.copyfile(filename, target_filepath)

    def exists(self, filename):
        if self.storage_type == 's3':
            with closing(self.client) as client:
                try:
                    client.head_object(Bucket=self.bucket_name, Key=filename)
                    return True
                except:
                    return False
        else:
            if not self.folder or self.folder.endswith('/'):
                filename = self.folder + filename
            else:
                filename = self.folder + '/' + filename

            return os.path.exists(filename)


storage = Storage()


def init(conf: StorageConfig):
    storage.init(conf)

import os
import sys
from datetime import datetime, timedelta

import boto3
from dateutil.tz import tzutc

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_ACCESS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")


class S3Utils:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_ACCESS_SECRET_KEY,
        )

    def get_s3_objects(self, file_path):
        """
        Retrieves an object from an S3 bucket.

        Args:
            file_path (str): The path of the file in the S3 bucket.

        Returns:
            dict: The response object containing the retrieved object.

        """
        res = self.client.get_object(Bucket=S3_BUCKET_NAME, Key=file_path)
        return res

    def download_s3_file(self, local_file_name, s3_object_key):
        meta_data = self.client.head_object(Bucket=S3_BUCKET_NAME, Key=s3_object_key)
        total_length = int(meta_data.get("ContentLength", 0))
        downloaded = 0

        def progress(chunk):
            nonlocal downloaded
            downloaded += chunk
            done = int(50 * downloaded / total_length)
            sys.stdout.write("\r[%s%s]" % ("=" * done, " " * (50 - done)))
            sys.stdout.flush()

        with open(local_file_name, "wb") as f:
            self.client.download_fileobj(
                S3_BUCKET_NAME, s3_object_key, f, Callback=progress
            )

        print(
            f"\nDownloaded {local_file_name} from S3 bucket {S3_BUCKET_NAME} Key {s3_object_key}"
        )

    def upload_file_to_s3(self, file_path, uploadto):
        """
        Uploads a file to Amazon S3.

        Args:
            file_path (str): The path of the file to be uploaded.
            uploadto (str): The destination folder in S3 where the file will be uploaded.

        Returns:
            str: The downloadable URL of the uploaded file.
        """
        self.client.upload_file(
            Bucket=S3_BUCKET_NAME,
            Filename=file_path,
            Key=uploadto,
        )

    def upload_folder_to_s3(self, local_folder, s3_folder):
        """
        Uploads all files in a local folder to a specified S3 folder.

        Args:
            local_folder (str): The path to the local folder containing the files to upload.
            s3_folder (str): The path to the S3 folder where the files will be uploaded.

        Returns:
            None
        """
        for root, dirs, files in os.walk(local_folder):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_folder)
                s3_path = os.path.join(s3_folder, relative_path)
                self.client.upload_file(local_path, S3_BUCKET_NAME, s3_path)

    def upload_file_text_to_s3(self, text, uploadto):
        """
        Uploads a text file to an S3 bucket.

        Args:
            text (str): The text content to be uploaded.
            uploadto (str): The key or path where the file will be uploaded in the S3 bucket.

        Returns:
            None
        """
        self.client.put_object(Bucket=S3_BUCKET_NAME, Key=uploadto, Body=text)

    def download_folder_from_s3(self, s3_folder, local_folder):
        # Get all objects in the S3 folder
        response = self.client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=s3_folder)

        if response.get("Contents"):
            objects = response["Contents"]

            # Download each object
            for obj in objects:
                s3_path = obj["Key"]
                local_path = os.path.join(
                    local_folder, os.path.relpath(s3_path, s3_folder)
                )
                local_dir = os.path.dirname(local_path)

                # Create local directories if they don't exist
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)

                # Download the object
                print(local_path)
                self.client.download_file(S3_BUCKET_NAME, s3_path, local_path)
            return True
        else:
            return False

    def filterd_list_md5_checksum(self, directory_name):
        """
        Filters the list of objects in the specified S3 bucket directory based on the last modified
        timestamp and file extensions.

        Args:
            directory_name (str): The name of the S3 bucket directory to filter.

        Returns:
            list: A list of MD5 checksums for the filtered S3 objects.
        """
        condition_timestamp = datetime.now(tz=tzutc()) - timedelta(minutes=5)
        paginator = self.client.get_paginator("list_objects_v2")
        s3_filtered_list = []

        for page in paginator.paginate(Bucket=S3_BUCKET_NAME, Prefix=directory_name):
            if "Contents" in page:
                for obj in page["Contents"]:
                    if obj["LastModified"] > condition_timestamp and (
                        obj["Key"].lower().endswith(".pdf")
                        or obj["Key"].lower().endswith(".txt")
                    ):
                        s3_filtered_list.append(obj)

        object_md5_checksums = [obj["ETag"].strip('"') for obj in s3_filtered_list]

        return object_md5_checksums

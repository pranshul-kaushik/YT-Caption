import os

from utils.s3_utils import S3Utils

S3 = S3Utils()


def upload_captions(uuid, local_file_paths):
    for local_file_path in local_file_paths:
        S3.upload_file_to_s3(
            local_file_path, f"{uuid}/captions/{os.path.basename(local_file_path)}"
        )
        os.remove(local_file_path)


def upload_document(uuid, local_file_path):
    S3.upload_file_to_s3(local_file_path, f"{uuid}/{os.path.basename(local_file_path)}")
    os.remove(local_file_path)


def dowload_document(uuid, local_file_path):
    S3.download_folder_from_s3(
        f"{uuid}/{os.path.basename(local_file_path)}", local_file_path
    )

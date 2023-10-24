#!/bin/python3

import sys
import os
import boto3

import standard_utils

CLIENT_CONFIG_FILE = "./configs.yml"
CLIENT_CONFIG = dict()

def download_from_s3(target_repo, local_filepath, s3_filepath):
    REPO_NAME = CLIENT_CONFIG["s3"]["storage-alias"][target_repo]
    BUCKET_NAME = CLIENT_CONFIG["s3"]["bucket-name"]
    KEY_FILEPATH = CLIENT_CONFIG["access"]["key-filepath"]

    s3_filepath_token = [ t for t in s3_filepath.split("/") if not t in [".", ""] ]
    s3_filepath = "/".join(s3_filepath_token)

    full_filepath = os.path.abspath(local_filepath)
    full_keypath = "{repo_name}/{s3_filepath}".format(repo_name=REPO_NAME, s3_filepath=s3_filepath)

    print("OPERATION SUMMARY")
    print("PULL : {full_filepath} <- {full_keypath}".format(full_filepath=full_filepath, full_keypath=full_keypath))

    client = standard_utils.init_boto3_client("s3", KEY_FILEPATH)
    client.download_file(Bucket=BUCKET_NAME, Key=full_keypath, Filename=full_filepath)

    return 0

# This method is to help allow other scripts to use the
# functinoality of download.py without needing to rewrite the functionality from scratch
def api_download_from_s3(client_config, target_repo, local_filepath, s3_filepath):
    global CLIENT_CONFIG, TARGET_REPO
    CLIENT_CONFIG = client_config
    return download_from_s3(target_repo, local_filepath, s3_filepath)

def help_message():
    print("USAGE: {} <TARGET_REPO> <TARGET_FILEPATH> <S3_FILEPATH>".format(sys.argv[0]))
    return

if __name__ == "__main__":
    mandatory_arguments = []
    try:
        (mandatory_arguments, _) = standard_utils.get_arguments( sys.argv, 3 )
    except ValueError:
        help_message()
        exit(1)
    [_, target_repo, local_filepath, s3_filepath] = mandatory_arguments

    CLIENT_CONFIG = standard_utils.initialize_configs_from_file( CLIENT_CONFIG_FILE ) 

    output = download_from_s3(target_repo, local_filepath, s3_filepath)

#!/bin/python3

import sys
import os
import boto3

import standard_utils

CLIENT_CONFIG_FILE = "./configs.yml"
CLIENT_CONFIG = dict()

def upload_file_to_s3(target_repo, local_filepath, s3_filepath):
    REPO_NAME = CLIENT_CONFIG["s3"]["storage-alias"][target_repo]
    BUCKET_NAME = CLIENT_CONFIG["s3"]["bucket-name"]
    KEY_FILEPATH = CLIENT_CONFIG["access"]["key-filepath"]

    s3_filepath_token = [ t for t in s3_filepath.split("/") if not t in [".", ""] ]
    s3_filepath = "/".join(s3_filepath_token)

    full_filepath = os.path.abspath(local_filepath)
    full_keypath = "{repo_name}/{s3_filepath}".format(repo_name=REPO_NAME, s3_filepath=s3_filepath)

    print("OPERATION SUMMARY")
    print("PUSH : {full_filepath} -> {full_keypath}".format(full_filepath=full_filepath, full_keypath=full_keypath))

    client = standard_utils.init_boto3_client("s3", KEY_FILEPATH) 
    client.upload_file(full_filepath, BUCKET_NAME, full_keypath)

    return 0

def help_message():
    print("USAGE: {} <TARGET_REPO> <LOCAL_FILEPATH> <S3_FILEPATH>".format(sys.argv[0]))
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

    exit_code = upload_file_to_s3(target_repo, local_filepath, s3_filepath)
    exit(exit_code)

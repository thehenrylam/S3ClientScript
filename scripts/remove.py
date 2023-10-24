#!/bin/python3

import sys
import os

import list
import standard_utils

CLIENT_CONFIG_FILE = "./configs.yml"
CLIENT_CONFIG = dict()
TARGET_REPO = None

def delete_file(client, filepath):
    bucket_name = CLIENT_CONFIG["s3"]["bucket-name"]

    print("REMOVE : {}".format(filepath))
    client.delete_object(Bucket=bucket_name, Key=filepath)

    return

def remove_from_s3(filepath):
    if (len(filepath) == 0):
        print("ERROR: Unable to accept the filepath to be an empty string")
        exit(1)
    
    print("OPERATION SUMMARY")

    key_filepath = CLIENT_CONFIG["access"]["key-filepath"]

    client = standard_utils.init_boto3_client("s3", key_filepath)

    s3_object_list = list.api_list_s3_objects(CLIENT_CONFIG, TARGET_REPO, filepath)
    s3_filepaths = [ s["Key"] for s in s3_object_list if "Key" in s ]

    for f in s3_filepaths:
        delete_file( client, f )

    return

def help_message():
    print("USAGE: {} <TARGET_REPO> <S3_FILEPATH>".format(sys.argv[0]))
    return

if __name__ == "__main__":
    mandatory_arguments = []
    try:
        (mandatory_arguments, _) = standard_utils.get_arguments( sys.argv, 2 )
    except ValueError:
        help_message()
        exit(1)
    [_, TARGET_REPO, s3_filepath] = mandatory_arguments

    CLIENT_CONFIG = standard_utils.initialize_configs_from_file( CLIENT_CONFIG_FILE )

    output = remove_from_s3(s3_filepath)


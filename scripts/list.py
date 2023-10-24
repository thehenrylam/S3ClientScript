#!/bin/python3

import sys
import boto3
import datetime
from dateutil.tz import tzutc
from operator import itemgetter

import standard_utils

CLIENT_CONFIG_FILE = "./configs.yml"
CLIENT_CONFIG = dict()
TARGET_REPO = None

def s3_list_objects(client, bucket_name, prefix, continuation_token=None):
    result = dict()
    if continuation_token != None:
        result = client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, ContinuationToken=continuation_token)
    else:
        result = client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    contents = result["Contents"] if "Contents" in result else []

    next_continuation_token = result["NextContinuationToken"] if "NextContinuationToken" in result else None

    return (contents, next_continuation_token)

def generate_list_of_s3_objects(s3_filepath):
    REPO_NAME = CLIENT_CONFIG["s3"]["storage-alias"][TARGET_REPO]
    bucket_name = CLIENT_CONFIG["s3"]["bucket-name"]
    key_filepath = CLIENT_CONFIG["access"]["key-filepath"]

    full_s3_filepath = "{}/{}".format(REPO_NAME, s3_filepath)

    client = standard_utils.init_boto3_client("s3", key_filepath)

    full_content = []

    (contents, next_continuation_token) = s3_list_objects(client, bucket_name, full_s3_filepath)
    full_content += contents

    while (next_continuation_token != None):
        (contents, next_continuation_token) = s3_list_objects(client, bucket_name, full_s3_filepath, next_continuation_token)
        full_content += contents

    sorted_full_content = sorted(full_content, key=itemgetter("LastModified"))

    return sorted_full_content

# This method is to help allow other scripts to use the 
# functionality of list.py without needing to rewrite the funtionality from scratch
def api_list_s3_objects(client_config, target_repo, filepath):
    global CLIENT_CONFIG, TARGET_REPO
    CLIENT_CONFIG = client_config
    TARGET_REPO = target_repo
    return generate_list_of_s3_objects(filepath)

def help_message():
    print("USAGE: {} <TARGET_REPO> [Optional: S3_FILEPATH]".format(sys.argv[0]))
    return

if __name__ == "__main__":
    mandatory_arguments, optional_arguments = [], []
    try:
        (mandatory_arguments, optional_arguments) = standard_utils.get_arguments( sys.argv, 1, 2 )
    except ValueError:
        help_message()
        exit(1)
    [_, TARGET_REPO] = mandatory_arguments
    [s3_filepath] = optional_arguments

    CLIENT_CONFIG = standard_utils.initialize_configs_from_file( CLIENT_CONFIG_FILE )

    s3_object_list = generate_list_of_s3_objects( s3_filepath )
    # Output the result for shell scripts to capture its output
    [ print( s["Key"] ) for s in s3_object_list if "Key" in s ]

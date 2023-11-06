#!/bin/python3

import sys
import os

import download
import standard_utils

CLIENT_CONFIG_FILE = "./configs.yml"

def split_filepath_by_name_and_path(filepath):
    filepath_tokens = filepath.split('/')
    filename = filepath_tokens[-1]
    dirpath = "/".join(filepath_tokens[:-1]) + "/"
    return [filename, dirpath]

def main(nxp_filepath):
    # Get the full nxp filepath
    full_nxp_filepath = os.path.abspath(nxp_filepath) 
    # Split the nxp filepath into the filename and dirpath
    [_, nxp_dirpath] = split_filepath_by_name_and_path(full_nxp_filepath)

    list_of_nexpulls = []
    with open(full_nxp_filepath) as fp:
        lines = fp.readlines()
        for i, incoming_line in enumerate(lines):
            # Strip out whitespace for each line
            l = incoming_line.strip()
            # If the line is empty, then skip it
            if (len(l) == 0):
                continue
            # If the line starts with a "#", then its a comment (Skip it)
            if (l[0] == '#'):
                continue
            # Attempt to split the token by the ',' character
            l_token = l.split(',')
            # If the l_token does not cleanly split into exactly two segments, raise it as an Error
            if (len(l_token) != 2):
                raise ValueError("ERROR: Line {} - Non-valid line detected: '{}'".format(i, l))
            # Add the l_token into the list of nexpulls
            list_of_nexpulls.append( l_token )

    for [repo_alias, s3_filepath] in list_of_nexpulls: 
        # Get the s3' object name
        [s3_object_name, _] = split_filepath_by_name_and_path(s3_filepath)
        # Combine the nxp_dirpath with the object name to create the destination path
        nxp_destination_path = "{}/{}".format(nxp_dirpath, s3_object_name)
        # Perform the download
        download.api_download_from_s3(CLIENT_CONFIG, repo_alias, nxp_destination_path, s3_filepath)

    return


def help_message():
    print("USAGE: {} <FILEPATH_OF_NXP_FILE>.nxp".format(sys.argv[0]))
    return

if __name__ == "__main__":
    mandatory_arguments = []
    try:
        (mandatory_arguments, _) = standard_utils.get_arguments( sys.argv, 1 )
    except ValueError:
        help_message()
        exit(1)
    [_, nxp_filepath] = mandatory_arguments

    CLIENT_CONFIG = standard_utils.initialize_configs_from_file( CLIENT_CONFIG_FILE )

    output = main(nxp_filepath)

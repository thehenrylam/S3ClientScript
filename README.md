# S3ClientScript

## Overview

A suite of helper scripts to perform the following actions for an S3 bucket:
* List
* Get
* Set
* NexPull (Aggregated Get requests determined by a `*.nxp` file)

This is typically used to allow a host (inside or outside AWS) to easily interact with an S3 Bucket.

**IMPORTANT:** Do not use this for client-side hosts. There is a high risk that malicious actors to steal the keys and grant access. 

## Best Practices
* Use this repository in a backend, and ideally having a reverse proxy to avoid direct exposure to the internet
* Keep the ansible key in a safe location, and do not share it with anyone
* Make sure that the key generated has minimal rights granted to it:
    * Make sure you are creating a new (non-root) user to have these keys
    * Only S3 DOWNLOAD, UPLOAD, REMOVE, and LIST permissions (These scripts won't need anything more)
    * Set the permissions to only work on the bucket that these scripts will be interacting with.
* If you suspect that the Ansible key or the AWS key has been leaked, perform the following actions immediately:
    * Delete the key in AWS IAM and regenerate a new one
    * Regenerate a new Ansible key and put its designated file
    * Recreate the secrets.yml file using the helper scripts (`./create-secrets.sh`)

## Setups

1. Create an ansible key file
    * `cd <reachable_directory>`
    * `vi ansible.key` (Put a strong password in there)
2. `cd <appdir>/secrets/ && ./create-secrets.sh` (Create the `secrets.yml` file)

``` YAML
# ./secrets.yml
access-key:
    id: "ACCESS_KEY_ID_FROM_AWS"
    secret: "ACCESS_KEY_SECRET_FROM_AWS"
```

3. `cd <appdir> && cp ./configs.TEMPLATE.yml ./configs.yml && vi ./configs.yml` (Initialize the `configs.yml` file)

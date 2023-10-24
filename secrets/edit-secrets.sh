#!/bin/bash

VAULT_PASSWORD_FILE="$1"
SECRETS_FILE="secrets.yml"
ansible-vault edit --vault-password-file "${VAULT_PASSWORD_FILE}" "${SECRETS_FILE}"

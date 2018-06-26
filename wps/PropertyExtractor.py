import boto3
import logging
import os
from base64 import b64decode

logger = logging.getLogger()
logger.setLevel(logging.INFO)
kms = boto3.client('kms')


def get_serverless_property(property_name):
        encrypted_expected_token = os.environ[property_name]
        return kms.decrypt(CiphertextBlob=b64decode(encrypted_expected_token))['Plaintext'].decode("utf-8")

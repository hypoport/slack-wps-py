"""
This function handles a Slack slash command and echoes the details back to the user.

Follow these steps to configure the slash command in Slack:

  1. Navigate to https://<your-team-domain>.slack.com/services/new

  2. Search for and select "Slash Commands".

  3. Enter a name for your command and click "Add Slash Command Integration".

  4. Copy the token string from the integration settings and use it in the next section.

  5. After you complete this blueprint, enter the provided API endpoint URL in the URL field.


To encrypt your secrets use the following steps:

  1. Create or use an existing KMS Key - http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html

  2. Click the "Enable Encryption Helpers" checkbox

  3. Paste <COMMAND_TOKEN> into the kmsEncryptedToken environment variable and click encrypt


Follow these steps to complete the configuration of your command API endpoint

  1. When completing the blueprint configuration select "Open" for security
     on the "Configure triggers" page.

  2. Enter a name for your execution role in the "Role name" field.
     Your function's execution role needs kms:Decrypt permissions. We have
     pre-selected the "KMS decryption permissions" policy template that will
     automatically add these permissions.

  3. Update the URL for your Slack slash command with the invocation URL for the
     created API resource in the prod stage.
"""

import boto3
import json
import logging
import os

from base64 import b64decode
from urllib.parse import parse_qs

from wps.wpsParser import WpsParser
from wps.wpsRepository import WpsRepository
from wps.commandType import CommandType

ENCRYPTED_EXPECTED_TOKEN = os.environ['kmsEncryptedSlackWpsToken']

kms = boto3.client('kms')
expected_slack_wps_token = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_EXPECTED_TOKEN))['Plaintext'].decode("utf-8")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def wps(event, context):
    params = parse_qs(event['body'])
    token = params['token'][0]
    if token != expected_slack_wps_token:
        logger.error("Request token (%s) does not match expected", token)
        raise Exception('Invalid request token')

    user = params['user_name'][0]
    # params['command'][0]
    channel = params['channel_name'][0]
    command_text = params['text'][0]

    try:
        command = WpsParser().parse(command_text)
        command['user'] = user

        if command['commandType'] == CommandType.GET:
            statuses = WpsRepository().get(command)
            response = 'What we know\n'
            for s in statuses:
                response = response + '@%s has status %s\n' % (s.user_name, s.status)

            return respond(None, response)
        elif command['commandType'] == CommandType.SET:
            WpsRepository().add(command)
            return respond(None, "Status %s saved for user %s" % (command['status'], user))
        else:
            pass

        # TODO WpsRepository().remove(command)

        return respond(None, "%s invoked %s in %s with the following text: %s" % (user, command, channel, command_text))
    except Exception as e:
        logger.error(e)
        return respond(None, "hilfe text %s invoked in %s with the following text: %s" % (user, channel, command_text))

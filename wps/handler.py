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

import logging
from urllib.parse import parse_qs

from wps import PropertyExtractor, slackApi
from wps.commandType import CommandType
from wps.wpsParser import WpsParser
from wps.wpsRepository import WpsRepository

expected_slack_wps_token = PropertyExtractor.get_serverless_property('kmsEncryptedSlackWpsToken')

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
    logger.info("Data from Slack: %s", params)
    token = params['token'][0]
    if token != expected_slack_wps_token:
        logger.error("Request token (%s) does not match expected", token)
        raise Exception('Invalid request token')

    try:
        user = params['user_name'][0]
        # params['command'][0]
        command_text = params['text'][0]

        command = WpsParser().parse(command_text)
        command['user'] = user

        command_type_ = command['commandType']
        if command_type_ == CommandType.GET:
            statuses = WpsRepository().get(command)
            response = create_response_text(statuses)
            return respond(None, response)
        elif command_type_ == CommandType.GET_GROUP:
            users = slackApi.slack_get_userIds_group(command['group'])
            statuses = WpsRepository().get(users)
            response = create_response_text(statuses, 'The following group members have a status\n')
            return respond(None, response)

        elif command_type_ == CommandType.SET:
            WpsRepository().add(command)
            return respond(None, "Status %s saved for user %s" % (command['status'], user))
        elif command_type_ == CommandType.CLEAR:
            WpsRepository().clear(command)
            return respond(None, "Cleared all status of user %s" % user)

        else:
            return respond(None, "Unexpected command - doing nothing")

    except Exception as e:
        logger.error(e)
        return respond(None, "Slack Workplace Status\n"
                             "Usage:\n"
                             "  setting your status\n"
                             "    /wps <status> \n"
                             "    /wps <status> from <date1> to <date2>\n"
                             "    /wps <status> on <date>\n"
                             "  clearing your status\n"
                             "    /wps clear\n"
                             "  getting status\n"
                             "    /wps @user\n"
                             "    /wps @user1 @user2\n"
                             "    /wps @user on <date>\n"
                             "    /wps @user from <date1> to <date2>\n"
                             "\nExamples:\n"
                             "  /wps sick from tomorrow to in 3 days\n"
                             "  /wps remote on tomorrow at 2pm\n"
                             "  /wps @john @jane\n"
                             "  /wps @john on in 3 days\n"
                             "  /wps @john on 23.06.2018\n"
                             "\nFor more details see https://github.com/hypoport/slack-wps-py/blob/master/README.md")


def create_response_text(statuses, start='What we know \n'):
    response = start
    for status in statuses:
        response = response + '@%s is %s from %s to %s\n' % (status.user_name, status.status,
                                                             status.from_date.strftime("%a %d.%m.%y %H:%M"),
                                                             status.to_date.strftime("%a %d.%m.%y %H:%M"))
    return response

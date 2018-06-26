import requests
import json
import sys

ENCRYPTED_EXPECTED_TOKEN = os.environ['kmsEncryptedSlackApiToken']
kms = boto3.client('kms')
token = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_EXPECTED_TOKEN))['Plaintext'].decode("utf-8")

def get_emoji(status):
    if status == 'sick':
        return ':face_with_thermometer:'
    elif status == 'vacation':
        return ':palm_tree:'
    elif status == 'offline':
        return ':sleeping_accommodation:'
    elif status == 'homeoffice':
        return ':house:'
    elif status == 'remote':
        return ':house:'
    elif status == 'workoffice':
        return ':office:'
    else:
        return ''

def slack_update_status(userID, status):
    url = 'https://slack.com/api/users.profile.set'
    emoji = getEmoji(status)

    payload = {}
    payload_profile = {}
    payload['user'] = userID
    payload_profile['status_text'] = status
    payload_profile['status_emoji'] = emoji
    payload['profile'] = payload_profile

    headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + token}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

def slack_get_userIds_channel(channel):
    url = 'https://slack.com/api/conversations.members'
    r = requests.get(url + '?token=' + token + '&channel=' + channel)
    if json.loads(r.text)['ok'] :
        return json.loads(r.text)['members']
    else:
        print('Conversation ' + channel + ' could not be fetched!')
        print(r.text)
        return []

def slack_get_userIds_group(group):
    url = 'https://slack.com/api/usergroups.users.list'
    r = requests.get(url + '?token=' + token + '&usergroup=' + group)
    if json.loads(r.text)['ok'] :
        return json.loads(r.text)['users']
    else:
        print('Group ' + group + ' could not be fetched!')
        print(r.text)
        return []

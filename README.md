# Workplace Status (WPS)

Workplace status `/wps` is a Slack command that helps teams to communicate better
by setting and sharing each worker's status easily.

# Usage

## list all commands

| command | description |
| ---- | ---- |
| `/wps` | gives and overview of what `wps` can do for you |

## status

| status | alternatives |
| ---------- | ----- |
| sick | krank |
| vacation | vacay vaca vac urlaub |
| offline | off |
| homeoffice | ho home |
| remote | rem rmt |
| workoffice | office work wo |

## setting status

| command | description |
| ---- | ---- |
| `/wps <status>` | sets _\<status\>_ for today |
| `/wps <status> from <date1> to <date2>` | sets _\<status\>_ for the specified range |
| `/wps <status> on <date>` | sets _\<status\>_ on the specified date |

## requesting status of colleagues, groups or members of a channel

| command | description |
| ---- | ---- |
| `/wps @john` | shows current status of _@john_ |
| `/wps @group` | shows current status of all members of usergroup _@group_ |
| `/wps @jane @john` | shows current status of _@jane_ and _@john_  |
| `/wps @john on <date>` | shows status on _\<date\>_ of _@john_ |
| `/wps @john from <date1> to <date2>` | shows status for the specified range |
| `/wps #foo | shows status of all members of channel _foo_ |


# CAUTION - work in progress !

All of the above is the wish list for the initial version of `/wps`.
The current code is the result of a hackathon and needs more work on it;)
Nevertheless, it's now open source so that everybody can contribute and
express their interest.

# Installation

TODO description of how to set all up from a client perspective

## current aws parts

AWS Lambda slack-wps-py-prod-wps

## deploy to amazon

run `serverless deploy`

To istall serverless on mac,
* run `npm install -g serverless serverless-python-requirements`

### Setup credentials
https://serverless.com/framework/docs/providers/aws/guide/credentials/

# Roadmap

## integrate with slack status

`wps` should interact with Slack's own status
(see [slack status API](https://api.slack.com/docs/presence-and-status))

## status trigger

`wps` should be able to trigger actions when a status is set.

| command | description |
| ---- | ---- |
| `/wps sick <channel>` | will trigger a _I'm sick_ message in _\<channel\>_ |


# Contributing

Please read [CONTRIBUTING](CONTRIBUTING.md) for details on our code of conduct, and the process
for submitting pull requests to us.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details

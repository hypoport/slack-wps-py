# *W*ork*P*lace *S*tatus (WPS)

Workplace status `/wps` is a slack command that helps teams to communicate better
by setting and sharing each workers status easily.

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

## requesting status of colleagues or groups

| command | description |
| ---- | ---- |
| `/wps @john` | shows current status of _@john_ |
| `/wps @group` | shows current status of all members of usergroup _@group_ |
| `/wps @jane @john` | shows current status of _@jane_ and _@john_  |
| `/wps @john on <date>` | shows status on _\<date\>_ of _@john_ |
| `/wps @john from <date1> to <date2` | shows status for the specified range |


# CAUTION - work in progress !

All of the above is the wish list for the initial version of `/wps`.
The current code is the result of a hackathon and needs more work on it;)
Nevertheless, it's now open source so that everybody can contribute and
express there interest.

# Installation

TODO description of how to set all up from a client perspective

# Roadmap

## integrate with slack status

`wps` should interact with slacks own status
(see [slack status API](https://api.slack.com/docs/presence-and-status))

## status trigger

`wps` should be able to trigger actions, when a status is set.

| command | description |
| ---- | ---- |
| `/wps sick <channel>` | will trigger a _I'm sick_ message in _\<channel\>_ |


# Contributing

Please read [CONTRIBUTING](CONTRIBUTING.md) for details on our code of conduct, and the process
for submitting pull requests to us.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details


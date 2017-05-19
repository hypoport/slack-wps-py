Workplace Status

# Status

sick / Krank
vacation vacay vaca vac / Urlaub
off offline / Abwesend   
homeoffice ho home
remote rem rmt
workoffice office work wo (default)

# Setting your status
- /wps _status_ - setzt _status_ für heute
- /wps _status_ from _datum_ to _datum2_ - setzt _status_ im zeitraum
- /wps _status_ on _datum_ - setzt status für _datum_
- /wps krank -> message an einen channel

# requesting status of colleagues or groups

- /wps @daniel                          -> liefert status von daniel (heute)
- /wps @usergroup                       -> liefert status der gruppe (heute)
- /wps @daniel on _datum_               -> liefert status am angegebenen _datum_
- /wps @daniel @susanne                 -> liefert status von daniel und susanne (heute)
- /wps @daniel from _datum_ to _datum2_ -> liefert status zwischen _datum_ und _datum2_
- /wps -> liefert status aller Teammitglieder

# Roadmap

- integrate with [slack status](https://api.slack.com/docs/presence-and-status)

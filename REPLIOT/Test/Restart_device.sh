#!/bin/bash
NAME_PLUG=$1

python3 kasa-off.py --plugid $NAME_PLUG --username "<TPLink username>" --password "<TPLink Password>"
sleep 5s
python3 kasa-on.py --plugid $NAME_PLUG --username "<TPLink username>" --password "<TPLink Password>"

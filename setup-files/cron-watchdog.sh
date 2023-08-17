#!/bin/bash
echo "Waiting for program start..."
pid=0
timepass=0
timewait=2
maxwait=10
while :; do
    pid=$(pidof python start.py)
    if [[ "$?" != '1' ]]; then
        break
    fi
    sleep $timewait
    ((timepass+=timewait))
    echo "Waited $timepass seconds... (max: $maxwait s)"
    if [[ $timepass -ge $maxwait ]]; then
        echo "MAXTIME REACHED"
        echo "restarting"
        break
    fi
done
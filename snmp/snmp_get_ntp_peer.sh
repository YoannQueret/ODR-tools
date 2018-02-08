#!/bin/sh

NB_PEER_SYNC=`/usr/bin/ntpq -np 2>/dev/null | grep -E '^\*' | wc -l`
echo $NB_PEER_SYNC

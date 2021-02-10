#!/bin/sh
while true
do
sleep 300
date > static/data.txt
git add static/data.txt
git commit -m "Heartbeat"
git push
done

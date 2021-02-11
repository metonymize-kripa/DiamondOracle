#!/bin/sh
while true
do
date > static/data.txt
git add static/data.txt
python ./src/python_helper_module.py
git commit -m "Heartbeat"
git push
sleep 300
done

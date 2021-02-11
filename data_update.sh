#!/bin/sh
while true
do
date > static/data.txt
git add static/data.txt
python ./src/python_helper_module.py
git add ./src/routes/index.svelte
git commit -m "Heartbeat"
git push
sleep 3600
done

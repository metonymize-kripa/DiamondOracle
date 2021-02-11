#!/bin/sh
while true
do
date > static/data.txt
git add static/data.txt
cd src; python3 python_helper_module.py; cd ..
git add ./src/routes/index.svelte
git commit -m "Heartbeat"
git push
sleep 3600
done

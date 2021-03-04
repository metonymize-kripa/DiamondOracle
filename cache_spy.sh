#!/bin/sh
while true
do
  curl https://fatneo.com/api/test?sym=SPY
  curl https://api.fatneo.com/parse/tsla%20wsb
  sleep 60
done

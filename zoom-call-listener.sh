#!/bin/bash
ZOOM_PROCESS_POLL_INTERVAL=5
SEMAPHORE_ADDRESS="http://192.168.1.207:8080"

echo "Starting zoom call listener"

status=`curl -s $SEMAPHORE_ADDRESS`
echo "Current status is $status"

while true; do
  if ps x | grep -E "\-key [0-9]{9,10}" > /dev/null; then
    if [ "$status" != "ON" ]; then
      echo "Zoom call started"
      status="ON"
      curl -s -XPOST -d ON $SEMAPHORE_ADDRESS > /dev/null
    fi
  else
    if [ "$status" == "ON" ]; then
      echo "Zoom call ended"
      status="OFF"
      curl -s -XPOST -d OFF $SEMAPHORE_ADDRESS > /dev/null 
    fi
  fi
  sleep $ZOOM_PROCESS_POLL_INTERVAL
done

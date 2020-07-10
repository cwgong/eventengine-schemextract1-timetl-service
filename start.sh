#!/bin/sh
#cd /data/eventengine-schemextract-timetl-service

LOGS_DIR=logs
if [ ! -d "${LOGS_DIR}" ]
then
  mkdir "${LOGS_DIR}"
fi

python3 eventengine-schemextract-timetl-service.py eventengine-schemextract-timetl-service.conf

echo "eventengine-schemextract-timetl-service starting..."

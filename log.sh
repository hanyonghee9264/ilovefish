#!/usr/bin/env bash
LOG_ERROR='/srv/projects/.log/error.log'
LOG_INFO='/srv/projects/.log/info.log'
CMD='sudo docker exec $(sudo docker ps -q) tail -f'
eb ssh --command "$CMD $LOG_ERROR $LOG_INFO"
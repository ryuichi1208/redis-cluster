#!/bin/bash

if [ $? -ne 0 ]; then
  LIBFOLDER=${0%/${0##*/}}
  source ${LIBFOLDER}/redis-bash-lib 2> /dev/null
  if [ $? -ne 0 ]; then
    echo "can't find redis-bash-lib in /usr/share/redis-bash or ${LIBFOLDER}"
    exit 127 
  fi
fi
REDISHOST=localhost
REDISPORT=6379
while getopts ":h:p:" opt
do
    case ${opt} in
        h) REDISHOST=${OPTARG};;
        p) REDISPORT=${OPTARG};;
    esac
done
shift $((${OPTIND} - 1))
while true
do
    exec 5>&-
    if [ "${REDISHOST}" != "" ] && [ "${REDISPORT}" != "" ]
    then
        exec 5<>/dev/tcp/${REDISHOST}/${REDISPORT} # open fd
    else
        echo "Wrong arguments"
        exit 255
    fi
    redis-client 5 SUBSCRIBE ${1} > /dev/null # subscribe to the pubsub channel in fd 5
    while true
    do
        unset ARGV
        OFS=${IFS};IFS=$'\n' # split the return correctly
        ARGV=($(redis-client 5))
        IFS=${OFS}
        if [ "${ARGV[0]}" = "message" ] && [ "${ARGV[1]}" = "${1}" ]
        then
            echo "Message from pubsub channel: ${ARGV[2]}"
        elif [ -z ${ARGV} ]
        then
            sleep 1
            break
        fi
    done
done

#!/bin/bash

cd /Flash-dev/backend
gitResults=`git pull`

if [[ $gitResults == "Already up to date." ]] ; then
   exit 0
else 
   eval systemctl restart FlashCapstone-dev > /dev/null
   exit 2
fi

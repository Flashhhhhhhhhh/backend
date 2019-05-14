#!/bin/bash

gitResults=`git pull`
if [[ $? != 0 ]] ; then
   echo "System attemped a 'git pull' of backend that failed" | mail -s "Failed to update backend" joseph.buelow@yahoo.com
   exit 1
fi

if [[ $gitResults == "Already up to date." ]] ; then
   exit 0
else 
   eval systemctl restart FlashCapstone > /dev/null
   if [[ $? != 0 ]] ; then
      echo "System attempted to restart backend and failed" | mail -s "Failed to restart FlashCapstone" joseph.buelow@yahoo.com
      exit 1
   fi
   exit 0
fi

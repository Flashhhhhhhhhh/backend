#!/bin/bash

gitResults=$(git pull)

if [ `echo $gitResults | grep "Already up to date."` ] ; then
   exit 0
else 
   eval `systemctl restart FlashCapstone`
fi

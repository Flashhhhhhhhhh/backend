#!/bin/bash

makeService () {
   eval cp /Flash/backend/install/FlashCapstone.service /usr/lib/systemd/system
   echo -e "To start Flash use sudo systemctl start FlashCapstone.service when this installer finishes"
}

makeFrontend () {
   eval cd /Flash
   eval git pull https://github.com/Flashhhhhhhhhh/frontend.git
   eval cp /Flash/frontend/build/* /var/www/html/
}

makeBackend () {
   eval cd /Flash
   eval git pull https://github.com/Flashhhhhhhhhh/backend.git
   if [ -f /bin/systemctl ] ; then
      makeService
   else
      echo -e "systemd not detected. To start Flash use:"
      echo -e "\tpython3 /Flash/backend/server.py"
   fi
}

checkPrerequisites () {
   if [[ ! -d /usr/lib/python3.7 ]] ; then
      echo -e "Please install python3.7.2 before installing Flash"
      exit 1
   fi
   if [[ ! -d /var/www/html ]] ; then
      echo -e "Please install apache server before installing Flash"
      exit 1
   fi
   if [[ -d /Flash ]] ; then
      echo -e "Flash already installed.\nWould you like to update? [y/n]: "
      while read line do
         if [ $line == "n" ] ; then
            echo -e "Aborting"
            exit 0
         elif [ $line == "y" ] ; then
            break
         fi
      done
   fi
}

main () {
   checkPrerequisites
   eval mkdir /Flash
   makeBackend
   makeFrontend
   eval chmod -R 777 /Flash
   echo -e "Flash successfully installed!\nExiting"
   exit 0
}

main

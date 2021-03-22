#!/bin/bash

exec &> /home/pi/myscript.log
echo $(date)

(
	exec /usr/bin/python3 /develop/rabbitmq_dev/pi_rabbit_control.py
)

exit 0

#PID=""
#function get_pid {
	#PID='pidof python3 ./pi_rabbit_control.py'
#}

#function start {
   #get_pid
   #if [ -z $PID ]; then
      #echo  "Starting server.."
      #./pi_rabbit_control.py  &
      #get_pid
      #echo "Done. PID=$PID"
   #else
#      echo "server is already running, PID=$PID"
#   fi
#}

#case "$1" in
#   start)
#      start
#   ;;
#   #stop)
#   #   stop
#   #;;
#   #restart)
#   #   restart
#   #;;
#   #status)
#   #   status
#   #;;
#   *)
#      echo "Usage: $0 {start|stop|restart|status}"
#esac

#!/bin/bash

# Function to start the servers
start_servers() {
  echo "Starting first database server"
  # Change directory to the location of your database/restaurant_sys
  cd ./database/restaurant_sys
  # Start the first server with settings v1
  python manage.py runserver 9000 --noreload --settings=restaurant_sys.settings.v1 &

  echo "Starting second database server"
  # Start the second server on port 8083 with settings v2
  python manage.py runserver 9001 --noreload --settings=restaurant_sys.settings.v2 &
}

flush_database() {
  echo "Flushing database"
  # Change directory to the location of your database/restaurant_sys
  cd ./database/restaurant_sys
  # Flush the database
  python manage.py flush --settings=restaurant_sys.settings.v1
  python manage.py flush --settings=restaurant_sys.settings.v2
}
# Function to stop the servers
stop_servers() {
  echo "Stopping database servers"
  # Find and stop the background servers (change the port numbers)
  pgrep -f "python manage.py runserver 9000" | xargs kill -9
  pgrep -f "python manage.py runserver 9001" | xargs kill -9
}

# Check the argument provided to the script
if [ "$1" == "start" ]; then
  start_servers
elif [ "$1" == "stop" ]; then
  stop_servers
elif [ "$1" == "flush" ]; then
  flush_database
else
  echo "Usage: $0 [start|stop]"
  exit 1
fi

#!/bin/bash
VERSION=0.0.2
if [ $1 = "version" -o $1 = "v" -o $1 = "-v" ]; then
  echo $VERSION

elif [ $1 = "install" -o $1 = "i" ]; then
  shift
  docker run -it -v $(pwd)/web:/app -w /app node:current-alpine yarn add "$@"
  
elif [ $1 = "init" ]; then
  pip3 install -r requirements.txt
  docker run -it -v $(pwd)/web:/app -w /app node:current-alpine yarn install
  
elif [ $1 = "build" ]; then
  docker run -it -v $(pwd)/web:/app -w /app -p 5555:5555 node:current-alpine yarn parcel watch --dist-dir dist --port 5555 --no-cache src/index.html

elif [[ $1 = "run" ]]; then
  . .address
  python3 kpl/ckpl.py
  # uvicorn --reload --host 0.0.0.0 --port 8000 api:app
  # uvicorn api:app --port 5000 --ssl-keyfile=./testcert-key.pem --ssl-certfile=./testcert.pem --reload

elif [[ $1 = "prod" || $1 = "production" ]]; then
  docker run -it -v $(pwd)/web:/app -w /app node:current-alpine yarn parcel build --no-cache src/index.html
  docker run -it --network host -v $(pwd):/app/ magnus-server
  
fi

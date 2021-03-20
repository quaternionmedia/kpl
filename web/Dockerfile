FROM node:current-alpine
WORKDIR /app
RUN npm upgrade -g yarn

CMD [ "/bin/sh", "/usr/local/bin/yarn", "parcel", "watch", "--port", "5555", "--no-cache", "/app/src/index.html" ]

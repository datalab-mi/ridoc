FROM node:12-alpine

WORKDIR /app
COPY package*.json  ./
COPY src ./
COPY rollup.config.js ./

RUN npm install

EXPOSE 5000 35729 3572

CMD [ "npm", "run","dev" ]

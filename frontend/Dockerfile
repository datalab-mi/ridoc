ARG PDFJS_VERSION

# https://mherman.org/blog/dockerizing-a-react-app/
# base image
FROM node:12.2.0-alpine
ENV PDFJS_VERSION "$PDFJS_VERSION"

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json ./
RUN npm install --silent
RUN npm install react-scripts@3.3.0 -g --silent

# PDF VIEWER
RUN wget "https://github.com/mozilla/pdf.js/releases/download/v2.3.200/pdfjs-2.3.200-dist.zip"
RUN mkdir -p public
RUN unzip -d public pdfjs-2.3.200-dist.zip
RUN rm pdfjs-2.3.200-dist.zip

EXPOSE 3000

# start app
CMD ["npm", "start"]

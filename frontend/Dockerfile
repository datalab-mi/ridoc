ARG PDFJS_VERSION
FROM node:12.2.0-alpine
ENV PDFJS_VERSION "$PDFJS_VERSION"

WORKDIR /app
COPY package*.json  ./
COPY src ./
COPY rollup.config.js ./

RUN npm install

EXPOSE 5000 35729 3572

# PDF VIEWER
RUN wget "https://github.com/mozilla/pdf.js/releases/download/v2.3.200/pdfjs-2.3.200-dist.zip"
RUN mkdir -p public
RUN unzip -d public pdfjs-2.3.200-dist.zip
RUN rm pdfjs-2.3.200-dist.zip

CMD [ "npm", "run","dev" ]

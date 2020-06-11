ARG PDFJS_VERSION
FROM node:12.2.0-alpine
ENV PDFJS_VERSION "$PDFJS_VERSION"

# For production, see https://github.com/mikenikles/sapper-on-cloud-run/blob/master/Dockerfile
WORKDIR /app
COPY . .
RUN npm install
EXPOSE 3000

# PDF VIEWER
RUN wget "https://github.com/mozilla/pdf.js/releases/download/v2.3.200/pdfjs-2.3.200-dist.zip"
RUN mkdir -p public
RUN unzip -d public pdfjs-2.3.200-dist.zip
RUN rm pdfjs-2.3.200-dist.zip

# tailwindcss
RUN npm install tailwindcss postcss-cli --save-dev

CMD [ "npm", "run","dev" ]

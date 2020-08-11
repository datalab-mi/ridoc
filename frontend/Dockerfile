#######################
# Step 1: Base target #
#######################
FROM node:12.2.0-alpine as base
ARG PDFJS_VERSION
ENV PDFJS_VERSION "$PDFJS_VERSION"

RUN apk update\
  && apk add ca-certificates wget\
  && update-ca-certificates

WORKDIR /app
COPY . .
RUN npm install

# PSDF VIEWER
RUN wget "https://github.com/mozilla/pdf.js/releases/download/v2.3.200/pdfjs-2.3.200-dist.zip"
RUN mkdir -p public
RUN unzip -d public pdfjs-2.3.200-dist.zip
RUN rm pdfjs-2.3.200-dist.zip

# tailwindcss
RUN npm install tailwindcss postcss-cli --save-dev

# For production, see https://github.com/mikenikles/sapper-on-cloud-run/blob/master/Dockerfile
################################
# Step 2: "development" target #
################################
FROM base as dev
EXPOSE 3000
CMD [ "npm", "run","dev" ]

################################
# Step 3:   "build" target     #
################################
FROM base as build
RUN npm run build
CMD ["npx", "sapper", "export"]

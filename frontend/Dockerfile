ARG VIEWERJS_VERSION

#######################
# Step 1: Base target #
#######################
FROM node:12.2.0-alpine as base
RUN   apk update \
 &&   apk add ca-certificates wget \
 &&   update-ca-certificates

WORKDIR /app
COPY . .
RUN npm config set strict-ssl false #Do not check certificate, proxy fault
RUN npm install

# ViewerJS
ARG VIEWERJS_VERSION
RUN wget "https://viewerjs.org/releases/viewerjs-${VIEWERJS_VERSION}.zip"
RUN mkdir ViewerJS
RUN unzip viewerjs-${VIEWERJS_VERSION}.zip
RUN mv viewerjs-${VIEWERJS_VERSION}/* ViewerJS

#DSFR (Design de l'Etat)
RUN  mkdir -p static/dsfr \
 &&  cp node_modules/@gouvfr/dsfr/dist/dsfr.module.min.js static/dsfr \
 &&  cp node_modules/@gouvfr/dsfr/dist/dsfr.module.min.js.map static/dsfr \
 &&  cp node_modules/@gouvfr/dsfr/dist/dsfr.nomodule.min.js static/dsfr \
 &&  cp node_modules/@gouvfr/dsfr/dist/dsfr.nomodule.min.js.map static/dsfr \
 &&  cp node_modules/@gouvfr/dsfr/dist/dsfr.min.css static/dsfr \
 &&  cp -r node_modules/@gouvfr/dsfr/dist/utility static/dsfr \
 &&  cp -r node_modules/@gouvfr/dsfr/dist/favicon static/dsfr  \
 &&  cp -r node_modules/@gouvfr/dsfr/dist/icons static/dsfr \
 &&  cp -r node_modules/@gouvfr/dsfr/dist/fonts static/dsfr

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
CMD ["npm", "run", "build"]
#CMD ["npx", "sapper", "export"]

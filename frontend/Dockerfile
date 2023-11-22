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
RUN mkdir static/fonts
RUN mv node_modules/@gouvfr/dsfr/dist/fonts/* static/fonts 

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
CMD ["npm", "run", "build"]
#CMD ["npx", "sapper", "export"]
################################
# Step 4: "production" target  #
################################
# This stage only needs the compiled Sapper application
# and the runtime dependencies.
FROM node:12.2.0-alpine as prod
EXPOSE 3000
USER node:node
WORKDIR /app
COPY --from=build --chown=node:node /app/__sapper__/build ./__sapper__/build
COPY --from=build --chown=node:node /app/static ./static
COPY --from=build --chown=node:node /app/node_modules ./node_modules
COPY --from=base --chown=node:node /app/ViewerJS ./ViewerJS
COPY --chown=node:node package.json .
CMD ["node","__sapper__/build"]
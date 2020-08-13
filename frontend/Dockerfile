#######################
# Step 1: Base target #
#######################
FROM node:12.2.0-alpine as base

WORKDIR /app
COPY . .
RUN npm install


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
CMD ["npm", "run", "build"]
#CMD ["npx", "sapper", "export"]

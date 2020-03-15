#######################
# Step 1: Base target #
#######################
FROM traefik:2.2 as dev

COPY acme.json /acme.json

EXPOSE 80

################################
# Step 2: "production" target #
################################
FROM dev as prod

EXPOSE 443

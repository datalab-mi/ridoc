#######################
# Step 1: Base target #
#######################
FROM python:3.7 as dev

RUN mkdir -p /app

COPY requirements.txt /app/

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# For debug purpose
#RUN pip install -e .

LABEL traefik.enable="true"
LABEL traefik.http.routers.python.rule="PathPrefix(`/api/v1`)"
LABEL traefik.http.routers.python.entrypoints="http"
LABEL traefik.http.services.python.loadbalancer.server.port="5000"

# run our application
CMD [ "python3", "webapp/app.py" ]

################################
# Step 2: "production" target #
################################
FROM dev as prod

EXPOSE 443

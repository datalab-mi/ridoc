#######################
# Step 1: Base target #
#######################
FROM python:3.8 as dev

WORKDIR /app

COPY requirements.txt .
COPY ./application .
COPY ./tools .
COPY ./setup.py .
COPY ./start.sh .

RUN  [ -f "start.sh" ] && chmod +x start.sh

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# For debug purpose
RUN pip install -e .

#LABEL traefik.enable="true"
#LABEL traefik.http.routers.python.rule="PathPrefix(`/api/v1`)"
#LABEL traefik.http.routers.python.entrypoints="http"
#LABEL traefik.http.services.python.loadbalancer.server.port="5000"


################################
# Step 2: "production" target #
################################
FROM dev as prod

EXPOSE 443

# run our application
CMD [ "sh", "start.sh" ]

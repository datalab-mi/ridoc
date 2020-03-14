FROM python:3.7

RUN mkdir -p /app

#COPY . /app
COPY requirements.txt /app/

WORKDIR /app

##RUN mkdir -p /matchid/code /matchid/conf/run /matchid/log /matchid/referential_data /data/matchID_test/ /matchid/upload
##
##WORKDIR /matchid
##
##VOLUME /matchid/code
##VOLUME /matchid/conf
##VOLUME /matchid/projects
##VOLUME /matchid/referential_data
##VOLUME /matchid/log
##VOLUME /matchid/models
##VOLUME /matchid/upload

RUN pip install --no-cache-dir -r requirements.txt

# run our application
#CMD [ "python3", "run.py" ]
CMD [ "python3", "webapp/app.py" ]

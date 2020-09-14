ARG ES_VERSION
FROM docker.elastic.co/logstash/logstash-oss:${ES_VERSION}

# Create nginx index in Elasticseartch if no exist

WORKDIR /app
COPY nginx_template.json .

ARG ELASTICSEARCH_HOSTS
#RUN curl -XDELETE http://browser-elasticsearch/nginx -vv
#RUN curl --header "content-type: application/JSON" -XPUT ${ELASTICSEARCH_HOSTS}/nginx -d '$(cat nginx_template.json)'

ARG ES_VERSION

FROM docker.elastic.co/elasticsearch/elasticsearch:${ES_VERSION}

ADD elasticsearch.yml /usr/share/elasticsearch/config

### Plugins ###
# Cannot work with our proxy....
#RUN bin/elasticsearch-plugin install --verbose analysis-icu

# Download from zip
RUN apt-get update && apt-get install -y \
    wget \
 && rm -rf /var/lib/apt/lists/*``

# /analysis-icu
ARG ES_VERSION
RUN wget "https://artifacts.elastic.co/downloads/elasticsearch-plugins/analysis-icu/analysis-icu-${ES_VERSION}.zip"
RUN mkdir -p plugins/analysis-icu
RUN unzip -d plugins/analysis-icu analysis-icu-${ES_VERSION}.zip

# /analysis-phonetic
ARG ES_VERSION
RUN wget "https://artifacts.elastic.co/downloads/elasticsearch-plugins/analysis-phonetic/analysis-phonetic-${ES_VERSION}.zip"
RUN mkdir -p plugins/analysis-phonetic
RUN unzip -d plugins/analysis-phonetic analysis-phonetic-${ES_VERSION}.zip

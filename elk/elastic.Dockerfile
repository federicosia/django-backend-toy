FROM docker.elastic.co/elasticsearch/elasticsearch:8.14.1
COPY  /elastic/elasticsearch.yml /usr/share/elasticsearch/config/
ENV ELASTIC_USERNAME=elastic-itshopper
ENV ELASTIC_PASSWORD=tidoz!@#6BtAqY7sQSck
FROM docker.elastic.co/logstash/logstash:8.14.1
RUN rm -f /usr/share/logstash/pipeline/logstash.conf
COPY /logstash/logstash.conf /usr/share/logstash/pipeline/
COPY /logstash/logstash.yml /usr/share/logstash/config/
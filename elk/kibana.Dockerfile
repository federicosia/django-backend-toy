FROM docker.elastic.co/kibana/kibana:8.14.1
ENV server_name=kibana-itshopper
ENV server_host=localhost
ENV elasticsearch_hosts='[ http://elastic-itshopper:9200 ]'
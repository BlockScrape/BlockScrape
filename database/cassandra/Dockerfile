FROM cassandra:latest

RUN mkdir /table

WORKDIR /table

COPY ./table_set_up .

RUN chmod +x /custom-docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD["cassandra", "-f"]
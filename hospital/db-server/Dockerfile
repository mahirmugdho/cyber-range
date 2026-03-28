FROM postgres:16-alpine

COPY init.sql /docker-entrypoint-initdb.d/
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
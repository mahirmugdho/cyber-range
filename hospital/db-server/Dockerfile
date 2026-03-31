FROM postgres:16-alpine

COPY init.sql /docker-entrypoint-initdb.d/
COPY pg_hba.conf /etc/postgresql/pg_hba.conf
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENV POSTGRES_HOST_AUTH_METHOD=md5

ENTRYPOINT ["/entrypoint.sh"]
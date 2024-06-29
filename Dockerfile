ARG POSTGRES_VERSION=16
FROM postgres:${POSTGRES_VERSION}
COPY ./settings/postgresql.conf /var/lib/postgresql/data/postgresql.conf

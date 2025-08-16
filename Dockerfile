# This image was forked from the official PostgreSQL image, so it could be
# signed and relied on as an internal dependency.
# The image is modified to include an older version of PostgreSQL, which
# allows us to upgrade the database from the old version to the new one.
ARG POSTGRES_VERSION=17
FROM postgres:${POSTGRES_VERSION} AS base

# we need to redeclare the ARG here, otherwise it will not
# be available in the section below the FROM statement.
ARG POSTGRES_VERSION=17
ARG POSTGRES_OLD_VERSION=16

ENV POSTGRES_VERSION=${POSTGRES_VERSION}
ENV POSTGRES_OLD_VERSION=${POSTGRES_OLD_VERSION}

# The old binaries will be in /usr/lib/postgresql/16/bin
ENV PGBINOLD=/usr/lib/postgresql/${POSTGRES_OLD_VERSION}/bin
ENV PGBINNEW=/usr/lib/postgresql/${POSTGRES_VERSION}/bin

# we are usually using /var/lib/postgresql/data as the data directory
# so this is why we are using it for the 'old' version instead of the
# path that is customized for the version.
ENV PGDATAOLD=/var/lib/postgresql/data
ENV PGDATANEW=/var/lib/postgresql/${POSTGRES_VERSION}/data

COPY bin/upgradeversion.sh /usr/local/bin/upgradeversion

FROM base AS install
# Enable and install old version of PostgreSQL.
RUN sed -i "s/\$/ ${POSTGRES_OLD_VERSION}/" /etc/apt/sources.list.d/pgdg.list;
RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		postgresql-${POSTGRES_OLD_VERSION} \
	; \
	rm -rf /var/lib/apt/lists/*;

FROM install AS no-gosu
RUN set -eux; \
    rm -rf /usr/local/bin/gosu;

FROM postgres:${POSTGRES_VERSION} AS su-exec
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends gcc libc-dev curl ca-certificates; \
    rm -rf /var/lib/apt/lists/*; \
    curl -o /usr/local/bin/su-exec.c https://raw.githubusercontent.com/ncopa/su-exec/master/su-exec.c; \
    gcc -Wall /usr/local/bin/su-exec.c -o /usr/local/bin/su-exec;

FROM no-gosu AS runtime
COPY --from=su-exec --chown=root:root --chmod=755 /usr/local/bin/su-exec /usr/local/bin/gosu
# We decided to use our own UID range.
# INFO: https://github.com/greenbone/automatix/blob/main/README.md
# Change to user root user to run the commands.
USER 0:0
RUN groupmod -g 10002 postgres && usermod -u 10002 -g 10002 postgres && \
  find / -uid 999 -not -path "/proc/*" -exec chown 10002 {} \; && \
  find / -gid 999 -not -path "/proc/*" -exec chown :10002 {} \;
USER 10002:10002

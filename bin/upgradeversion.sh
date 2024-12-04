#!/bin/bash

set -euo pipefail

# POSTGRES_VERSION, POSTGRES_OLD_VERSION
# PGDATAOLD, PGDATANEW, PGBINOLD, PGBINNEW
# are available from the Dockerfile

# If there is no initialized database, we do nothing
if [ ! -s "${PGDATAOLD}/PG_VERSION" ]; then
    echo "No database found. Exiting."
    exit 0
fi

# Check postgres version
echo -n "Current database version is "
cat ${PGDATAOLD}/PG_VERSION

# if the version is already current, we don't need to do anything
if [ "$(cat ${PGDATAOLD}/PG_VERSION)" == "${POSTGRES_VERSION}" ]; then
    echo "No need to update. exiting."
    exit 0
fi

# Abort if the old version is not supported
if [ "$(cat ${PGDATAOLD}/PG_VERSION)" != "${POSTGRES_OLD_VERSION}" ]; then
    echo "Only PostgreSQL ${POSTGRES_OLD_VERSION} is supported for migration with this image."
    exit 1
fi

# Initialize the new database, if it doesn't exist
if [ ! -s "${PGDATANEW}/PG_VERSION" ]; then
    initdb -D ${PGDATANEW} -U "${POSTGRES_USER}"

		# migrate auth settings as well
		cp --target-directory=${PGDATANEW}/ ${PGDATAOLD}/pg_hba.conf
fi

# mitigate: 'you must have read and write access in the current directory'
cd /var/lib/postgresql

pg_upgrade \
    -U "${POSTGRES_USER}" \
    --old-bindir ${PGBINOLD} \
    --new-bindir ${PGBINNEW} \
    --old-datadir ${PGDATAOLD} \
    --new-datadir ${PGDATANEW}

# Check postgres version
echo -n "New migrated database version is "
cat ${PGDATANEW}/PG_VERSION

# if first parameter is 'inplace', we copy the new postgres version to
# the old one. This is not an atomic operation, and therefore risky;
# If the copy operation is not successful, we will end up with a
# corrupted database.
if [ "${1:-}" == "inplace" ]; then
    rm -rf ${PGDATAOLD}/*
    mv --target-directory=${PGDATAOLD}/ ${PGDATANEW}/*
fi

#!/usr/bin/env bash

# This script is used to test the upgradeversion script without spinning up the
# whole OpenSight stack. It creates a new (outdated) PostgreSQL database,
# attempts to upgrade it and checks if the version file was updated correctly.

set -euo pipefail

cleanup() {
  sudo rm -rf "${tempdir}"
}

trap cleanup ERR

tempdir=$(mktemp -d -t opensight-postgres-test-XXXXX)

sudo chown -R 999:999 "${tempdir}"

# Start a PostgreSQL container with an outdated version
docker run -it --rm --user 999:999 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=keycloak -e POSTGRES_USER=keycloak -v "${tempdir}":/var/lib/postgresql/data packages.greenbone.net/opensight/opensight-postgres:16.6

# Upgrade the database
docker run -it --rm --user 999:999 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=keycloak -e POSTGRES_USER=keycloak -v "${tempdir}":/var/lib/postgresql/data packages.greenbone.net/opensight/opensight-postgres:17.6 upgradeversion inplace

# did everything work as expected?
sudo cat ${tempdir}/PG_VERSION

cleanup


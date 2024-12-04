#!/usr/bin/env bash
set -euo pipefail

# This script is used to test the upgradeversion script without spinning up the
# whole OpenSight stack. It creates a new (outdated) PostgreSQL database,
# attempts to upgrade it and checks if the version file was updated correctly.

DOCKER_IMAGE=packages.greenbone.net/opensight/opensight-postgres
PREVIOUS_VERSION=16.6  # released version to test the upgrade from

tempdir=$(mktemp -d -t opensight-postgres-test-XXXXX)

cleanup() {
  sudo rm -rf "${tempdir}"
}
trap cleanup ERR

sudo chown -R 999:999 "${tempdir}"

# Start a PostgreSQL container with an outdated version
docker run -it --rm \
  --user 999:999 \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=keycloak \
  -e POSTGRES_USER=keycloak \
  -v "${tempdir}":/var/lib/postgresql/data \
  ${DOCKER_IMAGE}:${PREVIOUS_VERSION}

# Upgrade the database with the test version
docker build -t ${DOCKER_IMAGE}:test .
docker run -it --rm \
  --user 999:999 -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=keycloak \
  -e POSTGRES_USER=keycloak \
  -v "${tempdir}":/var/lib/postgresql/data \
  ${DOCKER_IMAGE}:test upgradeversion inplace

# did everything work as expected?
sudo cat ${tempdir}/PG_VERSION

cleanup

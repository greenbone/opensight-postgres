![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_new-logo_horizontal_rgb_small.png)

# OpenSight Postgres

[![GitHub releases](https://img.shields.io/github/release/greenbone/opensight-postgres.svg)](https://github.com/greenbone/opensight-postgres/releases)

Opensight-Postgres is utilized to provide our Opensight services with the appropriate PostgreSQL container versions.

It is equivalent to the [postgres](https://hub.docker.com/_/postgres) Docker
image. Additionally one previous major version of postgres is added to the
image, so that it can be used to upgrade mounted database files to the
current version.

## Upgrade process
The opensight-postgres image can be used to upgrade older database versions
to the current version used by this image.

If the database is already upgraded, this will be a no-op and the upgrade
process will automatically terminate with exit code 0.

This does not happen automatically however, since it represents a backwards
incompatible change, and has potential to fail. It is therefore recommended
to create backups before attempting a migration.

Usage:

```
docker run \
    -it --rm \
    --user 999:999 \
    -v /path/to/database:/var/lib/postgres/data/ \
    opensight-postgres upgradeversion inplace
```

The inplace argument is required to perform the upgrade in the same mounted
directory. This has the implication that the database will be corrupted if
the upgrade fails. Therefore it is recommended to create a backup before
attempting the upgrade.

## Maintainer

This project is maintained by [Greenbone AG](https://www.greenbone.net/).

## Contributing

Your contributions are highly appreciated. Please
[create a pull request](https://github.com/greenbone/autohooks-plugin-mypy/pulls)
on GitHub. Bigger changes need to be discussed with the development team via the
[issues section at GitHub](https://github.com/greenbone/autohooks-plugin-mypy/issues)
first.

## License

Copyright (C) 2023-2024 [Greenbone AG](https://www.greenbone.net/)

Licensed under the [GNU General Public License v3.0 or later](LICENSE).

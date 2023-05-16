#!/bin/bash

# set bash fail on errors or unset variables
set -o errexit
set -o pipefail
set -o nounset

# run migrations
alembic upgrade head

exec "$@"

#!/bin/bash

set -e
set -x

pytest tests --asyncio-mode=strict --log-level=INFO

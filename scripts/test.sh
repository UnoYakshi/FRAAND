#!/bin/bash

set -e
set -x

coverage run -m pytest tests --asyncio-mode=strict --log-level=INFO
coverage report -m

#!/bin/bash

# start fastapi server using uvicorn
if [ "$FASTAPI_ENV" = "DEV" ]; then
    uvicorn \
        --reload \
        --host 0.0.0.0 \
        --port 8000 \
        --log-level "debug" \
        src.fraand_core.main:app

else
    uvicorn \
        --host 0.0.0.0 \
        --port 8000 \
        --workers 2 \
        --log-level "info" \
        src.fraand_core.main:app
fi

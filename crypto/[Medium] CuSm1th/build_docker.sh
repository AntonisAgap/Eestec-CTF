#!/bin/bash
docker rm -f crypto_cusm1th
docker build -t crypto_cusm1th . && \
docker run --name=crypto_cusm1th --rm -p8001:1337 -it crypto_cusm1th
#!/bin/bash
docker rm -f crypto_flipping_invitations
docker build -t crypto_flipping_invitations . && \
docker run --name=crypto_flipping_invitations --rm -p8000:1337 -it crypto_flipping_invitations
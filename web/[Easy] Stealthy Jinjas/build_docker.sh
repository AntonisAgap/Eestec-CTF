#!/bin/bash
docker rm -f web_stealthy_jinjas
docker build -t web_stealthy_jinjas . && \
docker run -d --name=web_stealthy_jinjas --rm -p2001:1337 -it web_stealthy_jinjas
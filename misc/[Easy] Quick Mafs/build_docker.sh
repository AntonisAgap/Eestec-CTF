#!/bin/bash
docker rm -f misc_quick_mafs
docker build -t misc_quick_mafs . && \
docker run -d --name=misc_quick_mafs --rm -p5000:1337 -it misc_quick_mafs
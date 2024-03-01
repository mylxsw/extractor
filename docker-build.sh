#!/usr/bin/env bash

VERSION=1.0.0

docker buildx build --platform=linux/amd64,linux/arm64 -t mylxsw/extractor:$VERSION . --push
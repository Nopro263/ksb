#!/bin/sh

docker run --rm -v "/tmp:/local" --net=host openapitools/openapi-generator-cli generate \
    -i http://localhost/api/openapi.json \
    -g javascript \
    -o /local/client


rm -rf ./nginx/html/client
cp -r /tmp/client/src ./nginx/html/client
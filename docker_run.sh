#!/bin/sh
# Run in docker

# Stop on errors
set -e

docker build -t ps4-ctrl .
docker run --rm --net=host -it ps4-ctrl

echo "-------------------"
echo "to test stuff use :"
echo "  docker run --rm --net=host -it ps4-ctrl -v -C 903a0d528cd5029272d15d0d771d7bb0f4e09974779a21c351b0f6c321fca498 search"
echo "  docker run --rm --net=host -it ps4-ctrl -v -H 10.254.2.107 -C 903a0d528cd5029272d15d0d771d7bb0f4e09974779a21c351b0f6c321fca498 wakeup"
echo "  docker run --rm --net=host -it --entrypoint /bin/bash ps4-ctrl"

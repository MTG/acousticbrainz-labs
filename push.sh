#!/bin/bash
#
# Build images from the currently checked out version of AcousticBrainz Labs
# and push it to the Docker Hub, with an optional tag (by default "beta").
#
# Usage:
#   $ ./push.sh  [tag]
#
# Examples:
#   $ ./push.sh beta             # will push image with tag beta 
#   $ ./push.sh v-2018-07-14.0   # will push images with tag v-2018-07-14.0 

git describe --tags --dirty --always > .git-version

TAG=${2:-beta}

echo "Building AcousticBrainz labs image with tag $TAG..."
docker build -t metabrainz/acousticbrainz-labs:$TAG \
        -f Dockerfile.prod .

echo "Done!"
echo "Pushing image to docker hub metabrainz/acousticbrainz-labs:$TAG..."
docker push metabrainz/acousticbrainz-labs:$TAG
echo "Done!"

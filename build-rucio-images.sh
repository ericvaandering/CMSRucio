#! /bin/sh

set -e

export RUCIO_VERSION=1.31.6
export CMS_VERSION=${RUCIO_VERSION}.ewv1

export HARBOR=registry.cern.ch/cmsrucio

podman build --build-arg RUCIO_VERSION=$RUCIO_VERSION -f docker/rucio-server/Dockerfile -t $HARBOR/rucio-server:release-$CMS_VERSION .
podman push $HARBOR/rucio-server:release-$CMS_VERSION

podman build --build-arg RUCIO_VERSION=$RUCIO_VERSION -f docker/rucio-daemons/Dockerfile -t $HARBOR/rucio-daemons:release-$CMS_VERSION .
podman push $HARBOR/rucio-daemons:release-$CMS_VERSION

podman build --build-arg RUCIO_VERSION=$RUCIO_VERSION -f docker/rucio-probes/Dockerfile -t $HARBOR/rucio-probes:release-$CMS_VERSION .
podman push $HARBOR/rucio-probes:release-$CMS_VERSION

podman build --build-arg RUCIO_VERSION=$RUCIO_VERSION -f docker/rucio-ui/Dockerfile -t $HARBOR/rucio-ui:release-$CMS_VERSION .
podman push $HARBOR/rucio-ui:release-$CMS_VERSION

podman build --build-arg TAG=master -f docker/rucio-webui/Dockerfile -t $HARBOR/rucio-webui:release-$CMS_VERSION .
podman push $HARBOR/rucio-webui:release-$CMS_VERSION

#cd ../rucio-upgrade
#podman build  --build-arg RUCIO_VERSION=$RUCIO_VERSION -t ericvaandering/rucio-upgrade:release-$CMS_VERSION .
#podman push ericvaandering/rucio-upgrade:release-$CMS_VERSION


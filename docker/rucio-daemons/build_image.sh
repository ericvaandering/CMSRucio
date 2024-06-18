#! /bin/sh

podman build  --build-arg RUCIO_VERSION=34.4.3  --net host . -f docker/rucio-daemons/Dockerfile -t registry.cern.ch/ckalenga/rucio-daemons:release-34.4.3.ck1
podman push registry.cern.ch/ckalenga/rucio-daemons:release-34.4.3.ck1

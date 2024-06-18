#! /bin/sh

podman build  --build-arg RUCIO_VERSION=release-34.4.4  --net host . -t registry.cern.ch/ckalenga/rucio-daemons:release-34.4.4.ck1
podman push registry.cern.ch/ckalenga/rucio-daemons:release-34.4.4.ck1


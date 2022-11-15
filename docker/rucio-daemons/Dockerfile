# Copyright European Organization for Nuclear Research (CERN) 2017
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Eric Vaandering, <ewv@fnal.gov>, 2018

ARG RUCIO_VERSION
FROM rucio/rucio-daemons:release-$RUCIO_VERSION
ARG CMS_TAG

# Add CMS policy package
RUN mkdir -p /opt/rucio/policy/cms
ADD https://raw.githubusercontent.com/dmwm/CMSRucio/master/src/policy/__init__.py /opt/rucio/policy/cms/
ADD https://raw.githubusercontent.com/dmwm/CMSRucio/master/src/policy/schema.py /opt/rucio/policy/cms/
ADD https://raw.githubusercontent.com/dmwm/CMSRucio/master/src/policy/permission.py /opt/rucio/policy/cms/
RUN chmod 755 /opt/rucio/policy/cms/*
# FIXME: Relocate cmstfc?

# Install what's needed out of dmwm/rucio/CMS branch
ADD install_mail_templates.sh /tmp/
RUN /tmp/install_mail_templates.sh

# Install globus SDK
RUN python3 -m pip install --no-cache-dir globus-sdk pyyaml
ADD globus-config.yml.j2 /tmp

ADD https://raw.githubusercontent.com/dmwm/CMSRucio/master/docker/CMSRucioClient/scripts/cmstfc.py /usr/local/lib/python3.6/site-packages/cmstfc.py
RUN chmod 755 /usr/local/lib/python3.6/site-packages/cmstfc.py

RUN mkdir -p /etc/grid-security && ln -s /cvmfs/grid.cern.ch/etc/grid-security/certificates /etc/grid-security/

ADD cms-entrypoint.sh /

# Cannot make patch directory unless there are patches
RUN mkdir -p /patch

# Igor's patch for container grouping issues
ADD https://patch-diff.githubusercontent.com/raw/rucio/rucio/pull/5886.patch /patch/5886.patch


ENTRYPOINT ["/cms-entrypoint.sh"]

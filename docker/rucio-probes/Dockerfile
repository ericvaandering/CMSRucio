# Copyright European Organization for Nuclear Research (CERN) 2017
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Eric Vaandering, <ewv@fnal.gov>, 2019-2020

ARG RUCIO_VERSION
FROM rucio/probes:$RUCIO_VERSION

# For now CMS versions use python3 explicitly. Can be removed when main container goes to python3
RUN ln -s /usr/bin/python3 /usr/local/bin/python

# Add CMS policy package
RUN mkdir -p /opt/rucio/policy/CMSRucioPolicy
COPY src/policy/CMSRucioPolicy /opt/rucio/policy/CMSRucioPolicy
# Make it search the policy directory. Needs a change for python upgrades
RUN echo "/opt/rucio/policy" > /usr/local/lib/python3.9/site-packages/policy.pth

# TODO: Remove Tooo old? Was there a PR for them in rucio probes?
#ADD https://raw.githubusercontent.com/ericvaandering/probes/hack_obsolete_replicas/common/check_obsolete_replicas /probes/common
#ADD https://raw.githubusercontent.com/nsmith-/probes/hack_replicas/common/check_deletable_replicas /probes/common

# Where from?
# Supplanted in PR115 ADD https://raw.githubusercontent.com/ericvaandering/probes/cms_check_expired_rules/common/check_expired_rules /probes/common
ADD https://raw.githubusercontent.com/ericvaandering/probes/cms_check_expired_locked/common/check_expired_locked_rules /probes/common


# TODO: Most of these don't work either, each with a different error - different reasons than above
# PR 132 - Not accepted into rucio/probes yet
ADD https://raw.githubusercontent.com/voetberg/rucio_probes/common_context_manager_update/common/check_expired_dids /probes/common
ADD https://raw.githubusercontent.com/voetberg/rucio_probes/common_context_manager_update/common/check_fts_backlog /probes/common
ADD https://raw.githubusercontent.com/voetberg/rucio_probes/common_context_manager_update/common/check_messages_to_submit /probes/common
ADD https://raw.githubusercontent.com/voetberg/rucio_probes/common_context_manager_update/common/check_new_dids /probes/common
ADD https://raw.githubusercontent.com/voetberg/rucio_probes/common_context_manager_update/common/check_stuck_rules /probes/common
ADD https://raw.githubusercontent.com/voetberg/rucio_probes/common_context_manager_update/common/check_transfer_queues_status /probes/common
ADD https://raw.githubusercontent.com/voetberg/rucio_probes/common_context_manager_update/common/check_unevaluated_dids /probes/common
ADD https://raw.githubusercontent.com/voetberg/rucio_probes/common_context_manager_update/common/check_unlocked_replicas /probes/common
ADD https://raw.githubusercontent.com/voetberg/rucio_probes/common_context_manager_update/common/check_updated_dids /probes/common

# PR 136 which was closed in favor of #145, which should be watched.
# N.b. they will not move to the CMS VO, so we need a change to flux as well
ADD https://raw.githubusercontent.com/ericvaandering/probes/cms_usage_probes/cms/check_deletable_replicas /probes/cms
ADD https://raw.githubusercontent.com/ericvaandering/probes/cms_usage_probes/cms/check_obsolete_replicas /probes/cms

# To be removed once the PR is available in our rucio version
# Patch for rules volume (https://github.com/dmwm/CMSRucio/issues/747, https://github.com/rucio/probes/pull/154)
ADD https://raw.githubusercontent.com/rucio/probes/b403db9dad980b60979895b0b09cd133eaa23a59/cms/check_requests_count_volume /probes/cms
# Patch for rse settings and attributes monitoring (https://github.com/dmwm/CMSRucio/issues/912, https://github.com/rucio/probes/pull/155)
ADD https://raw.githubusercontent.com/rucio/probes/35c608bb9206252a6685b1b8551fda916c85fb16/cms/check_rse_settings_attributes /probes/cms

RUN chmod +x /probes/common/check_*
RUN chmod +x /probes/cms/check_*

# Temporary while we are adding variables to the config. Push to rucio-containers
ADD https://raw.githubusercontent.com/ericvaandering/containers/probes_prom/probes/rucio.cfg.j2 /tmp/
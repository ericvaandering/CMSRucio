#! /usr/bin/env python

from __future__ import print_function
from rucio.client.client import Client
import pprint


rucio = Client()

tape_rses = rucio.list_rses('rse_type=TAPE')
rses_with_weights = []

for rse in tape_rses:
    pprint.pprint(rse)
    # values = rucio.get_rse(rse['rse'])
    attrs = rucio.list_rse_attributes(rse['rse'])
    # pprint.pprint(values)
    pprint.pprint(attrs)

    quota = attrs.get('ddm_quota', 10e12)
    requires_approval = attrs.get('requires_approval', False)
    rses_with_weights.append(((rse['rse'], requires_approval), quota))


pprint.pprint(rses_with_weights)

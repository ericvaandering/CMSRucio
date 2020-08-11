#! /usr/bin/env python

from __future__ import print_function
from rucio.client.client import Client
import pprint


rucio = Client()

tape_rses = rucio.list_rses('rse_type=TAPE')

for rse in tape_rses:
    pprint.pprint(rse)
    values = rucio.get_rse(rse['rse'])
    attrs = rucio.list_rse_attributes(rse['rse'])
    pprint.pprint(values)
    pprint.pprint(attrs)

    
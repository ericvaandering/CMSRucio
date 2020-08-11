#! /usr/bin/env python

from __future__ import print_function
from rucio.client.client import Client
import pprint


rucio = Client()

tape_rses = rucio.list_rses('rse_type=TAPE')

for rse in tape_rses:
    attrs = rucio.list_rse_attributes(rse)
    pprint(attrs)
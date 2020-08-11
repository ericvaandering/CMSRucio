#! /usr/bin/env python

from __future__ import print_function

import pprint
import random

from rucio.client.client import Client

rucio = Client()

tape_rses = rucio.list_rses('rse_type=TAPE\cms_type=test')
rses_with_weights = []


def weighted_choice(choices):
    # from https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
    # Python 3.6 includes something like this in the random library itself

    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


for rse in tape_rses:
    # pprint.pprint(rse)
    # values = rucio.get_rse(rse['rse'])
    attrs = rucio.list_rse_attributes(rse['rse'])
    # pprint.pprint(values)
    # pprint.pprint(attrs)

    quota = attrs.get('ddm_quota', 1e12)
    requires_approval = attrs.get('requires_approval', False)
    rses_with_weights.append(((rse['rse'], requires_approval), quota))

pprint.pprint(rses_with_weights)

choice = weighted_choice(rses_with_weights)

print(choice)

#! /usr/bin/env python3


import json

from subprocess import PIPE, Popen
# import requests
# from requests.exceptions import ReadTimeout
#
# from gfal2 import GError, Gfal2Context
#
# import rucio.rse.rsemanager as rsemgr
# from rucio.client.client import Client
# from rucio.common.exception import (DataIdentifierAlreadyExists, FileAlreadyExists, RucioException,
#                                     AccessDenied)
DEBUG_FLAG = False
DEFAULT_DASGOCLIENT = '/cvmfs/cms.cern.ch/common/dasgoclient'



def das_go_client(query, dasgoclient=DEFAULT_DASGOCLIENT, debug=DEBUG_FLAG):
    """
    just wrapping the dasgoclient command line
    """
    proc = Popen([dasgoclient, '-query=%s' % query, '-json'], stdout=PIPE)
    output = proc.communicate()[0]
    if debug:
        print('DEBUG:' + output)
    return json.loads(output)

BLOCK = "/StreamExpress/Run2018A-PromptCalibProdSiStripGains-Express-v1/ALCAPROMPT#50d78a18-38ef-4cd4-8721-a617c441aa5b"

def files_in_block(block=BLOCK):
    result = das_go_client(query='file block=%s' % block)
    files = []
    for record in result:
        files.append(record['file']['name'])
    return files


files = files_in_block(block=BLOCK)
print(files)


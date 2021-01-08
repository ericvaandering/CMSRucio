#! /usr/bin/env python3


import json
import pdb

from rucio.client import Client

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

_ = pdb.__name__

client = Client()


def das_go_client(query, dasgoclient=DEFAULT_DASGOCLIENT, debug=DEBUG_FLAG):
    """
    just wrapping the dasgoclient command line
    """
    proc = Popen([dasgoclient, '-query=%s' % query, '-json'], stdout=PIPE)
    output = proc.communicate()[0]
    if debug:
        print('DEBUG:' + output)
    return json.loads(output)


INCOMPLETE_BLOCKS = [
    (
    "/TTToSemiLeptonic_TuneCP5_erdON_13TeV-powheg-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM" +
    "#fa0c5e22-537a-4b7a-866a-17fa34cbdef9",
    'T1_IT_CNAF_Disk'),
    (
    "/TTToSemiLeptonic_TuneCP5_erdON_13TeV-powheg-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM" +
    "#fa0c5e22-537a-4b7a-866a-17fa34cbdef9",
    'T1_RU_JINR_Disk'),
]


# BLOCK = "/StreamExpress/Run2018A-PromptCalibProdSiStripGains-Express-v1/ALCAPROMPT#50d78a18-38ef-4cd4-8721-a617c441aa5b"
# RSE = 'T2_CH_CERN'


def files_in_block(block):
    result = das_go_client(query='file block=%s' % block)
    files = []
    for record in result:
        files.append(record['file'][0]['name'])
    return files


def dbs_file_info(filename):
    result = das_go_client(query='file file=%s' % filename)

    n_bytes = result[0]['file'][0]['size']
    adler32 = result[0]['file'][0]['adler32']

    return n_bytes, adler32


def files_in_rucio_ds(block):
    files = []
    for record in client.list_content(scope='cms', name=block):
        files.append(record['name'])
    return files


if __name__ == '__main__':
    """
    Sync site data manager roles to RSE attributes
    """

    for block, rse in INCOMPLETE_BLOCKS:
        print('Fixing %s at %s' % (block, rse))
        true_files = files_in_block(block=block)
        rucio_files = files_in_rucio_ds(block=block)

        print('%s files in DBS vs %s files in Rucio' % (len(true_files), len(rucio_files)))

        missing_files = set(true_files) - set(rucio_files)

        for m_file in true_files:
            n_bytes, adler32 = dbs_file_info(filename=m_file)
            result = client.add_replica(rse=rse, scope='cms', name=m_file, bytes=n_bytes, adler32=adler32)
            print('Added file (%s) %s with %s bytses and %s' % (result, m_file, n_bytes, adler32))
            result = client.attach_dids(scope='cms', name=block, dids=[{'scope': 'cms', 'name': m_file}])

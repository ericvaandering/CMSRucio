#! /bin/env python

from __future__ import absolute_import, division, print_function

from rucio.client.didclient import DIDClient
from rucio.client.replicaclient import ReplicaClient

from rucio.common.exception import DataIdentifierAlreadyExists
from rucio.common.exception import RucioException
from rucio.common.exception import FileAlreadyExists

class CMSRucio(object):
    """
    Interface for Rucio with the CMS data model

    CMS         Rucio
    File/LFN    File
    Block       Dataset
    Dataset     Container

    We try to use the correct terminology on for variable and parameter names where the CMS facing code uses
    File/Block/Dataset and the Rucio facing code uses File/Dataset/Container
    """

    def __init__(self, account, auth_type,  scope='cms', dry_run=False):
        self.account = account
        self.auth_type = auth_type
        self.scope = scope
        self.dry_run = dry_run

        self.didc = DIDClient(account=self.account, auth_type=self.auth_type)
        self.rc = ReplicaClient(account=self.account, auth_type=self.auth_type)

        pass

    def cmsBlocksInContainer(self, container, scope='cms'):

        block_names = []
        response = self.didc.get_did(scope=scope, name=container)
        if response['type'].upper() != 'CONTAINER':
            return block_names

        response = self.didc.list_content(scope=scope, name=container)
        for item in response:
            if item['type'].upper() == 'DATASET':
                block_names.append(item['name'])

        return block_names

    def getReplicaInfoForBlocks(self, scope='cms', dataset=None, block=None, node=None):  # Mirroring PhEDEx service

        """
        _blockreplicas_
        Get replicas for given blocks

        dataset        dataset name, can be multiple (*)
        block          block name, can be multiple (*)
        node           node name, can be multiple (*)
        se             storage element name, can be multiple (*)
        update_since  unix timestamp, only return replicas updated since this
                time
        create_since   unix timestamp, only return replicas created since this
                time
        complete       y or n, whether or not to require complete or incomplete
                blocks. Default is to return either
        subscribed     y or n, filter for subscription. default is to return either.
        custodial      y or n. filter for custodial responsibility.  default is
                to return either.
        group          group name.  default is to return replicas for any group.
        """

        block_names = []
        result = {'block': []}

        if isinstance(block, (list, set)):
            block_names = block
        elif block:
            block_names = [block]

        if isinstance(dataset, (list, set)):
            for dataset_name in dataset:
                block_names.extend(self.cmsBlocksInContainer(dataset_name, scope=scope))
        elif dataset:
            block_names.extend(self.cmsBlocksInContainer(dataset, scope=scope))

        for block_name in block_names:
            dids = [{'scope': scope, 'name': block_name}]

            response = self.rc.list_replicas(dids=dids)
            nodes = set()
            for item in response:
                for node, state in item['states'].items():
                    if state.upper() == 'AVAILABLE':
                        nodes.add(node)
            result['block'].append({block_name: list(nodes)})
        return result

    def register_dataset(self, block, dataset, lifetime=None):
        """
        Create the rucio dataset corresponding to a CMS block and attach it to the container (CMS dataset)
        """

        if self.dry_run:
            print(' Dry run only. Not creating dataset (CMS block %s).' % block)
            return

        try:
            self.didc.add_dataset(scope=self.scope, name=block, lifetime=lifetime)
        except DataIdentifierAlreadyExists:
            pass

        try:
            self.didc.attach_dids(scope=self.scope, name=dataset, dids=[{'scope': self.scope, 'name': block}])
        except RucioException:
            pass

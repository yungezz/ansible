#!/usr/bin/python
#
# Copyright (c) 2017 Zim Kalinowski, <zikalino@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: azure_rm_syncgroups
version_added: "2.5"
short_description: Get SyncGroups facts.
description:
    - Get facts of SyncGroups.

options:
    location_name:
        description:
            - The name of the region where the resource is located.
        required: True
    resource_group_name:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    database_name:
        description:
            - The name of the database on which the sync group is hosted.
        required: True
    sync_group_name:
        description:
            - The name of the sync group.
        required: True
    start_time:
        description:
            - Get logs generated after this time.
        required: True
    end_time:
        description:
            - Get logs generated before this time.
        required: True
    type:
        description:
            - The types of logs to retrieve.
        required: True
    continuation_token:
        description:
            - The continuation token for this operation.
        required: False

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create sample SyncGroups
        azure_rm_syncgroups:
          resource_group_name:
          server_name:
          database_name:
          sync_group_name:
          interval: "{{ interval }}"
          conflict_resolution_policy: "{{ conflict_resolution_policy }}"
          sync_database_id: "{{ sync_database_id }}"
          hub_database_user_name: "{{ hub_database_user_name }}"
          hub_database_password: "{{ hub_database_password }}"
          schema:
            tables:
              - columns:
                  - quoted_name: "{{ quoted_name }}"
                    data_size: "{{ data_size }}"
                    data_type: "{{ data_type }}"
                quoted_name: "{{ quoted_name }}"
            master_sync_member_name: "{{ master_sync_member_name }}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.sql import SqlManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMSyncGroupsFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            location_name=dict(
                type='str',
                required=True
            ),
            resource_group_name=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            database_name=dict(
                type='str',
                required=True
            ),
            sync_group_name=dict(
                type='str',
                required=True
            ),
            start_time=dict(
                type='str',
                required=True
            ),
            end_time=dict(
                type='str',
                required=True
            ),
            type=dict(
                type='string',
                required=True
            ),
            continuation_token=dict(
                type='str',
                required=False
            ),
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
            ansible_facts=dict(azure_dnsrecordset=[])
        )
        self.location_name = None
        self.resource_group_name = None
        self.server_name = None
        self.database_name = None
        self.sync_group_name = None
        self.start_time = None
        self.end_time = None
        self.type = None
        self.continuation_token = None
        super(AzureRMSyncGroupsFacts, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if (self.location_name is not None):
            self.results['ansible_facts']['list_sync_database_ids'] = self.list_sync_database_ids()
        elif (self.resource_group_name is not None and
              self.server_name is not None and
              self.database_name is not None and
              self.sync_group_name is not None):
            self.results['ansible_facts']['list_hub_schemas'] = self.list_hub_schemas()
        elif (self.resource_group_name is not None and
              self.server_name is not None and
              self.database_name is not None and
              self.sync_group_name is not None and
              self.start_time is not None and
              self.end_time is not None and
              self.type is not None):
            self.results['ansible_facts']['list_logs'] = self.list_logs()
        elif (self.resource_group_name is not None and
              self.server_name is not None and
              self.database_name is not None and
              self.sync_group_name is not None):
            self.results['ansible_facts']['get'] = self.get()
        elif (self.resource_group_name is not None and
              self.server_name is not None and
              self.database_name is not None):
            self.results['ansible_facts']['list_by_database'] = self.list_by_database()
        return self.results

    def list_sync_database_ids(self):
        '''
        Gets facts of the specified SyncGroups.

        :return: deserialized SyncGroupsinstance state dictionary
        '''
        self.log("Checking if the SyncGroups instance {0} is present".format(self.sync_group_name))
        found = False
        try:
            response = self.mgmt_client.sync_groups.list_sync_database_ids(self.location_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("SyncGroups instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the SyncGroups instance.')
        if found is True:
            return response.as_dict()

        return False

    def list_hub_schemas(self):
        '''
        Gets facts of the specified SyncGroups.

        :return: deserialized SyncGroupsinstance state dictionary
        '''
        self.log("Checking if the SyncGroups instance {0} is present".format(self.sync_group_name))
        found = False
        try:
            response = self.mgmt_client.sync_groups.list_hub_schemas(self.resource_group_name,
                                                                     self.server_name,
                                                                     self.database_name,
                                                                     self.sync_group_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("SyncGroups instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the SyncGroups instance.')
        if found is True:
            return response.as_dict()

        return False

    def list_logs(self):
        '''
        Gets facts of the specified SyncGroups.

        :return: deserialized SyncGroupsinstance state dictionary
        '''
        self.log("Checking if the SyncGroups instance {0} is present".format(self.sync_group_name))
        found = False
        try:
            response = self.mgmt_client.sync_groups.list_logs(self.resource_group_name,
                                                              self.server_name,
                                                              self.database_name,
                                                              self.sync_group_name,
                                                              self.start_time,
                                                              self.end_time,
                                                              self.type,
                                                              self.continuation_token)
            found = True
            self.log("Response : {0}".format(response))
            self.log("SyncGroups instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the SyncGroups instance.')
        if found is True:
            return response.as_dict()

        return False

    def get(self):
        '''
        Gets facts of the specified SyncGroups.

        :return: deserialized SyncGroupsinstance state dictionary
        '''
        self.log("Checking if the SyncGroups instance {0} is present".format(self.sync_group_name))
        found = False
        try:
            response = self.mgmt_client.sync_groups.get(self.resource_group_name,
                                                        self.server_name,
                                                        self.database_name,
                                                        self.sync_group_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("SyncGroups instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the SyncGroups instance.')
        if found is True:
            return response.as_dict()

        return False

    def list_by_database(self):
        '''
        Gets facts of the specified SyncGroups.

        :return: deserialized SyncGroupsinstance state dictionary
        '''
        self.log("Checking if the SyncGroups instance {0} is present".format(self.sync_group_name))
        found = False
        try:
            response = self.mgmt_client.sync_groups.list_by_database(self.resource_group_name,
                                                                     self.server_name,
                                                                     self.database_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("SyncGroups instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the SyncGroups instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    AzureRMSyncGroupsFacts()
if __name__ == '__main__':
    main()

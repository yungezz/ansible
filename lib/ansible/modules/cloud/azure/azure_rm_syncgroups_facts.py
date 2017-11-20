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
module: azure_rm_syncgroups_facts
version_added: "2.5"
short_description: Get SyncGroups facts.
description:
    - Get facts of SyncGroups.

options:
    resource_group_name:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: False
    server_name:
        description:
            - The name of the server.
        required: False
    database_name:
        description:
            - The name of the database on which the sync group is hosted.
        required: False
    sync_group_name:
        description:
            - The name of the sync group.
        required: False
    start_time:
        description:
            - Get logs generated after this time.
        required: False
    end_time:
        description:
            - Get logs generated before this time.
        required: False
    type:
        description:
            - The types of logs to retrieve.
        required: False
    continuation_token:
        description:
            - The continuation token for this operation.
        required: False
    location_name:
        description:
            - The name of the region where the resource is located.
        required: False

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: List instances of SyncGroups
        azure_rm_syncgroups_facts:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          database_name: "{{ database_name }}"
          sync_group_name: "{{ sync_group_name }}"
          start_time: "{{ start_time }}"
          end_time: "{{ end_time }}"
          type: "{{ type }}"
          continuation_token: "{{ continuation_token }}"

      - name: List instances of SyncGroups
        azure_rm_syncgroups_facts:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          database_name: "{{ database_name }}"
          sync_group_name: "{{ sync_group_name }}"

      - name: Get instance of SyncGroups
        azure_rm_syncgroups_facts:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          database_name: "{{ database_name }}"
          sync_group_name: "{{ sync_group_name }}"

      - name: List instances of SyncGroups
        azure_rm_syncgroups_facts:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          database_name: "{{ database_name }}"

      - name: List instances of SyncGroups
        azure_rm_syncgroups_facts:
          location_name: "{{ location_name }}"
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
            resource_group_name=dict(
                type='str',
                required=False
            ),
            server_name=dict(
                type='str',
                required=False
            ),
            database_name=dict(
                type='str',
                required=False
            ),
            sync_group_name=dict(
                type='str',
                required=False
            ),
            start_time=dict(
                type='str',
                required=False
            ),
            end_time=dict(
                type='str',
                required=False
            ),
            type=dict(
                type='str',
                required=False
            ),
            continuation_token=dict(
                type='str',
                required=False
            ),
            location_name=dict(
                type='str',
                required=False
            ),
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
            ansible_facts=dict(azure_dnsrecordset=[])
        )
        self.resource_group_name = None
        self.server_name = None
        self.database_name = None
        self.sync_group_name = None
        self.start_time = None
        self.end_time = None
        self.type = None
        self.continuation_token = None
        self.location_name = None
        super(AzureRMSyncGroupsFacts, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if (self.resource_group_name is not None and
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
            self.results['ansible_facts']['list_hub_schemas'] = self.list_hub_schemas()
        elif (self.resource_group_name is not None and
              self.server_name is not None and
              self.database_name is not None and
              self.sync_group_name is not None):
            self.results['ansible_facts']['get'] = self.get()
        elif (self.resource_group_name is not None and
              self.server_name is not None and
              self.database_name is not None):
            self.results['ansible_facts']['list_by_database'] = self.list_by_database()
        elif (self.location_name is not None):
            self.results['ansible_facts']['list_sync_database_ids'] = self.list_sync_database_ids()
        return self.results

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


def main():
    AzureRMSyncGroupsFacts()
if __name__ == '__main__':
    main()

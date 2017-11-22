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
module: azure_rm_syncagents
version_added: "2.5"
short_description: Manage an SyncAgents.
description:
    - Create, update and delete an instance of SyncAgents.

options:
    resource_group_name:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server on which the sync agent is hosted.
        required: True
    sync_agent_name:
        description:
            - The name of the sync agent.
        required: True
    sync_database_id:
        description:
            - ARM resource id of the sync database in the sync agent.
        required: False

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create (or update) SyncAgents
        azure_rm_syncagents:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          sync_agent_name: "{{ sync_agent_name }}"
          sync_database_id: "{{ sync_database_id }}"
'''

RETURN = '''
state:
    description: Current state of SyncAgents
    returned: always
    type: dict
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


class AzureRMSyncAgents(AzureRMModuleBase):
    """Configuration class for an Azure RM SyncAgents resource"""

    def __init__(self):
        self.module_arg_spec = dict(
            resource_group_name=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            sync_agent_name=dict(
                type='str',
                required=True
            ),
            sync_database_id=dict(
                type='str',
                required=False
            ),
            state=dict(
                type='str',
                required=False,
                default='present',
                choices=['present', 'absent']
            )
        )

        self.resource_group_name = None
        self.server_name = None
        self.sync_agent_name = None
        self.parameters = dict()

        self.results = dict(changed=False, state=dict())
        self.mgmt_client = None
        self.state = None

        super(AzureRMSyncAgents, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif key == "sync_database_id":
                self.parameters["sync_database_id"] = kwargs[key]

        response = None
        results = dict()
        to_be_updated = False

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        try:
            resource_group = self.get_resource_group(self.resource_group)
        except CloudError:
            self.fail('resource group {0} not found'.format(self.resource_group))

        response = self.get_syncagents()

        if not response:
            self.log("SyncAgents instance doesn't exist")
            if self.state == 'absent':
                self.log("Nothing to delete")
            else:
                to_be_updated = True
        else:
            self.log("SyncAgents instance already exists")
            if self.state == 'absent':
                self.delete_syncagents()
                self.results['changed'] = True
                self.log("SyncAgents instance deleted")
            elif self.state == 'present':
                self.log("Need to check if SyncAgents instance has to be deleted or may be updated")
                to_be_updated = True

        if self.state == 'present':

            self.log("Need to Create / Update the SyncAgents instance")

            if self.check_mode:
                return self.results

            if to_be_updated:
                self.results['state'] = self.create_update_syncagents()
                self.results['changed'] = True
            else:
                self.results['state'] = response

            self.log("Creation / Update done")

        return self.results

    def create_update_syncagents(self):
        '''
        Creates or updates SyncAgents with the specified configuration.

        :return: deserialized SyncAgents instance state dictionary
        '''
        self.log("Creating / Updating the SyncAgents instance {0}".format(self.sync_agent_name))

        try:
            response = self.mgmt_client.sync_agents.create_or_update(self.resource_group_name,
                                                                     self.server_name,
                                                                     self.sync_agent_name,
                                                                     self.parameters)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the SyncAgents instance.')
            self.fail("Error creating the SyncAgents instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_syncagents(self):
        '''
        Deletes specified SyncAgents instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the SyncAgents instance {0}".format(self.sync_agent_name))
        try:
            response = self.mgmt_client.sync_agents.delete(self.resource_group_name,
                                                           self.server_name,
                                                           self.sync_agent_name)
        except CloudError as e:
            self.log('Error attempting to delete the SyncAgents instance.')
            self.fail("Error deleting the SyncAgents instance: {0}".format(str(e)))

        return True

    def get_syncagents(self):
        '''
        Gets the properties of the specified SyncAgents.

        :return: deserialized SyncAgents instance state dictionary
        '''
        self.log("Checking if the SyncAgents instance {0} is present".format(self.sync_agent_name))
        found = False
        try:
            response = self.mgmt_client.sync_agents.get(self.resource_group_name,
                                                        self.server_name,
                                                        self.sync_agent_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("SyncAgents instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the SyncAgents instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMSyncAgents()

if __name__ == '__main__':
    main()

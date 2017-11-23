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
module: azure_rm_syncmembers
version_added: "2.5"
short_description: Manage an SyncMembers.
description:
    - Create, update and delete an instance of SyncMembers.

options:
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
            - The name of the sync group on which the sync member is hosted.
        required: True
    sync_member_name:
        description:
            - The name of the sync member.
        required: True
    database_type:
        description:
            - "Database type of the sync member. Possible values include: 'AzureSqlDatabase', 'SqlServerDatabase'
        required: False
    sync_agent_id:
        description:
            - ARM resource id of the sync agent in the sync member.
        required: False
    sql_server_database_id:
        description:
            - SQL Server database id of the sync member.
        required: False
    server_name:
        description:
            - Server name of the member database in the sync member
        required: False
    database_name:
        description:
            - Database name of the member database in the sync member.
        required: False
    user_name:
        description:
            - User name of the member database in the sync member.
        required: False
    password:
        description:
            - Password of the member database in the sync member.
        required: False
    sync_direction:
        description:
            - "Sync direction of the sync member. Possible values include: 'Bidirectional', 'OneWayMemberToHub', 'OneWayHubToMember'
        required: False

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create (or update) SyncMembers
        azure_rm_syncmembers:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          database_name: "{{ database_name }}"
          sync_group_name: "{{ sync_group_name }}"
          sync_member_name: "{{ sync_member_name }}"
          database_type: "{{ database_type }}"
          sync_agent_id: "{{ sync_agent_id }}"
          sql_server_database_id: "{{ sql_server_database_id }}"
          server_name: "{{ server_name }}"
          database_name: "{{ database_name }}"
          user_name: "{{ user_name }}"
          password: "{{ password }}"
          sync_direction: "{{ sync_direction }}"
'''

RETURN = '''
state:
    description: Current state of SyncMembers
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


class AzureRMSyncMembers(AzureRMModuleBase):
    """Configuration class for an Azure RM SyncMembers resource"""

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
            database_name=dict(
                type='str',
                required=True
            ),
            sync_group_name=dict(
                type='str',
                required=True
            ),
            sync_member_name=dict(
                type='str',
                required=True
            ),
            database_type=dict(
                type='str',
                required=False
            ),
            sync_agent_id=dict(
                type='str',
                required=False
            ),
            sql_server_database_id=dict(
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
            user_name=dict(
                type='str',
                required=False
            ),
            password=dict(
                type='str',
                required=False
            ),
            sync_direction=dict(
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
        self.database_name = None
        self.sync_group_name = None
        self.sync_member_name = None
        self.parameters = dict()

        self.results = dict(changed=False, state=dict())
        self.mgmt_client = None
        self.state = None

        super(AzureRMSyncMembers, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                 supports_check_mode=True,
                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif key == "database_type":
                self.parameters["database_type"] = kwargs[key]
            elif key == "sync_agent_id":
                self.parameters["sync_agent_id"] = kwargs[key]
            elif key == "sql_server_database_id":
                self.parameters["sql_server_database_id"] = kwargs[key]
            elif key == "server_name":
                self.parameters["server_name"] = kwargs[key]
            elif key == "database_name":
                self.parameters["database_name"] = kwargs[key]
            elif key == "user_name":
                self.parameters["user_name"] = kwargs[key]
            elif key == "password":
                self.parameters["password"] = kwargs[key]
            elif key == "sync_direction":
                self.parameters["sync_direction"] = kwargs[key]

        response = None
        results = dict()
        to_be_updated = False

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        try:
            resource_group = self.get_resource_group(self.resource_group)
        except CloudError:
            self.fail('resource group {0} not found'.format(self.resource_group))

        response = self.get_syncmembers()

        if not response:
            self.log("SyncMembers instance doesn't exist")
            if self.state == 'absent':
                self.log("Nothing to delete")
            else:
                to_be_updated = True
        else:
            self.log("SyncMembers instance already exists")
            if self.state == 'absent':
                self.delete_syncmembers()
                self.results['changed'] = True
                self.log("SyncMembers instance deleted")
            elif self.state == 'present':
                self.log("Need to check if SyncMembers instance has to be deleted or may be updated")
                to_be_updated = True

        if self.state == 'present':

            self.log("Need to Create / Update the SyncMembers instance")

            if self.check_mode:
                return self.results

            if to_be_updated:
                self.results['state'] = self.create_update_syncmembers()
                self.results['changed'] = True
            else:
                self.results['state'] = response

            self.log("Creation / Update done")

        return self.results

    def create_update_syncmembers(self):
        '''
        Creates or updates SyncMembers with the specified configuration.

        :return: deserialized SyncMembers instance state dictionary
        '''
        self.log("Creating / Updating the SyncMembers instance {0}".format(self.sync_member_name))

        try:
            response = self.mgmt_client.sync_members.create_or_update(self.resource_group_name,
                                                                      self.server_name,
                                                                      self.database_name,
                                                                      self.sync_group_name,
                                                                      self.sync_member_name,
                                                                      self.parameters)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the SyncMembers instance.')
            self.fail("Error creating the SyncMembers instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_syncmembers(self):
        '''
        Deletes specified SyncMembers instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the SyncMembers instance {0}".format(self.sync_member_name))
        try:
            response = self.mgmt_client.sync_members.delete(self.resource_group_name,
                                                            self.server_name,
                                                            self.database_name,
                                                            self.sync_group_name,
                                                            self.sync_member_name)
        except CloudError as e:
            self.log('Error attempting to delete the SyncMembers instance.')
            self.fail("Error deleting the SyncMembers instance: {0}".format(str(e)))

        return True

    def get_syncmembers(self):
        '''
        Gets the properties of the specified SyncMembers.

        :return: deserialized SyncMembers instance state dictionary
        '''
        self.log("Checking if the SyncMembers instance {0} is present".format(self.sync_member_name))
        found = False
        try:
            response = self.mgmt_client.sync_members.get(self.resource_group_name,
                                                         self.server_name,
                                                         self.database_name,
                                                         self.sync_group_name,
                                                         self.sync_member_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("SyncMembers instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the SyncMembers instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMSyncMembers()

if __name__ == '__main__':
    main()

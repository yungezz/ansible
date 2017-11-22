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
module: azure_rm_serverdnsaliases
version_added: "2.5"
short_description: Manage an ServerDnsAliases.
description:
    - Create, update and delete an instance of ServerDnsAliases.

options:
    resource_group_name:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server that the alias is pointing to.
        required: True
    dns_alias_name:
        description:
            - The name of the server DNS alias.
        required: True

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create (or update) ServerDnsAliases
        azure_rm_serverdnsaliases:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          dns_alias_name: "{{ dns_alias_name }}"
'''

RETURN = '''
state:
    description: Current state of ServerDnsAliases
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


class AzureRMServerDnsAliases(AzureRMModuleBase):
    """Configuration class for an Azure RM ServerDnsAliases resource"""

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
            dns_alias_name=dict(
                type='str',
                required=True
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
        self.dns_alias_name = None

        self.results = dict(changed=False, state=dict())
        self.mgmt_client = None
        self.state = None

        super(AzureRMServerDnsAliases, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

        response = None
        results = dict()
        to_be_updated = False

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        try:
            resource_group = self.get_resource_group(self.resource_group)
        except CloudError:
            self.fail('resource group {0} not found'.format(self.resource_group))

        response = self.get_serverdnsaliases()

        if not response:
            self.log("ServerDnsAliases instance doesn't exist")
            if self.state == 'absent':
                self.log("Nothing to delete")
            else:
                to_be_updated = True
        else:
            self.log("ServerDnsAliases instance already exists")
            if self.state == 'absent':
                self.delete_serverdnsaliases()
                self.results['changed'] = True
                self.log("ServerDnsAliases instance deleted")
            elif self.state == 'present':
                self.log("Need to check if ServerDnsAliases instance has to be deleted or may be updated")
                to_be_updated = True

        if self.state == 'present':

            self.log("Need to Create / Update the ServerDnsAliases instance")

            if self.check_mode:
                return self.results

            if to_be_updated:
                self.results['state'] = self.create_update_serverdnsaliases()
                self.results['changed'] = True
            else:
                self.results['state'] = response

            self.log("Creation / Update done")

        return self.results

    def create_update_serverdnsaliases(self):
        '''
        Creates or updates ServerDnsAliases with the specified configuration.

        :return: deserialized ServerDnsAliases instance state dictionary
        '''
        self.log("Creating / Updating the ServerDnsAliases instance {0}".format(self.dns_alias_name))

        try:
            response = self.mgmt_client.server_dns_aliases.create_or_update(self.resource_group_name,
                                                                            self.server_name,
                                                                            self.dns_alias_name)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the ServerDnsAliases instance.')
            self.fail("Error creating the ServerDnsAliases instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_serverdnsaliases(self):
        '''
        Deletes specified ServerDnsAliases instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the ServerDnsAliases instance {0}".format(self.dns_alias_name))
        try:
            response = self.mgmt_client.server_dns_aliases.delete(self.resource_group_name,
                                                                  self.server_name,
                                                                  self.dns_alias_name)
        except CloudError as e:
            self.log('Error attempting to delete the ServerDnsAliases instance.')
            self.fail("Error deleting the ServerDnsAliases instance: {0}".format(str(e)))

        return True

    def get_serverdnsaliases(self):
        '''
        Gets the properties of the specified ServerDnsAliases.

        :return: deserialized ServerDnsAliases instance state dictionary
        '''
        self.log("Checking if the ServerDnsAliases instance {0} is present".format(self.dns_alias_name))
        found = False
        try:
            response = self.mgmt_client.server_dns_aliases.get(self.resource_group_name,
                                                               self.server_name,
                                                               self.dns_alias_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("ServerDnsAliases instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the ServerDnsAliases instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMServerDnsAliases()

if __name__ == '__main__':
    main()

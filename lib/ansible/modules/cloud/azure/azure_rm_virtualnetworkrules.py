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
module: azure_rm_virtualnetworkrules
version_added: "2.5"
short_description: Manage an VirtualNetworkRules.
description:
    - Create, update and delete an instance of VirtualNetworkRules.

options:
    resource_group_name:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    virtual_network_rule_name:
        description:
            - The name of the virtual network rule.
        required: True
    virtual_network_subnet_id:
        description:
            - The ARM resource id of the virtual network subnet.
        required: True
    ignore_missing_vnet_service_endpoint:
        description:
            - Create firewall rule before the virtual network has vnet service endpoint enabled.
        required: False

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create (or update) VirtualNetworkRules
        azure_rm_virtualnetworkrules:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          virtual_network_rule_name: "{{ virtual_network_rule_name }}"
          virtual_network_subnet_id: "{{ virtual_network_subnet_id }}"
          ignore_missing_vnet_service_endpoint: "{{ ignore_missing_vnet_service_endpoint }}"
'''

RETURN = '''
state:
    description: Current state of VirtualNetworkRules
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


class AzureRMVirtualNetworkRules(AzureRMModuleBase):
    """Configuration class for an Azure RM VirtualNetworkRules resource"""

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
            virtual_network_rule_name=dict(
                type='str',
                required=True
            ),
            virtual_network_subnet_id=dict(
                type='str',
                required=True
            ),
            ignore_missing_vnet_service_endpoint=dict(
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
        self.virtual_network_rule_name = None
        self.parameters = dict()

        self.results = dict(changed=False, state=dict())
        self.mgmt_client = None
        self.state = None

        super(AzureRMVirtualNetworkRules, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                         supports_check_mode=True,
                                                         supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif key == "virtual_network_subnet_id":
                self.parameters["virtual_network_subnet_id"] = kwargs[key]
            elif key == "ignore_missing_vnet_service_endpoint":
                self.parameters["ignore_missing_vnet_service_endpoint"] = kwargs[key]

        response = None
        results = dict()
        to_be_updated = False

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        try:
            resource_group = self.get_resource_group(self.resource_group)
        except CloudError:
            self.fail('resource group {0} not found'.format(self.resource_group))

        response = self.get_virtualnetworkrules()

        if not response:
            self.log("VirtualNetworkRules instance doesn't exist")
            if self.state == 'absent':
                self.log("Nothing to delete")
            else:
                to_be_updated = True
        else:
            self.log("VirtualNetworkRules instance already exists")
            if self.state == 'absent':
                self.delete_virtualnetworkrules()
                self.results['changed'] = True
                self.log("VirtualNetworkRules instance deleted")
            elif self.state == 'present':
                self.log("Need to check if VirtualNetworkRules instance has to be deleted or may be updated")
                to_be_updated = True

        if self.state == 'present':

            self.log("Need to Create / Update the VirtualNetworkRules instance")

            if self.check_mode:
                return self.results

            if to_be_updated:
                self.results['state'] = self.create_update_virtualnetworkrules()
                self.results['changed'] = True
            else:
                self.results['state'] = response

            self.log("Creation / Update done")

        return self.results

    def create_update_virtualnetworkrules(self):
        '''
        Creates or updates VirtualNetworkRules with the specified configuration.

        :return: deserialized VirtualNetworkRules instance state dictionary
        '''
        self.log("Creating / Updating the VirtualNetworkRules instance {0}".format(self.virtual_network_rule_name))

        try:
            response = self.mgmt_client.virtual_network_rules.create_or_update(self.resource_group_name,
                                                                               self.server_name,
                                                                               self.virtual_network_rule_name,
                                                                               self.parameters)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the VirtualNetworkRules instance.')
            self.fail("Error creating the VirtualNetworkRules instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_virtualnetworkrules(self):
        '''
        Deletes specified VirtualNetworkRules instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the VirtualNetworkRules instance {0}".format(self.virtual_network_rule_name))
        try:
            response = self.mgmt_client.virtual_network_rules.delete(self.resource_group_name,
                                                                     self.server_name,
                                                                     self.virtual_network_rule_name)
        except CloudError as e:
            self.log('Error attempting to delete the VirtualNetworkRules instance.')
            self.fail("Error deleting the VirtualNetworkRules instance: {0}".format(str(e)))

        return True

    def get_virtualnetworkrules(self):
        '''
        Gets the properties of the specified VirtualNetworkRules.

        :return: deserialized VirtualNetworkRules instance state dictionary
        '''
        self.log("Checking if the VirtualNetworkRules instance {0} is present".format(self.virtual_network_rule_name))
        found = False
        try:
            response = self.mgmt_client.virtual_network_rules.get(self.resource_group_name,
                                                                  self.server_name,
                                                                  self.virtual_network_rule_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("VirtualNetworkRules instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the VirtualNetworkRules instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMVirtualNetworkRules()

if __name__ == '__main__':
    main()

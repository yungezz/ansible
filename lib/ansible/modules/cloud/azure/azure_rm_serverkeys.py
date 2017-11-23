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
module: azure_rm_serverkeys
version_added: "2.5"
short_description: Manage an ServerKeys.
description:
    - Create, update and delete an instance of ServerKeys.

options:
    resource_group_name:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    key_name:
        description:
            - "The name of the server key to be operated on (updated or created). The key name is required to be in the format of 'vault_key_version'. For ex
               ample, if the keyId is https://YourVaultName.vault.azure.net/keys/YourKeyName/01234567890123456789012345678901, then the server key name shoul
               d be formatted as: YourVaultName_YourKeyName_01234567890123456789012345678901"
        required: True
    kind:
        description:
            - Kind of encryption protector. This is metadata used for the Azure portal experience.
        required: False
    server_key_type:
        description:
            - "The server key type like 'ServiceManaged', 'AzureKeyVault'. Possible values include: 'ServiceManaged', 'AzureKeyVault'
        required: True
    uri:
        description:
            - The URI of the server key.
        required: False
    thumbprint:
        description:
            - Thumbprint of the server key.
        required: False
    creation_date:
        description:
            - The server key creation date.
        required: False

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create (or update) ServerKeys
        azure_rm_serverkeys:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          key_name: "{{ key_name }}"
          kind: "{{ kind }}"
          server_key_type: "{{ server_key_type }}"
          uri: "{{ uri }}"
          thumbprint: "{{ thumbprint }}"
          creation_date: "{{ creation_date }}"
'''

RETURN = '''
state:
    description: Current state of ServerKeys
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


class AzureRMServerKeys(AzureRMModuleBase):
    """Configuration class for an Azure RM ServerKeys resource"""

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
            key_name=dict(
                type='str',
                required=True
            ),
            kind=dict(
                type='str',
                required=False
            ),
            server_key_type=dict(
                type='str',
                required=True
            ),
            uri=dict(
                type='str',
                required=False
            ),
            thumbprint=dict(
                type='str',
                required=False
            ),
            creation_date=dict(
                type='datetime',
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
        self.key_name = None
        self.parameters = dict()

        self.results = dict(changed=False, state=dict())
        self.mgmt_client = None
        self.state = None

        super(AzureRMServerKeys, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                supports_check_mode=True,
                                                supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif key == "kind":
                self.parameters["kind"] = kwargs[key]
            elif key == "server_key_type":
                self.parameters["server_key_type"] = kwargs[key]
            elif key == "uri":
                self.parameters["uri"] = kwargs[key]
            elif key == "thumbprint":
                self.parameters["thumbprint"] = kwargs[key]
            elif key == "creation_date":
                self.parameters["creation_date"] = kwargs[key]

        response = None
        results = dict()
        to_be_updated = False

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        try:
            resource_group = self.get_resource_group(self.resource_group)
        except CloudError:
            self.fail('resource group {0} not found'.format(self.resource_group))

        response = self.get_serverkeys()

        if not response:
            self.log("ServerKeys instance doesn't exist")
            if self.state == 'absent':
                self.log("Nothing to delete")
            else:
                to_be_updated = True
        else:
            self.log("ServerKeys instance already exists")
            if self.state == 'absent':
                self.delete_serverkeys()
                self.results['changed'] = True
                self.log("ServerKeys instance deleted")
            elif self.state == 'present':
                self.log("Need to check if ServerKeys instance has to be deleted or may be updated")
                to_be_updated = True

        if self.state == 'present':

            self.log("Need to Create / Update the ServerKeys instance")

            if self.check_mode:
                return self.results

            if to_be_updated:
                self.results['state'] = self.create_update_serverkeys()
                self.results['changed'] = True
            else:
                self.results['state'] = response

            self.log("Creation / Update done")

        return self.results

    def create_update_serverkeys(self):
        '''
        Creates or updates ServerKeys with the specified configuration.

        :return: deserialized ServerKeys instance state dictionary
        '''
        self.log("Creating / Updating the ServerKeys instance {0}".format(self.key_name))

        try:
            response = self.mgmt_client.server_keys.create_or_update(self.resource_group_name,
                                                                     self.server_name,
                                                                     self.key_name,
                                                                     self.parameters)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the ServerKeys instance.')
            self.fail("Error creating the ServerKeys instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_serverkeys(self):
        '''
        Deletes specified ServerKeys instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the ServerKeys instance {0}".format(self.key_name))
        try:
            response = self.mgmt_client.server_keys.delete(self.resource_group_name,
                                                           self.server_name,
                                                           self.key_name)
        except CloudError as e:
            self.log('Error attempting to delete the ServerKeys instance.')
            self.fail("Error deleting the ServerKeys instance: {0}".format(str(e)))

        return True

    def get_serverkeys(self):
        '''
        Gets the properties of the specified ServerKeys.

        :return: deserialized ServerKeys instance state dictionary
        '''
        self.log("Checking if the ServerKeys instance {0} is present".format(self.key_name))
        found = False
        try:
            response = self.mgmt_client.server_keys.get(self.resource_group_name,
                                                        self.server_name,
                                                        self.key_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("ServerKeys instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the ServerKeys instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMServerKeys()

if __name__ == '__main__':
    main()

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
module: azure_rm_encryptionprotectors
version_added: "2.5"
short_description: Manage an EncryptionProtectors.
description:
    - Create, update and delete an instance of EncryptionProtectors.

options:
    resource_group_name:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    encryption_protector_name:
        description:
            - The name of the encryption protector to be updated.
        required: True
    kind:
        description:
            - Kind of encryption protector. This is metadata used for the Azure portal experience.
        required: False
    server_key_name:
        description:
            - The name of the server key.
        required: False
    server_key_type:
        description:
            - "The encryption protector type like 'ServiceManaged', 'AzureKeyVault'. Possible values include: 'ServiceManaged', 'AzureKeyVault'
        required: True

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create (or update) EncryptionProtectors
        azure_rm_encryptionprotectors:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          encryption_protector_name: "{{ encryption_protector_name }}"
          kind: "{{ kind }}"
          server_key_name: "{{ server_key_name }}"
          server_key_type: "{{ server_key_type }}"
'''

RETURN = '''
state:
    description: Current state of EncryptionProtectors
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


class AzureRMEncryptionProtectors(AzureRMModuleBase):
    """Configuration class for an Azure RM EncryptionProtectors resource"""

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
            encryption_protector_name=dict(
                type='str',
                required=True
            ),
            kind=dict(
                type='str',
                required=False
            ),
            server_key_name=dict(
                type='str',
                required=False
            ),
            server_key_type=dict(
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
        self.encryption_protector_name = None
        self.parameters = dict()

        self.results = dict(changed=False, state=dict())
        self.mgmt_client = None
        self.state = None

        super(AzureRMEncryptionProtectors, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                          supports_check_mode=True,
                                                          supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif key == "kind":
                self.parameters["kind"] = kwargs[key]
            elif key == "server_key_name":
                self.parameters["server_key_name"] = kwargs[key]
            elif key == "server_key_type":
                self.parameters["server_key_type"] = kwargs[key]

        response = None
        results = dict()
        to_be_updated = False

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        try:
            resource_group = self.get_resource_group(self.resource_group)
        except CloudError:
            self.fail('resource group {0} not found'.format(self.resource_group))

        response = self.get_encryptionprotectors()

        if not response:
            self.log("EncryptionProtectors instance doesn't exist")
            if self.state == 'absent':
                self.log("Nothing to delete")
            else:
                to_be_updated = True
        else:
            self.log("EncryptionProtectors instance already exists")
            if self.state == 'absent':
                self.delete_encryptionprotectors()
                self.results['changed'] = True
                self.log("EncryptionProtectors instance deleted")
            elif self.state == 'present':
                self.log("Need to check if EncryptionProtectors instance has to be deleted or may be updated")
                to_be_updated = True

        if self.state == 'present':

            self.log("Need to Create / Update the EncryptionProtectors instance")

            if self.check_mode:
                return self.results

            if to_be_updated:
                self.results['state'] = self.create_update_encryptionprotectors()
                self.results['changed'] = True
            else:
                self.results['state'] = response

            self.log("Creation / Update done")

        return self.results

    def create_update_encryptionprotectors(self):
        '''
        Creates or updates EncryptionProtectors with the specified configuration.

        :return: deserialized EncryptionProtectors instance state dictionary
        '''
        self.log("Creating / Updating the EncryptionProtectors instance {0}".format(self.encryption_protector_name))

        try:
            response = self.mgmt_client.encryption_protectors.create_or_update(self.resource_group_name,
                                                                               self.server_name,
                                                                               self.encryption_protector_name,
                                                                               self.parameters)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the EncryptionProtectors instance.')
            self.fail("Error creating the EncryptionProtectors instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_encryptionprotectors(self):
        '''
        Deletes specified EncryptionProtectors instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the EncryptionProtectors instance {0}".format(self.encryption_protector_name))
        try:
            response = self.mgmt_client.encryption_protectors.delete()
        except CloudError as e:
            self.log('Error attempting to delete the EncryptionProtectors instance.')
            self.fail("Error deleting the EncryptionProtectors instance: {0}".format(str(e)))

        return True

    def get_encryptionprotectors(self):
        '''
        Gets the properties of the specified EncryptionProtectors.

        :return: deserialized EncryptionProtectors instance state dictionary
        '''
        self.log("Checking if the EncryptionProtectors instance {0} is present".format(self.encryption_protector_name))
        found = False
        try:
            response = self.mgmt_client.encryption_protectors.get(self.resource_group_name,
                                                                  self.server_name,
                                                                  self.encryption_protector_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("EncryptionProtectors instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the EncryptionProtectors instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMEncryptionProtectors()

if __name__ == '__main__':
    main()

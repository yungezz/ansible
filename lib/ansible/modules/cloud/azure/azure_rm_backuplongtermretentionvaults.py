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
module: azure_rm_backuplongtermretentionvaults
version_added: "2.5"
short_description: Manage an BackupLongTermRetentionVaults.
description:
    - Create, update and delete an instance of BackupLongTermRetentionVaults.

options:
    resource_group_name:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    backup_long_term_retention_vault_name:
        description:
            - The name of the backup long term retention vault
        required: True
    recovery_services_vault_resource_id:
        description:
            - The azure recovery services vault resource id
        required: True

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create (or update) BackupLongTermRetentionVaults
        azure_rm_backuplongtermretentionvaults:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          backup_long_term_retention_vault_name: "{{ backup_long_term_retention_vault_name }}"
          recovery_services_vault_resource_id: "{{ recovery_services_vault_resource_id }}"
'''

RETURN = '''
state:
    description: Current state of BackupLongTermRetentionVaults
    returned: always
    type: dict
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.backuplongtermretentionvaults import backuplongtermretentionvaults
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMBackupLongTermRetentionVaults(AzureRMModuleBase):
    """Configuration class for an Azure RM BackupLongTermRetentionVaults resource"""

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
            backup_long_term_retention_vault_name=dict(
                type='str',
                required=True
            ),
            recovery_services_vault_resource_id=dict(
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
        self.backup_long_term_retention_vault_name = None
        self.parameters = dict()

        self.results = dict(changed=False, state=dict())
        self.mgmt_client = None
        self.state = None

        super(AzureRMBackupLongTermRetentionVaults, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                   supports_check_mode=True,
                                                                   supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif key == "recovery_services_vault_resource_id":
                self.parameters["recovery_services_vault_resource_id"] = kwargs[key]

        response = None
        results = dict()
        to_be_updated = False

        self.mgmt_client = self.get_mgmt_svc_client(backuplongtermretentionvaults,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        try:
            resource_group = self.get_resource_group(self.resource_group)
        except CloudError:
            self.fail('resource group {0} not found'.format(self.resource_group))

        response = self.get_backuplongtermretentionvaults()

        if not response:
            self.log("BackupLongTermRetentionVaults instance doesn't exist")
            if self.state == 'absent':
                self.log("Nothing to delete")
            else:
                to_be_updated = True
        else:
            self.log("BackupLongTermRetentionVaults instance already exists")
            if self.state == 'absent':
                self.delete_backuplongtermretentionvaults()
                self.results['changed'] = True
                self.log("BackupLongTermRetentionVaults instance deleted")
            elif self.state == 'present':
                self.log("Need to check if BackupLongTermRetentionVaults instance has to be deleted or may be updated")
                to_be_updated = True

        if self.state == 'present':

            self.log("Need to Create / Update the BackupLongTermRetentionVaults instance")

            if self.check_mode:
                return self.results

            if to_be_updated:
                self.results['state'] = self.create_update_backuplongtermretentionvaults()
                self.results['changed'] = True
            else:
                self.results['state'] = response

            self.log("Creation / Update done")

        return self.results

    def create_update_backuplongtermretentionvaults(self):
        '''
        Creates or updates BackupLongTermRetentionVaults with the specified configuration.

        :return: deserialized BackupLongTermRetentionVaults instance state dictionary
        '''
        self.log("Creating / Updating the BackupLongTermRetentionVaults instance {0}".format(self.backup_long_term_retention_vault_name))

        try:
            response = self.mgmt_client.backup_long_term_retention_vaults.create_or_update(self.resource_group_name,
                                                                                           self.server_name,
                                                                                           self.backup_long_term_retention_vault_name,
                                                                                           self.parameters)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the BackupLongTermRetentionVaults instance.')
            self.fail("Error creating the BackupLongTermRetentionVaults instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_backuplongtermretentionvaults(self):
        '''
        Deletes specified BackupLongTermRetentionVaults instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the BackupLongTermRetentionVaults instance {0}".format(self.backup_long_term_retention_vault_name))
        try:
            response = self.mgmt_client.backup_long_term_retention_vaults.delete()
        except CloudError as e:
            self.log('Error attempting to delete the BackupLongTermRetentionVaults instance.')
            self.fail("Error deleting the BackupLongTermRetentionVaults instance: {0}".format(str(e)))

        return True

    def get_backuplongtermretentionvaults(self):
        '''
        Gets the properties of the specified BackupLongTermRetentionVaults.

        :return: deserialized BackupLongTermRetentionVaults instance state dictionary
        '''
        self.log("Checking if the BackupLongTermRetentionVaults instance {0} is present".format(self.backup_long_term_retention_vault_name))
        found = False
        try:
            response = self.mgmt_client.backup_long_term_retention_vaults.get(self.resource_group_name,
                                                                              self.server_name,
                                                                              self.backup_long_term_retention_vault_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("BackupLongTermRetentionVaults instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the BackupLongTermRetentionVaults instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMBackupLongTermRetentionVaults()

if __name__ == '__main__':
    main()

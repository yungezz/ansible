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
module: azure_rm_databaseblobauditingpolicies
version_added: "2.5"
short_description: Manage an DatabaseBlobAuditingPolicies.
description:
    - Create, update and delete an instance of DatabaseBlobAuditingPolicies.

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
            - The name of the database for which the blob auditing policy will be defined.
        required: True
    blob_auditing_policy_name:
        description:
            - The name of the blob auditing policy.
        required: True
    state:
        description:
            - "Specifies the state of the policy. If state is Enabled, storageEndpoint and storageAccountAccessKey are required. Possible values include: 'En
               abled', 'Disabled'"
        required: True
    storage_endpoint:
        description:
            - Specifies the blob storage endpoint (e.g. https://MyAccount.blob.core.windows.net). If state is Enabled, storageEndpoint is required.
        required: False
    storage_account_access_key:
        description:
            - Specifies the identifier key of the auditing storage account. If state is Enabled, storageAccountAccessKey is required.
        required: False
    retention_days:
        description:
            - Specifies the number of days to keep in the audit logs.
        required: False
    audit_actions_and_groups:
        description:
            - Specifies the Actions and Actions-Groups to audit.
        required: False
    storage_account_subscription_id:
        description:
            - Specifies the blob storage subscription Id.
        required: False
    is_storage_secondary_key_in_use:
        description:
            - "Specifies whether storageAccountAccessKey value is the storage's secondary key.
        required: False

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create (or update) DatabaseBlobAuditingPolicies
        azure_rm_databaseblobauditingpolicies:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          database_name: "{{ database_name }}"
          blob_auditing_policy_name: "{{ blob_auditing_policy_name }}"
          state: "{{ state }}"
          storage_endpoint: "{{ storage_endpoint }}"
          storage_account_access_key: "{{ storage_account_access_key }}"
          retention_days: "{{ retention_days }}"
          audit_actions_and_groups:
            - XXXX - list of values -- not implemented str
          storage_account_subscription_id: "{{ storage_account_subscription_id }}"
          is_storage_secondary_key_in_use: "{{ is_storage_secondary_key_in_use }}"
'''

RETURN = '''
state:
    description: Current state of DatabaseBlobAuditingPolicies
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


class AzureRMDatabaseBlobAuditingPolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM DatabaseBlobAuditingPolicies resource"""

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
            blob_auditing_policy_name=dict(
                type='str',
                required=True
            ),
            state=dict(
                type='str',
                required=True
            ),
            storage_endpoint=dict(
                type='str',
                required=False
            ),
            storage_account_access_key=dict(
                type='str',
                required=False
            ),
            retention_days=dict(
                type='int',
                required=False
            ),
            audit_actions_and_groups=dict(
                type='str',
                required=False
            ),
            storage_account_subscription_id=dict(
                type='str',
                required=False
            ),
            is_storage_secondary_key_in_use=dict(
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
        self.blob_auditing_policy_name = None
        self.parameters = dict()

        self.results = dict(changed=False, state=dict())
        self.mgmt_client = None
        self.state = None

        super(AzureRMDatabaseBlobAuditingPolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                  supports_check_mode=True,
                                                                  supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif key == "state":
                self.parameters["state"] = kwargs[key]
            elif key == "storage_endpoint":
                self.parameters["storage_endpoint"] = kwargs[key]
            elif key == "storage_account_access_key":
                self.parameters["storage_account_access_key"] = kwargs[key]
            elif key == "retention_days":
                self.parameters["retention_days"] = kwargs[key]
            elif key == "audit_actions_and_groups":
                self.parameters["audit_actions_and_groups"] = kwargs[key]
            elif key == "storage_account_subscription_id":
                self.parameters["storage_account_subscription_id"] = kwargs[key]
            elif key == "is_storage_secondary_key_in_use":
                self.parameters["is_storage_secondary_key_in_use"] = kwargs[key]

        response = None
        results = dict()
        to_be_updated = False

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        try:
            resource_group = self.get_resource_group(self.resource_group)
        except CloudError:
            self.fail('resource group {0} not found'.format(self.resource_group))

        response = self.get_blobauditingpolicies()

        if not response:
            self.log("DatabaseBlobAuditingPolicies instance doesn't exist")
            if self.state == 'absent':
                self.log("Nothing to delete")
            else:
                to_be_updated = True
        else:
            self.log("DatabaseBlobAuditingPolicies instance already exists")
            if self.state == 'absent':
                self.delete_blobauditingpolicies()
                self.results['changed'] = True
                self.log("DatabaseBlobAuditingPolicies instance deleted")
            elif self.state == 'present':
                self.log("Need to check if DatabaseBlobAuditingPolicies instance has to be deleted or may be updated")
                to_be_updated = True

        if self.state == 'present':

            self.log("Need to Create / Update the DatabaseBlobAuditingPolicies instance")

            if self.check_mode:
                return self.results

            if to_be_updated:
                self.results['state'] = self.create_update_blobauditingpolicies()
                self.results['changed'] = True
            else:
                self.results['state'] = response

            self.log("Creation / Update done")

        return self.results

    def create_update_blobauditingpolicies(self):
        '''
        Creates or updates DatabaseBlobAuditingPolicies with the specified configuration.

        :return: deserialized DatabaseBlobAuditingPolicies instance state dictionary
        '''
        self.log("Creating / Updating the DatabaseBlobAuditingPolicies instance {0}".format(self.blob_auditing_policy_name))

        try:
            response = self.mgmt_client.database_blob_auditing_policies.create_or_update(self.resource_group_name,
                                                                                         self.server_name,
                                                                                         self.database_name,
                                                                                         self.blob_auditing_policy_name,
                                                                                         self.parameters)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the DatabaseBlobAuditingPolicies instance.')
            self.fail("Error creating the DatabaseBlobAuditingPolicies instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_blobauditingpolicies(self):
        '''
        Deletes specified DatabaseBlobAuditingPolicies instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the DatabaseBlobAuditingPolicies instance {0}".format(self.blob_auditing_policy_name))
        try:
            response = self.mgmt_client.database_blob_auditing_policies.delete()
        except CloudError as e:
            self.log('Error attempting to delete the DatabaseBlobAuditingPolicies instance.')
            self.fail("Error deleting the DatabaseBlobAuditingPolicies instance: {0}".format(str(e)))

        return True

    def get_blobauditingpolicies(self):
        '''
        Gets the properties of the specified DatabaseBlobAuditingPolicies.

        :return: deserialized DatabaseBlobAuditingPolicies instance state dictionary
        '''
        self.log("Checking if the DatabaseBlobAuditingPolicies instance {0} is present".format(self.blob_auditing_policy_name))
        found = False
        try:
            response = self.mgmt_client.database_blob_auditing_policies.get(self.resource_group_name,
                                                                            self.server_name,
                                                                            self.database_name,
                                                                            self.blob_auditing_policy_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("DatabaseBlobAuditingPolicies instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the DatabaseBlobAuditingPolicies instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMDatabaseBlobAuditingPolicies()

if __name__ == '__main__':
    main()

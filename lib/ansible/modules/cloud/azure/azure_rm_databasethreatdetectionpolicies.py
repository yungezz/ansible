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
module: azure_rm_databasethreatdetectionpolicies
version_added: "2.5"
short_description: Manage an DatabaseThreatDetectionPolicies.
description:
    - Create, update and delete an instance of DatabaseThreatDetectionPolicies.

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
            - The name of the database for which database Threat Detection policy is defined.
        required: True
    security_alert_policy_name:
        description:
            - The name of the security alert policy.
        required: True
    location:
        description:
            - The geo-location where the resource lives
        required: False
    state:
        description:
            - "Specifies the state of the policy. If state is Enabled, storageEndpoint and storageAccountAccessKey are required. Possible values include: 'Ne
               w', 'Enabled', 'Disabled'"
        required: True
    disabled_alerts:
        description:
            - "Specifies the semicolon-separated list of alerts that are disabled, or empty string to disable no alerts. Possible values: Sql_Injection; Sql_
               Injection_Vulnerability; Access_Anomaly; Usage_Anomaly."
        required: False
    email_addresses:
        description:
            - Specifies the semicolon-separated list of e-mail addresses to which the alert is sent.
        required: False
    email_account_admins:
        description:
            - "Specifies that the alert is sent to the account administrators. Possible values include: 'Enabled', 'Disabled'
        required: False
    storage_endpoint:
        description:
            - "Specifies the blob storage endpoint (e.g. https://MyAccount.blob.core.windows.net). This blob storage will hold all Threat Detection audit log
               s. If state is Enabled, storageEndpoint is required."
        required: False
    storage_account_access_key:
        description:
            - Specifies the identifier key of the Threat Detection audit storage account. If state is Enabled, storageAccountAccessKey is required.
        required: False
    retention_days:
        description:
            - Specifies the number of days to keep in the Threat Detection audit logs.
        required: False
    use_server_default:
        description:
            - "Specifies whether to use the default server policy. Possible values include: 'Enabled', 'Disabled'
        required: False

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create (or update) DatabaseThreatDetectionPolicies
        azure_rm_databasethreatdetectionpolicies:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          database_name: "{{ database_name }}"
          security_alert_policy_name: "{{ security_alert_policy_name }}"
          location: "{{ location }}"
          state: "{{ state }}"
          disabled_alerts: "{{ disabled_alerts }}"
          email_addresses: "{{ email_addresses }}"
          email_account_admins: "{{ email_account_admins }}"
          storage_endpoint: "{{ storage_endpoint }}"
          storage_account_access_key: "{{ storage_account_access_key }}"
          retention_days: "{{ retention_days }}"
          use_server_default: "{{ use_server_default }}"
'''

RETURN = '''
state:
    description: Current state of DatabaseThreatDetectionPolicies
    returned: always
    type: dict
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.databasesecurityalertpolicies import databasesecurityalertpolicies
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDatabaseThreatDetectionPolicies(AzureRMModuleBase):
    """Configuration class for an Azure RM DatabaseThreatDetectionPolicies resource"""

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
            security_alert_policy_name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
                required=False
            ),
            state=dict(
                type='str',
                required=True
            ),
            disabled_alerts=dict(
                type='str',
                required=False
            ),
            email_addresses=dict(
                type='str',
                required=False
            ),
            email_account_admins=dict(
                type='str',
                required=False
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
            use_server_default=dict(
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
        self.security_alert_policy_name = None
        self.parameters = dict()

        self.results = dict(changed=False, state=dict())
        self.mgmt_client = None
        self.state = None

        super(AzureRMDatabaseThreatDetectionPolicies, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                     supports_check_mode=True,
                                                                     supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif key == "location":
                self.parameters["location"] = kwargs[key]
            elif key == "state":
                self.parameters["state"] = kwargs[key]
            elif key == "disabled_alerts":
                self.parameters["disabled_alerts"] = kwargs[key]
            elif key == "email_addresses":
                self.parameters["email_addresses"] = kwargs[key]
            elif key == "email_account_admins":
                self.parameters["email_account_admins"] = kwargs[key]
            elif key == "storage_endpoint":
                self.parameters["storage_endpoint"] = kwargs[key]
            elif key == "storage_account_access_key":
                self.parameters["storage_account_access_key"] = kwargs[key]
            elif key == "retention_days":
                self.parameters["retention_days"] = kwargs[key]
            elif key == "use_server_default":
                self.parameters["use_server_default"] = kwargs[key]

        response = None
        results = dict()
        to_be_updated = False

        self.mgmt_client = self.get_mgmt_svc_client(databasesecurityalertpolicies,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        try:
            resource_group = self.get_resource_group(self.resource_group)
        except CloudError:
            self.fail('resource group {0} not found'.format(self.resource_group))

        response = self.get_databasesecurityalertpolicies()

        if not response:
            self.log("DatabaseThreatDetectionPolicies instance doesn't exist")
            if self.state == 'absent':
                self.log("Nothing to delete")
            else:
                to_be_updated = True
        else:
            self.log("DatabaseThreatDetectionPolicies instance already exists")
            if self.state == 'absent':
                self.delete_databasesecurityalertpolicies()
                self.results['changed'] = True
                self.log("DatabaseThreatDetectionPolicies instance deleted")
            elif self.state == 'present':
                self.log("Need to check if DatabaseThreatDetectionPolicies instance has to be deleted or may be updated")
                to_be_updated = True

        if self.state == 'present':

            self.log("Need to Create / Update the DatabaseThreatDetectionPolicies instance")

            if self.check_mode:
                return self.results

            if to_be_updated:
                self.results['state'] = self.create_update_databasesecurityalertpolicies()
                self.results['changed'] = True
            else:
                self.results['state'] = response

            self.log("Creation / Update done")

        return self.results

    def create_update_databasesecurityalertpolicies(self):
        '''
        Creates or updates DatabaseThreatDetectionPolicies with the specified configuration.

        :return: deserialized DatabaseThreatDetectionPolicies instance state dictionary
        '''
        self.log("Creating / Updating the DatabaseThreatDetectionPolicies instance {0}".format(self.security_alert_policy_name))

        try:
            response = self.mgmt_client.database_threat_detection_policies.create_or_update(self.resource_group_name,
                                                                                            self.server_name,
                                                                                            self.database_name,
                                                                                            self.security_alert_policy_name,
                                                                                            self.parameters)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the DatabaseThreatDetectionPolicies instance.')
            self.fail("Error creating the DatabaseThreatDetectionPolicies instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_databasesecurityalertpolicies(self):
        '''
        Deletes specified DatabaseThreatDetectionPolicies instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the DatabaseThreatDetectionPolicies instance {0}".format(self.security_alert_policy_name))
        try:
            response = self.mgmt_client.database_threat_detection_policies.delete()
        except CloudError as e:
            self.log('Error attempting to delete the DatabaseThreatDetectionPolicies instance.')
            self.fail("Error deleting the DatabaseThreatDetectionPolicies instance: {0}".format(str(e)))

        return True

    def get_databasesecurityalertpolicies(self):
        '''
        Gets the properties of the specified DatabaseThreatDetectionPolicies.

        :return: deserialized DatabaseThreatDetectionPolicies instance state dictionary
        '''
        self.log("Checking if the DatabaseThreatDetectionPolicies instance {0} is present".format(self.security_alert_policy_name))
        found = False
        try:
            response = self.mgmt_client.database_threat_detection_policies.get(self.resource_group_name,
                                                                               self.server_name,
                                                                               self.database_name,
                                                                               self.security_alert_policy_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("DatabaseThreatDetectionPolicies instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the DatabaseThreatDetectionPolicies instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMDatabaseThreatDetectionPolicies()

if __name__ == '__main__':
    main()

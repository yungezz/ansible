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
module: azure_rm_datamasking_datamaskingrules
version_added: "2.5"
short_description: Manage an DataMaskingRules.
description:
    - Create, update and delete an instance of DataMaskingRules.

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
            - The name of the database.
        required: True
    data_masking_policy_name:
        description:
            - The name of the database for which the data masking rule applies.
        required: True
    data_masking_rule_name:
        description:
            - The name of the data masking rule.
        required: True
    alias_name:
        description:
            - The alias name. This is a legacy parameter and is no longer used.
        required: False
    rule_state:
        description:
            - "The rule state. Used to delete a rule. To delete an existing rule, specify the schemaName, tableName, columnName, maskingFunction, and specify
                ruleState as disabled. However, if the rule doesn't already exist, the rule will be created with ruleState set to enabled, regardless of the
               provided value of ruleState. Possible values include: 'Disabled', 'Enabled'"
        required: False
    schema_name:
        description:
            - The schema name on which the data masking rule is applied.
        required: True
    table_name:
        description:
            - The table name on which the data masking rule is applied.
        required: True
    column_name:
        description:
            - The column name on which the data masking rule is applied.
        required: True
    masking_function:
        description:
            - "The masking function that is used for the data masking rule. Possible values include: 'Default', 'CCN', 'Email', 'Number', 'SSN', 'Text'
        required: True
    number_from:
        description:
            - The numberFrom property of the masking rule. Required if maskingFunction is set to Number, otherwise this parameter will be ignored.
        required: False
    number_to:
        description:
            - The numberTo property of the data masking rule. Required if maskingFunction is set to Number, otherwise this parameter will be ignored.
        required: False
    prefix_size:
        description:
            - "If maskingFunction is set to Text, the number of characters to show unmasked in the beginning of the string. Otherwise, this parameter will be
                ignored."
        required: False
    suffix_size:
        description:
            - If maskingFunction is set to Text, the number of characters to show unmasked at the end of the string. Otherwise, this parameter will be ignored.
        required: False
    replacement_string:
        description:
            - If maskingFunction is set to Text, the character to use for masking the unexposed part of the string. Otherwise, this parameter will be ignored.
        required: False

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create (or update) DataMaskingRules
        azure_rm_datamasking_datamaskingrules:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          database_name: "{{ database_name }}"
          data_masking_policy_name: "{{ data_masking_policy_name }}"
          data_masking_rule_name: "{{ data_masking_rule_name }}"
          alias_name: "{{ alias_name }}"
          rule_state: "{{ rule_state }}"
          schema_name: "{{ schema_name }}"
          table_name: "{{ table_name }}"
          column_name: "{{ column_name }}"
          masking_function: "{{ masking_function }}"
          number_from: "{{ number_from }}"
          number_to: "{{ number_to }}"
          prefix_size: "{{ prefix_size }}"
          suffix_size: "{{ suffix_size }}"
          replacement_string: "{{ replacement_string }}"
'''

RETURN = '''
state:
    description: Current state of DataMaskingRules
    returned: always
    type: dict
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.datamasking import datamasking
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMDataMaskingRules(AzureRMModuleBase):
    """Configuration class for an Azure RM DataMaskingRules resource"""

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
            data_masking_policy_name=dict(
                type='str',
                required=True
            ),
            data_masking_rule_name=dict(
                type='str',
                required=True
            ),
            alias_name=dict(
                type='str',
                required=False
            ),
            rule_state=dict(
                type='str',
                required=False
            ),
            schema_name=dict(
                type='str',
                required=True
            ),
            table_name=dict(
                type='str',
                required=True
            ),
            column_name=dict(
                type='str',
                required=True
            ),
            masking_function=dict(
                type='str',
                required=True
            ),
            number_from=dict(
                type='str',
                required=False
            ),
            number_to=dict(
                type='str',
                required=False
            ),
            prefix_size=dict(
                type='str',
                required=False
            ),
            suffix_size=dict(
                type='str',
                required=False
            ),
            replacement_string=dict(
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
        self.data_masking_policy_name = None
        self.data_masking_rule_name = None
        self.parameters = dict()

        self.results = dict(changed=False, state=dict())
        self.mgmt_client = None
        self.state = None

        super(AzureRMDataMaskingRules, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                      supports_check_mode=True,
                                                      supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif key == "alias_name":
                self.parameters["alias_name"] = kwargs[key]
            elif key == "rule_state":
                self.parameters["rule_state"] = kwargs[key]
            elif key == "schema_name":
                self.parameters["schema_name"] = kwargs[key]
            elif key == "table_name":
                self.parameters["table_name"] = kwargs[key]
            elif key == "column_name":
                self.parameters["column_name"] = kwargs[key]
            elif key == "masking_function":
                self.parameters["masking_function"] = kwargs[key]
            elif key == "number_from":
                self.parameters["number_from"] = kwargs[key]
            elif key == "number_to":
                self.parameters["number_to"] = kwargs[key]
            elif key == "prefix_size":
                self.parameters["prefix_size"] = kwargs[key]
            elif key == "suffix_size":
                self.parameters["suffix_size"] = kwargs[key]
            elif key == "replacement_string":
                self.parameters["replacement_string"] = kwargs[key]

        response = None
        results = dict()
        to_be_updated = False

        self.mgmt_client = self.get_mgmt_svc_client(datamasking,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        try:
            resource_group = self.get_resource_group(self.resource_group)
        except CloudError:
            self.fail('resource group {0} not found'.format(self.resource_group))

        response = self.get_datamasking()

        if not response:
            self.log("DataMaskingRules instance doesn't exist")
            if self.state == 'absent':
                self.log("Nothing to delete")
            else:
                to_be_updated = True
        else:
            self.log("DataMaskingRules instance already exists")
            if self.state == 'absent':
                self.delete_datamasking()
                self.results['changed'] = True
                self.log("DataMaskingRules instance deleted")
            elif self.state == 'present':
                self.log("Need to check if DataMaskingRules instance has to be deleted or may be updated")
                to_be_updated = True

        if self.state == 'present':

            self.log("Need to Create / Update the DataMaskingRules instance")

            if self.check_mode:
                return self.results

            if to_be_updated:
                self.results['state'] = self.create_update_datamasking()
                self.results['changed'] = True
            else:
                self.results['state'] = response

            self.log("Creation / Update done")

        return self.results

    def create_update_datamasking(self):
        '''
        Creates or updates DataMaskingRules with the specified configuration.

        :return: deserialized DataMaskingRules instance state dictionary
        '''
        self.log("Creating / Updating the DataMaskingRules instance {0}".format(self.))

        try:
            response = self.mgmt_client.data_masking_rules.create_or_update(self.resource_group_name,
                                                                            self.server_name,
                                                                            self.database_name,
                                                                            self.data_masking_policy_name,
                                                                            self.data_masking_rule_name,
                                                                            self.parameters)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the DataMaskingRules instance.')
            self.fail("Error creating the DataMaskingRules instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_datamasking(self):
        '''
        Deletes specified DataMaskingRules instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the DataMaskingRules instance {0}".format(self.))
        try:
            response = self.mgmt_client.data_masking_rules.delete()
        except CloudError as e:
            self.log('Error attempting to delete the DataMaskingRules instance.')
            self.fail("Error deleting the DataMaskingRules instance: {0}".format(str(e)))

        return True

    def get_datamasking(self):
        '''
        Gets the properties of the specified DataMaskingRules.

        :return: deserialized DataMaskingRules instance state dictionary
        '''
        self.log("Checking if the DataMaskingRules instance {0} is present".format(self.))
        found = False
        try:
            response = self.mgmt_client.data_masking_rules.get()
            found = True
            self.log("Response : {0}".format(response))
            self.log("DataMaskingRules instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the DataMaskingRules instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMDataMaskingRules()

if __name__ == '__main__':
    main()

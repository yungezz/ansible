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
module: azure_rm_serverazureadadministrators
version_added: "2.5"
short_description: Manage an ServerAzureADAdministrators.
description:
    - Create, update and delete an instance of ServerAzureADAdministrators.

options:
    resource_group_name:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    administrator_name:
        description:
            - Name of the server administrator resource.
        required: True
    administrator_type:
        description:
            - The type of administrator.
        required: True
    login:
        description:
            - The server administrator login value.
        required: True
    sid:
        description:
            - The server administrator Sid (Secure ID).
        required: True
    tenant_id:
        description:
            - The server Active Directory Administrator tenant id.
        required: True

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create (or update) ServerAzureADAdministrators
        azure_rm_serverazureadadministrators:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          administrator_name: "{{ administrator_name }}"
          administrator_type: "{{ administrator_type }}"
          login: "{{ login }}"
          sid: "{{ sid }}"
          tenant_id: "{{ tenant_id }}"
'''

RETURN = '''
state:
    description: Current state of ServerAzureADAdministrators
    returned: always
    type: dict
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.serverazureadadministrators import serverazureadadministrators
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMServerAzureADAdministrators(AzureRMModuleBase):
    """Configuration class for an Azure RM ServerAzureADAdministrators resource"""

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
            administrator_name=dict(
                type='str',
                required=True
            ),
            administrator_type=dict(
                type='str',
                required=True
            ),
            login=dict(
                type='str',
                required=True
            ),
            sid=dict(
                type='str',
                required=True
            ),
            tenant_id=dict(
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
        self.administrator_name = None
        self.properties = dict()

        self.results = dict(changed=False, state=dict())
        self.mgmt_client = None
        self.state = None

        super(AzureRMServerAzureADAdministrators, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                                 supports_check_mode=True,
                                                                 supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif key == "administrator_type":
                self.properties["administrator_type"] = kwargs[key]
            elif key == "login":
                self.properties["login"] = kwargs[key]
            elif key == "sid":
                self.properties["sid"] = kwargs[key]
            elif key == "tenant_id":
                self.properties["tenant_id"] = kwargs[key]

        response = None
        results = dict()
        to_be_updated = False

        self.mgmt_client = self.get_mgmt_svc_client(serverazureadadministrators,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        try:
            resource_group = self.get_resource_group(self.resource_group)
        except CloudError:
            self.fail('resource group {0} not found'.format(self.resource_group))

        response = self.get_serverazureadadministrators()

        if not response:
            self.log("ServerAzureADAdministrators instance doesn't exist")
            if self.state == 'absent':
                self.log("Nothing to delete")
            else:
                to_be_updated = True
        else:
            self.log("ServerAzureADAdministrators instance already exists")
            if self.state == 'absent':
                self.delete_serverazureadadministrators()
                self.results['changed'] = True
                self.log("ServerAzureADAdministrators instance deleted")
            elif self.state == 'present':
                self.log("Need to check if ServerAzureADAdministrators instance has to be deleted or may be updated")
                to_be_updated = True

        if self.state == 'present':

            self.log("Need to Create / Update the ServerAzureADAdministrators instance")

            if self.check_mode:
                return self.results

            if to_be_updated:
                self.results['state'] = self.create_update_serverazureadadministrators()
                self.results['changed'] = True
            else:
                self.results['state'] = response

            self.log("Creation / Update done")

        return self.results

    def create_update_serverazureadadministrators(self):
        '''
        Creates or updates ServerAzureADAdministrators with the specified configuration.

        :return: deserialized ServerAzureADAdministrators instance state dictionary
        '''
        self.log("Creating / Updating the ServerAzureADAdministrators instance {0}".format(self.administrator_name))

        try:
            response = self.mgmt_client.server_azure_ad_administrators.create_or_update(self.resource_group_name,
                                                                                        self.server_name,
                                                                                        self.administrator_name,
                                                                                        self.properties)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the ServerAzureADAdministrators instance.')
            self.fail("Error creating the ServerAzureADAdministrators instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_serverazureadadministrators(self):
        '''
        Deletes specified ServerAzureADAdministrators instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the ServerAzureADAdministrators instance {0}".format(self.administrator_name))
        try:
            response = self.mgmt_client.server_azure_ad_administrators.delete(self.resource_group_name,
                                                                              self.server_name,
                                                                              self.administrator_name)
        except CloudError as e:
            self.log('Error attempting to delete the ServerAzureADAdministrators instance.')
            self.fail("Error deleting the ServerAzureADAdministrators instance: {0}".format(str(e)))

        return True

    def get_serverazureadadministrators(self):
        '''
        Gets the properties of the specified ServerAzureADAdministrators.

        :return: deserialized ServerAzureADAdministrators instance state dictionary
        '''
        self.log("Checking if the ServerAzureADAdministrators instance {0} is present".format(self.administrator_name))
        found = False
        try:
            response = self.mgmt_client.server_azure_ad_administrators.get(self.resource_group_name,
                                                                           self.server_name,
                                                                           self.administrator_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("ServerAzureADAdministrators instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the ServerAzureADAdministrators instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMServerAzureADAdministrators()

if __name__ == '__main__':
    main()

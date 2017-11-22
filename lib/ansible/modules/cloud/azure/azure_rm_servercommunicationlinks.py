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
module: azure_rm_servercommunicationlinks
version_added: "2.5"
short_description: Manage an ServerCommunicationLinks.
description:
    - Create, update and delete an instance of ServerCommunicationLinks.

options:
    resource_group_name:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    communication_link_name:
        description:
            - The name of the server communication link.
        required: True
    partner_server:
        description:
            - The name of the partner server.
        required: True

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create (or update) ServerCommunicationLinks
        azure_rm_servercommunicationlinks:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          communication_link_name: "{{ communication_link_name }}"
          partner_server: "{{ partner_server }}"
'''

RETURN = '''
state:
    description: Current state of ServerCommunicationLinks
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


class AzureRMServerCommunicationLinks(AzureRMModuleBase):
    """Configuration class for an Azure RM ServerCommunicationLinks resource"""

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
            communication_link_name=dict(
                type='str',
                required=True
            ),
            partner_server=dict(
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
        self.communication_link_name = None
        self.parameters = dict()

        self.results = dict(changed=False, state=dict())
        self.mgmt_client = None
        self.state = None

        super(AzureRMServerCommunicationLinks, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                              supports_check_mode=True,
                                                              supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif key == "partner_server":
                self.parameters["partner_server"] = kwargs[key]

        response = None
        results = dict()
        to_be_updated = False

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        try:
            resource_group = self.get_resource_group(self.resource_group)
        except CloudError:
            self.fail('resource group {0} not found'.format(self.resource_group))

        response = self.get_servercommunicationlinks()

        if not response:
            self.log("ServerCommunicationLinks instance doesn't exist")
            if self.state == 'absent':
                self.log("Nothing to delete")
            else:
                to_be_updated = True
        else:
            self.log("ServerCommunicationLinks instance already exists")
            if self.state == 'absent':
                self.delete_servercommunicationlinks()
                self.results['changed'] = True
                self.log("ServerCommunicationLinks instance deleted")
            elif self.state == 'present':
                self.log("Need to check if ServerCommunicationLinks instance has to be deleted or may be updated")
                to_be_updated = True

        if self.state == 'present':

            self.log("Need to Create / Update the ServerCommunicationLinks instance")

            if self.check_mode:
                return self.results

            if to_be_updated:
                self.results['state'] = self.create_update_servercommunicationlinks()
                self.results['changed'] = True
            else:
                self.results['state'] = response

            self.log("Creation / Update done")

        return self.results

    def create_update_servercommunicationlinks(self):
        '''
        Creates or updates ServerCommunicationLinks with the specified configuration.

        :return: deserialized ServerCommunicationLinks instance state dictionary
        '''
        self.log("Creating / Updating the ServerCommunicationLinks instance {0}".format(self.communication_link_name))

        try:
            response = self.mgmt_client.server_communication_links.create_or_update(self.resource_group_name,
                                                                                    self.server_name,
                                                                                    self.communication_link_name,
                                                                                    self.parameters)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the ServerCommunicationLinks instance.')
            self.fail("Error creating the ServerCommunicationLinks instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_servercommunicationlinks(self):
        '''
        Deletes specified ServerCommunicationLinks instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the ServerCommunicationLinks instance {0}".format(self.communication_link_name))
        try:
            response = self.mgmt_client.server_communication_links.delete(self.resource_group_name,
                                                                          self.server_name,
                                                                          self.communication_link_name)
        except CloudError as e:
            self.log('Error attempting to delete the ServerCommunicationLinks instance.')
            self.fail("Error deleting the ServerCommunicationLinks instance: {0}".format(str(e)))

        return True

    def get_servercommunicationlinks(self):
        '''
        Gets the properties of the specified ServerCommunicationLinks.

        :return: deserialized ServerCommunicationLinks instance state dictionary
        '''
        self.log("Checking if the ServerCommunicationLinks instance {0} is present".format(self.communication_link_name))
        found = False
        try:
            response = self.mgmt_client.server_communication_links.get(self.resource_group_name,
                                                                       self.server_name,
                                                                       self.communication_link_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("ServerCommunicationLinks instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the ServerCommunicationLinks instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMServerCommunicationLinks()

if __name__ == '__main__':
    main()

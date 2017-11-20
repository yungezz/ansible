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
module: azure_rm_capabilities_facts
version_added: "2.5"
short_description: Get Capabilities facts.
description:
    - Get facts of Capabilities.

options:
    location_id:
        description:
            - The location id whose capabilities are retrieved.
        required: True

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: List instances of Capabilities
        azure_rm_capabilities_facts:
          location_id: "{{ location_id }}"
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase

try:
    from msrestazure.azure_exceptions import CloudError
    from msrestazure.azure_operation import AzureOperationPoller
    from azure.mgmt.capabilities import capabilities
    from msrest.serialization import Model
except ImportError:
    # This is handled in azure_rm_common
    pass


class AzureRMCapabilitiesFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            location_id=dict(
                type='str',
                required=True
            ),
        )
        # store the results of the module operation
        self.results = dict(
            changed=False,
            ansible_facts=dict(azure_dnsrecordset=[])
        )
        self.location_id = None
        super(AzureRMCapabilitiesFacts, self).__init__(self.module_arg_spec)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if (self.location_id is not None):
            self.results['ansible_facts']['list_by_location'] = self.list_by_location()
        return self.results

    def list_by_location(self):
        '''
        Gets facts of the specified Capabilities.

        :return: deserialized Capabilitiesinstance state dictionary
        '''
        self.log("Checking if the Capabilities instance {0} is present".format(self.))
        found = False
        try:
            response = self.mgmt_client.capabilities.list_by_location(self.location_id)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Capabilities instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Capabilities instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    AzureRMCapabilitiesFacts()
if __name__ == '__main__':
    main()

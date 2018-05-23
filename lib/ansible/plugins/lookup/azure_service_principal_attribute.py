# (c) 2018 Yunge Zhu, <yungez@microsoft.com>
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
lookup: azure_service_principal_attribute
author:
  - Yunge Zhu <yungez@microsoft.com>
version_added: "2.6"
short_description: Look up Azure service principal attributes.
description:
  - Describes attributes of your Azure service principal account. You can specify one of the listed
    attribute choices or omit it to see all attributes.
options:
  azure_client_id:
    description: azure service principal client id.
    required: True
  azure_secret:
    description: azure secret
    required: True
  azure_tenant:
    description: azure tenant
  azure_cloud_environment:
    description: azure cloud environment    
"""

EXAMPLES = """
vars:
  has_ec2_classic: "{{ lookup('aws_account_attribute', attribute='has-ec2-classic') }}"
  # true | false

  default_vpc_id: "{{ lookup('aws_account_attribute', attribute='default-vpc') }}"
  # vpc-xxxxxxxx | none

  account_details: "{{ lookup('aws_account_attribute', wantlist='true') }}"
  # {'default-vpc': ['vpc-xxxxxxxx'], 'max-elastic-ips': ['5'], 'max-instances': ['20'],
  #  'supported-platforms': ['VPC', 'EC2'], 'vpc-max-elastic-ips': ['5'], 'vpc-max-security-groups-per-interface': ['5']}

"""

RETURN = """
_raw:
  description:
    Returns the value(s) of the attribute (or all attributes if one is not specified).
"""

import copy

from ansible.errors import AnsibleError
from ansible.plugins import AnsiblePlugin
from ansible.plugins.lookup import LookupBase

try:
    from azure.common.credentials import ServicePrincipalCredentials
    from azure.graphrbac import GraphRbacManagementClient
    from msrestazure import azure_cloud
    from msrestazure.azure_exceptions import CloudError
    from adal import AuthenticationContext
except ImportError:
    raise AnsibleError(
        "The lookup azure_service_principal_attribute requires azure.graphrbac, msrest")



def _get_credentials(options):
    credentials = {}
    #credentials['azure_client_id'] = options.get('azure_client_id', None)
    credentials['azure_client_id'] = options['azure_client_id']
    #credentials['azure_secret'] = options.get('azure_secret', None)
    credentials['azure_secret'] = options['azure_secret']
    credentials['azure_tenant'] = options['azure_tenant']
    credentials['azure_cloud_environment'] = options.get(
        'azure_cloud_environment', None)

    return credentials


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):

        #self.set_options(var_options=variables, direct=kwargs)
        self.set_options(direct=kwargs)
        #credentials = _get_credentials(self._options)


        #if len(self._options) > 0:
        #    #raise AnsibleError("self._options is: {0} {1}".format(self._options['azure_client_id'], self._options['azure_secret']))
        #else:
        #    raise AnsibleError("options is null: {0}, {1}".format(kwargs, variables))
        credentials = {}
        credentials['azure_client_id'] = self.get_option('azure_client_id')
        credentials['azure_secret'] = self.get_option('azure_secret')
        credentials['azure_tenant'] = self.get_option('azure_tenant', 'common')

        _cloud_environment = azure_cloud.AZURE_PUBLIC_CLOUD
#        if self.get_option('azure_cloud_environment', None) is not None:
#            cloud_environment = azure_cloud.get_cloud_from_metadata_endpoint(
#                credentials['azure_cloud_environment'])

        azure_credentials = ServicePrincipalCredentials(client_id=credentials['azure_client_id'],
                                                        secret=credentials['azure_secret'],
                                                        tenant=credentials['azure_tenant'])
                                                        #cloud_environment=_cloud_environment)
                                                        #resource=_cloud_environment.endpoints.active_directory_graph_resource_id)

        auth_context = AuthenticationContext(_cloud_environment.endpoints.active_directory + '/' + credentials['azure_tenant'])
        
        # get on behalf of token 
        creds = auth_context.acquire_token_with_client_credentials(_cloud_environment.endpoints.active_directory_graph_resource_id, credentials['azure_client_id'], credentials['azure_secret']) 
        if creds is None:
            raise AnsibleError('invalid token')

        #creds = auth_context.acquire_token_with_client_credentials('00000002-0000-0000-c000-000000000000', credentials['azure_client_id'], credentials['azure_secret']) 
        copy_aad_cred = copy.deepcopy(azure_credentials)
        copy_aad_cred.token['access_token'] = creds['accessToken']
#        if auth_token is not None:
#            raise AnsibleError("auth_token is null {0} {1}");
#        else:
#            raise AnsibleError("auth_token is: {0}".format(auth_token))

        client = GraphRbacManagementClient(copy_aad_cred, credentials['azure_tenant'])
#, base_url=_cloud_environment.endpoints.active_directory_graph_resource_id)
        
        if not client:
            raise AnsibleError('invalid client')
        #else: 
        #    raise AnsibleError('valid client!')

        try:
            response = list(client.service_principals.list(filter="appId eq '{}'".format(credentials['azure_client_id'])))
            sp = response[0]

            return sp.object_id
        except CloudError as ex:
            raise AnsibleError(
                "Failed to get service principal object id: %s" % to_native(ex))
        return False

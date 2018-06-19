#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Dag Wieers (dagwieers) <dag@wieers.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: aci_taboo_contract
short_description: Manage taboo contracts (vz:BrCP)
description:
- Manage taboo contracts on Cisco ACI fabrics.
notes:
- The C(tenant) used must exist before using this module in your playbook.
  The M(aci_tenant) module can be used for this.
- More information about the internal APIC class B(vz:BrCP) from
  L(the APIC Management Information Model reference,https://developer.cisco.com/docs/apic-mim-ref/).
author:
- Dag Wieers (@dagwieers)
version_added: '2.4'
options:
  taboo_contract:
    description:
    - The name of the Taboo Contract.
    required: yes
    aliases: [ name ]
  description:
    description:
    - The description for the Taboo Contract.
    aliases: [ descr ]
  tenant:
    description:
    - The name of the tenant.
    required: yes
    aliases: [ tenant_name ]
  scope:
    description:
    - The scope of a service contract.
    - The APIC defaults to C(context) when unset during creation.
    choices: [ application-profile, context, global, tenant ]
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    choices: [ absent, present, query ]
    default: present
extends_documentation_fragment: aci
'''

EXAMPLES = r'''
- name: Add taboo contract
  aci_taboo_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: ansible_test
    taboo_contract: taboo_contract_test
    state: present

- name: Remove taboo contract
  aci_taboo_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: ansible_test
    taboo_contract: taboo_contract_test
    state: absent

- name: Query all taboo contracts
  aci_taboo_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    state: query

- name: Query a specific taboo contract
  aci_taboo_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: ansible_test
    taboo_contract: taboo_contract_test
    state: query
'''

RETURN = r'''
current:
  description: The existing configuration from the APIC after the module has finished
  returned: success
  type: list
  sample:
    [
        {
            "fvTenant": {
                "attributes": {
                    "descr": "Production environment",
                    "dn": "uni/tn-production",
                    "name": "production",
                    "nameAlias": "",
                    "ownerKey": "",
                    "ownerTag": ""
                }
            }
        }
    ]
error:
  description: The error information as returned from the APIC
  returned: failure
  type: dict
  sample:
    {
        "code": "122",
        "text": "unknown managed object class foo"
    }
raw:
  description: The raw output returned by the APIC REST API (xml or json)
  returned: parse error
  type: string
  sample: '<?xml version="1.0" encoding="UTF-8"?><imdata totalCount="1"><error code="122" text="unknown managed object class foo"/></imdata>'
sent:
  description: The actual/minimal configuration pushed to the APIC
  returned: info
  type: list
  sample:
    {
        "fvTenant": {
            "attributes": {
                "descr": "Production environment"
            }
        }
    }
previous:
  description: The original configuration from the APIC before the module has started
  returned: info
  type: list
  sample:
    [
        {
            "fvTenant": {
                "attributes": {
                    "descr": "Production",
                    "dn": "uni/tn-production",
                    "name": "production",
                    "nameAlias": "",
                    "ownerKey": "",
                    "ownerTag": ""
                }
            }
        }
    ]
proposed:
  description: The assembled configuration from the user-provided parameters
  returned: info
  type: dict
  sample:
    {
        "fvTenant": {
            "attributes": {
                "descr": "Production environment",
                "name": "production"
            }
        }
    }
filter_string:
  description: The filter string used for the request
  returned: failure or debug
  type: string
  sample: ?rsp-prop-include=config-only
method:
  description: The HTTP method used for the request to the APIC
  returned: failure or debug
  type: string
  sample: POST
response:
  description: The HTTP response from the APIC
  returned: failure or debug
  type: string
  sample: OK (30 bytes)
status:
  description: The HTTP status from the APIC
  returned: failure or debug
  type: int
  sample: 200
url:
  description: The HTTP url used for the request to the APIC
  returned: failure or debug
  type: string
  sample: https://10.11.12.13/api/mo/uni/tn-production.json
'''

from ansible.module_utils.network.aci.aci import ACIModule, aci_argument_spec
from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(
        taboo_contract=dict(type='str', required=False, aliases=['name']),  # Not required for querying all contracts
        tenant=dict(type='str', required=False, aliases=['tenant_name']),  # Not required for querying all contracts
        scope=dict(type='str', choices=['application-profile', 'context', 'global', 'tenant']),
        description=dict(type='str', aliases=['descr']),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['tenant', 'taboo_contract']],
            ['state', 'present', ['tenant', 'taboo_contract']],
        ],
    )

    taboo_contract = module.params['taboo_contract']
    description = module.params['description']
    scope = module.params['scope']
    state = module.params['state']
    tenant = module.params['tenant']

    aci = ACIModule(module)
    aci.construct_url(
        root_class=dict(
            aci_class='fvTenant',
            aci_rn='tn-{0}'.format(tenant),
            filter_target='eq(fvTenant.name, "{0}")'.format(tenant),
            module_object=tenant,
        ),
        subclass_1=dict(
            aci_class='vzTaboo',
            aci_rn='taboo-{0}'.format(taboo_contract),
            filter_target='eq(vzTaboo.name, "{0}")'.format(taboo_contract),
            module_object=taboo_contract,
        ),
    )

    aci.get_existing()

    if state == 'present':
        aci.payload(
            aci_class='vzTaboo',
            class_config=dict(
                name=taboo_contract,
                descr=description,
                scope=scope,
            ),
        )

        aci.get_diff(aci_class='vzTaboo')

        aci.post_config()

    elif state == 'absent':
        aci.delete_config()

    aci.exit_json()


if __name__ == "__main__":
    main()

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
module: azure_rm_xsql_databases
version_added: "2.5"
short_description: Manage an Databases.
description:
    - Create, update and delete an instance of Databases.

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
    location:
        description:
            - Resource location.
        required: True
    tags:
        description:
            - Resource tags.
        required: False
    sku:
        description:
            - The name and tier of the SKU.
        required: False
        suboptions:
            name:
                description:
                    - The name of the SKU, typically, a letter + Number code, e.g. P3.
                required: False
            tier:
                description:
                    - The tier of the particular SKU, e.g. Basic, Premium.
                required: False
            size:
                description:
                    - Size of the particular SKU
                required: False
            family:
                description:
                    - If the service has different generations of hardware, for the same SKU, then that can be captured here.
                required: False
            capacity:
                description:
                    - Capacity of the particular SKU.
                required: False
    create_mode:
        description:
            - "Specifies the mode of database creation.\n\n\n\nDefault: regular database creation.\n\n\n\nCopy: creates a database as a copy of an existing d
               atabase. sourceDatabaseId must be specified as the resource ID of the source database.\n\n\n\nSecondary: creates a database as a secondary rep
               lica of an existing database. sourceDatabaseId must be specified as the resource ID of the existing primary database.\n\n\n\nPointInTimeRestor
               e: Creates a database by restoring a point in time backup of an existing database. sourceDatabaseId must be specified as the resource ID of th
               e existing database, and restorePointInTime must be specified.\n\n\n\nRecovery: Creates a database by restoring a geo-replicated backup. sourc
               eDatabaseId must be specified as the recoverable database resource ID to restore.\n\n\n\nRestore: Creates a database by restoring a backup of
               a deleted database. sourceDatabaseId must be specified. If sourceDatabaseId is the database's original resource ID, then sourceDatabaseDeletio
               nDate must be specified. Otherwise sourceDatabaseId must be the restorable dropped database resource ID and sourceDatabaseDeletionDate is igno
               red. restorePointInTime may also be specified to restore from an earlier point in time.\n\n\n\nRestoreLongTermRetentionBackup: Creates a datab
               ase by restoring from a long term retention vault. recoveryServicesRecoveryPointResourceId must be specified as the recovery point resource ID
               .\n\n\n\nCopy, Secondary, and RestoreLongTermRetentionBackup are not supported for DataWarehouse edition. Possible values include: 'Default',
               'Copy', 'Secondary', 'PointInTimeRestore', 'Restore', 'Recovery', 'RestoreExternalBackup', 'RestoreExternalBackupSecondary', 'RestoreLongTermR
               etentionBackup'"
        required: False
    collation:
        description:
            - The collation of the database.
        required: False
    max_size_bytes:
        description:
            - The max size of the database expressed in bytes.
        required: False
    sample_name:
        description:
            - "The name of the sample schema to apply when creating this database. Possible values include: 'AdventureWorksLT', 'WideWorldImportersStd', 'Wid
               eWorldImportersFull'"
        required: False
    elastic_pool_id:
        description:
            - The resource identifier of the elastic pool containing this database.
        required: False
    source_database_id:
        description:
            - The resource identifier of the source database associated with create operation of this database.
        required: False
    restore_point_in_time:
        description:
            - Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database.
        required: False
    source_database_deletion_date:
        description:
            - Specifies the time that the database was deleted.
        required: False
    recovery_services_recovery_point_id:
        description:
            - The resource identifier of the recovery point associated with create operation of this database.
        required: False
    long_term_retention_backup_resource_id:
        description:
            - The resource identifier of the long term retention backup associated with create operation of this database.
        required: False
    recoverable_database_id:
        description:
            - The resource identifier of the recoverable database associated with create operation of this database.
        required: False
    restorable_dropped_database_id:
        description:
            - The resource identifier of the restorable dropped database associated with create operation of this database.
        required: False
    catalog_collation:
        description:
            - "Collation of the metadata catalog. Possible values include: 'DATABASE_DEFAULT', 'SQL_Latin1_General_CP1_CI_AS'
        required: False
    zone_redundant:
        description:
            - Whether or not this database is zone redundant, which means the replicas of this database will be spread across multiple availability zones.
        required: False

extends_documentation_fragment:
    - azure
    - azure_tags

author:
    - "Zim Kalinowski (@zikalino)"

'''

EXAMPLES = '''
      - name: Create (or update) Databases
        azure_rm_xsql_databases:
          resource_group_name: "{{ resource_group_name }}"
          server_name: "{{ server_name }}"
          database_name: "{{ database_name }}"
          location: "{{ location }}"
          tags: "{{ tags }}"
          sku:
            name: "{{ name }}"
            tier: "{{ tier }}"
            size: "{{ size }}"
            family: "{{ family }}"
            capacity: "{{ capacity }}"
          create_mode: "{{ create_mode }}"
          collation: "{{ collation }}"
          max_size_bytes: "{{ max_size_bytes }}"
          sample_name: "{{ sample_name }}"
          elastic_pool_id: "{{ elastic_pool_id }}"
          source_database_id: "{{ source_database_id }}"
          restore_point_in_time: "{{ restore_point_in_time }}"
          source_database_deletion_date: "{{ source_database_deletion_date }}"
          recovery_services_recovery_point_id: "{{ recovery_services_recovery_point_id }}"
          long_term_retention_backup_resource_id: "{{ long_term_retention_backup_resource_id }}"
          recoverable_database_id: "{{ recoverable_database_id }}"
          restorable_dropped_database_id: "{{ restorable_dropped_database_id }}"
          catalog_collation: "{{ catalog_collation }}"
          zone_redundant: "{{ zone_redundant }}"
'''

RETURN = '''
state:
    description: Current state of Databases
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


class AzureRMDatabases(AzureRMModuleBase):
    """Configuration class for an Azure RM Databases resource"""

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
            location=dict(
                type='str',
                required=True
            ),
            tags=dict(
                type='dict',
                required=False
            ),
            sku=dict(
                type='dict',
                required=False
            ),
            create_mode=dict(
                type='str',
                required=False
            ),
            collation=dict(
                type='str',
                required=False
            ),
            max_size_bytes=dict(
                type='long',
                required=False
            ),
            sample_name=dict(
                type='str',
                required=False
            ),
            elastic_pool_id=dict(
                type='str',
                required=False
            ),
            source_database_id=dict(
                type='str',
                required=False
            ),
            restore_point_in_time=dict(
                type='datetime',
                required=False
            ),
            source_database_deletion_date=dict(
                type='datetime',
                required=False
            ),
            recovery_services_recovery_point_id=dict(
                type='str',
                required=False
            ),
            long_term_retention_backup_resource_id=dict(
                type='str',
                required=False
            ),
            recoverable_database_id=dict(
                type='str',
                required=False
            ),
            restorable_dropped_database_id=dict(
                type='str',
                required=False
            ),
            catalog_collation=dict(
                type='str',
                required=False
            ),
            zone_redundant=dict(
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
        self.parameters = dict()

        self.results = dict(changed=False, state=dict())
        self.mgmt_client = None
        self.state = None

        super(AzureRMDatabases, self).__init__(derived_arg_spec=self.module_arg_spec,
                                               supports_check_mode=True,
                                               supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""

        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif key == "location":
                self.parameters["location"] = kwargs[key]
            elif key == "tags":
                self.parameters["tags"] = kwargs[key]
            elif key == "sku":
                self.parameters["sku"] = kwargs[key]
            elif key == "create_mode":
                self.parameters["create_mode"] = kwargs[key]
            elif key == "collation":
                self.parameters["collation"] = kwargs[key]
            elif key == "max_size_bytes":
                self.parameters["max_size_bytes"] = kwargs[key]
            elif key == "sample_name":
                self.parameters["sample_name"] = kwargs[key]
            elif key == "elastic_pool_id":
                self.parameters["elastic_pool_id"] = kwargs[key]
            elif key == "source_database_id":
                self.parameters["source_database_id"] = kwargs[key]
            elif key == "restore_point_in_time":
                self.parameters["restore_point_in_time"] = kwargs[key]
            elif key == "source_database_deletion_date":
                self.parameters["source_database_deletion_date"] = kwargs[key]
            elif key == "recovery_services_recovery_point_id":
                self.parameters["recovery_services_recovery_point_id"] = kwargs[key]
            elif key == "long_term_retention_backup_resource_id":
                self.parameters["long_term_retention_backup_resource_id"] = kwargs[key]
            elif key == "recoverable_database_id":
                self.parameters["recoverable_database_id"] = kwargs[key]
            elif key == "restorable_dropped_database_id":
                self.parameters["restorable_dropped_database_id"] = kwargs[key]
            elif key == "catalog_collation":
                self.parameters["catalog_collation"] = kwargs[key]
            elif key == "zone_redundant":
                self.parameters["zone_redundant"] = kwargs[key]

        response = None
        results = dict()
        to_be_updated = False

        self.mgmt_client = self.get_mgmt_svc_client(SqlManagementClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)

        try:
            resource_group = self.get_resource_group(self.resource_group)
        except CloudError:
            self.fail('resource group {0} not found'.format(self.resource_group))

        response = self.get_databases()

        if not response:
            self.log("Databases instance doesn't exist")
            if self.state == 'absent':
                self.log("Nothing to delete")
            else:
                to_be_updated = True
        else:
            self.log("Databases instance already exists")
            if self.state == 'absent':
                self.delete_databases()
                self.results['changed'] = True
                self.log("Databases instance deleted")
            elif self.state == 'present':
                self.log("Need to check if Databases instance has to be deleted or may be updated")
                to_be_updated = True

        if self.state == 'present':

            self.log("Need to Create / Update the Databases instance")

            if self.check_mode:
                return self.results

            if to_be_updated:
                self.results['state'] = self.create_update_databases()
                self.results['changed'] = True
            else:
                self.results['state'] = response

            self.log("Creation / Update done")

        return self.results

    def create_update_databases(self):
        '''
        Creates or updates Databases with the specified configuration.

        :return: deserialized Databases instance state dictionary
        '''
        self.log("Creating / Updating the Databases instance {0}".format(self.database_name))

        try:
            response = self.mgmt_client.databases.create_or_update(self.resource_group_name,
                                                                   self.server_name,
                                                                   self.database_name,
                                                                   self.parameters)
            if isinstance(response, AzureOperationPoller):
                response = self.get_poller_result(response)

        except CloudError as exc:
            self.log('Error attempting to create the Databases instance.')
            self.fail("Error creating the Databases instance: {0}".format(str(exc)))
        return response.as_dict()

    def delete_databases(self):
        '''
        Deletes specified Databases instance in the specified subscription and resource group.

        :return: True
        '''
        self.log("Deleting the Databases instance {0}".format(self.database_name))
        try:
            response = self.mgmt_client.databases.delete(self.resource_group_name,
                                                         self.server_name,
                                                         self.database_name)
        except CloudError as e:
            self.log('Error attempting to delete the Databases instance.')
            self.fail("Error deleting the Databases instance: {0}".format(str(e)))

        return True

    def get_databases(self):
        '''
        Gets the properties of the specified Databases.

        :return: deserialized Databases instance state dictionary
        '''
        self.log("Checking if the Databases instance {0} is present".format(self.database_name))
        found = False
        try:
            response = self.mgmt_client.databases.get(self.resource_group_name,
                                                      self.server_name,
                                                      self.database_name)
            found = True
            self.log("Response : {0}".format(response))
            self.log("Databases instance : {0} found".format(response.name))
        except CloudError as e:
            self.log('Did not find the Databases instance.')
        if found is True:
            return response.as_dict()

        return False


def main():
    """Main execution"""
    AzureRMDatabases()

if __name__ == '__main__':
    main()

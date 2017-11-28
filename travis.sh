#!/bin/bash

exit_code=0

create_resource_group () {
	name=$1
	ansible-playbook create_resource_group.yml --extra-vars="name=$name"
}

delete_resource_group () {
	name=$1
	ansible-playbook delete_resource_group.yml --extra-vars="name=$name"
}

run_test () {
	test_name=$1
	group_name="ansible-integration-${test_name##azure_rm}"
	# create resource group
	create_resource_group $group_name
	# setup the test credential file
	rm test/integration/cloud-config-azure.yml
	touch test/integration/cloud-config-azure.yml
	echo "AZURE_CLIENT_ID: ${clientId}
AZURE_SECRET: ${secret}
AZURE_SUBSCRIPTION_ID: ${subscriptionId}
AZURE_TENANT: ${tenant}
RESOURCE_GROUP: $group_name
RESOURCE_GROUP_SECONDARY: $group_name" >> test/integration/cloud-config-azure.yml

	# run test
	ansible-test integration $test_name --docker

	if [ $? -ne 0 ]; then
		exit_code=1
	fi

	# delete resource group
	delete_resource_group $group_name
}

# Set up dev environment
setup () {
	apt-get update && apt-get install -y libssl-dev libffi-dev python-dev python-pip docker.io
	pip install pip --upgrade
	pip install ansible[azure]

	# create credential file
	mkdir ~/.azure
	touch ~/.azure/credentials
	echo "[default]
subscription_id=${subscriptionId}
client_id=${clientId}
secret=${secret}
tenant=${tenant}" >> ~/.azure/credentials

	# set up dev mode
	git clone https://github.com/VSChina/ansible.git
	cd ansible
	pip install virtualenv
	virtualenv venv
	. venv/bin/activate
	pip install packaging azure azure-cli
	pip install -r requirements.txt
	pip install -r packaging/requirements/requirements-azure.txt
	. hacking/env-setup
}

# Scan for available test
scan_test () {
	# list all the integration in this repo
	# find ./test/integration/targets -name azure_rm_*
	# 'test/integration/targets/azure_rm_*'
	for file in "test/integration/targets/azure_rm_*"; do
		name=${file##test/integration/targets}
		# run the test
		run_test $name
	done
}

setup
scan_test
exit $exit_code
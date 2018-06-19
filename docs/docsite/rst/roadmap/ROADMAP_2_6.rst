===========
Ansible 2.6
===========

.. contents:: Topics

Release Schedule
----------------

Proposed
========

- 2018-05-17 Core Freeze (Core Engine and Non-Community Modules)
- 2018-05-17 Alpha Release 1
- 2018-05-24 Alpha Release 2
- 2018-05-25 Community Freeze (Community Modules)
- 2018-05-31 Branch stable-2.6
- 2018-05-31 Release Candidate 1
- 2018-06-07 Release Candidate 2
- 2018-06-14 Release Candidate 3
- 2018-06-28 Final Release

Engine improvements
-------------------

- Version 2.6 is largely going to be a stabilization release for Core code.
- Some of the items covered in this release, but are not limited to are the following:

  - ``ansible-inventory``
  - ``import_*``
  - ``include_*``
  - Test coverage
  - Performance Testing

Core Modules
------------
- Adopt-a-module Campaign

  - Review current status of all Core Modules
  - Reduce backlog of open issues against these modules

Cloud Modules
-------------

Network
-------

Connection work
================

* New connection plugin: eAPI `proposal#102 <https://github.com/ansible/proposals/issues/102>`_
* New connection plugin: NX-API
* Support for configurable options for network_cli & netconf

Modules
=======

* New ``cli_config`` - platform agnostic module for sending text based config over network_cli
* New ``cli_command`` - platform agnostic command module
* New ``network_get`` - platform agnostic module for pulling configuration via SCP/SFTP over network_cli
* New ``network_put`` - platform agnostic module for pushing configuration via SCP/SFTP over network_cli

Other Features
================

* Stretch & tech preview: Configuration caching for network_cli. Opt-in feature to avoid ``show running`` performance hit


Windows
-------





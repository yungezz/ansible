.. _porting_2.6_guide:

*************************
Ansible 2.6 Porting Guide
*************************

This section discusses the behavioral changes between Ansible 2.5 and Ansible 2.6.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with `Ansible Changelog <https://github.com/ansible/ansible/blob/devel/CHANGELOG.md#2.6>`_ to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at :ref:`porting guides <porting_guides>`.

.. contents:: Topics

Playbook
========

No notable changes.

Deprecated
==========

* In the :ref:`nxos_igmp_interface module<nxos_igmp_interface_module>`, ``oif_prefix`` and ``oif_source`` properties are deprecated. Use ``ois_ps`` parameter with a dictionary of prefix and source to values instead.

Modules
=======

Major changes in popular modules are detailed here



Modules removed
---------------

The following modules no longer exist:


Deprecation notices
-------------------

The following modules will be removed in Ansible 2.10. Please update your playbooks accordingly.


Noteworthy module changes
-------------------------

* The ``upgrade`` module option for ``win_chocolatey`` has been removed; use ``state: latest`` instead.
* The ``reboot`` module option for ``win_feature`` has been removed; use the ``win_reboot`` action plugin instead
* The ``win_iis_webapppool`` module no longer accepts a string for the ``atributes`` module option; use the free form dictionary value instead
* The ``name`` module option for ``win_package`` has been removed; this is not used anywhere and should just be removed from your playbooks
* The ``win_regedit`` module no longer automatically corrects the hive path ``HCCC`` to ``HKCC``; use ``HKCC`` because this is the correct hive path

Plugins
=======

No notable changes.

Porting custom scripts
======================

No notable changes.

Networking
==========

No notable changes.

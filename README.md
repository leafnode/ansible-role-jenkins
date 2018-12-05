# jenkins

[![Build Status](https://travis-ci.com/iroquoisorg/ansible-role-jenkins.svg?branch=master)](https://travis-ci.com/iroquoisorg/ansible-role-memcached)

Ansible role for jenkins

This role was prepared and tested for Ubuntu 16.04.

# Installation

`$ ansible-galaxy install iroquoisorg.jenkins`

# Default settings

```

jenkins_domain: 127.0.0.1
jenkins_ansible_callbacks: []
ansible_backup_vault_pass: ""
jenkins_ansible_version: 2.3
jenkins_basicauth_users: []
jenkins_scripts:
  - "clean-workspace.groovy"
jenkins_home_dir: "/var/lib/jenkins"
jenkins_slave: false
jenkins_do_snapshots: false
jenkins_rundeck: false
jenkins_db: []
# jenkins_db:
#  - { database: foo, owner: bar }

```

# Development

Please check [development guide](DEVELOPMENT.md) for details about developing and testing this role.

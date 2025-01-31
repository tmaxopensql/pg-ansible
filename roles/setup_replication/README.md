# setup_replication

This Ansible Galaxy Role configures Replication on PostgresSQL versions: 14 on instances previously
configured.

## Requirements

The requirements for this ansible galaxy role are:

1. Ansible
2. `tmax_opensql.postgres` -> `setup_repo` - for repository installation
3. `tmax_opensql.postgres` -> `install_dbserver` - for installation of
   PostgreSQL binaries.
4. `tmax_opensql.postgres` -> `setup_extension` - for installation of
   PostgreSQL binaries.

## Role variables

When executing the role via ansible there are three required variables:

- **_os_**

Operating Systems supported are: CentOS7 and RHEL7

- **_pg_version_**

  Postgres Versions supported are: `14.0`, `14.1`, `14.2`, `14.3`,`14.3`, `14.5`, `14.6`, `14.7`, `14.8`, `15.0`, `15.1`, `15.2`, `15.3`

- **_pg_type_**

  Database Engine supported are: `PG`

### `use_system_user`

Start PostgreSQL systemd unit using this parameter.
If set to false, systemd unit is not used and it operates in the form of process through command.
Default: true

Example:
```yaml
use_system_user: false
```

### `standby_quorum_type`

Using this parameters user can set backend flag registered in pgpool-II.
Users can set only "any" or "first".

```yaml
standby_quorum_type: "any"
```

The rest of the variables can be configured and are available in the:

  * [roles/setup_replication/defaults/main.yml](./defaults/main.yml)
  * [roles/setup_replication/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)
  * [roles/setup_replication/vars/PG_Debian.yml](./vars/PG_Debian.yml)

## Dependencies

The `setup_replication` role does not have any dependencies on any other roles.

## Example Playbook

### Hosts file content

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    primary:
      hosts:
        primary1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
    standby:
      hosts:
        standby1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: synchronous
        standby2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: asynchronous
```

### How to include the `setup_replication` role in your Playbook

Below is an example of how to include the `setup_replication` role:

```yaml
---
- hosts: standby
  name: Setup Postgres replication on Instances
  become: true
  gather_facts: true

  collections:
    - tmax_opensql.postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14.6
        pg_type: "PG"

  roles:
    - setup_replication
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/setup_replication/defaults/main.yml](./defaults/main.yml)
  * [roles/setup_replication/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)
  * [roles/setup_replication/vars/PG_Debian.yml](./vars/PG_Debian.yml)

## Database engines supported
### Supported OS
- CentOS7
- CentOS8
- Rocky8
- Rocky9

### Supported PostgreSQL Version
- 14.0 - 14.8
- 15.0 - 15.3

## Playbook execution examples

```bash
# To deploy community Postgres version 14 on CentOS7 hosts with the user centos
$ ansible-playbook playbook.yml \
  -u centos \
  -i inventory.yml \
  --extra-vars="pg_version=14.6 pg_type=PG"
```

## License

BSD

## Author information

Author:
  * [Sang Myeung Lee](https://github.com/sungmu1)

Original Author:
  * EDB Postgres - www.enterprisedb.com

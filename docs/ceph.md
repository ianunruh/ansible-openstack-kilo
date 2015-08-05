# Ceph

## Procedure

### Ceph deployment

You will need at least one node to act as a monitor and ideally two or more nodes to act as OSDs.

#### All nodes

Ensure the following variables are set properly for all nodes.

```yaml
ceph_public_network: YOUR_PUBLIC_NETWORK_CIDR
ceph_cluster_network: YOUR_CLUSTER_NETWORK_CIDR
ceph_mon_interface: PUBLIC_NETWORK_INTERFACE_FOR_MONS
```

#### Monitor nodes

Ensure that all monitor nodes are present in the `ceph-mon` group. If you wish to use a group name
other than `ceph-mon`, you can override that across all nodes with the following variable.

```yaml
ceph_group_mon: YOUR_GROUP_NAME
```

Ensure that all monitor nodes have the `ceph-mon` role.

```yaml
- hosts: ceph-mon
  roles:
    - ceph-mon
```

#### OSD nodes

Ensure that all OSDs have the `ceph-osd` role.

```yaml
- hosts: ceph-osd
  roles:
    - ceph-osd
```

If you wish to use directories, then set the following variable according to each OSD node. Note that directories
should only be used for testing purposes. In production environments, use disks with separate journal SSDs.

```yaml
ceph_osd_directories:
  - /path/to/osd-directory-1
  - /path/to/osd-directory-2
```

If you wish to use physical disks, then set the following variables according to each OSD node. Each disk will have a data partition
and a journal partition.

```yaml
ceph_osd_disks:
  - /dev/sdb
  - /dev/sdc

ceph_osd_journal_size: 10240
```

Refer to the [OSD config reference](http://ceph.com/docs/master/rados/configuration/osd-config-ref/#journal-settings) for more details
on selecting the optimal journal size for your disks.

If you wish to use a separate disk for the journals (e.g. an SSD) then set the following variables.

```yaml
ceph_osd_disks:
  - /dev/sdb
  - /dev/sdc

ceph_osd_journal_disks:
  - /dev/sdd
  - /dev/sdd

ceph_osd_journal_size: 10240
```

Each element in the `ceph_osd_journal_disks` list must specify the journal disk for the corresponding element in the `ceph_osd_disks` list. The
role will validate that the lists are the same length but you must ensure that all elements are present and valid.

### Glance

To configure Glance to store images in Ceph, first ensure that the `ceph-client` role in present on the controller node.

```yaml
- hosts: controller
  roles:
    - ceph-client
    - glance
```

Then ensure that the following variables are set.

```yaml
glance_configure_ceph: true

glance_default_store: rbd
glance_stores:
  - rbd
  - http
```

When `glance_configure_ceph` is enabled, it performs the following steps for your convenience.

1. Copy the admin keyring to the node
2. Ensure that the `images` pool is present on Ceph
3. Retrieve a keyring with the necessary capabilities for Glance

### Cinder

To configure Cinder to use Ceph as a backend, first ensure that the `ceph-client` role is present on the storage nodes.

```yaml
- hosts: storage
  roles:
    - ceph-client
    - cinder
```

Then ensure that the following variables are set on the storage nodes.

```yaml
cinder_configure_ceph: true

cinder_backends:
  rbd:
    volume_driver: cinder.volume.drivers.rbd.RBDDriver
    rbd_ceph_conf: /etc/ceph/ceph.conf
    rbd_user: cinder
    rbd_pool: volumes
    rbd_secret_uuid: a0e9787e-2fcd-4172-a2dd-bd3139eabd14
```

This will configure Cinder to utilize the `volumes` pool for volumes.

The `a0e9787e-2fcd-4172-a2dd-bd3139eabd14` value corresponds to the UUID of the secret stored in libvirt on the compute nodes that is
used to mount volumes from Cinder. `a0e9787e-2fcd-4172-a2dd-bd3139eabd14` is the default secret UUID configured in the `nova` role.

When `cinder_configure_ceph` is enabled, it performs the following steps for your convenience.

1. Copy the admin keyring to the node
2. Ensure that the `volumes`, `backups` and `vms` pools are present in Ceph
3. Retrieve a keyring with the necessary capabilities for Cinder

### Cinder backup

To configure Cinder to use Ceph as a backup driver, first ensure that the `ceph-client` role is present on the nodes with `cinder-backup`.

```yaml
- hosts: controller
  roles:
    - ceph-client
    - cinder
```

Then ensure that the following variables are set on the nodes with `cinder-backup`.

```yaml
cinder_configure_ceph: true

cinder_backup_driver: cinder.backup.drivers.ceph
```

### Nova

The next step is to configure Nova to be able to mount volumes from Ceph directly. Ensure that the `ceph-client` role is present on the
compute nodes.

```yaml
- hosts: compute
  roles:
    - ceph-client
    - nova
```

Then ensure that the following variable are set on the compute nodes.

```yaml
nova_configure_ceph: true
```

If you plan on using Ceph for instance ephemeral storage, then you'll also need to set the following variable.

```yaml
nova_compute_libvirt_images_type: rbd
```

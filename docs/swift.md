# Swift

## Prerequisites

* One or more nodes with one or more hard drives for Swift storage

## Procedure

Ensure the Swift role is present in the playbook for the controller and storage nodes

```yaml
- hosts: controller:swift-storage
  roles:
    - swift
```

Ensure all nodes have configuration needed for building the rings

```yaml
swift_replicas: 2

swift_account_devices:
  - r1z1-1.1.1.1:6002/sdb
  - r1z1-2.2.2.2:6002/sdb

swift_container_devices:
  - r1z1-1.1.1.1:6001/sdb
  - r1z1-2.2.2.2:6001/sdb

swift_objects_devices:
  - r1z1-1.1.1.1:6000/sdb
  - r1z1-2.2.2.2:6000/sdb
```

Ensure controller nodes have the correct role enabled

```yaml
swift_role_controller: true
```

Ensure storage nodes have the correct role enabled

```yaml
swift_role_storage: true
```

# KVM hypervisor

## Prerequisites

* Hosts with the ability to use KVM acceleration

## Procedure

Ensure all compute nodes with KVM acceleration use the correct virt type

```yaml
nova_compute_libvirt_virt_type: kvm
```

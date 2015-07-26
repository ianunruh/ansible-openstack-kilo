# Neutron DVR

## Prerequisites

* Tenant networks use the VXLAN type driver
* Service and compute nodes all have the external network configured for the L3 agent (e.g. flat, VLAN, etc.)

## Procedure

Ensure distributed routing is enabled everywhere (all nodes with the Neutron role)

```yaml
neutron_router_distributed: true
neutron_ovs_distributed_routing: true
```

Ensure the L3 agents on service nodes are set to `dvr_snat` mode.

```yaml
openstack_role_network: true

neutron_l3_agent_mode: dvr_snat
```

Ensure compute nodes have the L3 and metadata agents, and ensure that the L3 agents are set to `dvr` mode.

```yaml
openstack_role_compute: true

neutron_component_l3_agent: true
neutron_component_metadata_agent: true

neutron_l3_agent_mode: dvr
```

Any bridge mappings used for external networks must be present on both compute and service nodes.

```yaml
neutron_ovs_bridge_mappings:
  - physnet1:br-eth1
```

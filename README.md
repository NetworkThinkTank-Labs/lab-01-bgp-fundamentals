# Lab 01 â€” BGP Fundamentals

![BGP Fundamentals](diagrams/topology-placeholder.png)

> **NetworkThinkTank Labs** â€” Hands-on networking labs for engineers, by engineers.
> Blog: [networkthinktank.blog](https://networkthinktank.blog)

---

## ðŸ“– Blog Article Summary

This lab accompanies our blog series on BGP (Border Gateway Protocol) fundamentals. BGP is the routing protocol that holds the internet together â€” itâ€™s the protocol used between autonomous systems (AS) to exchange routing information. Understanding BGP is essential for any network engineer working in service provider, enterprise, or cloud environments.

In this lab, youâ€™ll build a multi-AS BGP topology from scratch, configure eBGP and iBGP peerings, manipulate path attributes, and troubleshoot common BGP issues that youâ€™ll encounter in production networks.

---

## ðŸŽ¯ Lab Objectives

By completing this lab, you will be able to:

1. **Configure eBGP peerings** between routers in different autonomous systems
2. **Configure iBGP peerings** within the same autonomous system
3. **Verify BGP neighbor adjacencies** and troubleshoot peering failures
4. **Understand BGP path selection** and the BGP best-path algorithm
5. **Manipulate BGP attributes** (Local Preference, MED, AS-Path Prepending, Weight)
6. **Implement route filtering** using prefix-lists and route-maps
7. **Configure BGP route aggregation** (summarization)
8. **Troubleshoot common BGP issues** in a realistic lab environment

---

## ðŸ—ºï¸ Lab Topology

```
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚           AS 65001 (ISP-A)          â”‚
                    â”‚                                     â”‚
                    â”‚   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”      â”‚
                    â”‚   â”‚  R1     â”‚â”€â”€â”€â”€â”€â”‚  R2     â”‚      â”‚
                    â”‚   â”‚ (RR)    â”‚     â”‚         â”‚      â”‚
                    â”‚   â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜      â”‚
                    â”‚        â”‚               â”‚            â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                             â”‚               â”‚
                    â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€ eBGP â”€â”€â”€â”€
                             â”‚               â”‚
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚   AS 65002     â”‚ â”‚   AS 65003        â”‚
                    â”‚                â”‚ â”‚                    â”‚
                    â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚ â”‚   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”‚
                    â”‚  â”‚  R3     â”‚   â”‚ â”‚   â”‚  R4     â”‚     â”‚
                    â”‚  â”‚ (CE)    â”‚   â”‚ â”‚   â”‚ (CE)    â”‚     â”‚
                    â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚ â”‚   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â”‚
                    â”‚                â”‚ â”‚                    â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Device Details

| Device | Role | Loopback0 | AS Number | Platform |
|--------|------|-----------|-----------|----------|
| R1 | Route Reflector / PE | 10.0.0.1/32 | 65001 | Cisco IOS-XE |
| R2 | PE Router | 10.0.0.2/32 | 65001 | Cisco IOS-XE |
| R3 | Customer Edge | 10.0.0.3/32 | 65002 | Cisco IOS-XE |
| R4 | Customer Edge | 10.0.0.4/32 | 65003 | Cisco IOS-XE |

### IP Addressing

| Link | Network | R1 | R2 | R3 | R4 |
|------|---------|----|----|----|----|
| R1â€“R2 | 10.1.12.0/30 | .1 | .2 | â€” | â€” |
| R1â€“R3 | 10.1.13.0/30 | .1 | â€” | .2 | â€” |
| R2â€“R4 | 10.1.24.0/30 | â€” | .1 | â€” | .2 |

---

## ðŸ“‹ Prerequisites

- **Virtualization Platform**: EVE-NG, GNS3, or Cisco CML/VIRL
- **Router Images**: Cisco IOS-XE (CSR1000v) or IOSv
- **Knowledge**: Basic IP routing, OSPF fundamentals, subnetting
- **Tools**: SSH client (PuTTY/SecureCRT), Wireshark (optional)

---

## ðŸ”§ Step-by-Step Instructions

### Phase 1: Base Configuration

1. Configure hostnames and interface IP addresses on all routers
2. Configure Loopback0 interfaces on all routers
3. Verify IP connectivity between directly connected interfaces using `ping`

### Phase 2: iBGP Configuration (AS 65001)

4. Configure iBGP between R1 and R2 using Loopback0 addresses
5. Configure OSPF as the IGP within AS 65001 (for loopback reachability)
6. Configure R1 as a Route Reflector for R2

```
! R1 â€” Route Reflector Configuration
router bgp 65001
 bgp router-id 10.0.0.1
 neighbor 10.0.0.2 remote-as 65001
 neighbor 10.0.0.2 update-source Loopback0
 neighbor 10.0.0.2 route-reflector-client
 !
 address-family ipv4 unicast
  network 10.0.0.1 mask 255.255.255.255
 exit-address-family
```

### Phase 3: eBGP Configuration

7. Configure eBGP between R1 and R3 (AS 65001 â†” AS 65002)
8. Configure eBGP between R2 and R4 (AS 65001 â†” AS 65003)
9. Advertise customer networks into BGP

``````
! R3 â€” eBGP Peering with R1
router bgp 65002
 bgp router-id 10.0.0.3
 neighbor 10.1.13.1 remote-as 65001
 !
 address-family ipv4 unicast
  network 192.168.3.0 mask 255.255.255.0
  network 10.0.0.3 mask 255.255.255.255
 exit-address-family
``````

### Phase 4: BGP Attribute Manipulation

10. Configure Local Preference on R1 to prefer routes via R3
11. Configure AS-Path Prepending on R4 to make its path less preferred
12. Configure MED (Multi-Exit Discriminator) between AS 65001 and AS 65002

``````
! Route-map for Local Preference
route-map SET-LOCAL-PREF permit 10
 set local-preference 200
!
router bgp 65001
 neighbor 10.1.13.2 route-map SET-LOCAL-PREF in
``````

### Phase 5: Route Filtering

13. Create prefix-lists to filter specific routes
14. Apply route-maps with prefix-lists to BGP neighbors
15. Verify filtering with `show ip bgp` and `show ip bgp neighbors <ip> advertised-routes`

``````
! Prefix-list to deny default route
ip prefix-list DENY-DEFAULT seq 5 deny 0.0.0.0/0
ip prefix-list DENY-DEFAULT seq 10 permit 0.0.0.0/0 le 32
!
router bgp 65001
 neighbor 10.1.13.2 prefix-list DENY-DEFAULT in
``````

### Phase 6: Route Aggregation

16. Configure BGP route summarization on R1
17. Verify summarized routes are advertised to peers

``````
! BGP Aggregation
router bgp 65001
 address-family ipv4 unicast
  aggregate-address 192.168.0.0 255.255.0.0 summary-only
``````

---

## ðŸ“ Real Device Configurations

Full device configurations are located in the [``configs/``](configs/) directory:

- [``configs/R1-route-reflector.cfg``](configs/R1-route-reflector.cfg) â€” R1 Route Reflector (AS 65001)
- [``configs/R2-pe-router.cfg``](configs/R2-pe-router.cfg) â€” R2 PE Router (AS 65001)
- [``configs/R3-customer-edge.cfg``](configs/R3-customer-edge.cfg) â€” R3 Customer Edge (AS 65002)
- [``configs/R4-customer-edge.cfg``](configs/R4-customer-edge.cfg) â€” R4 Customer Edge (AS 65003)

---

## âš ï¸ What Can Go Wrong â€” Troubleshooting Guide

### 1. BGP Neighbor Stuck in "Active" State
**Symptom**: ``show ip bgp summary`` shows neighbor in Active state

**Common Causes**:
- TCP port 179 blocked by ACL or firewall
- Incorrect neighbor IP address configured
- Missing ``update-source`` for iBGP (using physical vs loopback)
- IGP not converged (iBGP canâ€™t reach loopback)

**Fix**:
```
! Verify TCP connectivity
telnet 10.0.0.2 179

! Check for ACLs blocking BGP
show ip access-lists
show ip interface <interface>

! Verify IGP reachability
show ip route 10.0.0.2
ping 10.0.0.2 source loopback0
```

### 2. BGP Routes Not Appearing in the Table
**Symptom**: `show ip bgp` doesnâ€™t show expected routes

**Common Causes**:
- Network statement doesnâ€™t match exact prefix/mask in routing table
- Missing `address-family ipv4 unicast` activation
- Route-map or prefix-list filtering the routes
- Next-hop unreachable (iBGP next-hop-self not configured)

**Fix**:
```
! Check if network exists in routing table
show ip route 192.168.3.0

! Check BGP table for filtered routes
show ip bgp neighbors 10.1.13.2 received-routes
show ip bgp neighbors 10.1.13.2 advertised-routes

! Configure next-hop-self for iBGP
router bgp 65001
 neighbor 10.0.0.2 next-hop-self
```

### 3. Suboptimal Path Selection
**Symptom**: Traffic takes an unexpected path

**Common Causes**:
- Local Preference overriding AS-Path length
- Weight set on one router (Weight is local to the router)
- MED comparison only between same-neighbor-AS routes
- BGP best-path algorithm order misunderstood

**Fix**:
```
! View the full BGP path selection details
show ip bgp 192.168.3.0
show ip bgp 192.168.3.0 bestpath

! Check attributes
show ip bgp neighbors 10.1.13.2 routes
show route-map
```

### 4. Route Reflector Loop
**Symptom**: Routing loops or routes appearing with unexpected cluster-list

**Common Causes**:
- Multiple route reflectors with incorrect cluster-id
- Missing route-reflector-client command
- Originator-ID / Cluster-ID conflicts

**Fix**:
```
! Verify RR configuration
show ip bgp neighbors 10.0.0.2 | include route-reflector
show ip bgp 192.168.3.0 | include Cluster
```

### 5. Authentication Mismatch
**Symptom**: BGP session flaps or wonâ€™t establish

**Common Causes**:
- MD5 password mismatch between peers
- Key-chain misconfiguration

**Fix**:
```
! Verify MD5 authentication
show ip bgp neighbors 10.1.13.2 | include password
debug ip bgp neighbor 10.1.13.2 events
```

---

## ðŸ”¬ Verification Commands Cheat Sheet

| Command | Purpose |
|---------|---------|
| `show ip bgp summary` | View BGP neighbor status and prefix counts |
| `show ip bgp` | View BGP table with all paths |
| `show ip bgp neighbors <ip>` | Detailed neighbor information |
| `show ip bgp neighbors <ip> advertised-routes` | Routes advertised to a specific peer |
| `show ip bgp neighbors <ip> received-routes` | Routes received from a specific peer |
| `show ip bgp <prefix>` | Detailed info about a specific prefix |
| `show route-map` | View configured route-maps |
| `show ip prefix-list` | View configured prefix-lists |
| `debug ip bgp updates` | Debug BGP update messages (use with caution!) |
| `clear ip bgp * soft` | Soft reset all BGP sessions |

---

## ðŸ“š References

- [RFC 4271 â€” BGP-4 Protocol Specification](https://datatracker.ietf.org/doc/html/rfc4271)
- [RFC 4456 â€” BGP Route Reflection](https://datatracker.ietf.org/doc/html/rfc4456)
- [Cisco BGP Configuration Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/configuration/xe-16/irg-xe-16-book.html)
- [NetworkThinkTank Blog â€” BGP Series](https://networkthinktank.blog)
- [BGP Best Path Selection Algorithm](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/13753-25.html)

---

## ðŸ“‚ Repository Structure

```
lab-01-bgp-fundamentals/
â”œâ”€â”€ README.md
â”œâ”€â”€ lab-files/
â”‚   â”œâ”€â”€ bgp-peering-template.txt
â”‚   â””â”€â”€ verification-script.py
â”œâ”€â”€ diagrams/
â”‚   â”œâ”€â”€ topology-placeholder.png
â”‚   â””â”€â”€ bgp-topology.drawio
â””â”€â”€ configs/
    â”œâ”€â”€ R1-route-reflector.cfg
    â”œâ”€â”€ R2-pe-router.cfg
    â”œâ”€â”€ R3-customer-edge.cfg
    â””â”€â”€ R4-customer-edge.cfg
```

---

*Created by [NetworkThinkTank Labs](https://github.com/NetworkThinkTank-Labs) | Blog: [networkthinktank.blog](https://networkthinktank.blog)*

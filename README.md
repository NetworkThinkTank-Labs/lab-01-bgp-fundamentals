# Lab 01 -- BGP Fundamentals

> **NetworkThinkTank Labs** -- Hands-on networking labs for engineers, by engineers. Blog: [networkthinktank.blog](https://networkthinktank.blog)

---

## Blog Article Summary

This lab accompanies our blog series on **BGP (Border Gateway Protocol) fundamentals**. BGP is the routing protocol that holds the internet together -- it is the protocol used between autonomous systems (AS) to exchange routing information. Understanding BGP is essential for any network engineer working in service provider, enterprise, or cloud environments.

In this lab, you will build a multi-AS BGP topology from scratch, configure eBGP and iBGP peerings, manipulate path attributes, and troubleshoot common BGP issues that you will encounter in production networks.

---

## Lab Objectives

By completing this lab, you will be able to:

1. Configure eBGP peerings between routers in different autonomous systems
2. Configure iBGP peerings within the same autonomous system
3. Verify BGP neighbor adjacencies and troubleshoot peering failures
4. Understand BGP path selection and the BGP best-path algorithm
5. Manipulate BGP attributes (Local Preference, MED, AS-Path Prepending)
6. Implement route filtering using prefix-lists and route-maps
7. Configure BGP route reflectors for iBGP scalability

---

## Lab Topology

```
                    AS 65001                         AS 65002
              +-----------------+             +-----------------+
              |                 |             |                 |
              |   R1 (ISP-A)   |             |   R4 (ISP-B)   |
              |   Lo0: 1.1.1.1 |             |   Lo0: 4.4.4.4 |
              |                 |             |                 |
              +--------+--------+             +--------+--------+
                       |                               |
                       | eBGP                          | eBGP
                       | 10.0.12.0/30                  | 10.0.34.0/30
                       |                               |
              +--------+--------+             +--------+--------+
              |                 |             |                 |
              |   R2 (Edge-1)  +-------------+   R3 (Edge-2)  |
              |   Lo0: 2.2.2.2 |    iBGP     |   Lo0: 3.3.3.3 |
              |                 | 10.0.23.0/30|                 |
              +-----------------+             +-----------------+
                        AS 65100 (Customer)
```

> Full topology diagrams are available in the [`/diagrams`](./diagrams) folder.

---

## Prerequisites

| Requirement | Details |
|---|---|
| **Platform** | GNS3, EVE-NG, or Cisco CML |
| **Router Images** | Cisco IOSv, CSR1000v, or equivalent |
| **Knowledge** | CCNA-level routing and switching |
| **Tools** | Terminal emulator (SecureCRT, PuTTY, or built-in console) |

---

## Step-by-Step Instructions

### Phase 1 -- Base Connectivity

1. Deploy the topology using your preferred platform (see `/lab-files`).
2. Assign IP addresses on all interfaces per the addressing table.
3. Configure loopback interfaces on all routers.
4. Verify Layer 3 reachability between directly connected neighbors with `ping`.

### Phase 2 -- eBGP Configuration

5. Configure eBGP peering between R1 (AS 65001) and R2 (AS 65100).
6. Configure eBGP peering between R4 (AS 65002) and R3 (AS 65100).
7. Advertise loopback networks into BGP using `network` statements.
8. Verify BGP neighbor adjacency: `show bgp summary`.
9. Verify routes in the BGP table: `show bgp ipv4 unicast`.

### Phase 3 -- iBGP Configuration

10. Configure iBGP peering between R2 and R3 (both in AS 65100) using loopback addresses.
11. Ensure IGP (OSPF/EIGRP) is running between R2 and R3 for loopback reachability.
12. Configure `next-hop-self` on R2 and R3 for eBGP-learned routes.
13. Verify iBGP-learned routes appear in the routing table.

### Phase 4 -- Path Manipulation

14. Apply **Local Preference** on R2 to prefer routes via ISP-A (AS 65001).
15. Apply **AS-Path Prepending** on R3 to influence inbound traffic from ISP-B.
16. Configure **MED** to signal path preference to external peers.
17. Verify best-path selection: `show bgp ipv4 unicast <prefix>`.

### Phase 5 -- Route Reflector & Filtering

18. Configure R2 as a BGP Route Reflector with R3 as its client.
19. Implement prefix-list based route filtering to control inbound/outbound advertisements.
20. Apply route-maps for granular policy control.
21. Verify filtering: `show ip prefix-list`, `show route-map`.

---

## Real Configurations

Production-ready configuration snippets are provided in the [`/configs`](./configs) folder:

| File | Description |
|---|---|
| `R1-isp-a-config.txt` | ISP-A router R1 -- eBGP configuration |
| `R2-edge-1-config.txt` | Customer edge R2 -- eBGP + iBGP + Route Reflector |
| `R3-edge-2-config.txt` | Customer edge R3 -- eBGP + iBGP client |
| `R4-isp-b-config.txt` | ISP-B router R4 -- eBGP configuration |

---

## What Can Go Wrong -- Common Issues & Fixes

### 1. BGP Neighbor Stuck in Idle State
- **Cause:** No route to the neighbor IP address, or incorrect `neighbor` statement.
- **Fix:** Verify reachability with `ping`. Ensure `neighbor <IP> remote-as <ASN>` is correct. Check that the source interface is up.

### 2. BGP Neighbor Stuck in Active State
- **Cause:** TCP port 179 blocked by an ACL or firewall, or the remote side is not configured.
- **Fix:** Check ACLs on both routers. Verify both sides have matching `remote-as` configuration. Test TCP connectivity.

### 3. iBGP Routes Not Appearing in Routing Table
- **Cause:** iBGP next-hop is unreachable (common when peering via loopbacks).
- **Fix:** Use `neighbor <IP> next-hop-self` on the router redistributing eBGP routes to iBGP. Alternatively, ensure IGP carries the next-hop network.

### 4. Routes Learned but Not Installed (RIB Failure)
- **Cause:** A route with a lower administrative distance already exists in the routing table.
- **Fix:** Check `show bgp ipv4 unicast rib-failure`. Review static routes or IGP routes that may conflict.

### 5. Asymmetric Routing or Suboptimal Path Selection
- **Cause:** Local Preference, MED, or AS-Path length not configured as intended.
- **Fix:** Use `show bgp ipv4 unicast <prefix>` to review all path attributes step by step. Adjust route-maps accordingly.

### 6. Route Reflector Not Propagating Routes to Clients
- **Cause:** Missing `neighbor <IP> route-reflector-client` command on the RR.
- **Fix:** Verify RR configuration. Ensure the RR has the routes in its own BGP table before it can reflect them.

---

## References

- [RFC 4271 -- BGP-4 Specification](https://datatracker.ietf.org/doc/html/rfc4271)
- [RFC 4456 -- BGP Route Reflection](https://datatracker.ietf.org/doc/html/rfc4456)
- [Cisco BGP Configuration Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/configuration/xe-16/irg-xe-16-book.html)
- [BGP Best Path Selection Algorithm](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/13753-25.html)
- [NetworkThinkTank Blog](https://networkthinktank.blog)

---

## Repository Structure

```
lab-01-bgp-fundamentals/
|-- README.md
|-- configs/
|   +-- .gitkeep
|-- diagrams/
|   +-- .gitkeep
+-- lab-files/
    +-- .gitkeep
```

---

> **Pro Tip:** Always troubleshoot BGP from the bottom up -- verify physical connectivity, IP reachability, and TCP port 179 access before diving into BGP-specific issues.

**Happy Labbing!**

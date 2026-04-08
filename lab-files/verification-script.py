#!/usr/bin/env python3
"""
BGP Lab Verification Script — NetworkThinkTank Labs
Verifies BGP peerings, route advertisements, and path attributes.
Requires: pip install netmiko
"""

from netmiko import ConnectHandler

DEVICES = [
    {"device_type": "cisco_ios", "host": "10.0.0.1", "username": "admin", "password": "admin", "secret": "admin"},
    {"device_type": "cisco_ios", "host": "10.0.0.2", "username": "admin", "password": "admin", "secret": "admin"},
    {"device_type": "cisco_ios", "host": "10.0.0.3", "username": "admin", "password": "admin", "secret": "admin"},
    {"device_type": "cisco_ios", "host": "10.0.0.4", "username": "admin", "password": "admin", "secret": "admin"},
]

VERIFICATION_COMMANDS = [
    "show ip bgp summary",
    "show ip bgp",
    "show ip route bgp",
    "show ip bgp neighbors | include BGP neighbor|BGP state",
]

def verify_bgp(device):
    print(f"\n{'='*60}")
    print(f"  Device: {device['host']}")
    print(f"{'='*60}")
    try:
        conn = ConnectHandler(**device)
        conn.enable()
        for cmd in VERIFICATION_COMMANDS:
            print(f"\n--- {cmd} ---")
            output = conn.send_command(cmd)
            print(output)
        conn.disconnect()
    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == "__main__":
    print("BGP Lab Verification — NetworkThinkTank Labs")
    print("=" * 60)
    for device in DEVICES:
        verify_bgp(device)
    print("\n[✓] Verification complete.")


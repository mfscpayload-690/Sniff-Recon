"""
helpers.py

Optional helper functions for Sniff Recon.
"""

def get_protocol_name(proto_num):
    """
    Map protocol number to protocol name.

    Args:
        proto_num (int): Protocol number.

    Returns:
        str: Protocol name or "UNKNOWN" if not found.
    """
    protocol_map = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
        2: "IGMP",
        89: "OSPF",
        # Add more protocol mappings as needed
    }
    return protocol_map.get(proto_num, "UNKNOWN")

"""
pcap_parser.py

Parser for .pcap and .pcapng files using Scapy.
Extracts source IP, destination IP, protocol number, and packet size.
"""

from scapy.all import rdpcap, IP
from utils.helpers import get_protocol_name

def parse_pcap(file_path):
    """
    Parse a pcap or pcapng file and extract relevant packet information.

    Args:
        file_path (str): Path to the pcap file.

    Returns:
        list: A list of dictionaries with keys:
            - src_ip
            - dst_ip
            - protocol
            - packet_size
    """
    packets = rdpcap(file_path)
    parsed_data = []

    for pkt in packets:
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            proto_num = pkt[IP].proto
            protocol = get_protocol_name(proto_num)
            packet_size = len(pkt)
            parsed_data.append({
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "protocol": protocol,
                "packet_size": packet_size
            })

    return parsed_data

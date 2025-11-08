"""Parser for .pcap and .pcapng files using Scapy.
Extracts timestamp, source IP, destination IP, protocol, source port, and destination port.
Returns data as a pandas DataFrame.
"""

from scapy.all import rdpcap
from scapy.layers.inet import IP, TCP, UDP
import pandas as pd
from src.utils.helpers import get_protocol_name

def parse_pcap(file_path: str) -> pd.DataFrame:
    """
    Parse a pcap or pcapng file and extract relevant packet information.

    Args:
        file_path (str): Path to the pcap file.

    Returns:
        pd.DataFrame: DataFrame with columns:
            - Timestamp
            - Source IP
            - Destination IP
            - Protocol (TCP/UDP/ICMP/Other)
            - Source Port
            - Destination Port
    """
    packets = rdpcap(file_path)
    parsed_data = []

    for pkt in packets:
        if IP in pkt:
            timestamp = pkt.time
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            proto_num = pkt[IP].proto
            protocol_name = get_protocol_name(proto_num)
            # Map protocol to TCP/UDP/ICMP/Other
            if protocol_name in ['TCP', 'UDP', 'ICMP']:
                protocol = protocol_name
            else:
                protocol = 'Other'

            # Extract ports if TCP or UDP
            src_port = None
            dst_port = None
            if protocol == 'TCP' and TCP in pkt:
                src_port = pkt[TCP].sport
                dst_port = pkt[TCP].dport
            elif protocol == 'UDP' and UDP in pkt:
                src_port = pkt[UDP].sport
                dst_port = pkt[UDP].dport

            parsed_data.append({
                'Timestamp': timestamp,
                'Source IP': src_ip,
                'Destination IP': dst_ip,
                'Protocol': protocol,
                'Source Port': src_port,
                'Destination Port': dst_port
            })

    df = pd.DataFrame(parsed_data)
    return df

def generate_summary(df: pd.DataFrame) -> dict:
    """
    Generate a summary dictionary from the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame returned by parse_pcap.

    Returns:
        dict: Summary with keys:
            - total_packets
            - unique_source_ips
            - unique_destination_ips
            - top_5_source_ips
            - top_5_destination_ips
            - protocol_distribution
    """
    total_packets = len(df)
    unique_source_ips = df['Source IP'].nunique()
    unique_destination_ips = df['Destination IP'].nunique()
    top_5_source_ips = df['Source IP'].value_counts().head(5).to_dict()
    top_5_destination_ips = df['Destination IP'].value_counts().head(5).to_dict()
    protocol_distribution = df['Protocol'].value_counts().to_dict()

    summary = {
        'total_packets': total_packets,
        'unique_source_ips': unique_source_ips,
        'unique_destination_ips': unique_destination_ips,
        'top_5_source_ips': top_5_source_ips,
        'top_5_destination_ips': top_5_destination_ips,
        'protocol_distribution': protocol_distribution
    }
    return summary

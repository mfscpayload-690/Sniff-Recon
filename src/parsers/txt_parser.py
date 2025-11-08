"""
txt_parser.py

Placeholder parser for .txt files.
Basic parser logic or placeholder for future expansion.
"""

import re
from src.utils.helpers import get_protocol_name

def parse_txt(file_path):
    """
    Parse a TXT file with structured logs of format:
    "SRC=... DST=... PROTO=... SIZE=..."

    Args:
        file_path (str): Path to the TXT file.

    Returns:
        list: A list of dictionaries with keys:
            - src_ip
            - dst_ip
            - protocol
            - packet_size
    """
    parsed_data = []
    pattern = re.compile(r"SRC=(?P<src_ip>\\S+) DST=(?P<dst_ip>\\S+) PROTO=(?P<proto>\\d+) SIZE=(?P<size>\\d+)")
    with open(file_path, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                src_ip = match.group('src_ip')
                dst_ip = match.group('dst_ip')
                proto_num = int(match.group('proto'))
                protocol = get_protocol_name(proto_num)
                packet_size = int(match.group('size'))
                parsed_data.append({
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "protocol": protocol,
                    "packet_size": packet_size
                })
    return parsed_data

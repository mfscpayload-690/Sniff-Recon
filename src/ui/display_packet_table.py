import streamlit as st
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
from scapy.packet import Packet
from typing import List, Optional
import pandas as pd
import binascii
import datetime

def inject_modern_css():
    """Inject modern CSS for beautiful packet analyzer UI"""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global styles */
        .main {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #e0e0e0;
        }
        
        /* Packet table styling */
        .packet-table-container {
            background: rgba(30, 30, 30, 0.8);
            border-radius: 16px;
            border: 1px solid rgba(0, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            margin: 1rem 0;
            overflow: hidden;
        }
        
        /* Protocol layer cards */
        .protocol-card {
            background: linear-gradient(145deg, rgba(30, 30, 30, 0.9), rgba(20, 20, 20, 0.9));
            border: 2px solid rgba(0, 255, 255, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0, 255, 255, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .protocol-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #00ffff, #00b3b3, #00ffff);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        
        .protocol-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0, 255, 255, 0.2);
            border-color: rgba(0, 255, 255, 0.6);
        }
        
        .protocol-card:hover::before {
            transform: scaleX(1);
        }
        
        .protocol-header {
            font-size: 1.25rem;
            font-weight: 600;
            color: #00ffff;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .protocol-header::before {
            content: '🔍';
            font-size: 1.1rem;
        }
        
        .protocol-content {
            background: rgba(15, 15, 15, 0.5);
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid rgba(0, 255, 255, 0.1);
        }
        
        .field-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(0, 255, 255, 0.1);
            transition: background-color 0.2s ease;
        }
        
        .field-row:hover {
            background: rgba(0, 255, 255, 0.05);
            border-radius: 8px;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        .field-row:last-child {
            border-bottom: none;
        }
        
        .field-label {
            font-weight: 500;
            color: #00b3b3;
            min-width: 120px;
        }
        
        .field-value {
            color: #e0e0e0;
            font-family: 'Courier New', monospace;
            text-align: right;
            word-break: break-all;
        }
        
        /* Hex dump styling */
        .hex-dump-container {
            background: rgba(15, 15, 15, 0.8);
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid rgba(0, 255, 255, 0.2);
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            line-height: 1.4;
            max-height: 400px;
            overflow-y: auto;
        }
        
        /* Packet summary styling */
        .packet-summary {
            background: linear-gradient(145deg, rgba(30, 30, 30, 0.9), rgba(20, 20, 20, 0.9));
            border: 2px solid rgba(0, 255, 255, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0, 255, 255, 0.1);
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .summary-item {
            background: rgba(15, 15, 15, 0.5);
            border-radius: 8px;
            padding: 1rem;
            border: 1px solid rgba(0, 255, 255, 0.1);
            text-align: center;
        }
        
        .summary-label {
            font-size: 0.9rem;
            color: #00b3b3;
            margin-bottom: 0.5rem;
        }
        
        .summary-value {
            font-size: 1.1rem;
            font-weight: 600;
            color: #00ffff;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .protocol-card {
                padding: 1rem;
                margin: 0.5rem 0;
            }
            
            .field-row {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.25rem;
            }
            
            .field-value {
                text-align: left;
            }
            
            .summary-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Animation for cards */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .protocol-card {
            animation: fadeInUp 0.6s ease forwards;
        }
        
        .protocol-card:nth-child(1) { animation-delay: 0.1s; }
        .protocol-card:nth-child(2) { animation-delay: 0.2s; }
        .protocol-card:nth-child(3) { animation-delay: 0.3s; }
        .protocol-card:nth-child(4) { animation-delay: 0.4s; }
        .protocol-card:nth-child(5) { animation-delay: 0.5s; }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(15, 15, 15, 0.5);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #00ffff, #00b3b3);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #00b3b3, #00ffff);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def extract_packet_summary(packets: List[Packet]) -> pd.DataFrame:
    """Extract summary information from packets to build a DataFrame."""
    rows = []
    for i, pkt in enumerate(packets, start=1):
        timestamp = getattr(pkt, "time", "N/A")
        length = len(pkt)

        src_ip = "-"
        dst_ip = "-"
        protocol = "-"
        info = ""

        if IP in pkt:
            ip_layer = pkt[IP]
            src_ip = ip_layer.src
            dst_ip = ip_layer.dst
            proto_num = ip_layer.proto
            if proto_num == 6:
                protocol = "TCP"
            elif proto_num == 17:
                protocol = "UDP"
            elif proto_num == 1:
                protocol = "ICMP"
            else:
                protocol = f"Protocol {proto_num}"
        else:
            protocol = pkt.lastlayer().name if pkt.lastlayer() else "-"

        # Enhanced info field
        if protocol == "TCP" and TCP in pkt:
            tcp_layer = pkt[TCP]
            flags = []
            if tcp_layer.flags & 0x01: flags.append("FIN")
            if tcp_layer.flags & 0x02: flags.append("SYN")
            if tcp_layer.flags & 0x04: flags.append("RST")
            if tcp_layer.flags & 0x08: flags.append("PSH")
            if tcp_layer.flags & 0x10: flags.append("ACK")
            if tcp_layer.flags & 0x20: flags.append("URG")
            info = f"Port {tcp_layer.sport} → {tcp_layer.dport} [{', '.join(flags)}]"
        elif protocol == "UDP" and UDP in pkt:
            udp_layer = pkt[UDP]
            info = f"Port {udp_layer.sport} → {udp_layer.dport}"
        elif protocol == "ICMP" and ICMP in pkt:
            icmp_layer = pkt[ICMP]
            info = f"Type {icmp_layer.type}"

        # Format timestamp
        try:
            ts_float = float(timestamp)
            timestamp_str = datetime.datetime.fromtimestamp(ts_float).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        except Exception:
            timestamp_str = str(timestamp)

        rows.append({
            "No.": i,
            "Timestamp": timestamp_str,
            "Source IP": src_ip,
            "Destination IP": dst_ip,
            "Protocol": protocol,
            "Length": length,
            "Info": info,
        })

    return pd.DataFrame(rows)

def render_field_row(label: str, value: str):
    """Render a field row with hover effects"""
    st.markdown(
        f"""
        <div class="field-row">
            <span class="field-label">{label}</span>
            <span class="field-value">{value}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_ethernet_layer(pkt: Packet):
    """Render Ethernet layer in a beautiful card"""
    st.markdown('<div class="protocol-card">', unsafe_allow_html=True)
    st.markdown('<div class="protocol-header">Ethernet Layer</div>', unsafe_allow_html=True)
    
    if Ether in pkt:
        eth_layer = pkt[Ether]
        st.markdown('<div class="protocol-content">', unsafe_allow_html=True)
        render_field_row("Source MAC", eth_layer.src)
        render_field_row("Destination MAC", eth_layer.dst)
        render_field_row("Type", f"0x{eth_layer.type:04x}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="protocol-content">', unsafe_allow_html=True)
        st.markdown('<div class="field-row"><span class="field-value">Ethernet header not available</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_ip_layer(pkt: Packet):
    """Render IP layer in a beautiful card"""
    st.markdown('<div class="protocol-card">', unsafe_allow_html=True)
    st.markdown('<div class="protocol-header">IP Layer</div>', unsafe_allow_html=True)
    
    if IP in pkt:
        ip_layer = pkt[IP]
        st.markdown('<div class="protocol-content">', unsafe_allow_html=True)
        render_field_row("Version", str(ip_layer.version))
        render_field_row("Header Length", f"{ip_layer.ihl * 4} bytes")
        render_field_row("Type of Service", f"0x{ip_layer.tos:02x}")
        render_field_row("Total Length", f"{ip_layer.len} bytes")
        render_field_row("Identification", f"0x{ip_layer.id:04x}")
        render_field_row("Flags", f"0x{int(ip_layer.flags):02x}")
        render_field_row("Fragment Offset", str(ip_layer.frag))
        render_field_row("Time to Live", str(ip_layer.ttl))
        render_field_row("Protocol", f"{ip_layer.proto} ({get_protocol_name(ip_layer.proto)})")
        render_field_row("Header Checksum", f"0x{ip_layer.chksum:04x}")
        render_field_row("Source IP", ip_layer.src)
        render_field_row("Destination IP", ip_layer.dst)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="protocol-content">', unsafe_allow_html=True)
        st.markdown('<div class="field-row"><span class="field-value">IP header not available</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_transport_layer(pkt: Packet):
    """Render Transport layer (TCP/UDP) in a beautiful card"""
    st.markdown('<div class="protocol-card">', unsafe_allow_html=True)
    
    if TCP in pkt:
        tcp_layer = pkt[TCP]
        st.markdown('<div class="protocol-header">TCP Layer</div>', unsafe_allow_html=True)
        st.markdown('<div class="protocol-content">', unsafe_allow_html=True)
        render_field_row("Source Port", str(tcp_layer.sport))
        render_field_row("Destination Port", str(tcp_layer.dport))
        render_field_row("Sequence Number", str(tcp_layer.seq))
        render_field_row("Acknowledgment", str(tcp_layer.ack))
        render_field_row("Data Offset", f"{tcp_layer.dataofs * 4} bytes")
        render_field_row("Reserved", str(tcp_layer.reserved))
        
        # TCP Flags
        flags = []
        if tcp_layer.flags & 0x01: flags.append("FIN")
        if tcp_layer.flags & 0x02: flags.append("SYN")
        if tcp_layer.flags & 0x04: flags.append("RST")
        if tcp_layer.flags & 0x08: flags.append("PSH")
        if tcp_layer.flags & 0x10: flags.append("ACK")
        if tcp_layer.flags & 0x20: flags.append("URG")
        render_field_row("Flags", f"0x{int(tcp_layer.flags):02x} [{', '.join(flags)}]")
        
        render_field_row("Window Size", str(tcp_layer.window))
        render_field_row("Checksum", f"0x{tcp_layer.chksum:04x}")
        render_field_row("Urgent Pointer", str(tcp_layer.urgptr))
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif UDP in pkt:
        udp_layer = pkt[UDP]
        st.markdown('<div class="protocol-header">UDP Layer</div>', unsafe_allow_html=True)
        st.markdown('<div class="protocol-content">', unsafe_allow_html=True)
        render_field_row("Source Port", str(udp_layer.sport))
        render_field_row("Destination Port", str(udp_layer.dport))
        render_field_row("Length", f"{udp_layer.len} bytes")
        render_field_row("Checksum", f"0x{udp_layer.chksum:04x}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif ICMP in pkt:
        icmp_layer = pkt[ICMP]
        st.markdown('<div class="protocol-header">ICMP Layer</div>', unsafe_allow_html=True)
        st.markdown('<div class="protocol-content">', unsafe_allow_html=True)
        render_field_row("Type", str(icmp_layer.type))
        render_field_row("Code", str(icmp_layer.code))
        render_field_row("Checksum", f"0x{icmp_layer.chksum:04x}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.markdown('<div class="protocol-header">Transport Layer</div>', unsafe_allow_html=True)
        st.markdown('<div class="protocol-content">', unsafe_allow_html=True)
        st.markdown('<div class="field-row"><span class="field-value">Transport layer header not available</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_application_layer(pkt: Packet):
    """Render Application layer in a beautiful card"""
    st.markdown('<div class="protocol-card">', unsafe_allow_html=True)
    st.markdown('<div class="protocol-header">Application Layer</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="protocol-content">', unsafe_allow_html=True)
    
    # Try to identify application layer protocols
    if pkt.haslayer("Raw"):
        raw_layer = pkt["Raw"]
        raw_data = raw_layer.load
        
        # Try to decode as text
        try:
            text_data = raw_data.decode('utf-8', errors='ignore')
            if text_data.strip():
                st.markdown('<div class="field-row"><span class="field-label">Raw Data (Text)</span></div>', unsafe_allow_html=True)
                st.code(text_data, language="text")
        except:
            pass
        
        # Show hex representation
        if raw_data:
            st.markdown('<div class="field-row"><span class="field-label">Raw Data (Hex)</span></div>', unsafe_allow_html=True)
            hex_str = binascii.hexlify(raw_data).decode("utf-8")
            formatted_hex = " ".join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))
            st.code(formatted_hex, language="plaintext")
    else:
        st.markdown('<div class="field-row"><span class="field-value">No application layer data available</span></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_hex_dump(pkt: Packet):
    """Render hex dump in a beautiful card"""
    st.markdown('<div class="protocol-card">', unsafe_allow_html=True)
    st.markdown('<div class="protocol-header">Hex Dump View</div>', unsafe_allow_html=True)
    
    raw_bytes = bytes(pkt)
    if raw_bytes:
        st.markdown('<div class="hex-dump-container">', unsafe_allow_html=True)
        hex_dump = format_hex_dump(raw_bytes)
        st.code(hex_dump, language="plaintext")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="protocol-content">', unsafe_allow_html=True)
        st.markdown('<div class="field-row"><span class="field-value">No raw data available</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def format_hex_dump(data: bytes) -> str:
    """Format bytes into a readable hex dump"""
    lines = []
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_bytes = " ".join(f"{b:02x}" for b in chunk)
        ascii_bytes = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        lines.append(f"{i:08x}  {hex_bytes:<48}  {ascii_bytes}")
    return "\n".join(lines)

def get_protocol_name(proto_num: int) -> str:
    """Get protocol name from protocol number"""
    protocols = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
        53: "DNS",
        80: "HTTP",
        443: "HTTPS",
        22: "SSH",
        21: "FTP",
        25: "SMTP",
        110: "POP3",
        143: "IMAP"
    }
    return protocols.get(proto_num, "Unknown")

def display_packet_table(packets: List[Packet]):
    """Display modern packet analyzer with beautiful UI"""
    # Inject CSS
    inject_modern_css()
    
    st.markdown('<div class="section-heading">PACKET SUMMARY TABLE</div>', unsafe_allow_html=True)
    
    df = extract_packet_summary(packets)
    
    # Display the table using Streamlit's dataframe (no PyArrow needed)
    st.markdown('<div class="packet-table-container">', unsafe_allow_html=True)
    st.dataframe(
        df,
        width='stretch',
        height=400,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Packet selection using number input
    st.markdown('<div class="section-heading">SELECT PACKET FOR ANALYSIS</div>', unsafe_allow_html=True)
    packet_number = st.number_input(
        "Enter packet number to analyze:",
        min_value=1,
        max_value=len(packets),
        value=1,
        step=1
    )
    
    if packet_number:
        selected_index = packet_number - 1
        pkt = packets[selected_index]
        packet_row = df.iloc[selected_index]
        
        # Packet summary section
        st.markdown('<div class="section-heading">SELECTED PACKET ANALYSIS</div>', unsafe_allow_html=True)
        st.markdown('<div class="packet-summary">', unsafe_allow_html=True)
        st.markdown('<div class="summary-grid">', unsafe_allow_html=True)
        
        # Summary items
        summary_items = [
            ("Packet Number", str(packet_row["No."])),
            ("Timestamp", packet_row["Timestamp"]),
            ("Source IP", packet_row["Source IP"]),
            ("Destination IP", packet_row["Destination IP"]),
            ("Protocol", packet_row["Protocol"]),
            ("Length", f"{packet_row['Length']} bytes")
        ]
        
        for label, value in summary_items:
            st.markdown(
                f"""
                <div class="summary-item">
                    <div class="summary-label">{label}</div>
                    <div class="summary-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Protocol layers section
        st.markdown('<div class="section-heading">PROTOCOL LAYER ANALYSIS</div>', unsafe_allow_html=True)
        
        # Render each protocol layer
        render_ethernet_layer(pkt)
        render_ip_layer(pkt)
        render_transport_layer(pkt)
        render_application_layer(pkt)
        render_hex_dump(pkt) 
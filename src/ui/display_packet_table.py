"""
Packet Table Display Module
============================
Display network packets in an interactive table with filtering and inspection.
Uses shared CSS from styles.css for consistent styling.
"""

import streamlit as st
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
from scapy.packet import Packet
from typing import List, Optional
import pandas as pd
import binascii
from src.ui.icons import icon


def extract_packet_summary(packets: List[Packet]) -> pd.DataFrame:
    """Extract summary information from packets into a DataFrame."""
    data = []
    
    for idx, pkt in enumerate(packets):
        row = {
            "id": idx + 1,
            "time": float(pkt.time) if hasattr(pkt, 'time') else 0,
            "src_ip": "",
            "dst_ip": "",
            "protocol": "Unknown",
            "length": len(pkt),
            "info": ""
        }
        
        # Extract IP layer info
        if IP in pkt:
            row["src_ip"] = pkt[IP].src
            row["dst_ip"] = pkt[IP].dst
            row["protocol"] = get_protocol_name(pkt[IP].proto)
        elif Ether in pkt:
            row["src_ip"] = pkt[Ether].src
            row["dst_ip"] = pkt[Ether].dst
            row["protocol"] = "Ethernet"
        
        # Get transport layer info
        if TCP in pkt:
            row["protocol"] = "TCP"
            row["info"] = f"Port {pkt[TCP].sport} → {pkt[TCP].dport}"
            flags = []
            if pkt[TCP].flags.S: flags.append("SYN")
            if pkt[TCP].flags.A: flags.append("ACK")
            if pkt[TCP].flags.F: flags.append("FIN")
            if pkt[TCP].flags.R: flags.append("RST")
            if pkt[TCP].flags.P: flags.append("PSH")
            if flags:
                row["info"] += f" [{','.join(flags)}]"
        elif UDP in pkt:
            row["protocol"] = "UDP"
            row["info"] = f"Port {pkt[UDP].sport} → {pkt[UDP].dport}"
        elif ICMP in pkt:
            row["protocol"] = "ICMP"
            row["info"] = f"Type {pkt[ICMP].type}, Code {pkt[ICMP].code}"
        
        data.append(row)
    
    return pd.DataFrame(data)


def get_protocol_name(proto_num: int) -> str:
    """Convert protocol number to name."""
    protocols = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
        41: "IPv6",
        47: "GRE",
        50: "ESP",
        51: "AH",
        89: "OSPF",
        132: "SCTP"
    }
    return protocols.get(proto_num, f"Proto-{proto_num}")


def get_protocol_badge_class(protocol: str) -> str:
    """Get CSS class for protocol badge."""
    protocol_upper = protocol.upper()
    if "TCP" in protocol_upper:
        return "sr-protocol-tcp"
    elif "UDP" in protocol_upper:
        return "sr-protocol-udp"
    elif "ICMP" in protocol_upper:
        return "sr-protocol-icmp"
    elif "HTTP" in protocol_upper:
        return "sr-protocol-http"
    elif "DNS" in protocol_upper:
        return "sr-protocol-dns"
    return "sr-protocol-other"


def render_packet_inspector(packet: Packet) -> None:
    """Render detailed packet inspection view."""
    eye_icon = icon("eye", "lg")
    st.markdown(f"""
        <div class="sr-inspector">
            <div class="sr-inspector-header">{eye_icon} Packet Details</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Ethernet Layer
    if Ether in packet:
        with st.expander("Ethernet Layer", expanded=True):
            eth = packet[Ether]
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Source MAC:** `{eth.src}`")
            with col2:
                st.markdown(f"**Destination MAC:** `{eth.dst}`")
            st.markdown(f"**Type:** `0x{eth.type:04x}`")
    
    # IP Layer
    if IP in packet:
        with st.expander("IP Layer", expanded=True):
            ip = packet[IP]
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Source IP:** `{ip.src}`")
                st.markdown(f"**Version:** `{ip.version}`")
                st.markdown(f"**TTL:** `{ip.ttl}`")
            with col2:
                st.markdown(f"**Destination IP:** `{ip.dst}`")
                st.markdown(f"**Protocol:** `{get_protocol_name(ip.proto)}`")
                st.markdown(f"**Total Length:** `{ip.len}` bytes")
    
    # TCP Layer
    if TCP in packet:
        with st.expander("TCP Layer", expanded=True):
            tcp = packet[TCP]
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Source Port:** `{tcp.sport}`")
                st.markdown(f"**Sequence:** `{tcp.seq}`")
                st.markdown(f"**Window:** `{tcp.window}`")
            with col2:
                st.markdown(f"**Destination Port:** `{tcp.dport}`")
                st.markdown(f"**Acknowledgment:** `{tcp.ack}`")
                flags = []
                if tcp.flags.S: flags.append("SYN")
                if tcp.flags.A: flags.append("ACK")
                if tcp.flags.F: flags.append("FIN")
                if tcp.flags.R: flags.append("RST")
                if tcp.flags.P: flags.append("PSH")
                st.markdown(f"**Flags:** `{', '.join(flags) if flags else 'None'}`")
    
    # UDP Layer
    if UDP in packet:
        with st.expander("UDP Layer", expanded=True):
            udp = packet[UDP]
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Source Port:** `{udp.sport}`")
            with col2:
                st.markdown(f"**Destination Port:** `{udp.dport}`")
            st.markdown(f"**Length:** `{udp.len}` bytes")
    
    # ICMP Layer
    if ICMP in packet:
        with st.expander("ICMP Layer", expanded=True):
            icmp = packet[ICMP]
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Type:** `{icmp.type}`")
            with col2:
                st.markdown(f"**Code:** `{icmp.code}`")
    
    # Hex Dump
    with st.expander("Raw Data (Hex)", expanded=False):
        raw_bytes = bytes(packet)
        hex_dump = format_hex_dump(raw_bytes)
        st.code(hex_dump, language=None)


def format_hex_dump(data: bytes, bytes_per_line: int = 16) -> str:
    """Format bytes into a readable hex dump."""
    lines = []
    for i in range(0, len(data), bytes_per_line):
        chunk = data[i:i + bytes_per_line]
        hex_part = ' '.join(f'{b:02x}' for b in chunk)
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        lines.append(f"{i:08x}  {hex_part:<{bytes_per_line * 3}}  |{ascii_part}|")
    return '\n'.join(lines)


def display_packet_table(packets: List[Packet]) -> None:
    """Display packets in an interactive table with filtering."""
    if not packets:
        st.warning("No packets to display.")
        return
    
    # Extract packet data
    df = extract_packet_summary(packets)
    
    bar_icon = icon("bar-chart")
    # Search and filter bar
    st.markdown(f"""
        <div class="sr-table-toolbar">
            <div style="font-weight: 600; color: var(--accent-cyan);">
                {bar_icon} {len(df)} Packets
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input(
            "Search",
            placeholder="Filter by IP, port, or keyword...",
            key="packet_search",
            label_visibility="collapsed"
        )
    
    with col2:
        protocols = ["All"] + df["protocol"].unique().tolist()
        selected_protocol = st.selectbox(
            "Protocol",
            protocols,
            key="protocol_filter",
            label_visibility="collapsed"
        )
    
    with col3:
        sort_options = ["ID", "Time", "Length", "Protocol"]
        sort_by = st.selectbox(
            "Sort by",
            sort_options,
            key="sort_by",
            label_visibility="collapsed"
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_term:
        mask = (
            filtered_df["src_ip"].str.contains(search_term, case=False, na=False) |
            filtered_df["dst_ip"].str.contains(search_term, case=False, na=False) |
            filtered_df["info"].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if selected_protocol != "All":
        filtered_df = filtered_df[filtered_df["protocol"] == selected_protocol]
    
    # Sort
    sort_column_map = {"ID": "id", "Time": "time", "Length": "length", "Protocol": "protocol"}
    filtered_df = filtered_df.sort_values(by=sort_column_map.get(sort_by, "id"))
    
    # Show filtered count
    if len(filtered_df) != len(df):
        st.info(f"Showing {len(filtered_df)} of {len(df)} packets")
    
    # Display table
    st.markdown("""
        <style>
        .packet-row { 
            padding: 0.75rem 1rem;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            transition: background 0.15s;
        }
        .packet-row:hover {
            background: rgba(0, 212, 255, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Paginate
    page_size = 50
    total_pages = max(1, (len(filtered_df) + page_size - 1) // page_size)
    
    if "packet_page" not in st.session_state:
        st.session_state["packet_page"] = 0
    
    current_page = st.session_state["packet_page"]
    start_idx = current_page * page_size
    end_idx = min(start_idx + page_size, len(filtered_df))
    
    page_df = filtered_df.iloc[start_idx:end_idx]
    
    # Render packets
    for _, row in page_df.iterrows():
        protocol_class = get_protocol_badge_class(row["protocol"])
        
        with st.container():
            cols = st.columns([0.5, 1.5, 1.5, 1, 0.8, 2])
            
            with cols[0]:
                st.markdown(f"**#{row['id']}**")
            with cols[1]:
                st.markdown(f"`{row['src_ip']}`")
            with cols[2]:
                st.markdown(f"`{row['dst_ip']}`")
            with cols[3]:
                st.markdown(f"<span class='sr-protocol-badge {protocol_class}'>{row['protocol']}</span>", unsafe_allow_html=True)
            with cols[4]:
                st.markdown(f"{row['length']} B")
            with cols[5]:
                st.markdown(f"<span style='color: var(--text-secondary);'>{row['info']}</span>", unsafe_allow_html=True)
    
    # Pagination controls
    if total_pages > 1:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("◀ Previous", disabled=current_page == 0, key="prev_page"):
                st.session_state["packet_page"] = max(0, current_page - 1)
                st.rerun()
        
        with col2:
            st.markdown(f"<div style='text-align: center; padding: 0.5rem;'>Page {current_page + 1} of {total_pages}</div>", unsafe_allow_html=True)
        
        with col3:
            if st.button("Next ▶", disabled=current_page >= total_pages - 1, key="next_page"):
                st.session_state["packet_page"] = min(total_pages - 1, current_page + 1)
                st.rerun()
    
    # Packet inspector
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    eye_icon = icon("eye")
    st.markdown(f"### {eye_icon} Inspect Packet", unsafe_allow_html=True)
    
    packet_id = st.number_input(
        "Enter packet ID to inspect",
        min_value=1,
        max_value=len(packets),
        value=1,
        key="inspect_packet_id"
    )
    
    if st.button("Inspect Packet", key="inspect_btn"):
        if 1 <= packet_id <= len(packets):
            render_packet_inspector(packets[packet_id - 1])
        else:
            st.error("Invalid packet ID")
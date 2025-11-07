import streamlit as st
import pandas as pd
import binascii
from scapy.packet import Packet
from scapy.layers.inet import IP, TCP, UDP, ICMP
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from typing import List, Optional

def inject_modern_css():
    """Inject modern CSS for beautiful packet viewer UI"""
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
    """
    Extract summary information from packets to build a DataFrame with columns:
    No., Timestamp, Source IP, Destination IP, Protocol, Length, Info
    """
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
                protocol = str(proto_num)
        else:
            protocol = pkt.lastlayer().name if pkt.lastlayer() else "-"

        # Info field: try to get meaningful info like HTTP GET or TCP flags
        if protocol == "TCP" and TCP in pkt:
            tcp_layer = pkt[TCP]
            flags = tcp_layer.sprintf("%flags%")
            info = flags if flags else ""
            # Check for HTTP layer (simple heuristic)
            if pkt.haslayer("Raw"):
                raw_payload = pkt["Raw"].load
                try:
                    raw_str = raw_payload.decode(errors="ignore")
                    if raw_str.startswith("GET") or raw_str.startswith("POST"):
                        info = raw_str.splitlines()[0]
                except Exception:
                    pass
        elif protocol == "UDP" and UDP in pkt:
            # Check for DNS
            if pkt.haslayer("DNS"):
                dns_layer = pkt["DNS"]
                if dns_layer.qr == 0:
                    info = f"DNS Query: {dns_layer.qd.qname.decode() if dns_layer.qd else ''}"
                else:
                    info = "DNS Response"
            else:
                info = "UDP Packet"
        elif protocol == "ICMP" and ICMP in pkt:
            icmp_layer = pkt[ICMP]
            info = icmp_layer.type

        # Format timestamp nicely
        try:
            import datetime
            ts_float = float(timestamp)
            timestamp_str = datetime.datetime.fromtimestamp(ts_float).strftime("%Y-%m-%d %H:%M:%S.%f")
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

    df = pd.DataFrame(rows)
    return df

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

def display_protocol_layer(layer, indent=0):
    """
    Recursively display protocol layer fields in a tree-like structure with indentation.
    """
    if layer is None:
        return

    layer_name = layer.name if hasattr(layer, "name") else "Layer"
    indent_str = " " * (indent * 4)
    st.markdown(f"{indent_str}**{layer_name}**")

    fields = getattr(layer, "fields", {})
    if fields:
        for field_name, value in fields.items():
            st.markdown(f"{indent_str}- **{field_name}**: {value}")
    else:
        st.markdown(f"{indent_str}- No fields available")

    # Recurse into payload if present and not NoPayload
    if hasattr(layer, "payload") and layer.payload:
        if layer.payload.name != "NoPayload":
            display_protocol_layer(layer.payload, indent + 1)

def format_hex_ascii(data: bytes, highlight_range: Optional[range] = None) -> str:
    """
    Format bytes into hex + ASCII string similar to Wireshark hex dump.
    Highlight_range is a range of bytes to highlight (optional).
    """
    lines = []
    length = len(data)
    for i in range(0, length, 16):
        chunk = data[i:i+16]
        hex_bytes = []
        ascii_bytes = []
        for j, b in enumerate(chunk):
            hex_byte = f"{b:02X}"
            if highlight_range and (i + j) in highlight_range:
                # Highlight by surrounding with brackets
                hex_byte = f"[{hex_byte}]"
                ascii_char = chr(b) if 32 <= b <= 126 else "."
                ascii_char = f"[{ascii_char}]"
            else:
                ascii_char = chr(b) if 32 <= b <= 126 else "."
            hex_bytes.append(hex_byte)
            ascii_bytes.append(ascii_char)
        hex_part = " ".join(hex_bytes)
        ascii_part = "".join(ascii_bytes)
        lines.append(f"{i:08X}  {hex_part:<48}  {ascii_part}")
    return "\n".join(lines)

def display_hex_dump(pkt: Packet, highlight_range: Optional[range] = None):
    """
    Display raw packet payload in hex + ASCII format with optional highlight.
    """
    raw_bytes = bytes(pkt)
    if not raw_bytes:
        st.write("No raw payload available.")
        return

    st.markdown("### Hex Dump Viewer")
    hex_ascii_str = format_hex_ascii(raw_bytes, highlight_range)
    st.code(hex_ascii_str, language="plaintext")

def display_packet_table(packets: List[Packet]):
    """
    Display interactive packet table using Streamlit AgGrid.
    When a row is selected, show expandable packet detail view and hex dump viewer.
    """
    # Inject modern CSS
    inject_modern_css()
    
    st.markdown("## 📊 Packet Summary Table")

    df = extract_packet_summary(packets)

    # Configure AgGrid options for sorting, filtering, single row selection
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_default_column(editable=False, filter=True, sortable=True, resizable=True)
    gb.configure_selection(selection_mode="single", use_checkbox=False)
    grid_options = gb.build()

    # Display the table with modern styling
    st.markdown('<div class="packet-table-container">', unsafe_allow_html=True)
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        height=300,
        width="100%",
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        theme="dark",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    selected_rows = grid_response.get("selected_rows", [])
    if selected_rows:
        selected_index = selected_rows[0]["No."] - 1
        pkt = packets[selected_index]

        # Expandable section for packet details
        with st.expander(f"🔍 Packet Details - No. {selected_rows[0]['No.']}"):
            st.markdown('<div class="protocol-card">', unsafe_allow_html=True)
            display_protocol_layer(pkt)
            st.markdown('</div>', unsafe_allow_html=True)

            # Hex dump viewer below protocol details
            st.markdown('<div class="protocol-card">', unsafe_allow_html=True)
            display_hex_dump(pkt)
            st.markdown('</div>', unsafe_allow_html=True)

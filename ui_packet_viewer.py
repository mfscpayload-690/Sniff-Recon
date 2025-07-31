import streamlit as st
import pandas as pd
import binascii
from scapy.packet import Packet
from scapy.layers.inet import IP, TCP, UDP, ICMP
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from typing import List, Optional

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
    st.markdown("## Packet Summary Table")

    df = extract_packet_summary(packets)

    # Configure AgGrid options for sorting, filtering, single row selection
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_default_column(editable=False, filter=True, sortable=True, resizable=True)
    gb.configure_selection(selection_mode="single", use_checkbox=False)
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        height=300,
        width="100%",
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        theme="light",
    )

    selected_rows = grid_response.get("selected_rows", [])
    if selected_rows:
        selected_index = selected_rows[0]["No."] - 1
        pkt = packets[selected_index]

        # Expandable section for packet details
        with st.expander(f"Packet Details - No. {selected_rows[0]['No.']}"):
            display_protocol_layer(pkt)

            # Hex dump viewer below protocol details
            display_hex_dump(pkt)

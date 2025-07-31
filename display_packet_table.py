import streamlit as st
from scapy.layers.inet import IP, TCP, UDP
from scapy.packet import Packet
from typing import List
import pandas as pd
import binascii

from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

def extract_packet_summary(packets: List[Packet]) -> pd.DataFrame:
    """
    Extract summary information from packets to build a DataFrame.

    Columns: Index, Timestamp, Source IP, Destination IP, Protocol, Length
    """
    rows = []
    for i, pkt in enumerate(packets, start=1):
        timestamp = getattr(pkt, "time", "N/A")
        length = len(pkt)

        src_ip = "-"
        dst_ip = "-"
        protocol = "-"

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

        try:
            import datetime
            ts_float = float(timestamp)
            timestamp_str = datetime.datetime.fromtimestamp(ts_float).strftime("%Y-%m-%d %H:%M:%S.%f")
        except Exception:
            timestamp_str = str(timestamp)

        rows.append({
            "Index": i,
            "Timestamp": timestamp_str,
            "Source IP": src_ip,
            "Destination IP": dst_ip,
            "Protocol": protocol,
            "Length": length,
        })

    df = pd.DataFrame(rows)
    return df

def display_layer_details(pkt: Packet):
    """
    Display detailed layer-wise breakdown of a packet.
    """
    st.markdown("### Detailed Packet Breakdown")
    layer = pkt
    layer_index = 1
    while layer:
        layer_name = layer.name if hasattr(layer, "name") else f"Layer {layer_index}"
        st.markdown(f"**{layer_index}. {layer_name}**")

        fields = layer.fields if hasattr(layer, "fields") else {}
        if fields:
            for field_name, value in fields.items():
                st.write(f"- **{field_name}**: {value}")
        else:
            st.write("- No fields available")

        if hasattr(layer, "payload") and layer.payload:
            if layer.payload.name == "NoPayload":
                break
            layer = layer.payload
            layer_index += 1
        else:
            break

    # Optionally show raw payload bytes
    raw_bytes = bytes(pkt)
    if raw_bytes:
        st.markdown("**Raw Payload Bytes (hex):**")
        hex_str = binascii.hexlify(raw_bytes).decode("utf-8")
        # Format hex string in groups of 2 chars (1 byte) separated by space
        formatted_hex = " ".join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))
        st.code(formatted_hex, language="plaintext")

def render_ethernet_header(pkt: Packet):
    st.markdown("#### Ethernet Header")
    if hasattr(pkt, "src") and hasattr(pkt, "dst") and hasattr(pkt, "type"):
        st.write(f"- **Source MAC:** {pkt.src}")
        st.write(f"- **Destination MAC:** {pkt.dst}")
        st.write(f"- **Type:** {pkt.type}")
    else:
        st.write("- Ethernet header not available")

def render_ip_header(pkt: Packet):
    st.markdown("#### IP Header")
    if IP in pkt:
        ip_layer = pkt[IP]
        st.write(f"- **Version:** {ip_layer.version}")
        st.write(f"- **Header Length:** {ip_layer.ihl}")
        st.write(f"- **Type of Service:** {ip_layer.tos}")
        st.write(f"- **Total Length:** {ip_layer.len}")
        st.write(f"- **Identification:** {ip_layer.id}")
        st.write(f"- **Flags:** {ip_layer.flags}")
        st.write(f"- **Fragment Offset:** {ip_layer.frag}")
        st.write(f"- **Time to Live:** {ip_layer.ttl}")
        st.write(f"- **Protocol:** {ip_layer.proto}")
        st.write(f"- **Header Checksum:** {ip_layer.chksum}")
        st.write(f"- **Source IP:** {ip_layer.src}")
        st.write(f"- **Destination IP:** {ip_layer.dst}")
    else:
        st.write("- IP header not available")

def render_transport_header(pkt: Packet):
    st.markdown("#### Transport Layer Header")
    if TCP in pkt:
        tcp_layer = pkt[TCP]
        st.write(f"- **Source Port:** {tcp_layer.sport}")
        st.write(f"- **Destination Port:** {tcp_layer.dport}")
        st.write(f"- **Sequence Number:** {tcp_layer.seq}")
        st.write(f"- **Acknowledgment Number:** {tcp_layer.ack}")
        st.write(f"- **Data Offset:** {tcp_layer.dataofs}")
        st.write(f"- **Reserved:** {tcp_layer.reserved}")
        st.write(f"- **Flags:** {tcp_layer.flags}")
        st.write(f"- **Window:** {tcp_layer.window}")
        st.write(f"- **Checksum:** {tcp_layer.chksum}")
        st.write(f"- **Urgent Pointer:** {tcp_layer.urgptr}")
    elif UDP in pkt:
        udp_layer = pkt[UDP]
        st.write(f"- **Source Port:** {udp_layer.sport}")
        st.write(f"- **Destination Port:** {udp_layer.dport}")
        st.write(f"- **Length:** {udp_layer.len}")
        st.write(f"- **Checksum:** {udp_layer.chksum}")
    else:
        st.write("- Transport layer header not available")

def render_application_layer(pkt: Packet):
    st.markdown("#### Application Layer")
    # Show raw payload if available and not empty
    if hasattr(pkt, "payload") and pkt.payload:
        payload = pkt.payload
        # If payload has fields, show them
        if hasattr(payload, "fields") and payload.fields:
            for field_name, value in payload.fields.items():
                st.write(f"- **{field_name}:** {value}")
        else:
            # Show raw payload bytes as hex
            raw_bytes = bytes(payload)
            if raw_bytes:
                hex_str = binascii.hexlify(raw_bytes).decode("utf-8")
                formatted_hex = " ".join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))
                st.code(formatted_hex, language="plaintext")
            else:
                st.write("- No application layer data available")
    else:
        st.write("- Application layer not available")

def render_hex_view(pkt: Packet):
    st.markdown("#### Hex Dump View")
    raw_bytes = bytes(pkt)
    if raw_bytes:
        hex_str = binascii.hexlify(raw_bytes).decode("utf-8")
        formatted_hex = " ".join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))
        st.code(formatted_hex, language="plaintext")
    else:
        st.write("- No raw data available")

def display_packet_table(packets: List[Packet]):
    """
    Display a scrollable, sortable summary table of packets using Streamlit's AgGrid.
    Show detailed layer-wise breakdown below the table when a row is selected.
    """
    st.markdown("### Packet Summary Table")

    df = extract_packet_summary(packets)

    # Configure AgGrid options with dark theme and hover effects
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode="single", use_checkbox=False)
    gb.configure_grid_options(domLayout='normal')
    gb.configure_default_column(cellStyle={
        "styleConditions": [
            {
                "condition": "params.node.rowIndex % 2 == 0",
                "style": {"backgroundColor": "#1e1e1e"}
            },
            {
                "condition": "params.node.rowIndex % 2 == 1",
                "style": {"backgroundColor": "#121212"}
            }
        ]
    })
    grid_options = gb.build()

    # Display the AgGrid table with dark theme
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        height=300,
        width='100%',
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=False,
        allow_unsafe_jscode=False,
        theme="dark"
    )

    if grid_response is not None and isinstance(grid_response, dict):
        selected_rows = list(grid_response.get("selected_rows", []))
    else:
        selected_rows = []

    if selected_rows and isinstance(selected_rows[0], dict):
        selected_index = selected_rows[0].get("Index", None)
    else:
        selected_index = None

    # Get packet corresponding to selected index (Index is 1-based, list is 0-based)
    if selected_index is not None:
        pkt = packets[selected_index - 1]

        # Display packet summary info
        st.markdown("### Selected Packet Details")
        st.write(f"**Packet Number:** {selected_index}")
        st.write(f"**Timestamp:** {selected_rows[0].get('Timestamp', 'N/A')}")
        st.write(f"**Source IP:** {selected_rows[0].get('Source IP', 'N/A')}")
        st.write(f"**Destination IP:** {selected_rows[0].get('Destination IP', 'N/A')}")
        st.write(f"**Protocol:** {selected_rows[0].get('Protocol', 'N/A')}")
        st.write(f"**Length:** {selected_rows[0].get('Length', 'N/A')}")

        # Protocol Layer Cards Section with styled expandable cards
        st.markdown(
            """
            <style>
            .protocol-card {
                background-color: #1e1e1e;
                border: 1px solid #00ffff;
                border-radius: 12px;
                padding: 1rem;
                margin-bottom: 1rem;
                box-shadow: 0 0 10px #00ffff;
                transition: box-shadow 0.3s ease;
            }
            .protocol-card:hover {
                box-shadow: 0 0 20px #00ffff;
            }
            .protocol-header {
                font-weight: 700;
                color: #00ffff;
                cursor: pointer;
                user-select: none;
            }
            .protocol-content {
                margin-top: 0.5rem;
                max-height: 200px;
                overflow-y: auto;
                border-top: 1px solid #00ffff;
                padding-top: 0.5rem;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        def render_expandable_card(title, render_func):
            with st.expander(f"{title}"):
                st.markdown(f'<div class="protocol-card">', unsafe_allow_html=True)
                render_func(pkt)
                st.markdown('</div>', unsafe_allow_html=True)

        render_expandable_card("Ethernet Layer", render_ethernet_header)
        render_expandable_card("IP Layer", render_ip_header)
        render_expandable_card("UDP/TCP Layer", render_transport_header)
        render_expandable_card("Application Layer", render_application_layer)

        with st.expander("Hex Dump View"):
            render_hex_view(pkt)

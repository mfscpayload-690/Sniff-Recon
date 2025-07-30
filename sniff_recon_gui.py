import streamlit as st
import os
import json
import tempfile

from parsers.pcap_parser import parse_pcap
from parsers.csv_parser import parse_csv
from parsers.txt_parser import parse_txt

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

def save_summary(summary):
    with open("output/summary.json", "w") as f:
        json.dump(summary, f, indent=4)

def main():
    st.title("Sniff Recon - Basic GUI")

    st.markdown(
        """
        Upload a `.pcap`, `.csv`, or `.txt` file to parse and display a summary table.
        """
    )

    uploaded_file = st.file_uploader(
        "Upload a file", type=["pcap", "pcapng", "csv", "txt"]
    )

    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        file_ext = uploaded_file.name.split(".")[-1].lower()

        # Parse based on file extension
        if file_ext in ["pcap", "pcapng"]:
            summary = parse_pcap(tmp_file_path)
        elif file_ext == "csv":
            summary = parse_csv(tmp_file_path)
            # Ensure keys match expected summary keys, map if needed
            # We expect keys: src_ip, dst_ip, protocol, packet_size
            # If keys differ, try to map common variants
            mapped_summary = []
            for row in summary:
                mapped_row = {
                    "src_ip": row.get("src_ip") or row.get("Source IP") or row.get("source_ip") or row.get("src"),
                    "dst_ip": row.get("dst_ip") or row.get("Destination IP") or row.get("destination_ip") or row.get("dst"),
                    "protocol": row.get("protocol") or row.get("Protocol"),
                    "packet_size": row.get("packet_size") or row.get("Packet Size") or row.get("packet_size_bytes") or row.get("size"),
                }
                mapped_summary.append(mapped_row)
            summary = mapped_summary
        elif file_ext == "txt":
            summary = parse_txt(tmp_file_path)
        else:
            st.error("Unsupported file type.")
            return

        # Remove temp file
        os.remove(tmp_file_path)

        if not summary:
            st.warning("No data parsed from the file.")
            return

        # Display summary table
        st.subheader("Parsed Summary")
        # Convert list of dicts to list of rows with consistent keys
        table_data = []
        for item in summary:
            table_data.append([
                item.get("src_ip", ""),
                item.get("dst_ip", ""),
                item.get("protocol", ""),
                item.get("packet_size", ""),
            ])

        st.table(
            {
                "Source IP": [row[0] for row in table_data],
                "Destination IP": [row[1] for row in table_data],
                "Protocol": [row[2] for row in table_data],
                "Packet Size": [row[3] for row in table_data],
            }
        )

        # Save summary to JSON file
        save_summary(summary)
        st.success("Summary saved to output/summary.json")

        # Button to download JSON
        with open("output/summary.json", "r") as f:
            json_data = f.read()

        st.download_button(
            label="Download Summary JSON",
            data=json_data,
            file_name="summary.json",
            mime="application/json",
        )

        # Option to view JSON in browser
        if st.button("View Summary JSON"):
            st.json(json.loads(json_data))


if __name__ == "__main__":
    main()

import streamlit as st
import os
import json
import tempfile
import pandas as pd

from parsers.pcap_parser import parse_pcap
from parsers.csv_parser import parse_csv
from parsers.txt_parser import parse_txt

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        # Handle EDecimal serialization by converting to float
        if o.__class__.__name__ == "EDecimal":
            return float(o)
        return super().default(o)

def save_summary(summary):
    with open("output/summary.json", "w") as f:
        json.dump(summary, f, indent=4, cls=CustomJSONEncoder)

def inject_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

        /* Dark background and text colors */
        .main {
            background-color: #121212;
            color: #e0e0e0;
            font-family: 'Inter', sans-serif;
            padding: 1rem 2rem;
        }

        /* Title animation */
        .title-animate {
            animation: fadeInDown 1s ease forwards;
            opacity: 0;
        }

        /* Description animation */
        .desc-animate {
            animation: fadeInUp 1s ease forwards;
            opacity: 0;
            animation-delay: 0.5s;
        }

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

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

        /* Styled dropzone */
        .dropzone {
            border: 2px dashed #00ffff;
            border-radius: 12px;
            padding: 3rem;
            text-align: center;
            color: #00ffff;
            font-size: 1.25rem;
            cursor: pointer;
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 1rem;
        }

        .dropzone:hover {
            background-color: #003333;
            box-shadow: 0 0 10px #00ffff;
        }

        /* Uploaded file info */
        .file-info {
            color: #00ffff;
            font-weight: 600;
            margin-bottom: 1rem;
        }

        /* Download buttons */
        .download-btn {
            background-color: #00ffff;
            color: #121212 !important;
            border: none;
            padding: 0.5rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease, color 0.3s ease;
            margin-right: 1rem;
        }

        .download-btn:hover {
            background-color: #00b3b3;
            color: #fff !important;
        }

        /* Scrollable container for summary table */
        .summary-table-container {
            max-height: 400px;
            overflow-y: auto;
            border-radius: 12px;
            box-shadow: 0 0 10px #00ffff;
            margin-bottom: 1rem;
        }

        /* Responsive layout */
        @media (max-width: 768px) {
            .main {
                padding: 1rem;
            }
            .dropzone {
                padding: 2rem;
                font-size: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    inject_custom_css()

    st.markdown('<h1 class="title-animate">Sniff Recon - Basic GUI</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="desc-animate">Upload a <code>.pcap</code>, <code>.csv</code>, or <code>.txt</code> file to parse and display a summary table.</p>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        label="Drag and drop or browse to upload a file",
        type=["pcap", "pcapng", "csv", "txt"],
        help="Max file size: 200MB. Allowed formats: .pcap, .pcapng, .csv, .txt",
        key="fileUploader",
    )

    if uploaded_file is not None:
        # Enforce max file size 200MB
        if uploaded_file.size > 200 * 1024 * 1024:
            st.error("File size exceeds 200MB limit. Please upload a smaller file.")
            return

        # Display uploaded file name and size
        file_info = f"Uploaded file: {uploaded_file.name} ({uploaded_file.size / (1024*1024):.2f} MB)"
        st.markdown(f'<div class="file-info">{file_info}</div>', unsafe_allow_html=True)

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
            # Map keys if needed
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

        # Convert list of dicts to Pandas DataFrame
        summary = pd.DataFrame(summary)

        # Safe check for empty or None DataFrame
        if summary is None or summary.empty:
            st.warning("Summary is empty or could not be generated.")
            return

        # Display summary table using st.dataframe with scrollable container
        st.subheader("Parsed Summary")
        st.markdown('<div class="summary-table-container">', unsafe_allow_html=True)
        from display_packet_table import display_packet_table
        import scapy.all as scapy

        packets = scapy.rdpcap(tmp_file_path)
        packets_list = list(packets)
        display_packet_table(packets_list)
        st.markdown('</div>', unsafe_allow_html=True)

        # Remove temp file
        os.remove(tmp_file_path)

        # Save summary to JSON file
        save_summary(summary.to_dict(orient="records"))
        st.success("Summary saved to output/summary.json")

        # Button to download JSON
        with open("output/summary.json", "r") as f:
            json_data = f.read()

        st.download_button(
            label="Download Summary JSON",
            data=json_data,
            file_name="summary.json",
            mime="application/json",
            key="downloadJson",
            help="Download the summary JSON file"
        )

        # Option to view JSON in browser
        if st.button("View Summary JSON"):
            st.json(json.loads(json_data))


if __name__ == "__main__":
    main()

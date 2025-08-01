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
            padding: 2rem;
        }
        
        /* Title styling */
        .main-title {
            background: linear-gradient(45deg, #00ffff, #00b3b3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1rem;
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from {
                text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
            }
            to {
                text-shadow: 0 0 30px rgba(0, 255, 255, 0.8), 0 0 40px rgba(0, 255, 255, 0.6);
            }
        }
        
        .subtitle {
            color: #00b3b3;
            text-align: center;
            font-size: 1.2rem;
            margin-bottom: 2rem;
            font-weight: 400;
        }
        
        /* File uploader styling */
        .stFileUploader {
            background: rgba(30, 30, 30, 0.8);
            border-radius: 16px;
            border: 2px dashed rgba(0, 255, 255, 0.3);
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            margin: 2rem 0;
        }
        
        .stFileUploader:hover {
            border-color: rgba(0, 255, 255, 0.6);
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        }
        
        /* File info styling */
        .file-info {
            background: linear-gradient(145deg, rgba(30, 30, 30, 0.9), rgba(20, 20, 20, 0.9));
            border: 2px solid rgba(0, 255, 255, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0, 255, 255, 0.1);
            text-align: center;
        }
        
        .file-info h3 {
            color: #00ffff;
            margin-bottom: 0.5rem;
        }
        
        .file-info p {
            color: #e0e0e0;
            margin: 0.25rem 0;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(45deg, #00ffff, #00b3b3);
            color: #121212;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 255, 255, 0.4);
        }
        
        /* Success message styling */
        .success-message {
            background: linear-gradient(145deg, rgba(0, 255, 0, 0.1), rgba(0, 200, 0, 0.1));
            border: 2px solid rgba(0, 255, 0, 0.3);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
            text-align: center;
            color: #00ff00;
        }
        
        /* Error message styling */
        .error-message {
            background: linear-gradient(145deg, rgba(255, 0, 0, 0.1), rgba(200, 0, 0, 0.1));
            border: 2px solid rgba(255, 0, 0, 0.3);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
            text-align: center;
            color: #ff6666;
        }
        
        /* Warning message styling */
        .warning-message {
            background: linear-gradient(145deg, rgba(255, 255, 0, 0.1), rgba(200, 200, 0, 0.1));
            border: 2px solid rgba(255, 255, 0, 0.3);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
            text-align: center;
            color: #ffff66;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main {
                padding: 1rem;
            }
            
            .main-title {
                font-size: 2rem;
            }
            
            .subtitle {
                font-size: 1rem;
            }
            
            .stFileUploader {
                padding: 1rem;
            }
        }
        
        /* Animation for page load */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .fade-in-up {
            animation: fadeInUp 0.8s ease forwards;
        }
        
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    # Inject modern CSS
    inject_modern_css()

    # Main title with animation
    st.markdown(
        '<h1 class="main-title fade-in-up">🔍 Sniff Recon</h1>',
        unsafe_allow_html=True
    )
    
    st.markdown(
        '<p class="subtitle fade-in-up">Advanced Network Packet Analyzer & Protocol Dissector</p>',
        unsafe_allow_html=True
    )

    # File upload section
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        label="📁 Upload Packet Capture File",
        type=["pcap", "pcapng", "csv", "txt"],
        help="Supported formats: .pcap, .pcapng, .csv, .txt (Max: 200MB)",
        key="fileUploader",
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        # File size validation
        if uploaded_file.size > 200 * 1024 * 1024:
            st.markdown(
                '<div class="error-message">❌ File size exceeds 200MB limit. Please upload a smaller file.</div>',
                unsafe_allow_html=True
            )
            return

        # Display file information
        file_size_mb = uploaded_file.size / (1024*1024)
        st.markdown(
            f"""
            <div class="file-info">
                <h3>📄 File Uploaded Successfully</h3>
                <p><strong>Name:</strong> {uploaded_file.name}</p>
                <p><strong>Size:</strong> {file_size_mb:.2f} MB</p>
                <p><strong>Type:</strong> {uploaded_file.type or 'Unknown'}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        file_ext = uploaded_file.name.split(".")[-1].lower()

        # Parse based on file extension
        try:
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
                st.markdown(
                    '<div class="error-message">❌ Unsupported file type.</div>',
                    unsafe_allow_html=True
                )
                return

            # Convert to DataFrame
            summary = pd.DataFrame(summary)

            # Check for empty DataFrame
            if summary is None or summary.empty:
                st.markdown(
                    '<div class="warning-message">⚠️ Summary is empty or could not be generated.</div>',
                    unsafe_allow_html=True
                )
                return

            # Display packet analysis
            st.markdown("## 📊 Packet Analysis Results")
            
            # Import and display packet table
            from display_packet_table import display_packet_table
            import scapy.all as scapy

            try:
                packets = scapy.rdpcap(tmp_file_path)
                packets_list = list(packets)
                display_packet_table(packets_list)
            except Exception as e:
                st.markdown(
                    f'<div class="error-message">❌ Error reading packet file: {str(e)}</div>',
                    unsafe_allow_html=True
                )

            # Save summary to JSON
            save_summary(summary.to_dict(orient="records"))
            
            st.markdown(
                '<div class="success-message">✅ Analysis complete! Summary saved to output/summary.json</div>',
                unsafe_allow_html=True
            )

            # Download section
            st.markdown("## 💾 Download Results")
            
            # Button to download JSON
            with open("output/summary.json", "r") as f:
                json_data = f.read()

            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label="📥 Download Summary JSON",
                    data=json_data,
                    file_name="sniff_recon_summary.json",
                    mime="application/json",
                    key="downloadJson",
                    help="Download the complete analysis summary"
                )

            with col2:
                if st.button("👁️ View Raw JSON"):
                    st.json(json.loads(json_data))

        except Exception as e:
            st.markdown(
                f'<div class="error-message">❌ Error processing file: {str(e)}</div>',
                unsafe_allow_html=True
            )
        finally:
            # Clean up temp file
            try:
                os.remove(tmp_file_path)
            except:
                pass

if __name__ == "__main__":
    main()

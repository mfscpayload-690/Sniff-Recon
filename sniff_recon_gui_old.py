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
        /* Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@600;700;800&family=Rajdhani:wght@600;700&family=Exo+2:wght@700;800&display=swap');
        
        /* Global styles */
        .main {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #e0e0e0;
            padding: 2rem;
        }
        
        /* Title styling */
        .main-title {
            font-family: 'Orbitron','Rajdhani','Exo 2','Inter',sans-serif;
            letter-spacing: 2px;
            color: #00e6ff;
            text-shadow: 0 0 8px rgba(0, 238, 255, 0.7), 0 0 18px rgba(0, 238, 255, 0.4);
            font-size: 3rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.25rem;
            animation: neonPulse 2.4s ease-in-out infinite;
            text-transform: uppercase;
        }
        
        @keyframes neonPulse {
            0% { text-shadow: 0 0 8px rgba(0, 238, 255, 0.6), 0 0 18px rgba(0, 238, 255, 0.35); }
            50% { text-shadow: 0 0 14px rgba(0, 255, 255, 0.85), 0 0 28px rgba(0, 255, 255, 0.55); }
            100% { text-shadow: 0 0 8px rgba(0, 238, 255, 0.6), 0 0 18px rgba(0, 238, 255, 0.35); }
        }
        
        .subtitle {
            color: #66ffff;
            text-align: center;
            font-size: 1.15rem;
            margin-bottom: 2rem;
            font-weight: 500;
            text-shadow: 0 0 6px rgba(102, 255, 255, 0.35);
        }

        /* Typewriter */
        .typewriter {
            display: inline-block;
            white-space: nowrap;
            overflow: hidden;
            border-right: 0.12em solid rgba(102,255,255,0.65);
            animation: caret 0.9s step-end infinite;
        }
        .typewriter .cursor { color: #66ffff; animation: blink 1.1s steps(2, start) infinite; }
        @keyframes blink { to { visibility: hidden; } }
        @keyframes caret { 50% { border-color: transparent; } }
        
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
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(30, 30, 30, 0.8);
            border-radius: 12px;
            padding: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(15, 15, 15, 0.5);
            border-radius: 8px;
            color: #e0e0e0;
            border: 1px solid rgba(0, 255, 255, 0.2);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(45deg, #00ffff, #00b3b3);
            color: #121212;
            font-weight: 600;
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

        /* Modal (popup) styles */
        .sr-modal-overlay {
            position: fixed; inset: 0; background: rgba(0,0,0,0.55);
            display: flex; align-items: center; justify-content: center;
            z-index: 9999;
        }
        .sr-modal {
            width: min(720px, 92vw);
            background: linear-gradient(145deg, rgba(18, 18, 30, 0.95), rgba(10, 10, 20, 0.95));
            border: 1px solid rgba(0,255,255,0.25);
            box-shadow: 0 12px 40px rgba(0,255,255,0.15), inset 0 0 18px rgba(0,255,255,0.06);
            border-radius: 14px; padding: 1.25rem 1.25rem 1rem;
            color: #e0f7ff;
        }
        .sr-modal h3 { color: #00ffff; margin: 0 0 0.8rem 0; font-family: 'Exo 2','Inter',sans-serif; }
        .sr-modal .sr-body { 
            margin: 0.5rem 0; 
            color: #e0f7ff; 
            line-height: 1.6;
            font-size: 0.98rem;
        }
        .sr-modal .sr-close {
            margin-top: 1rem;
        }

        /* Sidebar simple buttons */
        .stSidebar .stButton > button {
            width: 100%;
            background: linear-gradient(45deg, #00ffff, #00b3b3);
            color: #121212; border: none; border-radius: 8px;
            padding: 0.65rem 0.8rem; font-weight: 600; font-size: 0.95rem;
            box-shadow: 0 4px 15px rgba(0, 255, 255, 0.28);
            margin-bottom: 0.75rem;
            transition: all 0.3s ease;
        }
        .stSidebar .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 255, 255, 0.4);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    # Set page config to prevent JavaScript errors
    st.set_page_config(
        page_title="Sniff Recon - Network Packet Analyzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject modern CSS
    inject_modern_css()

    # Sidebar: About, Contact, Help Desk (left side)
    with st.sidebar:
        st.markdown('<div class="sr-card"><h4>About</h4>', unsafe_allow_html=True)
        if st.button("About Sniff Recon", key="aboutBtn"):
            st.session_state["sr_modal"] = {"type": "about"}
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sr-card"><h4>Contact Us</h4>', unsafe_allow_html=True)
        if st.button("Contact Team", key="contactBtn"):
            st.session_state["sr_modal"] = {"type": "contact"}
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sr-card"><h4>Help Desk</h4>', unsafe_allow_html=True)
        faq_items = [
            ("Why use Sniff Recon?", "Sniff Recon quickly parses packet captures and highlights patterns, anomalies, and potential threats with AI-assisted summaries."),
            ("Supported files?", "PCAP, PCAPNG, CSV, and TXT are supported. CSV column names are auto-mapped when possible."),
            ("Is AI required?", "No. When AI providers aren’t configured, the app still provides local statistical analysis and summaries."),
            ("File size limit?", "The UI limits uploads to 200MB to protect memory. Large captures should be trimmed or filtered before upload."),
            ("Is my data stored?", "Summaries are saved to output/summary.json locally. Packet data is processed in-memory and temp files are cleaned up.")
        ]
        for idx, (q, _a) in enumerate(faq_items):
            if st.button(q, key=f"faqBtn{idx}"):
                st.session_state["sr_modal"] = {"type": "faq", "index": idx}
        st.markdown('</div>', unsafe_allow_html=True)

    # Main title with neon glow (keep logo/title feel and spacing)
    st.markdown(
        '<h1 class="main-title fade-in-up">SNIFF RECON</h1>',
        unsafe_allow_html=True
    )

    # Tagline: one-time typewriter; then steady with blinking cursor
    tagline_text = "Advanced Network Packet Analyzer & AI-Powered Protocol Dissector"
    if not st.session_state.get("sr_tagline_done"):
        st.markdown(
            f'''
            <p class="subtitle fade-in-up">
              <span id="sr-typewriter" class="typewriter"></span><span class="cursor">_</span>
            </p>
            <script>
              const txt = {json.dumps(tagline_text)};
              const el = window.parent.document.getElementById('sr-typewriter');
              if (el) {{
                  let i=0; const speed=28;
                  const type = () => {{
                      if (i <= txt.length) {{ el.textContent = txt.substring(0,i); i++; setTimeout(type, speed); }}
                  }}; type();
              }}
            </script>
            ''',
            unsafe_allow_html=True,
        )
        # Mark as done to avoid re-animating on further reruns
        st.session_state["sr_tagline_done"] = True
    else:
        st.markdown(
            f'<p class="subtitle fade-in-up">{tagline_text} <span class="cursor">_</span></p>',
            unsafe_allow_html=True,
        )

    # Optional modal renderer (centered popup)
    modal = st.session_state.get("sr_modal")
    if modal:
        # Build modal content
        title = ""
        body = ""
        if modal.get("type") == "about":
            title = "About Sniff Recon"
            body = (
                "Sniff Recon is a Streamlit-based network packet analyzer that supports PCAP/CSV/TXT parsing, "
                "with optional multi-provider AI analysis. It emphasizes safe defaults, memory-aware parsing, and "
                "clear visualizations to help you investigate traffic quickly."
            )
        elif modal.get("type") == "contact":
            title = "Contact Us"
            body = (
                "For support or inquiries, please open an issue on the repository or email the maintainers. "
                "Remember to exclude sensitive data when sharing captures."
            )
        elif modal.get("type") == "faq":
            idx = int(modal.get("index", 0))
            q, a = faq_items[idx]
            title = q
            body = a

        # Render overlay
        st.markdown('<div class="sr-modal-overlay">', unsafe_allow_html=True)
        st.markdown('<div class="sr-modal">', unsafe_allow_html=True)
        st.markdown(f'<h3>{title}</h3><p>{body}</p>', unsafe_allow_html=True)
        close_col = st.columns([1,1,1])[1]
        with close_col:
            if st.button("Close", key="srCloseModal", help="Close this dialog"):
                st.session_state["sr_modal"] = None
        st.markdown('</div></div>', unsafe_allow_html=True)

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
            if summary is None or len(summary) == 0:
                st.markdown(
                    '<div class="warning-message">⚠️ Summary is empty or could not be generated.</div>',
                    unsafe_allow_html=True
                )
                return

            # Create tabs for different analysis views
            tab1, tab2, tab3 = st.tabs(["📊 Packet Analysis", "🤖 AI Analysis", "💾 Export Results"])
            
            with tab1:
                # Display packet analysis
                st.markdown("## 📊 Packet Analysis Results")
                
# Import and display packet table
                from display_packet_table import display_packet_table
                import scapy.all as scapy

                try:
                    packets = scapy.PcapReader(tmp_file_path)
                    packets_list = []
                    total_bytes = os.path.getsize(tmp_file_path)
                    bytes_read = 0
                    progress_text = "Loading and parsing packets..."
                    progress_bar = st.progress(0, text=progress_text)
                    last_update_fraction = 0

                    for pkt in packets:
                        packets_list.append(pkt)
                        pos = packets._current_packet if hasattr(packets, '_current_packet') else len(packets_list)
                        # Estimate progress (fallback to number of packets)
                        fraction = min(1.0, (packets._file.tell() / total_bytes)) if hasattr(packets, '_file') else min(1.0, pos/10000)
                        # Avoid excessive redraws
                        if fraction - last_update_fraction > 0.01 or fraction == 1.0:
                            progress_bar.progress(fraction, text=progress_text)
                            last_update_fraction = fraction
                    progress_bar.empty()
                    packets.close()
                    display_packet_table(packets_list)
                except Exception as e:
                    st.markdown(
                        f'<div class="error-message">❌ Error reading packet file: {str(e)}</div>',
                        unsafe_allow_html=True
                    )
            
            with tab2:
                # AI Analysis tab
                try:
                    from ai_query_interface import render_ai_query_interface, render_ai_quick_analysis
                    import scapy.all as scapy
                    
                    packets = scapy.rdpcap(tmp_file_path)
                    packets_list = list(packets)
                    
                    # Quick AI analysis
                    render_ai_quick_analysis(packets_list)
                    
                    # AI Query interface
                    render_ai_query_interface(packets_list)
                    
                except Exception as e:
                    st.markdown(
                        f'<div class="error-message">❌ Error initializing AI analysis: {str(e)}</div>',
                        unsafe_allow_html=True
                    )
            
            with tab3:
                # Export Results tab
                st.markdown("## 💾 Export Analysis Results")
                
                # Save summary to JSON
                save_summary(summary.to_dict(orient="records"))
                
                st.markdown(
                    '<div class="success-message">✅ Analysis complete! Summary saved to output/summary.json</div>',
                    unsafe_allow_html=True
                )

                # Download section
                col1, col2 = st.columns(2)
                
                # Button to download JSON
                with open("output/summary.json", "r") as f:
                    json_data = f.read()

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

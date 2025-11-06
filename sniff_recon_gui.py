import streamlit as st
import os
import os
import json
import tempfile
import pandas as pd
import streamlit as st

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
    st.markdown(
        """
        <style>
        /* Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@600;700;800&display=swap');

        /* Global styles */
        .main {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #e0e0e0;
            padding: 2rem;
        }

        /* Title styling */
        .main-title {
            font-family: 'Orbitron','Inter',sans-serif;
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
        .typewriter { display: inline-block; white-space: nowrap; overflow: hidden; border-right: 0.12em solid rgba(102,255,255,0.65); animation: caret 0.9s step-end infinite; }
        .typewriter .cursor { color: #66ffff; animation: blink 1.1s steps(2, start) infinite; }
        @keyframes blink { to { visibility: hidden; } }
        @keyframes caret { 50% { border-color: transparent; } }

        /* File uploader */
        .stFileUploader {
            background: rgba(30, 30, 30, 0.8);
            border-radius: 16px;
            border: 2px dashed rgba(0, 255, 255, 0.3);
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            margin: 2rem 0;
        }
        .stFileUploader:hover { border-color: rgba(0, 255, 255, 0.6); box-shadow: 0 0 20px rgba(0, 255, 255, 0.2); }

        /* File info */
        .file-info { background: linear-gradient(145deg, rgba(30, 30, 30, 0.9), rgba(20, 20, 20, 0.9)); border: 2px solid rgba(0, 255, 255, 0.3); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 4px 20px rgba(0, 255, 255, 0.1); text-align: center; }
        .file-info h3 { color: #00ffff; margin-bottom: 0.5rem; }
        .file-info p { color: #e0e0e0; margin: 0.25rem 0; }

        /* Messages */
        .success-message { background: linear-gradient(145deg, rgba(0,255,0,0.1), rgba(0,200,0,0.1)); border: 2px solid rgba(0,255,0,0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0; text-align: center; color: #00ff00; }
        .error-message { background: linear-gradient(145deg, rgba(255,0,0,0.1), rgba(200,0,0,0.1)); border: 2px solid rgba(255,0,0,0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0; text-align: center; color: #ff6666; }
        .warning-message { background: linear-gradient(145deg, rgba(255,255,0,0.1), rgba(200,200,0,0.1)); border: 2px solid rgba(255,255,0,0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0; text-align: center; color: #ffff66; }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; background: rgba(30,30,30,0.8); border-radius: 12px; padding: 8px; }
        .stTabs [data-baseweb="tab"] { background: rgba(15,15,15,0.5); border-radius: 8px; color: #e0e0e0; border: 1px solid rgba(0,255,255,0.2); }
        .stTabs [aria-selected="true"] { background: linear-gradient(45deg, #00ffff, #00b3b3); color: #121212; font-weight: 600; }

        /* Modal */
        .sr-modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center; z-index: 9999; }
        .sr-modal { width: min(640px, 90vw); background: linear-gradient(145deg, rgba(18,18,30,0.98), rgba(10,10,20,0.98)); border: 2px solid rgba(0,255,255,0.35); box-shadow: 0 0 40px rgba(0,255,255,0.25), inset 0 0 20px rgba(0,255,255,0.08); border-radius: 16px; padding: 1.25rem 1.25rem 1rem; color: #e8f8ff; }
        .sr-modal h3 { color: #00ffff; margin: 0 0 0.6rem 0; font-family: 'Inter',sans-serif; text-shadow: 0 0 8px rgba(0,255,255,0.5); }
        .sr-modal-body { margin: 0.75rem 0; min-height: 60px; line-height: 1.6; font-size: 1.05rem; }

        /* Animations */
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px);} to { opacity: 1; transform: translateY(0);} }
        .fade-in-up { animation: fadeInUp 0.8s ease forwards; }

        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    # Set page config
    st.set_page_config(
        page_title="Sniff Recon - Network Packet Analyzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_modern_css()

    # Sidebar: About and Help only
    with st.sidebar:
        st.markdown('<h3 style="color:#00ffff; margin-bottom:1rem; font-family: Orbitron,sans-serif;">Quick Access</h3>', unsafe_allow_html=True)
        if st.button("📖 About", key="aboutBtn", use_container_width=True):
            st.session_state["sr_modal"] = {"type": "about"}
            st.rerun()
        if st.button("❓ Help Desk", key="helpBtn", use_container_width=True):
            st.session_state["sr_modal"] = {"type": "help"}
            st.rerun()

    # Title
    st.markdown('<h1 class="main-title fade-in-up">🔍 Sniff Recon</h1>', unsafe_allow_html=True)

    # Tagline with one-time typewriter
    tagline_text = "Advanced Network Packet Analyzer & AI-Powered Protocol Dissector"
    if not st.session_state.get("sr_tagline_done"):
        tagline_html = """
            <p class="subtitle fade-in-up"><span id="sr-typewriter" class="typewriter"></span><span class="cursor">_</span></p>
            <script>
                const txt = %%TAGLINE_JSON%%;
                const el = window.parent.document.getElementById('sr-typewriter');
                if (el) { let i=0; const speed=28; const type = () => { if (i <= txt.length) { el.textContent = txt.substring(0,i); i++; setTimeout(type, speed); } }; type(); }
            </script>
        """
        st.markdown(tagline_html.replace("%%TAGLINE_JSON%%", json.dumps(tagline_text)), unsafe_allow_html=True)
        st.session_state["sr_tagline_done"] = True
    else:
        st.markdown(f'<p class="subtitle fade-in-up">{tagline_text} <span class="cursor">_</span></p>', unsafe_allow_html=True)

    # Modal renderer
    modal = st.session_state.get("sr_modal")
    if modal:
        modal_type = modal.get("type")
        title = "About Sniff Recon" if modal_type == "about" else "Help Desk"
        if modal_type == "about":
            body = (
                "Sniff Recon is a Streamlit-based network packet analyzer that supports PCAP, PCAPNG, CSV, and TXT files. "
                "It includes optional multi-provider AI analysis, memory-aware parsing, and clear visualizations to help you investigate network traffic quickly and safely."
            )
        else:
            body = (
                "🔹 Why use Sniff Recon? Quickly parse captures and highlight patterns, anomalies, and potential threats with AI-assisted summaries.\\n\\n"
                "🔹 Supported files: PCAP, PCAPNG, CSV, TXT. CSV column names are auto-mapped when possible.\\n\\n"
                "🔹 Is AI required? No—local statistical analysis works without any API keys.\\n\\n"
                "🔹 File size limit: 200MB to protect memory. Prefer trimming/filtering large captures.\\n\\n"
                "🔹 Data handling: Summaries saved to output/summary.json. Packet data processed via temp files and cleaned up."
            )

        # Overlay + modal shell
        st.markdown('<div class="sr-modal-overlay"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sr-modal">', unsafe_allow_html=True)
        st.markdown(f'<h3>{title}</h3>', unsafe_allow_html=True)

        modal_id = f"sr-modal-{modal_type}"
        if not st.session_state.get(f"{modal_id}_typed"):
            modal_html_template = """
                <div class="sr-modal-body" id="%%ID%%"></div>
                <script>
                  (function() {
                      const txt = %%BODY%%;
                      const el = window.parent.document.getElementById('%%ID%%');
                      if (el && el.textContent === '') {
                          let i = 0; const speed = 12;
                          const type = () => { if (i < txt.length) { el.textContent += txt.charAt(i); i++; setTimeout(type, speed); } };
                          type();
                      }
                  })();
                </script>
            """
            modal_html = (
                modal_html_template
                .replace("%%ID%%", modal_id)
                .replace("%%BODY%%", json.dumps(body))
            )
            st.markdown(modal_html, unsafe_allow_html=True)
            st.session_state[f"{modal_id}_typed"] = True
        else:
            st.markdown(f'<div class="sr-modal-body">{body.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button("✖ Close", key="srCloseModal", help="Close this popup"):
                st.session_state["sr_modal"] = None
                st.session_state[f"{modal_id}_typed"] = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # File uploader
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="📁 Upload Packet Capture File",
        type=["pcap", "pcapng", "csv", "txt"],
        help="Supported formats: .pcap, .pcapng, .csv, .txt (Max: 200MB)",
        key="fileUploader",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        # Size guard
        if uploaded_file.size > 200 * 1024 * 1024:
            st.markdown('<div class="error-message">❌ File size exceeds 200MB limit. Please upload a smaller file.</div>', unsafe_allow_html=True)
            return

        # File info
        file_size_mb = uploaded_file.size / (1024 * 1024)
        st.markdown(
            f"""
            <div class=\"file-info\">
                <h3>📄 File Uploaded Successfully</h3>
                <p><strong>Name:</strong> {uploaded_file.name}</p>
                <p><strong>Size:</strong> {file_size_mb:.2f} MB</p>
                <p><strong>Type:</strong> {uploaded_file.type or 'Unknown'}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        file_ext = uploaded_file.name.split(".")[-1].lower()

        try:
            # Parse by type
            if file_ext in ["pcap", "pcapng"]:
                summary = parse_pcap(tmp_file_path)
            elif file_ext == "csv":
                parsed = parse_csv(tmp_file_path)
                mapped = []
                for row in parsed:
                    mapped.append({
                        "src_ip": row.get("src_ip") or row.get("Source IP") or row.get("source_ip") or row.get("src"),
                        "dst_ip": row.get("dst_ip") or row.get("Destination IP") or row.get("destination_ip") or row.get("dst"),
                        "protocol": row.get("protocol") or row.get("Protocol"),
                        "packet_size": row.get("packet_size") or row.get("Packet Size") or row.get("packet_size_bytes") or row.get("size"),
                    })
                summary = mapped
            elif file_ext == "txt":
                summary = parse_txt(tmp_file_path)
            else:
                st.markdown('<div class="error-message">❌ Unsupported file type.</div>', unsafe_allow_html=True)
                return

            # Normalize to DataFrame
            summary = pd.DataFrame(summary)
            if summary is None or len(summary) == 0:
                st.markdown('<div class="warning-message">⚠️ Summary is empty or could not be generated.</div>', unsafe_allow_html=True)
                return

            # Tabs
            tab1, tab2, tab3 = st.tabs(["📊 Packet Analysis", "🤖 AI Analysis", "💾 Export Results"])

            # Tab 1: Packet analysis
            with tab1:
                st.markdown("## 📊 Packet Analysis Results")
                from display_packet_table import display_packet_table
                import scapy.all as scapy
                try:
                    packets = scapy.PcapReader(tmp_file_path)
                    packets_list = []
                    total_bytes = os.path.getsize(tmp_file_path)
                    progress_text = "Loading and parsing packets..."
                    progress_bar = st.progress(0, text=progress_text)
                    last_fraction = 0
                    for pkt in packets:
                        packets_list.append(pkt)
                        if hasattr(packets, '_file'):
                            fraction = min(1.0, packets._file.tell() / max(total_bytes, 1))
                        else:
                            # Fallback: approximate by count
                            fraction = min(1.0, len(packets_list) / 10000)
                        if fraction - last_fraction > 0.01 or fraction >= 1.0:
                            progress_bar.progress(fraction, text=progress_text)
                            last_fraction = fraction
                    progress_bar.empty()
                    packets.close()
                    display_packet_table(packets_list)
                except Exception as e:
                    st.markdown(f'<div class=\"error-message\">❌ Error reading packet file: {str(e)}</div>', unsafe_allow_html=True)

            # Tab 2: AI analysis
            with tab2:
                try:
                    from ai_query_interface import render_ai_query_interface, render_ai_quick_analysis
                    import scapy.all as scapy
                    packets = scapy.rdpcap(tmp_file_path)
                    packets_list = list(packets)
                    render_ai_quick_analysis(packets_list)
                    render_ai_query_interface(packets_list)
                except Exception as e:
                    st.markdown(f'<div class=\"error-message\">❌ Error initializing AI analysis: {str(e)}</div>', unsafe_allow_html=True)

            # Tab 3: Export
            with tab3:
                st.markdown("## 💾 Export Analysis Results")
                save_summary(summary.to_dict(orient="records"))
                st.markdown('<div class=\"success-message\">✅ Analysis complete! Summary saved to output/summary.json</div>', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with open("output/summary.json", "r") as f:
                    json_data = f.read()
                with col1:
                    st.download_button(
                        label="📥 Download Summary JSON",
                        data=json_data,
                        file_name="sniff_recon_summary.json",
                        mime="application/json",
                        key="downloadJson",
                        help="Download the complete analysis summary",
                    )
                with col2:
                    if st.button("👁️ View Raw JSON"):
                        st.json(json.loads(json_data))
        except Exception as e:
            st.markdown(f'<div class=\"error-message\">❌ Error processing file: {str(e)}</div>', unsafe_allow_html=True)
        finally:
            try:
                os.remove(tmp_file_path)
            except Exception:
                pass


if __name__ == "__main__":
    main()


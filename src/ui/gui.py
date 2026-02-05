"""
Sniff-Recon GUI Module
======================
Main Streamlit interface for the network packet analyzer.
Clean, modular implementation using external CSS design system.
"""

import streamlit as st
import os
import sys
import json
import tempfile
import pandas as pd
from pathlib import Path
from dataclasses import asdict, is_dataclass
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.parsers.pcap_parser import parse_pcap
from src.parsers.csv_parser import parse_csv
from src.parsers.txt_parser import parse_txt
from src.ui.icons import icon, ICONS

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Load environment variables
load_dotenv()
load_dotenv('/app/.env', override=False)  # Docker path


class CustomJSONEncoder(json.JSONEncoder):
    """Handle special types for JSON serialization."""
    def default(self, o):
        if o.__class__.__name__ == "EDecimal":
            return float(o)
        if is_dataclass(o) and not isinstance(o, type):
            return asdict(o)
        return super().default(o)


def save_summary(summary: dict) -> None:
    """Save analysis summary to JSON file."""
    with open("output/summary.json", "w") as f:
        json.dump(summary, f, indent=4, cls=CustomJSONEncoder)


def load_css() -> str:
    """Load CSS from external file."""
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        return css_path.read_text()
    return ""


def get_favicon_path() -> str:
    """Get the path to the favicon file."""
    # Try different possible paths
    possible_paths = [
        Path(__file__).parent.parent.parent / "assets" / "favicon" / "favicon.ico",
        Path("/app/assets/favicon/favicon.ico"),  # Docker path
        Path("assets/favicon/favicon.ico"),
    ]
    for path in possible_paths:
        if path.exists():
            return str(path)
    return "🔍"  # Fallback to emoji


def get_logo_path() -> str:
    """Get the path to the logo file."""
    possible_paths = [
        Path(__file__).parent.parent.parent / "assets" / "favicon" / "sniff-recon-logo.png",
        Path("/app/assets/favicon/sniff-recon-logo.png"),  # Docker path
        Path("assets/favicon/sniff-recon-logo.png"),
    ]
    for path in possible_paths:
        if path.exists():
            return str(path)
    return None


def check_ollama_status() -> tuple[bool, str]:
    """Check if Ollama is available and return status."""
    import urllib.request
    import urllib.error
    
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    try:
        response = urllib.request.urlopen(f"{ollama_url}/api/tags", timeout=2)
        if response.status == 200:
            return True, os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
    except Exception:
        pass
    return False, ""


def render_header() -> None:
    """Render the application header with logo and status indicators."""
    ollama_online, model_name = check_ollama_status()
    logo_path = get_logo_path()
    
    # Build logo HTML
    if logo_path:
        import base64
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="sr-logo-img" alt="Sniff-Recon">'
    else:
        search_icon = icon("search", "lg")
        logo_html = search_icon
    
    st.markdown(f"""
        <div class="sr-header">
            <div class="sr-logo">
                {logo_html}
                <div>
                    <div class="sr-logo-text">SNIFF-RECON</div>
                    <div class="sr-logo-tagline">AI-Powered Network Packet Analyzer</div>
                </div>
            </div>
            <div class="sr-status-group">
    """, unsafe_allow_html=True)
    
    bot_icon = icon("bot")
    if ollama_online:
        st.markdown(f"""
                <div class="sr-status-badge sr-status-online">
                    <span class="sr-status-dot"></span>
                    Ollama Online
                </div>
                <div class="sr-provider-badge">
                    {bot_icon} {model_name}
                </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
                <div class="sr-status-badge sr-status-offline">
                    <span class="sr-status-dot"></span>
                    Ollama Offline
                </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_upload_zone() -> object:
    """Render the file upload zone with styling."""
    upload_icon = icon("upload", "lg")
    st.markdown(f"""
        <div class="sr-section">
            <div class="sr-section-title">
                {upload_icon} Upload Packet Capture
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        label="Drop your file here or click to browse",
        type=["pcap", "pcapng", "csv", "txt"],
        help="Supported: PCAP, PCAPNG, CSV, TXT (max 200MB)",
        key="main_file_uploader"
    )
    
    if uploaded_file is None:
        st.markdown("""
            <div style="text-align: center; padding: 1rem; color: var(--text-muted);">
                <div style="margin-bottom: 0.5rem;">Supported formats:</div>
                <div style="display: flex; justify-content: center; gap: 0.5rem;">
                    <span class="sr-format-tag">PCAP</span>
                    <span class="sr-format-tag">PCAPNG</span>
                    <span class="sr-format-tag">CSV</span>
                    <span class="sr-format-tag">TXT</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    return uploaded_file


def render_file_info(uploaded_file) -> None:
    """Display information about the uploaded file."""
    file_size_mb = uploaded_file.size / (1024 * 1024)
    
    file_icon = icon("file-text", "2xl")
    st.markdown(f"""
        <div class="sr-card-glow" style="margin: 1rem 0;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 2rem; color: var(--accent-cyan);">{file_icon}</div>
                <div>
                    <div style="font-weight: 600; color: var(--accent-cyan);">{uploaded_file.name}</div>
                    <div style="color: var(--text-secondary); font-size: 0.875rem;">
                        {file_size_mb:.2f} MB • {uploaded_file.type or 'Unknown type'}
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_stats_cards(df: pd.DataFrame) -> None:
    """Render statistics cards from parsed data."""
    total_packets = len(df)
    
    # Count protocols
    protocols = df.get('protocol', pd.Series()).value_counts()
    top_protocol = protocols.index[0] if len(protocols) > 0 else "N/A"
    
    # Count unique IPs
    src_ips = df.get('src_ip', pd.Series()).nunique()
    dst_ips = df.get('dst_ip', pd.Series()).nunique()
    unique_ips = src_ips + dst_ips
    
    col1, col2, col3, col4 = st.columns(4)
    
    bar_icon = icon("bar-chart", "xl")
    layers_icon = icon("layers", "xl")
    globe_icon = icon("globe", "xl")
    zap_icon = icon("zap", "xl")
    
    with col1:
        st.markdown(f"""
            <div class="sr-stat-card">
                <div class="sr-stat-icon">{bar_icon}</div>
                <div class="sr-stat-content">
                    <div class="sr-stat-value">{total_packets:,}</div>
                    <div class="sr-stat-label">Total Packets</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="sr-stat-card">
                <div class="sr-stat-icon">{layers_icon}</div>
                <div class="sr-stat-content">
                    <div class="sr-stat-value">{len(protocols)}</div>
                    <div class="sr-stat-label">Protocols</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="sr-stat-card">
                <div class="sr-stat-icon">{globe_icon}</div>
                <div class="sr-stat-content">
                    <div class="sr-stat-value">{unique_ips}</div>
                    <div class="sr-stat-label">Unique IPs</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="sr-stat-card">
                <div class="sr-stat-icon">{zap_icon}</div>
                <div class="sr-stat-content">
                    <div class="sr-stat-value">{top_protocol}</div>
                    <div class="sr-stat-label">Top Protocol</div>
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_landing_page() -> None:
    """Render the landing page content when no file is uploaded."""
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <div style="font-size: 1.25rem; color: var(--text-secondary); margin-bottom: 2rem;">
                Upload a packet capture file to begin analysis
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature icons
    activity_icon = icon("activity", "2xl")
    brain_icon = icon("brain", "2xl")
    shield_icon = icon("shield-check", "2xl")
    
    # Quick features overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="sr-card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; color: var(--accent-cyan);">{activity_icon}</div>
                <div style="font-weight: 600; color: var(--accent-cyan); margin-bottom: 0.5rem;">
                    Packet Analysis
                </div>
                <div style="color: var(--text-secondary); font-size: 0.875rem;">
                    Deep inspection of network packets with protocol dissection
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="sr-card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; color: var(--accent-purple);">{brain_icon}</div>
                <div style="font-weight: 600; color: var(--accent-purple); margin-bottom: 0.5rem;">
                    AI-Powered Insights
                </div>
                <div style="color: var(--text-secondary); font-size: 0.875rem;">
                    Ask questions about your traffic in natural language
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="sr-card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; color: var(--accent-green);">{shield_icon}</div>
                <div style="font-weight: 600; color: var(--accent-green); margin-bottom: 0.5rem;">
                    Privacy-First
                </div>
                <div style="color: var(--text-secondary); font-size: 0.875rem;">
                    100% local analysis with offline AI (Ollama)
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Help section
    rocket_icon = icon("rocket", "lg")
    st.markdown(f"""
        <div style="margin-top: 3rem;">
            <div class="sr-section-title">{rocket_icon} Quick Start</div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("How to use Sniff-Recon", expanded=False):
        st.markdown("""
            **Step 1:** Upload a packet capture file (PCAP, PCAPNG, CSV, or TXT)
            
            **Step 2:** Explore the **Packet Analysis** tab to view detailed packet information
            
            **Step 3:** Use the **AI Analysis** tab to ask questions about your traffic
            
            **Step 4:** Export your findings using the **Export** tab
        """)
    
    with st.expander("Supported File Formats", expanded=False):
        st.markdown("""
            - **PCAP/PCAPNG**: Standard packet capture format from Wireshark, tcpdump, etc.
            - **CSV**: Comma-separated values with packet data
            - **TXT**: Text-based packet exports
            
            *Maximum file size: 200MB*
        """)


def render_footer() -> None:
    """Render the application footer."""
    github_icon = icon("github")
    coffee_icon = icon("coffee")
    heart_icon = icon("heart")
    st.markdown(f"""
        <div class="sr-footer">
            <div class="sr-footer-left">
                <span class="sr-footer-version">Sniff-Recon v1.2.0</span>
                <div class="sr-footer-links">
                    <a href="https://github.com/mfscpayload-690/Sniff-Recon" target="_blank" class="sr-footer-link">
                        {github_icon} GitHub
                    </a>
                    <a href="https://github.com/mfscpayload-690/Sniff-Recon/issues" target="_blank" class="sr-footer-link">
                        Report Issue
                    </a>
                    <a href="https://buymeacoffee.com/mfscpayload690" target="_blank" class="sr-footer-link sr-coffee-link">
                        {coffee_icon} Buy Me a Coffee
                    </a>
                </div>
            </div>
            <div class="sr-footer-right">
                <span style="color: var(--text-muted); font-size: 0.875rem;">
                    Made with {heart_icon} for the security community
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)


def process_file(uploaded_file, tmp_file_path: str, file_ext: str):
    """Process the uploaded file and return parsed data."""
    if file_ext in ["pcap", "pcapng"]:
        return parse_pcap(tmp_file_path)
    elif file_ext == "csv":
        parsed = parse_csv(tmp_file_path)
        return [{
            "src_ip": row.get("src_ip") or row.get("Source IP") or row.get("src"),
            "dst_ip": row.get("dst_ip") or row.get("Destination IP") or row.get("dst"),
            "protocol": row.get("protocol") or row.get("Protocol"),
            "packet_size": row.get("packet_size") or row.get("Packet Size") or row.get("size"),
        } for row in parsed]
    elif file_ext == "txt":
        return parse_txt(tmp_file_path)
    return None


def main():
    """Main application entry point."""
    # Get favicon path
    favicon = get_favicon_path()
    
    # Page configuration
    st.set_page_config(
        page_title="Sniff-Recon - Network Packet Analyzer",
        page_icon=favicon,
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    
    # Load and inject CSS
    css = load_css()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    # Render header
    render_header()
    
    # File upload section
    uploaded_file = render_upload_zone()
    
    # Landing page or analysis
    if uploaded_file is None:
        render_landing_page()
    else:
        # File size check
        if uploaded_file.size > 200 * 1024 * 1024:
            st.markdown("""
                <div class="sr-alert sr-alert-error">
                    ❌ File size exceeds 200MB limit. Please upload a smaller file.
                </div>
            """, unsafe_allow_html=True)
            return
        
        # Show file info
        render_file_info(uploaded_file)
        
        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        
        file_ext = uploaded_file.name.split(".")[-1].lower()
        
        try:
            # Parse file
            with st.spinner("Processing file..."):
                summary = process_file(uploaded_file, tmp_file_path, file_ext)
            
            if summary is None:
                st.markdown("""
                    <div class="sr-alert sr-alert-error">
                        ❌ Unsupported file type.
                    </div>
                """, unsafe_allow_html=True)
                return
            
            # Convert to DataFrame
            df = pd.DataFrame(summary)
            if df.empty:
                st.markdown("""
                    <div class="sr-alert sr-alert-warning">
                        ⚠️ No packets found in file.
                    </div>
                """, unsafe_allow_html=True)
                return
            
            # Render stats
            render_stats_cards(df)
            
            # Main tabs with improved navigation
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Packet Analysis", 
                "🤖 AI Analysis", 
                "📤 Export",
                "⚙️ Settings"
            ])
            
            with tab4:
                from src.ui.settings import render_settings_page
                render_settings_page()
            
            with tab1:
                st.markdown("""
                    <div class="sr-section-title">Packet Details</div>
                """, unsafe_allow_html=True)
                
                from src.ui.display_packet_table import display_packet_table
                import scapy.all as scapy
                
                try:
                    packets = scapy.PcapReader(tmp_file_path)
                    packets_list = list(packets)
                    packets.close()
                    display_packet_table(packets_list)
                except Exception as e:
                    st.error(f"Error reading packets: {e}")
            
            with tab2:
                st.markdown("""
                    <div class="sr-section-title">AI-Powered Analysis</div>
                """, unsafe_allow_html=True)
                
                try:
                    from src.ai.ai_query_interface import render_ai_query_interface, render_ai_quick_analysis
                    import scapy.all as scapy
                    
                    packets = scapy.rdpcap(tmp_file_path)
                    packets_list = list(packets)
                    
                    render_ai_quick_analysis(packets_list)
                    render_ai_query_interface(packets_list)
                except Exception as e:
                    st.error(f"Error initializing AI: {e}")
            
            with tab3:
                st.markdown("""
                    <div class="sr-section-title">Export Results</div>
                """, unsafe_allow_html=True)
                
                # Save summary
                save_summary(df.to_dict(orient="records"))
                
                st.markdown("""
                    <div class="sr-alert sr-alert-success">
                        ✅ Analysis complete! Ready to export.
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    with open("output/summary.json", "r") as f:
                        json_data = f.read()
                    
                    st.download_button(
                        label="📥 Download JSON",
                        data=json_data,
                        file_name="sniff_recon_analysis.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("👁️ View JSON", use_container_width=True):
                        st.json(json.loads(json_data))
                
                # Session export
                st.markdown("---")
                st.markdown("**Session Management**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    try:
                        session_data = {
                            "ai_responses": st.session_state.get("ai_responses", []),
                            "user_query": st.session_state.get("user_query", ""),
                        }
                        session_json = json.dumps(session_data, indent=4, cls=CustomJSONEncoder)
                        
                        st.download_button(
                            label="💾 Export Session",
                            data=session_json,
                            file_name="sniff_recon_session.json",
                            mime="application/json",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Error exporting session: {e}")
                
                with col2:
                    uploaded_session = st.file_uploader("Import Session", type=["json"], key="import_session")
                    if uploaded_session:
                        try:
                            imported = json.load(uploaded_session)
                            st.session_state["ai_responses"] = imported.get("ai_responses", [])
                            st.session_state["user_query"] = imported.get("user_query", "")
                            st.success("Session imported!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Import error: {e}")
            
            # Start again button
            st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Start New Analysis", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
        
        except Exception as e:
            st.markdown(f"""
                <div class="sr-alert sr-alert-error">
                    ❌ Error processing file: {str(e)}
                </div>
            """, unsafe_allow_html=True)
        
        finally:
            try:
                os.remove(tmp_file_path)
            except Exception:
                pass
    
    # Footer
    render_footer()


if __name__ == "__main__":
    main()

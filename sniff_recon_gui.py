import streamlit as stimport streamlit as st

import osimport os

import jsonimport json

import tempfileimport tempfile

import pandas as pdimport pandas as pd



from parsers.pcap_parser import parse_pcapfrom parsers.pcap_parser import parse_pcap

from parsers.csv_parser import parse_csvfrom parsers.csv_parser import parse_csv

from parsers.txt_parser import parse_txtfrom parsers.txt_parser import parse_txt



# Ensure output directory exists# Ensure output directory exists

os.makedirs("output", exist_ok=True)os.makedirs("output", exist_ok=True)



class CustomJSONEncoder(json.JSONEncoder):class CustomJSONEncoder(json.JSONEncoder):

    def default(self, o):    def default(self, o):

        # Handle EDecimal serialization by converting to float        # Handle EDecimal serialization by converting to float

        if o.__class__.__name__ == "EDecimal":        if o.__class__.__name__ == "EDecimal":

            return float(o)            return float(o)

        return super().default(o)        return super().default(o)



def save_summary(summary):def save_summary(summary):

    with open("output/summary.json", "w") as f:    with open("output/summary.json", "w") as f:

        json.dump(summary, f, indent=4, cls=CustomJSONEncoder)        json.dump(summary, f, indent=4, cls=CustomJSONEncoder)



def inject_modern_css():def inject_modern_css():

    """Inject modern CSS for beautiful packet analyzer UI"""    """Inject modern CSS for beautiful packet analyzer UI"""

    st.markdown(    st.markdown(

        """        """

        <style>        <style>

        /* Fonts */        /* Fonts */

        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@600;700;800&family=Rajdhani:wght@600;700&family=Exo+2:wght@700;800&display=swap');        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@600;700;800&family=Rajdhani:wght@600;700&family=Exo+2:wght@700;800&display=swap');

                

        /* Global styles */        /* Global styles */

        .main {        .main {

            font-family: 'Inter', sans-serif;            font-family: 'Inter', sans-serif;

            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);

            color: #e0e0e0;            color: #e0e0e0;

            padding: 2rem;            padding: 2rem;

        }        }

                

        /* Title styling */        /* Title styling */

        .main-title {        .main-title {

            font-family: 'Orbitron','Rajdhani','Exo 2','Inter',sans-serif;            font-family: 'Orbitron','Rajdhani','Exo 2','Inter',sans-serif;

            letter-spacing: 2px;            letter-spacing: 2px;

            color: #00e6ff;            color: #00e6ff;

            text-shadow: 0 0 8px rgba(0, 238, 255, 0.7), 0 0 18px rgba(0, 238, 255, 0.4);            text-shadow: 0 0 8px rgba(0, 238, 255, 0.7), 0 0 18px rgba(0, 238, 255, 0.4);

            font-size: 3rem;            font-size: 3rem;

            font-weight: 800;            font-weight: 800;

            text-align: center;            text-align: center;

            margin-bottom: 0.25rem;            margin-bottom: 0.25rem;

            animation: neonPulse 2.4s ease-in-out infinite;            animation: neonPulse 2.4s ease-in-out infinite;

            text-transform: uppercase;            text-transform: uppercase;

        }        }

                

        @keyframes neonPulse {        @keyframes neonPulse {

            0% { text-shadow: 0 0 8px rgba(0, 238, 255, 0.6), 0 0 18px rgba(0, 238, 255, 0.35); }            0% { text-shadow: 0 0 8px rgba(0, 238, 255, 0.6), 0 0 18px rgba(0, 238, 255, 0.35); }

            50% { text-shadow: 0 0 14px rgba(0, 255, 255, 0.85), 0 0 28px rgba(0, 255, 255, 0.55); }            50% { text-shadow: 0 0 14px rgba(0, 255, 255, 0.85), 0 0 28px rgba(0, 255, 255, 0.55); }

            100% { text-shadow: 0 0 8px rgba(0, 238, 255, 0.6), 0 0 18px rgba(0, 238, 255, 0.35); }            100% { text-shadow: 0 0 8px rgba(0, 238, 255, 0.6), 0 0 18px rgba(0, 238, 255, 0.35); }

        }        }

                

        .subtitle {        .subtitle {

            color: #66ffff;            color: #66ffff;

            text-align: center;            text-align: center;

            font-size: 1.15rem;            font-size: 1.15rem;

            margin-bottom: 2rem;            margin-bottom: 2rem;

            font-weight: 500;            font-weight: 500;

            text-shadow: 0 0 6px rgba(102, 255, 255, 0.35);            text-shadow: 0 0 6px rgba(102, 255, 255, 0.35);

        }        }



        /* Typewriter */        /* Typewriter */

        .typewriter {        .typewriter {

            display: inline-block;            display: inline-block;

            white-space: nowrap;            white-space: nowrap;

            overflow: hidden;            overflow: hidden;

            border-right: 0.12em solid rgba(102,255,255,0.65);            border-right: 0.12em solid rgba(102,255,255,0.65);

            animation: caret 0.9s step-end infinite;            animation: caret 0.9s step-end infinite;

        }        }

        .typewriter .cursor { color: #66ffff; animation: blink 1.1s steps(2, start) infinite; }        .typewriter .cursor { color: #66ffff; animation: blink 1.1s steps(2, start) infinite; }

        @keyframes blink { to { visibility: hidden; } }        @keyframes blink { to { visibility: hidden; } }

        @keyframes caret { 50% { border-color: transparent; } }        @keyframes caret { 50% { border-color: transparent; } }

                

        /* File uploader styling */        /* File uploader styling */

        .stFileUploader {        .stFileUploader {

            background: rgba(30, 30, 30, 0.8);            background: rgba(30, 30, 30, 0.8);

            border-radius: 16px;            border-radius: 16px;

            border: 2px dashed rgba(0, 255, 255, 0.3);            border: 2px dashed rgba(0, 255, 255, 0.3);

            padding: 2rem;            padding: 2rem;

            text-align: center;            text-align: center;

            transition: all 0.3s ease;            transition: all 0.3s ease;

            margin: 2rem 0;            margin: 2rem 0;

        }        }

                

        .stFileUploader:hover {        .stFileUploader:hover {

            border-color: rgba(0, 255, 255, 0.6);            border-color: rgba(0, 255, 255, 0.6);

            box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);            box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);

        }        }

                

        /* File info styling */        /* File info styling */

        .file-info {        .file-info {

            background: linear-gradient(145deg, rgba(30, 30, 30, 0.9), rgba(20, 20, 20, 0.9));            background: linear-gradient(145deg, rgba(30, 30, 30, 0.9), rgba(20, 20, 20, 0.9));

            border: 2px solid rgba(0, 255, 255, 0.3);            border: 2px solid rgba(0, 255, 255, 0.3);

            border-radius: 16px;            border-radius: 16px;

            padding: 1.5rem;            padding: 1.5rem;

            margin: 1rem 0;            margin: 1rem 0;

            box-shadow: 0 4px 20px rgba(0, 255, 255, 0.1);            box-shadow: 0 4px 20px rgba(0, 255, 255, 0.1);

            text-align: center;            text-align: center;

        }        }

                

        .file-info h3 {        .file-info h3 {

            color: #00ffff;            color: #00ffff;

            margin-bottom: 0.5rem;            margin-bottom: 0.5rem;

        }        }

                

        .file-info p {        .file-info p {

            color: #e0e0e0;            color: #e0e0e0;

            margin: 0.25rem 0;            margin: 0.25rem 0;

        }        }

                

        /* Button styling */        /* Button styling */

        .stButton > button {        .stButton > button {

            background: linear-gradient(45deg, #00ffff, #00b3b3);            background: linear-gradient(45deg, #00ffff, #00b3b3);

            color: #121212;            color: #121212;

            border: none;            border: none;

            border-radius: 12px;            border-radius: 12px;

            padding: 0.75rem 2rem;            padding: 0.75rem 2rem;

            font-weight: 600;            font-weight: 600;

            font-size: 1rem;            font-size: 1rem;

            cursor: pointer;            cursor: pointer;

            transition: all 0.3s ease;            transition: all 0.3s ease;

            box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3);            box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3);

        }        }

                

        .stButton > button:hover {        .stButton > button:hover {

            transform: translateY(-2px);            transform: translateY(-2px);

            box-shadow: 0 8px 25px rgba(0, 255, 255, 0.4);            box-shadow: 0 8px 25px rgba(0, 255, 255, 0.4);

        }        }

                

        /* Success message styling */        /* Success message styling */

        .success-message {        .success-message {

            background: linear-gradient(145deg, rgba(0, 255, 0, 0.1), rgba(0, 200, 0, 0.1));            background: linear-gradient(145deg, rgba(0, 255, 0, 0.1), rgba(0, 200, 0, 0.1));

            border: 2px solid rgba(0, 255, 0, 0.3);            border: 2px solid rgba(0, 255, 0, 0.3);

            border-radius: 12px;            border-radius: 12px;

            padding: 1rem;            padding: 1rem;

            margin: 1rem 0;            margin: 1rem 0;

            text-align: center;            text-align: center;

            color: #00ff00;            color: #00ff00;

        }        }

                

        /* Error message styling */        /* Error message styling */

        .error-message {        .error-message {

            background: linear-gradient(145deg, rgba(255, 0, 0, 0.1), rgba(200, 0, 0, 0.1));            background: linear-gradient(145deg, rgba(255, 0, 0, 0.1), rgba(200, 0, 0, 0.1));

            border: 2px solid rgba(255, 0, 0, 0.3);            border: 2px solid rgba(255, 0, 0, 0.3);

            border-radius: 12px;            border-radius: 12px;

            padding: 1rem;            padding: 1rem;

            margin: 1rem 0;            margin: 1rem 0;

            text-align: center;            text-align: center;

            color: #ff6666;            color: #ff6666;

        }        }

                

        /* Warning message styling */        /* Warning message styling */

        .warning-message {        .warning-message {

            background: linear-gradient(145deg, rgba(255, 255, 0, 0.1), rgba(200, 200, 0, 0.1));            background: linear-gradient(145deg, rgba(255, 255, 0, 0.1), rgba(200, 200, 0, 0.1));

            border: 2px solid rgba(255, 255, 0, 0.3);            border: 2px solid rgba(255, 255, 0, 0.3);

            border-radius: 12px;            border-radius: 12px;

            padding: 1rem;            padding: 1rem;

            margin: 1rem 0;            margin: 1rem 0;

            text-align: center;            text-align: center;

            color: #ffff66;            color: #ffff66;

        }        }

                

        /* Tab styling */        /* Tab styling */

        .stTabs [data-baseweb="tab-list"] {        .stTabs [data-baseweb="tab-list"] {

            gap: 8px;            gap: 8px;

            background: rgba(30, 30, 30, 0.8);            background: rgba(30, 30, 30, 0.8);

            border-radius: 12px;            border-radius: 12px;

            padding: 8px;            padding: 8px;

        }        }

                

        .stTabs [data-baseweb="tab"] {        .stTabs [data-baseweb="tab"] {

            background: rgba(15, 15, 15, 0.5);            background: rgba(15, 15, 15, 0.5);

            border-radius: 8px;            border-radius: 8px;

            color: #e0e0e0;            color: #e0e0e0;

            border: 1px solid rgba(0, 255, 255, 0.2);            border: 1px solid rgba(0, 255, 255, 0.2);

        }        }

                

        .stTabs [aria-selected="true"] {        .stTabs [aria-selected="true"] {

            background: linear-gradient(45deg, #00ffff, #00b3b3);            background: linear-gradient(45deg, #00ffff, #00b3b3);

            color: #121212;            color: #121212;

            font-weight: 600;            font-weight: 600;

        }        }

                

        /* Responsive design */        /* Responsive design */

        @media (max-width: 768px) {        @media (max-width: 768px) {

            .main {            .main {

                padding: 1rem;                padding: 1rem;

            }            }

                        

            .main-title {            .main-title {

                font-size: 2rem;                font-size: 2rem;

            }            }

                        

            .subtitle {            .subtitle {

                font-size: 1rem;                font-size: 1rem;

            }            }

                        

            .stFileUploader {            .stFileUploader {

                padding: 1rem;                padding: 1rem;

            }            }

        }        }

                

        /* Animation for page load */        /* Animation for page load */

        @keyframes fadeInUp {        @keyframes fadeInUp {

            from {            from {

                opacity: 0;                opacity: 0;

                transform: translateY(30px);                transform: translateY(30px);

            }            }

            to {            to {

                opacity: 1;                opacity: 1;

                transform: translateY(0);                transform: translateY(0);

            }            }

        }        }

                

        .fade-in-up {        .fade-in-up {

            animation: fadeInUp 0.8s ease forwards;            animation: fadeInUp 0.8s ease forwards;

        }        }

                

        /* Hide default Streamlit elements */        /* Hide default Streamlit elements */

        #MainMenu {visibility: hidden;}        #MainMenu {visibility: hidden;}

        footer {visibility: hidden;}        footer {visibility: hidden;}

        header {visibility: hidden;}        header {visibility: hidden;}



        /* Modal (popup) styles with typewriter */        /* Modal (popup) styles */

        .sr-modal-overlay {        .sr-modal-overlay {

            position: fixed; inset: 0; background: rgba(0,0,0,0.7);            position: fixed; inset: 0; background: rgba(0,0,0,0.55);

            display: flex; align-items: center; justify-content: center;            display: flex; align-items: center; justify-content: center;

            z-index: 9999;            z-index: 9999;

        }        }

        .sr-modal {        .sr-modal {

            width: min(640px, 90vw);            width: min(720px, 92vw);

            background: linear-gradient(145deg, rgba(18, 18, 30, 0.98), rgba(10, 10, 20, 0.98));            background: linear-gradient(145deg, rgba(18, 18, 30, 0.95), rgba(10, 10, 20, 0.95));

            border: 2px solid rgba(0,255,255,0.4);            border: 1px solid rgba(0,255,255,0.25);

            box-shadow: 0 0 40px rgba(0,255,255,0.25), inset 0 0 20px rgba(0,255,255,0.08);            box-shadow: 0 12px 40px rgba(0,255,255,0.15), inset 0 0 18px rgba(0,255,255,0.06);

            border-radius: 16px; padding: 1.5rem;            border-radius: 14px; padding: 1.25rem 1.25rem 1rem;

            color: #e8f8ff;            color: #e0f7ff;

        }        }

        .sr-modal h3 {         .sr-modal h3 { color: #00ffff; margin: 0 0 0.6rem 0; font-family: 'Exo 2','Inter',sans-serif; }

            color: #00ffff;         .sr-modal p { margin: 0.35rem 0; color: #d5f9ff; }

            margin: 0 0 1rem 0;         .sr-modal .sr-close {

            font-family: 'Exo 2','Inter',sans-serif;             margin-top: 0.8rem;

            text-shadow: 0 0 8px rgba(0,255,255,0.5);        }

        }

        .sr-modal-body {         /* Sidebar mini cards */

            margin: 1rem 0;         .sr-card {

            color: #e8f8ff;             border: 1px solid rgba(0,255,255,0.25);

            line-height: 1.6;            border-radius: 10px;

            min-height: 60px;            padding: 0.75rem; margin-bottom: 0.6rem;

            font-size: 1.05rem;            background: rgba(20,25,35,0.65);

        }            box-shadow: inset 0 0 12px rgba(0,255,255,0.06);

        .sr-modal-close {        }

            margin-top: 1rem;        .sr-card h4 { color: #00ffff; margin: 0 0 0.35rem 0; font-size: 0.95rem; }

        }        .sr-mini-btn > button {

        </style>            width: 100%;

        """,            background: linear-gradient(45deg, #00ffff, #00b3b3);

        unsafe_allow_html=True,            color: #121212; border: none; border-radius: 8px;

    )            padding: 0.45rem 0.6rem; font-weight: 600; font-size: 0.9rem;

            box-shadow: 0 4px 15px rgba(0, 255, 255, 0.28);

def main():        }

    # Set page config to prevent JavaScript errors        </style>

    st.set_page_config(        """,

        page_title="Sniff Recon - Network Packet Analyzer",        unsafe_allow_html=True,

        page_icon="🔍",    )

        layout="wide",

        initial_sidebar_state="expanded"def main():

    )    # Set page config to prevent JavaScript errors

        st.set_page_config(

    # Inject modern CSS        page_title="Sniff Recon - Network Packet Analyzer",

    inject_modern_css()        page_icon="🔍",

        layout="wide",

    # Sidebar: About and Help Desk buttons only (simple, no expanded content)        initial_sidebar_state="expanded"

    with st.sidebar:    )

        st.markdown('<h3 style="color:#00ffff; margin-bottom:1rem; font-family: Orbitron,sans-serif;">Quick Access</h3>', unsafe_allow_html=True)    

        if st.button("📖 About", key="aboutBtn", use_container_width=True):    # Inject modern CSS

            st.session_state["sr_modal"] = {"type": "about"}    inject_modern_css()

            st.rerun()

        if st.button("❓ Help Desk", key="helpBtn", use_container_width=True):    # Sidebar: About, Contact, Help Desk (left side)

            st.session_state["sr_modal"] = {"type": "help"}    with st.sidebar:

            st.rerun()        st.markdown('<div class="sr-card"><h4>About</h4>', unsafe_allow_html=True)

        if st.button("About Sniff Recon", key="aboutBtn"):

    # Main title with original goggles icon restored            st.session_state["sr_modal"] = {"type": "about"}

    st.markdown(        st.markdown('</div>', unsafe_allow_html=True)

        '<h1 class="main-title fade-in-up">🔍 Sniff Recon</h1>',

        unsafe_allow_html=True        st.markdown('<div class="sr-card"><h4>Contact Us</h4>', unsafe_allow_html=True)

    )        if st.button("Contact Team", key="contactBtn"):

            st.session_state["sr_modal"] = {"type": "contact"}

    # Tagline: one-time typewriter; then steady with blinking cursor        st.markdown('</div>', unsafe_allow_html=True)

    tagline_text = "Advanced Network Packet Analyzer & AI-Powered Protocol Dissector"

    if not st.session_state.get("sr_tagline_done"):        st.markdown('<div class="sr-card"><h4>Help Desk</h4>', unsafe_allow_html=True)

        st.markdown(        faq_items = [

            f'''            ("Why use Sniff Recon?", "Sniff Recon quickly parses packet captures and highlights patterns, anomalies, and potential threats with AI-assisted summaries."),

            <p class="subtitle fade-in-up">            ("Supported files?", "PCAP, PCAPNG, CSV, and TXT are supported. CSV column names are auto-mapped when possible."),

              <span id="sr-typewriter" class="typewriter"></span><span class="cursor">_</span>            ("Is AI required?", "No. When AI providers aren’t configured, the app still provides local statistical analysis and summaries."),

            </p>            ("File size limit?", "The UI limits uploads to 200MB to protect memory. Large captures should be trimmed or filtered before upload."),

            <script>            ("Is my data stored?", "Summaries are saved to output/summary.json locally. Packet data is processed in-memory and temp files are cleaned up.")

              const txt = {json.dumps(tagline_text)};        ]

              const el = window.parent.document.getElementById('sr-typewriter');        for idx, (q, _a) in enumerate(faq_items):

              if (el) {{            if st.button(q, key=f"faqBtn{idx}"):

                  let i=0; const speed=28;                st.session_state["sr_modal"] = {"type": "faq", "index": idx}

                  const type = () => {{        st.markdown('</div>', unsafe_allow_html=True)

                      if (i <= txt.length) {{ el.textContent = txt.substring(0,i); i++; setTimeout(type, speed); }}

                  }}; type();    # Main title with neon glow (keep logo/title feel and spacing)

              }}    st.markdown(

            </script>        '<h1 class="main-title fade-in-up">SNIFF RECON</h1>',

            ''',        unsafe_allow_html=True

            unsafe_allow_html=True,    )

        )

        # Mark as done to avoid re-animating on further reruns    # Tagline: one-time typewriter; then steady with blinking cursor

        st.session_state["sr_tagline_done"] = True    tagline_text = "Advanced Network Packet Analyzer & AI-Powered Protocol Dissector"

    else:    if not st.session_state.get("sr_tagline_done"):

        st.markdown(        st.markdown(

            f'<p class="subtitle fade-in-up">{tagline_text} <span class="cursor">_</span></p>',            f'''

            unsafe_allow_html=True,            <p class="subtitle fade-in-up">

        )              <span id="sr-typewriter" class="typewriter"></span><span class="cursor">_</span>

            </p>

    # Modal renderer with typewriter for content            <script>

    modal = st.session_state.get("sr_modal")              const txt = {json.dumps(tagline_text)};

    if modal:              const el = window.parent.document.getElementById('sr-typewriter');

        modal_type = modal.get("type")              if (el) {{

        title = ""                  let i=0; const speed=28;

        body = ""                  const type = () => {{

                              if (i <= txt.length) {{ el.textContent = txt.substring(0,i); i++; setTimeout(type, speed); }}

        if modal_type == "about":                  }}; type();

            title = "About Sniff Recon"              }}

            body = (            </script>

                "Sniff Recon is a Streamlit-based network packet analyzer that supports PCAP, PCAPNG, CSV, and TXT file parsing. "            ''',

                "It features optional multi-provider AI analysis, memory-aware parsing, and clear visualizations to help you investigate network traffic quickly and safely."            unsafe_allow_html=True,

            )        )

        elif modal_type == "help":        # Mark as done to avoid re-animating on further reruns

            title = "Help Desk"        st.session_state["sr_tagline_done"] = True

            body = (    else:

                "🔹 Why use Sniff Recon? It quickly parses packet captures and highlights patterns, anomalies, and potential threats with AI-assisted summaries.\n\n"        st.markdown(

                "🔹 Supported files: PCAP, PCAPNG, CSV, and TXT. CSV column names are auto-mapped when possible.\n\n"            f'<p class="subtitle fade-in-up">{tagline_text} <span class="cursor">_</span></p>',

                "🔹 Is AI required? No. When AI providers aren't configured, the app still provides local statistical analysis and summaries.\n\n"            unsafe_allow_html=True,

                "🔹 File size limit: The UI limits uploads to 200MB to protect memory. Large captures should be trimmed or filtered before upload.\n\n"        )

                "🔹 Is my data stored? Summaries are saved to output/summary.json locally. Packet data is processed in-memory and temp files are cleaned up."

            )    # Optional modal renderer (centered popup)

    modal = st.session_state.get("sr_modal")

        # Render overlay and modal with typewriter    if modal:

        st.markdown('<div class="sr-modal-overlay"></div>', unsafe_allow_html=True)        # Build modal content

        st.markdown('<div class="sr-modal">', unsafe_allow_html=True)        title = ""

        st.markdown(f'<h3>{title}</h3>', unsafe_allow_html=True)        body = ""

                if modal.get("type") == "about":

        # Typewriter animation for modal body            title = "About Sniff Recon"

        modal_id = f"sr-modal-{modal_type}"            body = (

        if not st.session_state.get(f"{modal_id}_typed"):                "Sniff Recon is a Streamlit-based network packet analyzer that supports PCAP/CSV/TXT parsing, "

            st.markdown(                "with optional multi-provider AI analysis. It emphasizes safe defaults, memory-aware parsing, and "

                f'''                "clear visualizations to help you investigate traffic quickly."

                <div class="sr-modal-body" id="{modal_id}"></div>            )

                <script>        elif modal.get("type") == "contact":

                  (function() {{            title = "Contact Us"

                      const txt = {json.dumps(body)};            body = (

                      const el = window.parent.document.getElementById('{modal_id}');                "For support or inquiries, please open an issue on the repository or email the maintainers. "

                      if (el && el.textContent === '') {{                "Remember to exclude sensitive data when sharing captures."

                          let i = 0;            )

                          const speed = 12;        elif modal.get("type") == "faq":

                          const type = () => {{            idx = int(modal.get("index", 0))

                              if (i < txt.length) {{            q, a = faq_items[idx]

                                  el.textContent += txt.charAt(i);            title = q

                                  i++;            body = a

                                  setTimeout(type, speed);

                              }}        # Render overlay

                          }};        st.markdown('<div class="sr-modal-overlay">', unsafe_allow_html=True)

                          type();        st.markdown('<div class="sr-modal">', unsafe_allow_html=True)

                      }}        st.markdown(f'<h3>{title}</h3><p>{body}</p>', unsafe_allow_html=True)

                  }})();        close_col = st.columns([1,1,1])[1]

                </script>        with close_col:

                ''',            if st.button("Close", key="srCloseModal", help="Close this dialog"):

                unsafe_allow_html=True                st.session_state["sr_modal"] = None

            )        st.markdown('</div></div>', unsafe_allow_html=True)

            st.session_state[f"{modal_id}_typed"] = True

        else:    # File upload section

            # Already typed, show directly    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)

            st.markdown(f'<div class="sr-modal-body">{body.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)    

            uploaded_file = st.file_uploader(

        # Close button        label="📁 Upload Packet Capture File",

        col1, col2, col3 = st.columns([1, 1, 1])        type=["pcap", "pcapng", "csv", "txt"],

        with col2:        help="Supported formats: .pcap, .pcapng, .csv, .txt (Max: 200MB)",

            if st.button("✖ Close", key="srCloseModal", help="Close this popup"):        key="fileUploader",

                st.session_state["sr_modal"] = None    )

                # Clear typed flag for next open    

                st.session_state[f"{modal_id}_typed"] = False    st.markdown('</div>', unsafe_allow_html=True)

                st.rerun()

            if uploaded_file is not None:

        st.markdown('</div>', unsafe_allow_html=True)        # File size validation

        if uploaded_file.size > 200 * 1024 * 1024:

    # File upload section (unchanged)            st.markdown(

    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)                '<div class="error-message">❌ File size exceeds 200MB limit. Please upload a smaller file.</div>',

                    unsafe_allow_html=True

    uploaded_file = st.file_uploader(            )

        label="📁 Upload Packet Capture File",            return

        type=["pcap", "pcapng", "csv", "txt"],

        help="Supported formats: .pcap, .pcapng, .csv, .txt (Max: 200MB)",        # Display file information

        key="fileUploader",        file_size_mb = uploaded_file.size / (1024*1024)

    )        st.markdown(

                f"""

    st.markdown('</div>', unsafe_allow_html=True)            <div class="file-info">

                <h3>📄 File Uploaded Successfully</h3>

    if uploaded_file is not None:                <p><strong>Name:</strong> {uploaded_file.name}</p>

        # File size validation                <p><strong>Size:</strong> {file_size_mb:.2f} MB</p>

        if uploaded_file.size > 200 * 1024 * 1024:                <p><strong>Type:</strong> {uploaded_file.type or 'Unknown'}</p>

            st.markdown(            </div>

                '<div class="error-message">❌ File size exceeds 200MB limit. Please upload a smaller file.</div>',            """,

                unsafe_allow_html=True            unsafe_allow_html=True

            )        )

            return

        # Save uploaded file temporarily

        # Display file information        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:

        file_size_mb = uploaded_file.size / (1024*1024)            tmp_file.write(uploaded_file.read())

        st.markdown(            tmp_file_path = tmp_file.name

            f"""

            <div class="file-info">        file_ext = uploaded_file.name.split(".")[-1].lower()

                <h3>📄 File Uploaded Successfully</h3>

                <p><strong>Name:</strong> {uploaded_file.name}</p>        # Parse based on file extension

                <p><strong>Size:</strong> {file_size_mb:.2f} MB</p>        try:

                <p><strong>Type:</strong> {uploaded_file.type or 'Unknown'}</p>            if file_ext in ["pcap", "pcapng"]:

            </div>                summary = parse_pcap(tmp_file_path)

            """,            elif file_ext == "csv":

            unsafe_allow_html=True                summary = parse_csv(tmp_file_path)

        )                # Map keys if needed

                mapped_summary = []

        # Save uploaded file temporarily                for row in summary:

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:                    mapped_row = {

            tmp_file.write(uploaded_file.read())                        "src_ip": row.get("src_ip") or row.get("Source IP") or row.get("source_ip") or row.get("src"),

            tmp_file_path = tmp_file.name                        "dst_ip": row.get("dst_ip") or row.get("Destination IP") or row.get("destination_ip") or row.get("dst"),

                        "protocol": row.get("protocol") or row.get("Protocol"),

        file_ext = uploaded_file.name.split(".")[-1].lower()                        "packet_size": row.get("packet_size") or row.get("Packet Size") or row.get("packet_size_bytes") or row.get("size"),

                    }

        # Parse based on file extension                    mapped_summary.append(mapped_row)

        try:                summary = mapped_summary

            if file_ext in ["pcap", "pcapng"]:            elif file_ext == "txt":

                summary = parse_pcap(tmp_file_path)                summary = parse_txt(tmp_file_path)

            elif file_ext == "csv":            else:

                summary = parse_csv(tmp_file_path)                st.markdown(

                # Map keys if needed                    '<div class="error-message">❌ Unsupported file type.</div>',

                mapped_summary = []                    unsafe_allow_html=True

                for row in summary:                )

                    mapped_row = {                return

                        "src_ip": row.get("src_ip") or row.get("Source IP") or row.get("source_ip") or row.get("src"),

                        "dst_ip": row.get("dst_ip") or row.get("Destination IP") or row.get("destination_ip") or row.get("dst"),            # Convert to DataFrame

                        "protocol": row.get("protocol") or row.get("Protocol"),            summary = pd.DataFrame(summary)

                        "packet_size": row.get("packet_size") or row.get("Packet Size") or row.get("packet_size_bytes") or row.get("size"),

                    }            # Check for empty DataFrame

                    mapped_summary.append(mapped_row)            if summary is None or len(summary) == 0:

                summary = mapped_summary                st.markdown(

            elif file_ext == "txt":                    '<div class="warning-message">⚠️ Summary is empty or could not be generated.</div>',

                summary = parse_txt(tmp_file_path)                    unsafe_allow_html=True

            else:                )

                st.markdown(                return

                    '<div class="error-message">❌ Unsupported file type.</div>',

                    unsafe_allow_html=True            # Create tabs for different analysis views

                )            tab1, tab2, tab3 = st.tabs(["📊 Packet Analysis", "🤖 AI Analysis", "💾 Export Results"])

                return            

            with tab1:

            # Convert to DataFrame                # Display packet analysis

            summary = pd.DataFrame(summary)                st.markdown("## 📊 Packet Analysis Results")

                

            # Check for empty DataFrame# Import and display packet table

            if summary is None or len(summary) == 0:                from display_packet_table import display_packet_table

                st.markdown(                import scapy.all as scapy

                    '<div class="warning-message">⚠️ Summary is empty or could not be generated.</div>',

                    unsafe_allow_html=True                try:

                )                    packets = scapy.PcapReader(tmp_file_path)

                return                    packets_list = []

                    total_bytes = os.path.getsize(tmp_file_path)

            # Create tabs for different analysis views                    bytes_read = 0

            tab1, tab2, tab3 = st.tabs(["📊 Packet Analysis", "🤖 AI Analysis", "💾 Export Results"])                    progress_text = "Loading and parsing packets..."

                                progress_bar = st.progress(0, text=progress_text)

            with tab1:                    last_update_fraction = 0

                # Display packet analysis

                st.markdown("## 📊 Packet Analysis Results")                    for pkt in packets:

                                        packets_list.append(pkt)

# Import and display packet table                        pos = packets._current_packet if hasattr(packets, '_current_packet') else len(packets_list)

                from display_packet_table import display_packet_table                        # Estimate progress (fallback to number of packets)

                import scapy.all as scapy                        fraction = min(1.0, (packets._file.tell() / total_bytes)) if hasattr(packets, '_file') else min(1.0, pos/10000)

                        # Avoid excessive redraws

                try:                        if fraction - last_update_fraction > 0.01 or fraction == 1.0:

                    packets = scapy.PcapReader(tmp_file_path)                            progress_bar.progress(fraction, text=progress_text)

                    packets_list = []                            last_update_fraction = fraction

                    total_bytes = os.path.getsize(tmp_file_path)                    progress_bar.empty()

                    bytes_read = 0                    packets.close()

                    progress_text = "Loading and parsing packets..."                    display_packet_table(packets_list)

                    progress_bar = st.progress(0, text=progress_text)                except Exception as e:

                    last_update_fraction = 0                    st.markdown(

                        f'<div class="error-message">❌ Error reading packet file: {str(e)}</div>',

                    for pkt in packets:                        unsafe_allow_html=True

                        packets_list.append(pkt)                    )

                        pos = packets._current_packet if hasattr(packets, '_current_packet') else len(packets_list)            

                        # Estimate progress (fallback to number of packets)            with tab2:

                        fraction = min(1.0, (packets._file.tell() / total_bytes)) if hasattr(packets, '_file') else min(1.0, pos/10000)                # AI Analysis tab

                        # Avoid excessive redraws                try:

                        if fraction - last_update_fraction > 0.01 or fraction == 1.0:                    from ai_query_interface import render_ai_query_interface, render_ai_quick_analysis

                            progress_bar.progress(fraction, text=progress_text)                    import scapy.all as scapy

                            last_update_fraction = fraction                    

                    progress_bar.empty()                    packets = scapy.rdpcap(tmp_file_path)

                    packets.close()                    packets_list = list(packets)

                    display_packet_table(packets_list)                    

                except Exception as e:                    # Quick AI analysis

                    st.markdown(                    render_ai_quick_analysis(packets_list)

                        f'<div class="error-message">❌ Error reading packet file: {str(e)}</div>',                    

                        unsafe_allow_html=True                    # AI Query interface

                    )                    render_ai_query_interface(packets_list)

                                

            with tab2:                except Exception as e:

                # AI Analysis tab                    st.markdown(

                try:                        f'<div class="error-message">❌ Error initializing AI analysis: {str(e)}</div>',

                    from ai_query_interface import render_ai_query_interface, render_ai_quick_analysis                        unsafe_allow_html=True

                    import scapy.all as scapy                    )

                                

                    packets = scapy.rdpcap(tmp_file_path)            with tab3:

                    packets_list = list(packets)                # Export Results tab

                                    st.markdown("## 💾 Export Analysis Results")

                    # Quick AI analysis                

                    render_ai_quick_analysis(packets_list)                # Save summary to JSON

                                    save_summary(summary.to_dict(orient="records"))

                    # AI Query interface                

                    render_ai_query_interface(packets_list)                st.markdown(

                                        '<div class="success-message">✅ Analysis complete! Summary saved to output/summary.json</div>',

                except Exception as e:                    unsafe_allow_html=True

                    st.markdown(                )

                        f'<div class="error-message">❌ Error initializing AI analysis: {str(e)}</div>',

                        unsafe_allow_html=True                # Download section

                    )                col1, col2 = st.columns(2)

                            

            with tab3:                # Button to download JSON

                # Export Results tab                with open("output/summary.json", "r") as f:

                st.markdown("## 💾 Export Analysis Results")                    json_data = f.read()

                

                # Save summary to JSON                with col1:

                save_summary(summary.to_dict(orient="records"))                    st.download_button(

                                        label="📥 Download Summary JSON",

                st.markdown(                        data=json_data,

                    '<div class="success-message">✅ Analysis complete! Summary saved to output/summary.json</div>',                        file_name="sniff_recon_summary.json",

                    unsafe_allow_html=True                        mime="application/json",

                )                        key="downloadJson",

                        help="Download the complete analysis summary"

                # Download section                    )

                col1, col2 = st.columns(2)

                                with col2:

                # Button to download JSON                    if st.button("👁️ View Raw JSON"):

                with open("output/summary.json", "r") as f:                        st.json(json.loads(json_data))

                    json_data = f.read()

        except Exception as e:

                with col1:            st.markdown(

                    st.download_button(                f'<div class="error-message">❌ Error processing file: {str(e)}</div>',

                        label="📥 Download Summary JSON",                unsafe_allow_html=True

                        data=json_data,            )

                        file_name="sniff_recon_summary.json",        finally:

                        mime="application/json",            # Clean up temp file

                        key="downloadJson",            try:

                        help="Download the complete analysis summary"                os.remove(tmp_file_path)

                    )            except:

                pass

                with col2:

                    if st.button("👁️ View Raw JSON"):if __name__ == "__main__":

                        st.json(json.loads(json_data))    main()


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

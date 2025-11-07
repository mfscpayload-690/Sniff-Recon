import streamlit as st
import os
import json
import tempfile
import pandas as pd

from src.parsers.pcap_parser import parse_pcap
from src.parsers.csv_parser import parse_csv
from src.parsers.txt_parser import parse_txt

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

        /* ==================== ANIMATED BACKGROUND ==================== */
        .main {
            font-family: 'Inter', sans-serif;
            position: relative;
            overflow: hidden;
            /* Deep gradient base */
            background: radial-gradient(ellipse at top left, #0a0f16, #101823);
            color: #e0e0e0;
            padding: 2rem;
        }
        
        /* Vignette effect */
        .main::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.4) 100%);
            pointer-events: none;
            z-index: -10;
        }
        
        /* Digital mesh texture overlay */
        .main::after {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                repeating-linear-gradient(0deg, rgba(0,255,255,0.03) 0px, transparent 1px, transparent 2px, rgba(0,255,255,0.03) 3px),
                repeating-linear-gradient(90deg, rgba(0,255,255,0.03) 0px, transparent 1px, transparent 2px, rgba(0,255,255,0.03) 3px);
            background-size: 80px 80px;
            opacity: 0.15;
            pointer-events: none;
            z-index: -9;
            animation: gridPulse 8s ease-in-out infinite;
        }
        
        @keyframes gridPulse {
            0%, 100% { opacity: 0.1; }
            50% { opacity: 0.2; }
        }

        /* Animated data flow lines - MANY MORE */
        @keyframes flowLine1 {
            0% { transform: translateX(-100%) translateY(0); opacity: 0; }
            10% { opacity: 0.6; }
            90% { opacity: 0.6; }
            100% { transform: translateX(200vw) translateY(20px); opacity: 0; }
        }
        @keyframes flowLine2 {
            0% { transform: translateX(-100%) translateY(0); opacity: 0; }
            10% { opacity: 0.4; }
            90% { opacity: 0.4; }
            100% { transform: translateX(200vw) translateY(-30px); opacity: 0; }
        }
        @keyframes flowLine3 {
            0% { transform: translateX(-100%) translateY(0); opacity: 0; }
            10% { opacity: 0.5; }
            90% { opacity: 0.5; }
            100% { transform: translateX(200vw) translateY(40px); opacity: 0; }
        }
        @keyframes flowLine4 {
            0% { transform: translateX(200vw) translateY(0); opacity: 0; }
            10% { opacity: 0.5; }
            90% { opacity: 0.5; }
            100% { transform: translateX(-100vw) translateY(-20px); opacity: 0; }
        }
        @keyframes flowLine5 {
            0% { transform: translateX(-100%) translateY(0); opacity: 0; }
            10% { opacity: 0.7; }
            90% { opacity: 0.7; }
            100% { transform: translateX(200vw) translateY(-40px); opacity: 0; }
        }
        @keyframes flowLine6 {
            0% { transform: translateX(200vw) translateY(0); opacity: 0; }
            10% { opacity: 0.4; }
            90% { opacity: 0.4; }
            100% { transform: translateX(-100vw) translateY(30px); opacity: 0; }
        }

        /* ==================== END BACKGROUND ==================== */

        /* Background animation container */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            pointer-events: none;
            z-index: 0;
        }

        /* Network nodes - 6 floating elements */
        [data-testid="stSidebar"]::before,
        [data-testid="stSidebar"]::after,
        [data-testid="stToolbar"]::before,
        [data-testid="stToolbar"]::after,
        [data-testid="stDecoration"]::before,
        [data-testid="stDecoration"]::after {
            content: '';
            position: fixed;
            width: 4px;
            height: 4px;
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
        }
        
        [data-testid="stSidebar"]::before {
            background: radial-gradient(circle, #00ffff, transparent);
            box-shadow: 0 0 15px rgba(0,255,255,0.8), 0 0 30px rgba(0,255,255,0.4);
            animation: floatNode1 35s ease-in-out infinite;
        }
        [data-testid="stSidebar"]::after {
            background: radial-gradient(circle, #b084f4, transparent);
            box-shadow: 0 0 15px rgba(176,132,244,0.8), 0 0 30px rgba(176,132,244,0.4);
            animation: floatNode2 40s ease-in-out infinite 5s;
        }
        [data-testid="stToolbar"]::before {
            background: radial-gradient(circle, #4ad3b0, transparent);
            box-shadow: 0 0 15px rgba(74,211,176,0.8), 0 0 30px rgba(74,211,176,0.4);
            animation: floatNode3 32s ease-in-out infinite 10s;
        }
        [data-testid="stToolbar"]::after {
            background: radial-gradient(circle, #06b6d4, transparent);
            box-shadow: 0 0 15px rgba(6,182,212,0.8), 0 0 30px rgba(6,182,212,0.4);
            animation: floatNode4 38s ease-in-out infinite 15s;
        }
        [data-testid="stDecoration"]::before {
            background: radial-gradient(circle, #8b5cf6, transparent);
            box-shadow: 0 0 15px rgba(139,92,246,0.8), 0 0 30px rgba(139,92,246,0.4);
            animation: floatNode5 36s ease-in-out infinite 20s;
        }
        [data-testid="stDecoration"]::after {
            background: radial-gradient(circle, #00d4ff, transparent);
            box-shadow: 0 0 15px rgba(0,212,255,0.8), 0 0 30px rgba(0,212,255,0.4);
            animation: floatNode6 34s ease-in-out infinite 25s;
        }

        /* Particle dots - 20 PARTICLES FOR GALAXY EFFECT (GLOBAL ONLY) */
        .main::before, .main::after,
        body::before, body::after,
        html::before, html::after,
        .stApp::before, .stApp::after,
        #root::before, #root::after {
            content: '';
            position: fixed;
            width: 2px;
            height: 2px;
            border-radius: 50%;
            background: #00ffff;
            box-shadow: 0 0 4px rgba(0,255,255,0.8);
            pointer-events: none;
            z-index: 0;
        }
        .main::before { background: #b084f4; box-shadow: 0 0 4px #b084f4; animation: particleStream1 25s ease-in-out infinite; }
        .main::after { background: #4ad3b0; box-shadow: 0 0 4px #4ad3b0; animation: particleStream2 30s ease-in-out infinite 5s; }
        body::before { background: #06b6d4; box-shadow: 0 0 4px #06b6d4; animation: particleStream3 28s ease-in-out infinite 8s; }
        body::after { background: #8b5cf6; box-shadow: 0 0 4px #8b5cf6; animation: particleStream4 26s ease-in-out infinite 3s; }
        html::before { background: #00d4ff; box-shadow: 0 0 4px #00d4ff; animation: particleStream5 29s ease-in-out infinite 10s; }
        html::after { background: #00ffff; box-shadow: 0 0 4px #00ffff; animation: particleStream6 27s ease-in-out infinite 6s; }
        .stApp::before { background: #b084f4; box-shadow: 0 0 4px #b084f4; animation: particleStream7 31s ease-in-out infinite 12s; }
        .stApp::after { background: #4ad3b0; box-shadow: 0 0 4px #4ad3b0; animation: particleStream8 24s ease-in-out infinite 15s; }
        #root::before { background: #06b6d4; box-shadow: 0 0 4px #06b6d4; animation: particleStream9 27s ease-in-out infinite 2s; }
        #root::after { background: #8b5cf6; box-shadow: 0 0 4px #8b5cf6; animation: particleStream10 29s ease-in-out infinite 9s; }

        /* Ensure content is above animations */
        .main > div {
            position: relative;
            z-index: 10;
        }

        /* ==================== ORIGINAL STYLES ==================== */

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
            position: relative;
            z-index: 10;
        }
        @keyframes neonPulse {
            0% { text-shadow: 0 0 8px rgba(0, 
            238, 255, 0.6), 0 0 18px rgba(0, 238, 255, 0.35); }
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
            position: relative;
            z-index: 10;
        }

        /* File uploader */
        .stFileUploader {
            background: rgba(40, 40, 50, 0.95) !important;
            border-radius: 16px;
            border: 2px dashed rgba(0, 255, 255, 0.4) !important;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            margin: 2rem 0;
            position: relative;
            z-index: 10;
        }
        .stFileUploader:hover { 
            border-color: rgba(0, 255, 255, 0.7) !important; 
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.3) !important; 
            background: rgba(50, 50, 60, 0.98) !important;
        }
        /* File uploader text visibility fix */
        .stFileUploader label,
        .stFileUploader div,
        .stFileUploader span,
        .stFileUploader p,
        .stFileUploader small {
            color: #e0e0e0 !important;
        }
        .stFileUploader [data-testid="stMarkdownContainer"] p {
            color: #c0c0c0 !important;
            font-weight: 500 !important;
        }
        /* File uploader button */
        .stFileUploader button {
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.15), rgba(0, 200, 200, 0.15)) !important;
            border: 2px solid rgba(0, 255, 255, 0.4) !important;
            color: #00ffff !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.5rem !important;
            border-radius: 8px !important;
        }
        .stFileUploader button:hover {
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.25), rgba(0, 220, 220, 0.25)) !important;
            border-color: rgba(0, 255, 255, 0.6) !important;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.4) !important;
        }

        /* File info */
        .file-info { 
            background: linear-gradient(145deg, rgba(30, 30, 30, 0.9), rgba(20, 20, 20, 0.9)); 
            border: 2px solid rgba(0, 255, 255, 0.3); 
            border-radius: 16px; 
            padding: 1.5rem; 
            margin: 1rem 0; 
            box-shadow: 0 4px 20px rgba(0, 255, 255, 0.1); 
            text-align: center;
            position: relative;
            z-index: 10;
        }
        .file-info h3 { color: #00ffff; margin-bottom: 0.5rem; }
        .file-info p { color: #e0e0e0; margin: 0.25rem 0; }

        /* Messages */
        .success-message { background: linear-gradient(145deg, rgba(0,255,0,0.1), rgba(0,200,0,0.1)); border: 2px solid rgba(0,255,0,0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0; text-align: center; color: #00ff00; position: relative; z-index: 10; }
        .error-message { background: linear-gradient(145deg, rgba(255,0,0,0.1), rgba(200,0,0,0.1)); border: 2px solid rgba(255,0,0,0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0; text-align: center; color: #ff6666; position: relative; z-index: 10; }
        .warning-message { background: linear-gradient(145deg, rgba(255,255,0,0.1), rgba(200,200,0,0.1)); border: 2px solid rgba(255,255,0,0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0; text-align: center; color: #ffff66; position: relative; z-index: 10; }

        /* Pill-style tab buttons */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1.2rem !important;
            background: transparent !important;
            justify-content: center !important;
            padding: 1rem 0 !important;
            border-bottom: none !important;
        }
        .stTabs [data-baseweb="tab"] {
            height: auto !important;
            white-space: pre-wrap !important;
            background: rgba(0,255,255,0.06) !important;
            border: 2.5px solid rgba(0,255,255,0.6) !important;
            border-radius: 999px !important;
            color: #00ffff !important;
            padding: 0.65rem 1.8rem !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            font-family: Orbitron, Inter, sans-serif !important;
            transition: all 0.22s cubic-bezier(0.4, 2, 0.6, 1) !important;
            box-shadow: 0 0 0px rgba(0,255,255,0) !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background: linear-gradient(90deg, rgba(0,255,255,0.2) 60%, rgba(176,132,244,0.2) 100%) !important;
            color: #fff !important;
            border-color: #8b5cf6 !important;
            box-shadow: 0 0 10px rgba(0,255,255,0.35) !important;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #00ffff 60%, #b084f4 100%) !important;
            color: #0f1419 !important;
            border-color: #fff !important;
            box-shadow: 0 0 18px rgba(0,255,255,0.6), 0 0 32px rgba(176,132,244,0.6) !important;
            transform: scale(1.05) !important;
        }
        .stTabs [data-baseweb="tab"]:active {
            animation: tabPulse 0.3s !important;
        }
        @keyframes tabPulse {
            0% { box-shadow: 0 0 0 0 rgba(0,255,255,0.35); }
            70% { box-shadow: 0 0 0 10px rgba(0,255,255,0.2); }
            100% { box-shadow: 0 0 0 0 rgba(0,255,255,0); }
        }

        /* Animations */
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px);} to { opacity: 1; transform: translateY(0);} }
        .fade-in-up { animation: fadeInUp 0.8s ease forwards; }

        /* Section Headings */
        .section-heading {
            font-family: 'Orbitron', 'Inter', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: #00ffff;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin: 2rem 0 1.5rem 0;
            padding-bottom: 0.8rem;
            border-bottom: 3px solid #00ffff;
            box-shadow: 0 3px 15px rgba(0,255,255,0.3);
            position: relative;
            display: inline-block;
            width: 100%;
        }
        .section-heading::before {
            content: '▶';
            margin-right: 0.8rem;
            color: #00ffff;
            text-shadow: 0 0 10px rgba(0,255,255,0.8);
        }
        .section-heading::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 30%;
            height: 3px;
            background: linear-gradient(90deg, #b084f4, transparent);
            animation: underlinePulse 2s ease-in-out infinite;
        }
        @keyframes underlinePulse {
            0%, 100% { opacity: 0.6; width: 30%; }
            50% { opacity: 1; width: 50%; }
        }

        /* Subsection Headings */
        .subsection-heading {
            font-family: 'Orbitron', 'Inter', sans-serif;
            font-size: 1.3rem;
            font-weight: 600;
            color: #b084f4;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(176,132,244,0.4);
            display: inline-block;
            width: 100%;
        }
        .subsection-heading::before {
            content: '▸';
            margin-right: 0.6rem;
            color: #b084f4;
        }

        /* Start Again Button */
        .start-again-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 3rem 0 2rem 0;
            padding: 2rem 0;
        }
        .start-again-btn {
            font-family: 'Orbitron', 'Inter', sans-serif;
            font-size: 1.2rem;
            font-weight: 600;
            color: #0f1419;
            background: linear-gradient(135deg, #00ffff 0%, #00cccc 100%);
            border: none;
            border-radius: 12px;
            padding: 1rem 3rem;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(0,255,255,0.4), 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 2px;
            position: relative;
            overflow: hidden;
        }
        .start-again-btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255,255,255,0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        .start-again-btn:hover {
            background: linear-gradient(135deg, #00ffff 0%, #4dffff 100%);
            box-shadow: 0 0 30px rgba(0,255,255,0.6), 0 6px 20px rgba(0,0,0,0.4);
            transform: translateY(-2px);
            animation: gentlePulse 1.5s ease-in-out infinite;
        }
        .start-again-btn:hover::before {
            width: 300px;
            height: 300px;
        }
        .start-again-btn:active {
            transform: translateY(0px);
            box-shadow: 0 0 15px rgba(0,255,255,0.5), 0 2px 10px rgba(0,0,0,0.3);
        }
        @keyframes gentlePulse {
            0%, 100% { box-shadow: 0 0 20px rgba(0,255,255,0.4), 0 4px 15px rgba(0,0,0,0.3); }
            50% { box-shadow: 0 0 35px rgba(0,255,255,0.7), 0 6px 20px rgba(0,0,0,0.4); }
        }
        
        /* Style Streamlit button for Start Again */
        .start-again-container button[kind="primary"] {
            font-family: 'Orbitron', 'Inter', sans-serif !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            color: #0f1419 !important;
            background: linear-gradient(135deg, #00ffff 0%, #00cccc 100%) !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 1rem 3rem !important;
            box-shadow: 0 0 20px rgba(0,255,255,0.4), 0 4px 15px rgba(0,0,0,0.3) !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            height: auto !important;
        }
        .start-again-container button[kind="primary"]:hover {
            background: linear-gradient(135deg, #00ffff 0%, #4dffff 100%) !important;
            box-shadow: 0 0 30px rgba(0,255,255,0.6), 0 6px 20px rgba(0,0,0,0.4) !important;
            transform: translateY(-2px) !important;
            animation: gentlePulse 1.5s ease-in-out infinite !important;
        }
        .start-again-container button[kind="primary"]:active {
            transform: translateY(0px) !important;
            box-shadow: 0 0 15px rgba(0,255,255,0.5), 0 2px 10px rgba(0,0,0,0.3) !important;
        }

        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    # Set page config - LOCK sidebar open
    st.set_page_config(
        page_title="Sniff Recon - Network Packet Analyzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_modern_css()

    # NO CANVAS/DIV INJECTION - Keep layout clean

    # Additional styles for locked sidebar and bright content
    st.markdown('''
        <style>
        /* LOCK SIDEBAR - Remove collapse button */
        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(15,15,30,0.98) 0%, rgba(10,10,20,0.98) 100%);
            border-right: none;
            min-width: 280px !important;
        }
        [data-testid="stSidebar"] button {
            background: linear-gradient(135deg, rgba(0,180,180,0.4), rgba(0,120,120,0.4)) !important;
            border: 2px solid rgba(0,255,255,0.5) !important;
            color: #00ffff !important;
            border-radius: 10px !important;
            padding: 0.7rem 1rem !important;
            margin: 0.4rem 0 !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stSidebar"] button:hover {
            background: linear-gradient(135deg, rgba(0,220,220,0.6), rgba(0,180,180,0.6)) !important;
            border-color: rgba(0,255,255,0.9) !important;
            box-shadow: 0 0 20px rgba(0,255,255,0.5) !important;
            transform: translateY(-2px);
        }
        /* Bright answer box */
        .answer-box {
            background: linear-gradient(145deg, rgba(10,50,60,0.98), rgba(10,40,50,0.98)) !important;
            border: 2px solid rgba(0,255,255,0.7) !important;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: #f0f8ff !important;
            box-shadow: 0 0 30px rgba(0,255,255,0.4), inset 0 0 20px rgba(0,255,255,0.15) !important;
            font-size: 1.1rem;
            line-height: 1.8;
        }
        .answer-box h4 {
            color: #00ffff !important;
            margin-bottom: 0.8rem;
            font-size: 1.4rem;
            font-weight: 700 !important;
            text-shadow: 0 0 12px rgba(0,255,255,0.7) !important;
        }
        .answer-box p {
            color: #e8f8ff !important;
            font-weight: 500 !important;
            margin-bottom: 0.7rem !important;
        }
        /* Sidebar question items */
        .help-question {
            background: rgba(0,100,100,0.3);
            border-left: 3px solid #00ffff;
            padding: 0.6rem 0.8rem;
            margin: 0.4rem 0;
            cursor: pointer;
            border-radius: 5px;
            color: #99ffff;
            font-size: 0.95rem;
            transition: all 0.2s;
        }
        .help-question:hover {
            background: rgba(0,150,150,0.5);
            border-left-color: #00ffff;
            box-shadow: 0 0 10px rgba(0,255,255,0.3);
            transform: translateX(5px);
        }
        </style>
    ''', unsafe_allow_html=True)

    # Main content
    # Title
    st.markdown('<h1 class="main-title fade-in-up">🔍 Sniff Recon</h1>', unsafe_allow_html=True)

    # Tagline
    tagline_text = "Advanced Network Packet Analyzer & AI-Powered Protocol Dissector"
    st.markdown(
        f'<p class="subtitle fade-in-up" style="margin-bottom: 2rem;">{tagline_text}</p>',
        unsafe_allow_html=True
    )

    # File uploader (check early to control sidebar visibility)
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="📁 Upload Packet Capture File",
        type=["pcap", "pcapng", "csv", "txt"],
        help="Supported formats: .pcap, .pcapng, .csv, .txt (Max: 200MB)",
        key="fileUploader",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar - only show if no file is uploaded
    if uploaded_file is None:
        with st.sidebar:
            st.markdown('<h3 style="color:#00ffff; margin-bottom:1.2rem; font-family: Orbitron,sans-serif; text-align: center; text-shadow: 0 0 12px rgba(0,255,255,0.6); font-size: 1.4rem;">Quick Access</h3>', unsafe_allow_html=True)
            
            # About button with TOGGLE
            if st.button("📖 About Sniff Recon", key="aboutBtn", use_container_width=True):
                # Toggle: if already showing about, hide it; otherwise show it
                current = st.session_state.get("show_section")
                if current == "about":
                    st.session_state["show_section"] = None  # Hide
                else:
                    st.session_state["show_section"] = "about"  # Show
            
            # Help section with questions
            st.markdown('<div style="margin-top: 1.5rem; padding-top: 1rem;"></div>', unsafe_allow_html=True)
            st.markdown('<h4 style="color:#00ffff; margin-bottom:0.8rem; font-family: Orbitron,sans-serif; font-size: 1.1rem;">❓ Help Topics</h4>', unsafe_allow_html=True)
            
            help_questions = [
                ("🔹 Why use Sniff Recon?", "why"),
                ("🔹 What files are supported?", "files"),
                ("🔹 Is AI required?", "ai"),
                ("🔹 File size limits?", "size"),
                ("🔹 How is data handled?", "data")
            ]
            
            for question, key in help_questions:
                if st.button(question, key=f"help_{key}", use_container_width=True):
                    # Toggle for help questions too
                    current = st.session_state.get("show_section")
                    section_key = f"help_{key}"
                    if current == section_key:
                        st.session_state["show_section"] = None  # Hide
                    else:
                        st.session_state["show_section"] = section_key  # Show

    # Show selected section content ONLY if no file is uploaded
    show_section = st.session_state.get("show_section")
    
    # Only show sidebar content if no file is being analyzed
    if show_section and uploaded_file is None:
        if show_section == "about":
            st.markdown('''
                <div class="answer-box fade-in-up">
                    <h4>📖 About Sniff Recon</h4>
                    <p>Sniff Recon is a powerful Streamlit-based network packet analyzer that supports PCAP, PCAPNG, CSV, and TXT file formats.</p>
                    <p>It provides comprehensive packet analysis with optional multi-provider AI assistance, memory-aware parsing, and clear visualizations to help you investigate network traffic quickly and safely.</p>
                    <p>Built with modern cybersecurity professionals in mind, it combines ease of use with powerful analysis capabilities.</p>
                </div>
            ''', unsafe_allow_html=True)
        
        elif show_section and show_section.startswith("help_"):
            help_answers = {
                "help_why": ("🔹 Why use Sniff Recon?", "Quickly parse network captures and highlight patterns, anomalies, and potential security threats with AI-assisted summaries. Get instant insights without complex command-line tools."),
                "help_files": ("🔹 Supported File Formats", "PCAP, PCAPNG, CSV, and TXT files are supported. CSV column names are automatically mapped when possible to ensure compatibility with various export formats."),
                "help_ai": ("🔹 AI Requirement", "No, AI is NOT required! The tool provides local statistical analysis that works perfectly without any API keys. AI features are optional enhancements."),
                "help_size": ("🔹 File Size Limits", "Maximum file size is 200MB to protect system memory. For larger captures, prefer trimming or filtering the capture file before analysis."),
                "help_data": ("🔹 Data Handling", "Summaries are saved to output/summary.json. All packet data is processed via temporary files and automatically cleaned up after analysis. Your data stays local and secure.")
            }
            
            if show_section in help_answers:
                title, answer = help_answers[show_section]
                st.markdown(f'''
                    <div class="answer-box fade-in-up">
                        <h4>{title}</h4>
                        <p>{answer}</p>
                    </div>
                ''', unsafe_allow_html=True)

    # Process uploaded file
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

            # Use Streamlit tabs with enhanced pill CSS (already in inject_modern_css)
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Packet Analysis", "🧠 AI Analysis", "📤 Export Results", "⚙️ Advanced Settings"])

            # Tab 1: Packet analysis  
            with tab1:
                st.markdown('<div class="section-heading">PACKET ANALYSIS</div>', unsafe_allow_html=True)
                from src.ui.display_packet_table import display_packet_table
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
                    from src.ai.ai_query_interface import render_ai_query_interface, render_ai_quick_analysis
                    import scapy.all as scapy
                    packets = scapy.rdpcap(tmp_file_path)
                    packets_list = list(packets)
                    render_ai_quick_analysis(packets_list)
                    render_ai_query_interface(packets_list)
                except Exception as e:
                    st.markdown(f'<div class=\"error-message\">❌ Error initializing AI analysis: {str(e)}</div>', unsafe_allow_html=True)
            
            # Tab 3: Export
            with tab3:
                st.markdown('<div class="section-heading">EXPORT ANALYSIS RESULTS</div>', unsafe_allow_html=True)
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
            
            # Tab 4: Advanced Settings
            with tab4:
                st.markdown("## ⚙️ Advanced Settings")
                st.info("Advanced settings coming soon! Let us know what options you'd like to see.")
            
            # Start Again Button (Footer)
            st.markdown('<div class="start-again-container">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 START AGAIN", key="start_again_btn", use_container_width=True):
                    # Clear all session state
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.markdown(f'<div class=\"error-message\">❌ Error processing file: {str(e)}</div>', unsafe_allow_html=True)
        finally:
            try:
                os.remove(tmp_file_path)
            except Exception:
                pass


if __name__ == "__main__":
    main()


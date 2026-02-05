"""
Settings Module
================
User-configurable settings for Sniff-Recon.
Stores settings in session state for security (no persistent storage of sensitive data).
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import os
import urllib.request
import urllib.error
import json
from src.ui.icons import icon


def get_available_ollama_models() -> List[str]:
    """Fetch available models from Ollama API."""
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    try:
        response = urllib.request.urlopen(f"{ollama_url}/api/tags", timeout=5)
        if response.status == 200:
            data = json.loads(response.read().decode())
            models = [model["name"] for model in data.get("models", [])]
            return models if models else ["qwen2.5-coder:7b"]
    except Exception:
        pass
    return ["qwen2.5-coder:7b", "llama3.2:3b", "mistral:7b"]


def init_settings() -> None:
    """Initialize default settings in session state."""
    defaults = {
        # AI Settings
        "ai_enabled": True,
        "ai_model": os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b"),
        "ai_temperature": 0.7,
        "ai_max_tokens": 500,
        
        # Display Settings
        "packets_per_page": 25,
        "default_sort": "Time",
        "show_hex_dump": True,
        
        # Export Settings  
        "default_export_format": "JSON",
        "include_metadata": True,
    }
    
    for key, value in defaults.items():
        if f"settings_{key}" not in st.session_state:
            st.session_state[f"settings_{key}"] = value


def get_setting(key: str) -> Any:
    """Get a setting value from session state."""
    init_settings()
    return st.session_state.get(f"settings_{key}")


def set_setting(key: str, value: Any) -> None:
    """Set a setting value in session state."""
    st.session_state[f"settings_{key}"] = value


def render_settings_page() -> None:
    """Render the settings interface."""
    init_settings()
    
    settings_icon = icon("settings", "lg")
    st.markdown(f"""
        <div class="sr-section-header">
            {settings_icon}
            <span>Settings</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Two column layout
    col1, col2 = st.columns(2)
    
    # === AI Settings ===
    with col1:
        brain_icon = icon("brain")
        st.markdown(f"""
            <div class="sr-settings-section">
                <div class="sr-settings-title">{brain_icon} AI Configuration</div>
            </div>
        """, unsafe_allow_html=True)
        
        # AI Enabled toggle
        ai_enabled = st.toggle(
            "Enable AI Features",
            value=get_setting("ai_enabled"),
            key="toggle_ai_enabled",
            help="Turn AI-powered analysis on or off"
        )
        set_setting("ai_enabled", ai_enabled)
        
        # Model Selection
        available_models = get_available_ollama_models()
        current_model = get_setting("ai_model")
        
        # Ensure current model is in list
        if current_model not in available_models:
            available_models.insert(0, current_model)
        
        selected_model = st.selectbox(
            "AI Model",
            options=available_models,
            index=available_models.index(current_model) if current_model in available_models else 0,
            key="select_ai_model",
            help="Select the Ollama model for AI analysis",
            disabled=not ai_enabled
        )
        set_setting("ai_model", selected_model)
        
        # Temperature
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=get_setting("ai_temperature"),
            step=0.1,
            key="slider_temperature",
            help="Higher = more creative, Lower = more focused",
            disabled=not ai_enabled
        )
        set_setting("ai_temperature", temperature)
        
        # Max tokens
        max_tokens = st.number_input(
            "Max Response Tokens",
            min_value=100,
            max_value=2000,
            value=get_setting("ai_max_tokens"),
            step=100,
            key="input_max_tokens",
            help="Maximum length of AI responses",
            disabled=not ai_enabled
        )
        set_setting("ai_max_tokens", max_tokens)
    
    # === Display Settings ===
    with col2:
        eye_icon = icon("eye")
        st.markdown(f"""
            <div class="sr-settings-section">
                <div class="sr-settings-title">{eye_icon} Display Settings</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Packets per page
        packets_options = [10, 25, 50, 100]
        packets_per_page = st.selectbox(
            "Packets Per Page",
            options=packets_options,
            index=packets_options.index(get_setting("packets_per_page")) if get_setting("packets_per_page") in packets_options else 1,
            key="select_packets_per_page",
            help="Number of packets to display per page"
        )
        set_setting("packets_per_page", packets_per_page)
        
        # Default sort
        sort_options = ["Time", "Source IP", "Destination IP", "Protocol", "Length"]
        default_sort = st.selectbox(
            "Default Sort Column",
            options=sort_options,
            index=sort_options.index(get_setting("default_sort")) if get_setting("default_sort") in sort_options else 0,
            key="select_default_sort"
        )
        set_setting("default_sort", default_sort)
        
        # Show hex dump
        show_hex = st.toggle(
            "Show Hex Dump in Inspector",
            value=get_setting("show_hex_dump"),
            key="toggle_hex_dump"
        )
        set_setting("show_hex_dump", show_hex)
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        # Export settings
        download_icon = icon("download")
        st.markdown(f"""
            <div class="sr-settings-section">
                <div class="sr-settings-title">{download_icon} Export Settings</div>
            </div>
        """, unsafe_allow_html=True)
        
        export_formats = ["JSON", "CSV", "TXT"]
        default_format = st.selectbox(
            "Default Export Format",
            options=export_formats,
            index=export_formats.index(get_setting("default_export_format")) if get_setting("default_export_format") in export_formats else 0,
            key="select_export_format"
        )
        set_setting("default_export_format", default_format)
        
        include_meta = st.toggle(
            "Include Metadata in Exports",
            value=get_setting("include_metadata"),
            key="toggle_metadata"
        )
        set_setting("include_metadata", include_meta)
    
    # Model refresh button
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    refresh_icon = icon("refresh")
    if st.button(f"🔄 Refresh Available Models", key="refresh_models"):
        # Force refresh
        st.cache_data.clear()
        st.rerun()
    
    # Status message
    st.markdown(f"""
        <div class="sr-alert sr-alert-info" style="margin-top: 1rem;">
            {icon("info")} Settings are stored in your session and will reset when you close the browser.
        </div>
    """, unsafe_allow_html=True)

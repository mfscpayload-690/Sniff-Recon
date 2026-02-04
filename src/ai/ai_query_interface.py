"""
AI Query Interface Module
=========================
Chat-like interface for AI-powered packet analysis.
Supports multiple AI providers with visual badges and clean UX.
"""

import streamlit as st
from typing import List, Dict, Any
from src.ai.ai_module import ai_engine, PacketSummary
from scapy.packet import Packet
import time
import os
from datetime import datetime
from src.ui.icons import icon


def get_provider_info(provider: str) -> tuple[str, str, str]:
    """Get badge info for provider: (icon_name, label, color class)."""
    provider_lower = provider.lower()
    
    if "ollama" in provider_lower:
        return "shield-check", "OFFLINE", "sr-status-online"
    elif "auto" in provider_lower or "balanced" in provider_lower:
        return "zap", "AUTO", "sr-provider-badge"
    elif "groq" in provider_lower:
        return "rocket", "GROQ", "sr-provider-badge"
    elif "openai" in provider_lower or "gpt" in provider_lower:
        return "sparkles", "OpenAI", "sr-provider-badge"
    elif "anthropic" in provider_lower or "claude" in provider_lower:
        return "brain", "Claude", "sr-provider-badge"
    elif "gemini" in provider_lower or "google" in provider_lower:
        return "sparkles", "Gemini", "sr-provider-badge"
    else:
        return "globe", "CLOUD", "sr-provider-badge"


def render_provider_selector() -> str:
    """Render AI provider selection with visual badges."""
    from src.ai.multi_agent_ai import get_active_providers
    
    # Initialize session state
    if 'selected_ai_provider' not in st.session_state:
        st.session_state.selected_ai_provider = "Auto (Load Balanced)"
    
    # Get active providers
    active_providers = get_active_providers()
    provider_options = ["Auto (Load Balanced)"] + list(active_providers)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected = st.selectbox(
            "AI Provider",
            options=provider_options,
            index=provider_options.index(st.session_state.selected_ai_provider) 
                  if st.session_state.selected_ai_provider in provider_options else 0,
            key="ai_provider_select",
            label_visibility="collapsed"
        )
        st.session_state.selected_ai_provider = selected
    
    with col2:
        icon_name, label, _ = get_provider_info(selected)
        provider_icon = icon(icon_name)
        if "ollama" in selected.lower():
            badge_style = "background: var(--accent-green-dim); color: var(--accent-green); border: 1px solid var(--accent-green);"
        else:
            badge_style = "background: var(--accent-purple-dim); color: var(--accent-purple); border: 1px solid var(--accent-purple);"
        
        st.markdown(f"""
            <div style="{badge_style} padding: 0.5rem 1rem; border-radius: 999px; text-align: center; font-weight: 600; font-size: 0.875rem;">
                {provider_icon} {label}
            </div>
        """, unsafe_allow_html=True)
    
    # Provider-specific info
    if "ollama" in selected.lower():
        shield_icon = icon("shield-check")
        st.info(f"{shield_icon} **Local Mode**: All analysis runs on your machine. No data sent externally.")
    
    return selected


def render_chat_messages() -> None:
    """Render the chat message history."""
    if 'ai_responses' not in st.session_state:
        st.session_state.ai_responses = []
    
    messages = st.session_state.ai_responses
    
    if not messages:
        bot_icon = icon("bot", "2xl")
        st.markdown(f"""
            <div style="text-align: center; padding: 2rem; color: var(--text-muted);">
                <div style="font-size: 2rem; margin-bottom: 1rem; color: var(--accent-purple);">{bot_icon}</div>
                <div>Ask a question about your packet data to start the conversation</div>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Chat container
    for msg in messages:
        query = msg.get('query', '')
        response = msg.get('response', {})
        timestamp = msg.get('timestamp', '')
        provider = msg.get('provider', 'AI')
        
        # User message
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
                <div style="max-width: 80%; background: var(--accent-cyan-dim); border: 1px solid var(--accent-cyan); 
                            border-radius: 16px 16px 4px 16px; padding: 1rem;">
                    <div style="color: var(--text-primary);">{query}</div>
                    <div style="color: var(--text-muted); font-size: 0.75rem; margin-top: 0.5rem; text-align: right;">
                        {timestamp}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # AI response
        response_text = response.get('analysis', response) if isinstance(response, dict) else str(response)
        icon_name, label, _ = get_provider_info(provider)
        provider_icon = icon(icon_name)
        
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
                <div style="max-width: 80%; background: var(--bg-tertiary); border: 1px solid var(--border-subtle); 
                            border-radius: 16px 16px 16px 4px; padding: 1rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="font-weight: 600; color: var(--accent-purple);">{provider_icon} {label}</span>
                    </div>
                    <div style="color: var(--text-primary); line-height: 1.6;">{response_text}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_suggested_queries() -> str:
    """Render suggested query buttons and return selected query."""
    suggestions = [
        "What protocols are being used?",
        "Are there any suspicious patterns?",
        "Show me the top talkers",
        "Summarize this traffic",
        "Find any anomalies"
    ]
    
    sparkles_icon = icon("sparkles")
    st.markdown(f"**{sparkles_icon} Quick Questions:**", unsafe_allow_html=True)
    
    cols = st.columns(len(suggestions))
    selected_query = None
    
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(suggestion, key=f"suggest_{i}", use_container_width=True):
                selected_query = suggestion
    
    return selected_query


def send_query(query: str, packets: List[Packet], provider: str) -> Dict[str, Any]:
    """Send query to AI and get response."""
    # Convert packets to summaries
    summaries = []
    for pkt in packets[:100]:  # Limit to 100 packets for context
        summary = PacketSummary(
            src_ip=str(pkt.src) if hasattr(pkt, 'src') else "",
            dst_ip=str(pkt.dst) if hasattr(pkt, 'dst') else "",
            protocol=str(pkt.payload.name) if hasattr(pkt, 'payload') else "Unknown",
            length=len(pkt),
            timestamp=float(pkt.time) if hasattr(pkt, 'time') else 0
        )
        summaries.append(summary)
    
    # Use AI engine
    try:
        if provider == "Auto (Load Balanced)":
            response = ai_engine.query(query, summaries)
        else:
            response = ai_engine.query(query, summaries, force_provider=provider)
        return response
    except Exception as e:
        return {"error": str(e), "analysis": f"Error: {str(e)}"}


def render_ai_query_interface(packets: List[Packet]) -> None:
    """Render the main AI query interface."""
    # Initialize session state
    if 'ai_responses' not in st.session_state:
        st.session_state.ai_responses = []
    
    # AI Panel Header
    st.markdown("""
        <div class="sr-ai-panel">
            <div class="sr-ai-header">
                <div class="sr-ai-title">
                    🤖 AI Assistant
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Provider selector
    selected_provider = render_provider_selector()
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Suggested queries
    suggested = render_suggested_queries()
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Chat messages
    render_chat_messages()
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Query input
    col1, col2 = st.columns([5, 1])
    
    with col1:
        # Use suggested query if clicked
        default_value = suggested if suggested else ""
        query = st.text_input(
            "Ask about your packets",
            value=default_value,
            placeholder="e.g., What protocols are most common?",
            key="ai_query_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_clicked = st.button("Send", key="send_query", use_container_width=True)
    
    # Handle query submission
    if (send_clicked or suggested) and query:
        with st.spinner("Analyzing packets..."):
            response = send_query(query, packets, selected_provider)
            
            # Add to chat history
            st.session_state.ai_responses.append({
                'query': query,
                'response': response,
                'provider': selected_provider,
                'timestamp': datetime.now().strftime("%H:%M")
            })
            
            st.rerun()
    
    # Clear chat button
    if st.session_state.ai_responses:
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.ai_responses = []
            st.rerun()


def render_ai_quick_analysis(packets: List[Packet]) -> None:
    """Render a quick AI analysis summary."""
    if not packets:
        return
    
    st.markdown("""
        <div class="sr-card" style="margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <span style="font-size: 1.5rem;">⚡</span>
                <span style="font-weight: 600; color: var(--accent-cyan);">Quick Stats</span>
            </div>
    """, unsafe_allow_html=True)
    
    # Calculate quick stats
    total = len(packets)
    protocols = {}
    ips = set()
    
    for pkt in packets[:1000]:  # Sample first 1000
        if hasattr(pkt, 'payload') and hasattr(pkt.payload, 'name'):
            proto = pkt.payload.name
            protocols[proto] = protocols.get(proto, 0) + 1
        if hasattr(pkt, 'src'):
            ips.add(str(pkt.src))
        if hasattr(pkt, 'dst'):
            ips.add(str(pkt.dst))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Packets", f"{total:,}")
    
    with col2:
        st.metric("Unique IPs", len(ips))
    
    with col3:
        top_proto = max(protocols, key=protocols.get) if protocols else "N/A"
        st.metric("Top Protocol", top_proto)
    
    st.markdown("</div>", unsafe_allow_html=True)
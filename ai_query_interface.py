"""
AI Query Interface for Streamlit

This module provides a beautiful Streamlit interface for AI-powered packet analysis queries.
"""

import streamlit as st
from typing import List, Dict, Any
from ai_module import ai_engine, PacketSummary
from scapy.packet import Packet
import time
import pandas as pd

def inject_ai_interface_css():
    """Inject CSS for the AI query interface"""
    st.markdown(
        """
        <style>
        /* AI Query Interface Styling */
        .ai-query-container {
            background: linear-gradient(145deg, rgba(30, 30, 30, 0.9), rgba(20, 20, 20, 0.9));
            border: 2px solid rgba(0, 255, 255, 0.3);
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
        }
        
        .ai-query-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: #00ffff;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .ai-query-header::before {
            content: '🤖';
            font-size: 1.3rem;
        }
        
        .query-input-container {
            background: rgba(15, 15, 15, 0.5);
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid rgba(0, 255, 255, 0.2);
            margin-bottom: 1rem;
        }
        
        .suggested-queries {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
        }
        
        .query-chip {
            background: linear-gradient(45deg, rgba(0, 255, 255, 0.1), rgba(0, 179, 179, 0.1));
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 20px;
            padding: 0.5rem 1rem;
            color: #00ffff;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }
        
        .query-chip:hover {
            background: linear-gradient(45deg, rgba(0, 255, 255, 0.2), rgba(0, 179, 179, 0.2));
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3);
        }
        
        .ai-response-container {
            background: linear-gradient(145deg, rgba(0, 255, 0, 0.05), rgba(0, 200, 0, 0.05));
            border: 2px solid rgba(0, 255, 0, 0.3);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            animation: fadeInUp 0.6s ease forwards;
        }
        
        .ai-response-header {
            font-size: 1.2rem;
            font-weight: 600;
            color: #00ff00;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .ai-response-header::before {
            content: '💡';
            font-size: 1.1rem;
        }
        
        .ai-response-content {
            color: #e0e0e0;
            line-height: 1.6;
            font-size: 1rem;
        }
        
        .ai-error-container {
            background: linear-gradient(145deg, rgba(255, 0, 0, 0.05), rgba(200, 0, 0, 0.05));
            border: 2px solid rgba(255, 0, 0, 0.3);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .ai-error-header {
            font-size: 1.2rem;
            font-weight: 600;
            color: #ff6666;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .ai-error-header::before {
            content: '⚠️';
            font-size: 1.1rem;
        }
        
        .loading-container {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            color: #00ffff;
        }
        
        .loading-spinner {
            border: 3px solid rgba(0, 255, 255, 0.3);
            border-top: 3px solid #00ffff;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin-right: 1rem;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
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
        
        /* Responsive design */
        @media (max-width: 768px) {
            .ai-query-container {
                padding: 1rem;
            }
            
            .suggested-queries {
                flex-direction: column;
            }
            
            .query-chip {
                text-align: center;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_ai_query_interface(packets: List[Packet]):
    """
    Render the AI query interface in Streamlit
    """
    # Inject CSS
    inject_ai_interface_css()
    
    # Initialize session state for AI responses
    if 'ai_responses' not in st.session_state:
        st.session_state.ai_responses = []
    
    # AI Query Section
    st.markdown('<div class="ai-query-container">', unsafe_allow_html=True)
    st.markdown('<div class="ai-query-header">AI-Powered Packet Analysis</div>', unsafe_allow_html=True)
    
    # Check API key status and show notification
    if not ai_engine.api_key_valid:
        st.warning(
            "⚠️ **API Key Issue Detected**: Your Hugging Face API key is invalid or missing. "
            "The app will provide local analysis instead. To enable AI-powered analysis, "
            "please update your `HUGGINGFACE_API_KEY` in the `.env` file. "
            "Get a free API key from [Hugging Face](https://huggingface.co/settings/tokens)."
        )
    
    st.markdown(
        "Ask questions about your network traffic in natural language. The AI will analyze the packet data and provide insights."
    )
    
    # Query input
    st.markdown('<div class="query-input-container">', unsafe_allow_html=True)
    
    # Get suggested queries
    suggested_queries = ai_engine.get_suggested_queries()
    
    # Display suggested queries as clickable chips
    st.markdown("**💡 Suggested Questions:**")
    st.markdown('<div class="suggested-queries">', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, query in enumerate(suggested_queries):
        col_idx = i % 2
        with cols[col_idx]:
            if st.button(query, key=f"suggested_{i}", help="Click to use this query"):
                st.session_state.user_query = query
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Query input field
    user_query = st.text_input(
        "🤖 Ask a question about your network traffic:",
        value=st.session_state.get('user_query', ''),
        placeholder="e.g., What are the top 5 source IP addresses?",
        key="ai_query_input"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Query button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        query_button = st.button(
            "🚀 Analyze with AI",
            type="primary",
            use_container_width=True,
            help="Send your question to the AI for analysis"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle AI query
    if query_button and user_query and packets:
        with st.spinner("🤖 AI is analyzing your network traffic..."):
            # Layered Filtering: Get suspicious, cluster, summarize
            suspicious = ai_engine.filter_suspicious_packets(packets)
            clusters = ai_engine.cluster_packets_by_ip(suspicious)
            triaged_summaries = ai_engine.summarize_clusters(clusters)

            if not triaged_summaries:
                st.warning("No suspicious packets found after triage. Using full summary for AI analysis.")
                packet_summary = ai_engine.extract_packet_statistics(packets)
            else:
                st.info(f"{len(triaged_summaries)} suspicious flows detected. Only summarizing these for AI.")
                packet_summary = PacketSummary(
                    total_packets=sum(x['packet_count'] for x in triaged_summaries),
                    unique_src_ips=[x['src_ip'] for x in triaged_summaries],
                    unique_dst_ips=[x['dst_ip'] for x in triaged_summaries],
                    protocol_distribution={},
                    top_src_ips={},
                    top_dst_ips={},
                    port_analysis={},
                    packet_sizes=[],
                    time_range=(0, 0),
                    suspicious_patterns=[pat for x in triaged_summaries for pat in x['suspicious_patterns']],
                )

            # Query AI
            ai_result = ai_engine.query_ai(user_query, packet_summary)
            
            # Store response in session state
            response_entry = {
                "query": user_query,
                "result": ai_result,
                "timestamp": time.time()
            }
            st.session_state.ai_responses.append(response_entry)
            
            # Clear the input
            st.session_state.user_query = ""
            st.rerun()
    
    # Display AI responses
    if st.session_state.ai_responses:
        st.markdown("## 📊 AI Analysis Results")
        
        for i, response_entry in enumerate(reversed(st.session_state.ai_responses)):
            result = response_entry["result"]
            query = response_entry["query"]
            
            if result.get("success"):
                # Success response
                header_text = "AI Analysis"
                header_icon = "🤖"
                
                # Check if this is a fallback response
                if result.get("fallback"):
                    header_text = "Local Analysis (AI Unavailable)"
                    header_icon = "📊"
                
                st.markdown(
                    f"""
                    <div class="ai-response-container">
                        <div class="ai-response-header">{header_icon} {header_text}</div>
                        <div style="margin-bottom: 1rem; color: #00b3b3; font-weight: 500;">
                            <strong>Question:</strong> {query}
                        </div>
                        <div class="ai-response-content">
                            {result["response"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Error response
                st.markdown(
                    f"""
                    <div class="ai-error-container">
                        <div class="ai-error-header">AI Analysis Error</div>
                        <div style="margin-bottom: 1rem; color: #00b3b3; font-weight: 500;">
                            <strong>Question:</strong> {query}
                        </div>
                        <div style="color: #ff6666;">
                            <strong>Error:</strong> {result.get("error", "Unknown error")}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Add a small separator
            if i < len(st.session_state.ai_responses) - 1:
                st.markdown("---")
        
        # Clear responses button
        if st.button("🗑️ Clear All Responses", type="secondary"):
            st.session_state.ai_responses = []
            st.rerun()

def render_ai_quick_analysis(packets: List[Packet]):
    """
    Render a quick AI analysis summary
    """
    if not packets:
        return
    
    # Extract basic statistics
    packet_summary = ai_engine.extract_packet_statistics(packets)
    
    st.markdown("## 🤖 Quick AI Analysis")
    
    # Create columns for statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Packets", packet_summary.total_packets)
        st.metric("Unique Source IPs", len(packet_summary.unique_src_ips))
    
    with col2:
        st.metric("Unique Dest IPs", len(packet_summary.unique_dst_ips))
        avg_size = sum(packet_summary.packet_sizes) / len(packet_summary.packet_sizes) if packet_summary.packet_sizes else 0
        st.metric("Avg Packet Size", f"{avg_size:.1f} bytes")
    
    with col3:
        # Most common protocol
        if packet_summary.protocol_distribution:
            top_protocol = max(packet_summary.protocol_distribution.items(), key=lambda x: x[1])
            st.metric("Top Protocol", f"{top_protocol[0]} ({top_protocol[1]})")
        
        # Suspicious patterns
        st.metric("Suspicious Patterns", len(packet_summary.suspicious_patterns))
    
    # Protocol distribution chart
    if packet_summary.protocol_distribution:
        st.markdown("### 📊 Protocol Distribution")
        protocol_df = pd.DataFrame(
            list(packet_summary.protocol_distribution.items()),
            columns=["Protocol", "Count"]
        )
        st.bar_chart(protocol_df.set_index("Protocol"))
    
    # Top IPs
    if packet_summary.top_src_ips:
        st.markdown("### 🌐 Top Source IPs")
        top_src_df = pd.DataFrame(
            list(packet_summary.top_src_ips.items())[:5],
            columns=["IP Address", "Packet Count"]
        )
        st.dataframe(top_src_df, use_container_width=True) 
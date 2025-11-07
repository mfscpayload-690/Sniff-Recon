"""
AI Module for Sniff Recon - Network Log Analyzer

This module provides natural language querying capabilities for packet analysis
using the Groq API.
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import pandas as pd
from scapy.packet import Packet
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import logging
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import multi-agent system
try:
    from src.ai.multi_agent_ai import multi_agent, query_ai_async, get_active_providers, get_suggested_queries
    USE_MULTI_AGENT = True
    logger.info("Multi-agent AI system loaded successfully")
except ImportError as e:
    logger.warning(f"Multi-agent system not available: {e}")
    USE_MULTI_AGENT = False

@dataclass
class PacketSummary:
    """Data class for packet summary statistics"""
    total_packets: int
    unique_src_ips: List[str]
    unique_dst_ips: List[str]
    protocol_distribution: Dict[str, int]
    top_src_ips: Dict[str, int]
    top_dst_ips: Dict[str, int]
    port_analysis: Dict[str, List[int]]
    packet_sizes: List[int]
    time_range: tuple
    suspicious_patterns: List[str]

class AIQueryEngine:
    """
    AI-powered query engine for natural language packet analysis
    """

    def filter_suspicious_packets(self, packets: List[Packet]) -> List[Packet]:
        """
        First pass: Return only the packets considered suspicious (layer 1 triage)
        Safer: Only applies rules to packets WITH an IP layer (others are just ignored or marked explicitly).
        """
        suspicious = []
        syn_counts = {}
        for pkt in packets:
            is_suspicious = False
            # Skip packets with no IP layer (broadcasts, ARP, etc.) - but optionally you could flag them.
            if IP not in pkt:
                continue
            # Malformed packet (catch scapy error or missing layers)
            try:
                if pkt is None or pkt.__class__.__name__ == 'NoPayload':
                    is_suspicious = True
            except Exception:
                is_suspicious = True
            # SYN rate (potential scan)
            if TCP in pkt:
                if pkt[TCP].flags & 0x02:  # SYN flag
                    syn_counts[pkt[IP].src] = syn_counts.get(pkt[IP].src, 0) + 1
                    if syn_counts[pkt[IP].src] > 10:
                        is_suspicious = True
            # Bad/odd port usage
            bad_ports = {0, 65535, 31337, 6667}
            if TCP in pkt and pkt[TCP].dport in bad_ports:
                is_suspicious = True
            if UDP in pkt and pkt[UDP].dport in bad_ports:
                is_suspicious = True
            # Weird protocols - could add more rules here
            # (e.g., very rare protocols)
            if is_suspicious:
                suspicious.append(pkt)
        return suspicious

    def cluster_packets_by_ip(self, suspicious_packets: List[Packet]) -> dict:
        """
        Second pass: Cluster suspicious packets by (src,dst) tuple.
        Ignores packets without an IP layer (should already be filtered out, but double check for safety).
        Returns dict of {(src,dst): [packets]}
        """
        clusters = {}
        for pkt in suspicious_packets:
            if IP not in pkt:
                continue    # Defensive, should not happen
            src = pkt[IP].src
            dst = pkt[IP].dst
            key = (src, dst)
            if key not in clusters:
                clusters[key] = []
            clusters[key].append(pkt)
        return clusters

    def summarize_clusters(self, clusters: dict) -> list:
        """
        Third pass: Summarize each group for LLM input
        Returns a list of dicts with group stats
        """
        summaries = []
        for (src, dst), pkts in clusters.items():
            summary = {
                'src_ip': src,
                'dst_ip': dst,
                'packet_count': len(pkts),
                'protocols': list(set([pkt[IP].proto for pkt in pkts if IP in pkt])),
                'ports': list(set([pkt[TCP].dport for pkt in pkts if TCP in pkt] + [pkt[UDP].dport for pkt in pkts if UDP in pkt])),
                'suspicious_patterns': [str(pkt.summary()) for pkt in pkts[:5]],
            }
            summaries.append(summary)
        return summaries

    def __init__(self):
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

        if not self.api_key or self.api_key == "your_groq_api_key_here":
            logger.warning("GROQ_API_KEY not found or invalid in environment variables")
            self.api_key = None
        elif self.api_key:
            logger.info(f"Groq API key loaded.")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "Content-Type": "application/json"
        }
        
        # Test API key validity
        self.api_key_valid = self._test_api_key()
        
        # Common query templates for better AI responses
        self.query_templates = {
            "top_ips": "Analyze the network traffic and identify the top {count} source IP addresses by packet count.",
            "protocol_analysis": "What protocols are being used in this network traffic? Provide a breakdown.",
            "suspicious_activity": "Analyze this network traffic for any suspicious or anomalous patterns.",
            "port_analysis": "What are the most common destination ports in this traffic?",
            "traffic_summary": "Provide a comprehensive summary of this network traffic analysis.",
            "intrusion_detection": "Look for signs of potential intrusion attempts or malicious activity."
        }
    
    def _test_api_key(self) -> bool:
        """Test if the API key is valid"""
        if not self.api_key:
            return False
        
        try:
            # Groq uses the OpenAI-compatible models endpoint for key validation
            response = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error testing Groq API key: {e}")
            return False
    
    
    def extract_packet_statistics(self, packets: List[Packet]) -> PacketSummary:
        """
        Extract comprehensive statistics from packet list for AI analysis
        """
        if not packets:
            return PacketSummary(0, [], [], {}, {}, {}, {}, [], (0, 0), [])
        
        # Basic statistics
        total_packets = len(packets)
        src_ips = []
        dst_ips = []
        protocols = {}
        src_ip_counts = {}
        dst_ip_counts = {}
        port_analysis = {"tcp": [], "udp": []}
        packet_sizes = []
        timestamps = []
        suspicious_patterns = []
        
        for pkt in packets:
            # Packet size
            packet_sizes.append(len(pkt))
            
            # Timestamp
            if hasattr(pkt, 'time'):
                timestamps.append(float(pkt.time))
            
            # IP layer analysis
            if IP in pkt:
                ip_layer = pkt[IP]
                src_ip = ip_layer.src
                dst_ip = ip_layer.dst
                
                src_ips.append(src_ip)
                dst_ips.append(dst_ip)
                
                # Count IPs
                src_ip_counts[src_ip] = src_ip_counts.get(src_ip, 0) + 1
                dst_ip_counts[dst_ip] = dst_ip_counts.get(dst_ip, 0) + 1
                
                # Protocol analysis
                proto_num = ip_layer.proto
                if proto_num == 6:
                    protocol = "TCP"
                elif proto_num == 17:
                    protocol = "UDP"
                elif proto_num == 1:
                    protocol = "ICMP"
                else:
                    protocol = f"Protocol_{proto_num}"
                
                protocols[protocol] = protocols.get(protocol, 0) + 1
                
                # Port analysis
                if TCP in pkt:
                    port_analysis["tcp"].append(pkt[TCP].dport)
                elif UDP in pkt:
                    port_analysis["udp"].append(pkt[UDP].dport)
                
                # Suspicious pattern detection
                if self._detect_suspicious_pattern(pkt):
                    suspicious_patterns.append(f"Suspicious activity from {src_ip} to {dst_ip}")
            
            elif Ether in pkt:
                protocols["Ethernet"] = protocols.get("Ethernet", 0) + 1
        
        # Get unique IPs
        unique_src_ips = list(set(src_ips))
        unique_dst_ips = list(set(dst_ips))
        
        # Sort top IPs
        top_src_ips = dict(sorted(src_ip_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        top_dst_ips = dict(sorted(dst_ip_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        
        # Time range
        time_range = (min(timestamps) if timestamps else 0, max(timestamps) if timestamps else 0)
        
        return PacketSummary(
            total_packets=total_packets,
            unique_src_ips=unique_src_ips,
            unique_dst_ips=unique_dst_ips,
            protocol_distribution=protocols,
            top_src_ips=top_src_ips,
            top_dst_ips=top_dst_ips,
            port_analysis=port_analysis,
            packet_sizes=packet_sizes,
            time_range=time_range,
            suspicious_patterns=suspicious_patterns
        )
    
    def _detect_suspicious_pattern(self, pkt: Packet) -> bool:
        """
        Detect suspicious patterns in packets
        """
        if IP not in pkt:
            return False
        
        # Check for common suspicious ports
        suspicious_ports = {22, 23, 3389, 445, 135, 139, 1433, 1521, 3306, 5432}
        
        if TCP in pkt:
            if pkt[TCP].dport in suspicious_ports:
                return True
            # Check for port scanning patterns
            if pkt[TCP].flags & 0x02:  # SYN flag
                return True
        
        # Check for ICMP (ping sweeps)
        if ICMP in pkt:
            return True
        
        return False
    
    def format_data_for_ai(self, packet_summary: PacketSummary) -> str:
        """
        Format packet data into a readable string for AI analysis
        """
        data_str = f"""
Network Traffic Analysis Data:

Total Packets: {packet_summary.total_packets}
Time Range: {packet_summary.time_range[0]:.2f} to {packet_summary.time_range[1]:.2f}

Protocol Distribution:
{json.dumps(packet_summary.protocol_distribution, indent=2)}

Top 5 Source IPs:
{json.dumps(dict(list(packet_summary.top_src_ips.items())[:5]), indent=2)}

Top 5 Destination IPs:
{json.dumps(dict(list(packet_summary.top_dst_ips.items())[:5]), indent=2)}

Port Analysis:
- TCP Ports: {list(set(packet_summary.port_analysis.get('tcp', [])))[:10]}
- UDP Ports: {list(set(packet_summary.port_analysis.get('udp', [])))[:10]}

Packet Size Statistics:
- Average: {sum(packet_summary.packet_sizes) / len(packet_summary.packet_sizes) if packet_summary.packet_sizes else 0:.2f} bytes
- Min: {min(packet_summary.packet_sizes) if packet_summary.packet_sizes else 0} bytes
- Max: {max(packet_summary.packet_sizes) if packet_summary.packet_sizes else 0} bytes

Suspicious Patterns Detected:
{chr(10).join(packet_summary.suspicious_patterns) if packet_summary.suspicious_patterns else "None detected"}
"""
        return data_str
    
    def query_ai_with_packets(self, user_query: str, packets: List[Packet]) -> Dict[str, Any]:
        """
        Send query to AI system with actual packet data (for multi-agent system)
        """
        # Try multi-agent system first if available
        if USE_MULTI_AGENT and hasattr(multi_agent, 'active_providers') and multi_agent.active_providers:  # type: ignore[possibly-unbound]
            try:
                # Use async query with actual packets
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(query_ai_async(user_query, packets))  # type: ignore[possibly-unbound]
                    if result.get('success'):
                        return result
                    else:
                        logger.warning(f"Multi-agent query failed: {result.get('error')}")
                except Exception as e:
                    logger.error(f"Multi-agent async query error: {e}")
                finally:
                    loop.close()
                    
            except Exception as e:
                logger.error(f"Multi-agent system error: {e}")
        
        # Fallback to original Groq implementation with packet summary
        packet_summary = self.extract_packet_statistics(packets)
        return self.query_ai(user_query, packet_summary)
    
    def query_ai(self, user_query: str, packet_summary: PacketSummary) -> Dict[str, Any]:
        """
        Send query to AI system (multi-agent or fallback to Groq)
        
        Note: This is the legacy method kept for backward compatibility.
        Use query_ai_with_packets() for direct packet analysis instead.
        """
        # Try multi-agent system first if available
        if USE_MULTI_AGENT and hasattr(multi_agent, 'active_providers') and multi_agent.active_providers:  # type: ignore[possibly-unbound]
            try:
                # Legacy: Uses empty packet list for compatibility with PacketSummary-based queries
                dummy_packets = []
                
                # Use async query with run_until_complete for sync compatibility
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(query_ai_async(user_query, dummy_packets))  # type: ignore[possibly-unbound]
                    if result.get('success'):
                        return result
                    else:
                        logger.warning(f"Multi-agent query failed: {result.get('error')}")
                except Exception as e:
                    logger.error(f"Multi-agent async query error: {e}")
                finally:
                    loop.close()
                    
            except Exception as e:
                logger.error(f"Multi-agent system error: {e}")
        
        # Fallback to original Groq implementation
        if not self.api_key_valid:
            return self._provide_fallback_analysis(user_query, packet_summary)

        try:
            data_context = self.format_data_for_ai(packet_summary)
            
            system_prompt = "You are a network security analyst. Analyze the following network traffic data and answer the user's question."
            user_prompt = f"""Network Data:
{data_context}

User Question: {user_query}

Please provide a clear, concise, and professional analysis. Focus on security implications and actionable insights."""

            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.7,
            }

            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content'].strip()
                
                return {
                    "success": True,
                    "response": ai_response,
                    "query": user_query,
                    "confidence": 0.9
                }
            
            else:
                logger.error(f"API request failed with status {response.status_code}: {response.text}")
                return self._provide_fallback_analysis(user_query, packet_summary)

        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            return self._provide_fallback_analysis(user_query, packet_summary)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return self._provide_fallback_analysis(user_query, packet_summary)
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to parse Groq response: {e}")
            return self._provide_fallback_analysis(user_query, packet_summary)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return self._provide_fallback_analysis(user_query, packet_summary)
    
    def _provide_fallback_analysis(self, user_query: str, packet_summary: PacketSummary) -> Dict[str, Any]:
        """
        Provide fallback analysis when AI API is unavailable
        """
        query_lower = user_query.lower()
        
        if "top" in query_lower and ("ip" in query_lower or "address" in query_lower):
            # Top IP analysis
            top_src = list(packet_summary.top_src_ips.items())[:5]
            top_dst = list(packet_summary.top_dst_ips.items())[:5]
            
            response = f"""**Top IP Addresses Analysis:**

**Top 5 Source IPs:**
{chr(10).join([f"- {ip}: {count} packets" for ip, count in top_src])}

**Top 5 Destination IPs:**
{chr(10).join([f"- {ip}: {count} packets" for ip, count in top_dst])}

*Note: This is a local analysis as the AI service is currently unavailable.*"""
            
        elif "suspicious" in query_lower or "unusual" in query_lower or "anomaly" in query_lower:
            # Suspicious activity analysis
            suspicious_count = len(packet_summary.suspicious_patterns)
            protocols = packet_summary.protocol_distribution
            
            response = f"""**Suspicious Activity Analysis:**

**Suspicious Patterns Detected:** {suspicious_count}
**Protocol Distribution:** {protocols}

**Security Insights:**
- Monitor traffic from unusual ports
- Check for port scanning patterns
- Review ICMP traffic for ping sweeps
- Investigate connections to suspicious IPs

*Note: This is a local analysis as the AI service is currently unavailable.*"""
            
        elif "protocol" in query_lower:
            # Protocol analysis
            protocols = packet_summary.protocol_distribution
            response = f"""**Protocol Analysis:**

**Protocol Distribution:**
{chr(10).join([f"- {proto}: {count} packets" for proto, count in protocols.items()])}

**Analysis:**
- Most common protocol: {max(protocols.items(), key=lambda x: x[1])[0] if protocols else 'N/A'}
- Total unique protocols: {len(protocols)}

*Note: This is a local analysis as the AI service is currently unavailable.*"""
            
        elif "port" in query_lower:
            # Port analysis
            tcp_ports = set(packet_summary.port_analysis.get('tcp', []))
            udp_ports = set(packet_summary.port_analysis.get('udp', []))
            
            response = f"""**Port Analysis:**

**TCP Ports:** {sorted(list(tcp_ports))[:10]}
**UDP Ports:** {sorted(list(udp_ports))[:10]}

**Common Ports Analysis:**
- HTTP/HTTPS (80/443): {'Present' if 80 in tcp_ports or 443 in tcp_ports else 'Not detected'}
- SSH (22): {'Present' if 22 in tcp_ports else 'Not detected'}
- DNS (53): {'Present' if 53 in udp_ports else 'Not detected'}

*Note: This is a local analysis as the AI service is currently unavailable.*"""
            
        else:
            # General summary
            response = f"""**Network Traffic Summary:**

**Basic Statistics:**
- Total Packets: {packet_summary.total_packets}
- Unique Source IPs: {len(packet_summary.unique_src_ips)}
- Unique Destination IPs: {len(packet_summary.unique_dst_ips)}
- Protocols: {list(packet_summary.protocol_distribution.keys())}
- Suspicious Patterns: {len(packet_summary.suspicious_patterns)}

**Recommendations:**
- Review traffic patterns for anomalies
- Monitor suspicious IP addresses
- Check for unusual port usage
- Investigate ICMP traffic

*Note: This is a local analysis as the AI service is currently unavailable. To enable AI-powered analysis, please set up your GROQ_API_KEY in the .env file.*"""
        
        return {
            "success": True,
            "response": response,
            "query": user_query,
            "confidence": 0.7,
            "fallback": True
        }
    
    def get_suggested_queries(self) -> List[str]:
        """
        Get a list of suggested queries for users
        """
        return [
            "What are the top 5 source IP addresses?",
            "Are there any suspicious patterns in this traffic?",
            "What protocols are being used most frequently?",
            "Show me the most common destination ports",
            "Is there any evidence of port scanning?",
            "Summarize the overall network activity",
            "Are there any potential security threats?",
            "What is the average packet size?",
            "Show me unusual traffic patterns",
            "Are there any failed connection attempts?"
        ]

# Global instance for easy access
ai_engine = AIQueryEngine() 
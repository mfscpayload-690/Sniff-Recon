"""
AI Module for Sniff Recon - Network Log Analyzer

This module provides natural language querying capabilities for packet analysis
using the Hugging Face Inference API with Mistral-7B-Instruct-v0.2 model.
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

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        if not self.api_key:
            logger.warning("HUGGINGFACE_API_KEY not found in environment variables")
            self.api_key = "YOUR_HF_API_KEY"  # Placeholder for development
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Common query templates for better AI responses
        self.query_templates = {
            "top_ips": "Analyze the network traffic and identify the top {count} source IP addresses by packet count.",
            "protocol_analysis": "What protocols are being used in this network traffic? Provide a breakdown.",
            "suspicious_activity": "Analyze this network traffic for any suspicious or anomalous patterns.",
            "port_analysis": "What are the most common destination ports in this traffic?",
            "traffic_summary": "Provide a comprehensive summary of this network traffic analysis.",
            "intrusion_detection": "Look for signs of potential intrusion attempts or malicious activity."
        }
    
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
    
    def query_ai(self, user_query: str, packet_summary: PacketSummary) -> Dict[str, Any]:
        """
        Send query to Hugging Face API and get response
        """
        try:
            # Format the data for AI
            data_context = self.format_data_for_ai(packet_summary)
            
            # Create the prompt
            prompt = f"""You are a network security analyst. Analyze the following network traffic data and answer the user's question.

Network Data:
{data_context}

User Question: {user_query}

Please provide a clear, concise, and professional analysis. Focus on security implications and actionable insights."""

            # Prepare the request payload
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                }
            }
            
            # Make the API request
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract the generated text
                if isinstance(result, list) and len(result) > 0:
                    ai_response = result[0].get('generated_text', '')
                    # Remove the prompt from the response
                    if prompt in ai_response:
                        ai_response = ai_response.replace(prompt, '').strip()
                else:
                    ai_response = str(result)
                
                return {
                    "success": True,
                    "response": ai_response,
                    "query": user_query,
                    "confidence": 0.9
                }
            
            else:
                logger.error(f"API request failed with status {response.status_code}: {response.text}")
                return {
                    "success": False,
                    "error": f"API request failed: {response.status_code}",
                    "query": user_query
                }
                
        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            return {
                "success": False,
                "error": "Request timed out. Please try again.",
                "query": user_query
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
                "query": user_query
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "query": user_query
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
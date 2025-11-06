#!/usr/bin/env python3
"""
Multi-Agent AI System for Sniff Recon
Supports multiple AI providers with intelligent load balancing and chunking for large files
"""

import os
import json
import requests
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod
import pandas as pd
from scapy.packet import Packet
from scapy.layers.inet import IP, TCP, UDP, ICMP
import logging
from dotenv import load_dotenv
import time
import hashlib
from concurrent.futures import ThreadPoolExecutor
import math

# Load environment variables
load_dotenv('/app/.env')  # Explicitly load from Docker mounted path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AIResponse:
    """Standardized AI response format"""
    success: bool
    response: str
    error: Optional[str] = None
    provider: Optional[str] = None
    tokens_used: Optional[int] = None
    response_time: Optional[float] = None
    chunk_id: Optional[str] = None

@dataclass
class PacketChunk:
    """Packet data chunk for processing"""
    chunk_id: str
    packets: List[Packet]
    summary: Dict[str, Any]
    size_mb: float
    packet_count: int

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def __init__(self, api_key: str, model_name: str = None):
        pass
    
    @abstractmethod
    async def query(self, prompt: str, context: str = None) -> AIResponse:
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def max_tokens(self) -> int:
        pass

class GroqProvider(AIProvider):
    """Groq AI Provider"""
    
    def __init__(self, api_key: str, model_name: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model_name = model_name
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    @property
    def name(self) -> str:
        return "Groq"
    
    @property
    def max_tokens(self) -> int:
        return 8192
    
    def test_connection(self) -> bool:
        try:
            response = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Groq connection test failed: {e}")
            return False
    
    async def query(self, prompt: str, context: str = None) -> AIResponse:
        start_time = time.time()
        
        messages = [
            {"role": "system", "content": "You are a network security expert analyzing packet capture data. Provide detailed, actionable insights."}
        ]
        
        if context:
            messages.append({"role": "user", "content": f"Context:\n{context}"})
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": 4000,
            "temperature": 0.1,
            "stream": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        response_time = time.time() - start_time
                        
                        return AIResponse(
                            success=True,
                            response=data["choices"][0]["message"]["content"],
                            provider=self.name,
                            tokens_used=data.get("usage", {}).get("total_tokens"),
                            response_time=response_time
                        )
                    else:
                        error_text = await response.text()
                        return AIResponse(
                            success=False,
                            response="",
                            error=f"HTTP {response.status}: {error_text}",
                            provider=self.name
                        )
        
        except Exception as e:
            return AIResponse(
                success=False,
                response="",
                error=str(e),
                provider=self.name
            )

class OpenAIProvider(AIProvider):
    """OpenAI Provider"""
    
    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model_name = model_name
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    @property
    def name(self) -> str:
        return "OpenAI"
    
    @property
    def max_tokens(self) -> int:
        return 4096 if "gpt-3.5" in self.model_name else 8192
    
    def test_connection(self) -> bool:
        try:
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {e}")
            return False
    
    async def query(self, prompt: str, context: str = None) -> AIResponse:
        start_time = time.time()
        
        messages = [
            {"role": "system", "content": "You are a network security expert analyzing packet capture data. Provide detailed, actionable insights."}
        ]
        
        if context:
            messages.append({"role": "user", "content": f"Context:\n{context}"})
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": 3000,
            "temperature": 0.1
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        response_time = time.time() - start_time
                        
                        return AIResponse(
                            success=True,
                            response=data["choices"][0]["message"]["content"],
                            provider=self.name,
                            tokens_used=data.get("usage", {}).get("total_tokens"),
                            response_time=response_time
                        )
                    else:
                        error_text = await response.text()
                        return AIResponse(
                            success=False,
                            response="",
                            error=f"HTTP {response.status}: {error_text}",
                            provider=self.name
                        )
        
        except Exception as e:
            return AIResponse(
                success=False,
                response="",
                error=str(e),
                provider=self.name
            )

class AnthropicProvider(AIProvider):
    """Anthropic Claude Provider"""
    
    def __init__(self, api_key: str, model_name: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key
        self.model_name = model_name
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
    
    @property
    def name(self) -> str:
        return "Anthropic"
    
    @property
    def max_tokens(self) -> int:
        return 4096
    
    def test_connection(self) -> bool:
        # Anthropic doesn't have a simple models endpoint, so we'll test with a minimal request
        try:
            payload = {
                "model": self.model_name,
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hello"}]
            }
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Anthropic connection test failed: {e}")
            return False
    
    async def query(self, prompt: str, context: str = None) -> AIResponse:
        start_time = time.time()
        
        content = "You are a network security expert analyzing packet capture data. Provide detailed, actionable insights.\n\n"
        if context:
            content += f"Context:\n{context}\n\n"
        content += prompt
        
        payload = {
            "model": self.model_name,
            "max_tokens": 3000,
            "messages": [{"role": "user", "content": content}]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        response_time = time.time() - start_time
                        
                        return AIResponse(
                            success=True,
                            response=data["content"][0]["text"],
                            provider=self.name,
                            tokens_used=data.get("usage", {}).get("input_tokens", 0) + data.get("usage", {}).get("output_tokens", 0),
                            response_time=response_time
                        )
                    else:
                        error_text = await response.text()
                        return AIResponse(
                            success=False,
                            response="",
                            error=f"HTTP {response.status}: {error_text}",
                            provider=self.name
                        )
        
        except Exception as e:
            return AIResponse(
                success=False,
                response="",
                error=str(e),
                provider=self.name
            )

class GoogleGeminiProvider(AIProvider):
    """Google Gemini AI Provider"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    @property
    def name(self) -> str:
        return "Google Gemini"
    
    @property
    def max_tokens(self) -> int:
        return 8192  # Gemini Flash supports up to 8K output tokens
    
    def test_connection(self) -> bool:
        try:
            # Test with a minimal request
            test_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": "Hello"}]}],
                "generationConfig": {"maxOutputTokens": 10}
            }
            response = requests.post(
                test_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Google Gemini connection test failed: {e}")
            return False
    
    async def query(self, prompt: str, context: str = None) -> AIResponse:
        start_time = time.time()
        
        # Build the full prompt
        full_prompt = "You are a network security expert analyzing packet capture data. Provide detailed, actionable insights.\n\n"
        if context:
            full_prompt += f"Context:\n{context}\n\n"
        full_prompt += prompt
        
        # Gemini API format
        api_url_with_key = f"{self.api_url}?key={self.api_key}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": full_prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 4000,
                "topP": 0.95,
                "topK": 40
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    api_url_with_key,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        response_time = time.time() - start_time
                        
                        # Extract text from Gemini response format
                        response_text = data["candidates"][0]["content"]["parts"][0]["text"]
                        
                        # Gemini uses different token counting
                        tokens_used = data.get("usageMetadata", {}).get("totalTokenCount", 0)
                        
                        return AIResponse(
                            success=True,
                            response=response_text,
                            provider=self.name,
                            tokens_used=tokens_used,
                            response_time=response_time
                        )
                    else:
                        error_text = await response.text()
                        return AIResponse(
                            success=False,
                            response="",
                            error=f"HTTP {response.status}: {error_text}",
                            provider=self.name
                        )
        
        except Exception as e:
            return AIResponse(
                success=False,
                response="",
                error=str(e),
                provider=self.name
            )

class MultiAgentAI:
    """Multi-Agent AI System with load balancing and chunking"""
    
    def __init__(self):
        self.providers: List[AIProvider] = []
        self.active_providers: List[AIProvider] = []
        self.chunk_size_mb = 5  # Process 5MB chunks
        self.max_packets_per_chunk = 5000  # Max packets per chunk
        
        # Initialize providers from environment variables
        self._initialize_providers()
        
        # Test provider connections
        self._test_providers()
        
        logger.info(f"Initialized {len(self.active_providers)} active AI providers")
    
    def _initialize_providers(self):
        """Initialize AI providers from environment variables"""
        
        # Groq
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key and groq_key != "your_groq_api_key_here":
            groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
            self.providers.append(GroqProvider(groq_key, groq_model))
        
        # OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key != "your_openai_api_key_here":
            openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            self.providers.append(OpenAIProvider(openai_key, openai_model))
        
        # Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key and anthropic_key != "your_anthropic_api_key_here":
            anthropic_model = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
            self.providers.append(AnthropicProvider(anthropic_key, anthropic_model))
        
        # Google Gemini
        google_key = os.getenv("GOOGLE_API_KEY")
        if google_key and google_key != "your_google_api_key_here":
            google_model = os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")
            self.providers.append(GoogleGeminiProvider(google_key, google_model))
    
    def _test_providers(self):
        """Test provider connections and populate active providers"""
        self.active_providers = []
        
        with ThreadPoolExecutor(max_workers=len(self.providers)) as executor:
            futures = {executor.submit(provider.test_connection): provider for provider in self.providers}
            
            for future in futures:
                provider = futures[future]
                try:
                    if future.result():
                        self.active_providers.append(provider)
                        logger.info(f"✅ {provider.name} provider is active")
                    else:
                        logger.warning(f"❌ {provider.name} provider connection failed")
                except Exception as e:
                    logger.error(f"❌ {provider.name} provider test error: {e}")
    
    def chunk_packets(self, packets: List[Packet]) -> List[PacketChunk]:
        """Split packets into manageable chunks for processing"""
        if not packets:
            return []
        
        chunks = []
        total_packets = len(packets)
        
        # Calculate chunk size based on both packet count and estimated size
        estimated_size_mb = (len(packets) * 1500) / (1024 * 1024)  # Rough estimate
        
        if estimated_size_mb <= self.chunk_size_mb and total_packets <= self.max_packets_per_chunk:
            # Small file, process as single chunk
            chunk_id = hashlib.md5(f"chunk_0_{total_packets}".encode()).hexdigest()[:8]
            summary = self._extract_chunk_statistics(packets)
            
            chunks.append(PacketChunk(
                chunk_id=chunk_id,
                packets=packets,
                summary=summary,
                size_mb=estimated_size_mb,
                packet_count=total_packets
            ))
        else:
            # Large file, split into chunks
            chunk_count = max(
                math.ceil(estimated_size_mb / self.chunk_size_mb),
                math.ceil(total_packets / self.max_packets_per_chunk)
            )
            
            packets_per_chunk = math.ceil(total_packets / chunk_count)
            
            for i in range(chunk_count):
                start_idx = i * packets_per_chunk
                end_idx = min((i + 1) * packets_per_chunk, total_packets)
                chunk_packets = packets[start_idx:end_idx]
                
                if not chunk_packets:
                    continue
                
                chunk_id = hashlib.md5(f"chunk_{i}_{len(chunk_packets)}".encode()).hexdigest()[:8]
                summary = self._extract_chunk_statistics(chunk_packets)
                chunk_size = (len(chunk_packets) * 1500) / (1024 * 1024)
                
                chunks.append(PacketChunk(
                    chunk_id=chunk_id,
                    packets=chunk_packets,
                    summary=summary,
                    size_mb=chunk_size,
                    packet_count=len(chunk_packets)
                ))
        
        logger.info(f"Split {total_packets} packets into {len(chunks)} chunks")
        return chunks
    
    def _extract_chunk_statistics(self, packets: List[Packet]) -> Dict[str, Any]:
        """Extract statistics from a packet chunk"""
        if not packets:
            return {}
        
        stats = {
            "total_packets": len(packets),
            "protocols": {},
            "src_ips": {},
            "dst_ips": {},
            "ports": {"tcp": [], "udp": []},
            "suspicious_patterns": [],
            "packet_sizes": []
        }
        
        syn_counts = {}
        
        for pkt in packets:
            # Packet size
            stats["packet_sizes"].append(len(pkt))
            
            # IP layer analysis
            if IP in pkt:
                src_ip = pkt[IP].src
                dst_ip = pkt[IP].dst
                proto_num = pkt[IP].proto
                
                # Count IPs
                stats["src_ips"][src_ip] = stats["src_ips"].get(src_ip, 0) + 1
                stats["dst_ips"][dst_ip] = stats["dst_ips"].get(dst_ip, 0) + 1
                
                # Protocol analysis
                if proto_num == 6:  # TCP
                    stats["protocols"]["TCP"] = stats["protocols"].get("TCP", 0) + 1
                    if TCP in pkt:
                        port = pkt[TCP].dport
                        stats["ports"]["tcp"].append(port)
                        
                        # Check for SYN flood
                        if pkt[TCP].flags & 0x02:  # SYN flag
                            syn_counts[src_ip] = syn_counts.get(src_ip, 0) + 1
                            if syn_counts[src_ip] > 50:
                                stats["suspicious_patterns"].append(f"Potential SYN flood from {src_ip}")
                        
                        # Check for suspicious ports
                        if port in [0, 65535, 31337, 6667]:
                            stats["suspicious_patterns"].append(f"Suspicious TCP port {port} from {src_ip}")
                
                elif proto_num == 17:  # UDP
                    stats["protocols"]["UDP"] = stats["protocols"].get("UDP", 0) + 1
                    if UDP in pkt:
                        port = pkt[UDP].dport
                        stats["ports"]["udp"].append(port)
                        
                        # Check for suspicious ports
                        if port in [0, 65535, 31337]:
                            stats["suspicious_patterns"].append(f"Suspicious UDP port {port} from {src_ip}")
                
                elif proto_num == 1:  # ICMP
                    stats["protocols"]["ICMP"] = stats["protocols"].get("ICMP", 0) + 1
                else:
                    stats["protocols"]["Other"] = stats["protocols"].get("Other", 0) + 1
        
        # Remove duplicates from suspicious patterns
        stats["suspicious_patterns"] = list(set(stats["suspicious_patterns"]))
        
        return stats
    
    def _select_provider(self) -> Optional[AIProvider]:
        """Select the best available provider using round-robin"""
        if not self.active_providers:
            return None
        
        # Simple round-robin for now
        # TODO: Implement more sophisticated load balancing
        provider = self.active_providers[0]
        self.active_providers.append(self.active_providers.pop(0))  # Move to end
        return provider
    
    async def query_single_chunk(self, prompt: str, chunk: PacketChunk) -> AIResponse:
        """Query AI for a single packet chunk"""
        provider = self._select_provider()
        if not provider:
            return AIResponse(
                success=False,
                response="",
                error="No active AI providers available",
                chunk_id=chunk.chunk_id
            )
        
        # Create context from chunk statistics
        context = self._format_chunk_context(chunk)
        
        # Execute query
        response = await provider.query(prompt, context)
        response.chunk_id = chunk.chunk_id
        
        return response
    
    def _format_chunk_context(self, chunk: PacketChunk) -> str:
        """Format chunk statistics as context for AI"""
        stats = chunk.summary
        
        context = f"""
PACKET CHUNK ANALYSIS (ID: {chunk.chunk_id})
=========================================

Basic Statistics:
- Total Packets: {stats.get('total_packets', 0)}
- Chunk Size: {chunk.size_mb:.2f} MB
- Average Packet Size: {sum(stats.get('packet_sizes', [0])) / len(stats.get('packet_sizes', [1])):.1f} bytes

Protocol Distribution:
"""
        
        for protocol, count in stats.get('protocols', {}).items():
            context += f"- {protocol}: {count} packets\n"
        
        context += "\nTop Source IPs:\n"
        top_src_ips = sorted(stats.get('src_ips', {}).items(), key=lambda x: x[1], reverse=True)[:5]
        for ip, count in top_src_ips:
            context += f"- {ip}: {count} packets\n"
        
        context += "\nTop Destination IPs:\n"
        top_dst_ips = sorted(stats.get('dst_ips', {}).items(), key=lambda x: x[1], reverse=True)[:5]
        for ip, count in top_dst_ips:
            context += f"- {ip}: {count} packets\n"
        
        if stats.get('suspicious_patterns'):
            context += "\nSuspicious Patterns Detected:\n"
            for pattern in stats.get('suspicious_patterns', [])[:10]:  # Limit to 10
                context += f"- {pattern}\n"
        
        return context
    
    async def query(self, prompt: str, packets: List[Packet]) -> List[AIResponse]:
        """Query AI system with automatic chunking for large files"""
        if not self.active_providers:
            return [AIResponse(
                success=False,
                response="",
                error="No active AI providers available"
            )]
        
        # Split into chunks
        chunks = self.chunk_packets(packets)
        
        if not chunks:
            return [AIResponse(
                success=False,
                response="",
                error="No valid packet data to analyze"
            )]
        
        logger.info(f"Processing {len(chunks)} chunks with {len(self.active_providers)} providers")
        
        # Process chunks concurrently
        tasks = []
        for chunk in chunks:
            tasks.append(self.query_single_chunk(prompt, chunk))
        
        # Execute all queries
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        final_responses = []
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                final_responses.append(AIResponse(
                    success=False,
                    response="",
                    error=str(response),
                    chunk_id=chunks[i].chunk_id if i < len(chunks) else None
                ))
            else:
                final_responses.append(response)
        
        return final_responses
    
    def combine_responses(self, responses: List[AIResponse]) -> str:
        """Combine multiple chunk responses into a coherent analysis"""
        successful_responses = [r for r in responses if r.success]
        failed_responses = [r for r in responses if not r.success]
        
        # Log failures for debugging
        if failed_responses:
            for failed in failed_responses:
                logger.error(f"❌ Provider {failed.provider} failed: {failed.error}")
        
        if not successful_responses:
            return "❌ Analysis failed for all chunks. Please check your AI provider connections."
        
        combined = f"🔍 **Multi-Chunk Analysis Summary** ({len(successful_responses)}/{len(responses)} chunks analyzed successfully)\n\n"
        
        for i, response in enumerate(successful_responses, 1):
            combined += f"### Chunk {i} Analysis ({response.provider}):\n"
            combined += f"{response.response}\n\n"
            combined += "---\n\n"
        
        if failed_responses:
            combined += f"⚠️ **Note**: {len(failed_responses)} chunks failed to analyze due to errors.\n"
        
        # Add performance summary
        total_time = sum(r.response_time for r in successful_responses if r.response_time)
        total_tokens = sum(r.tokens_used for r in successful_responses if r.tokens_used)
        
        combined += f"\n📊 **Performance Summary**:\n"
        combined += f"- Total processing time: {total_time:.2f} seconds\n"
        combined += f"- Total tokens used: {total_tokens}\n"
        combined += f"- Providers used: {', '.join(set(r.provider for r in successful_responses))}\n"
        
        return combined

# Global instance
multi_agent = MultiAgentAI()

# Convenience functions for backward compatibility
async def query_ai_async(prompt: str, packets: List[Packet]) -> Dict[str, Any]:
    """Async query function"""
    responses = await multi_agent.query(prompt, packets)
    combined_response = multi_agent.combine_responses(responses)
    
    return {
        "success": any(r.success for r in responses),
        "response": combined_response,
        "error": None if any(r.success for r in responses) else "All providers failed",
        "provider_responses": responses
    }

def query_ai(prompt: str, packets: List[Packet]) -> Dict[str, Any]:
    """Synchronous wrapper for async query"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(query_ai_async(prompt, packets))
    except Exception as e:
        return {
            "success": False,
            "response": "",
            "error": str(e)
        }
    finally:
        loop.close()

def get_active_providers() -> List[str]:
    """Get list of active provider names"""
    return [provider.name for provider in multi_agent.active_providers]

def get_suggested_queries() -> List[str]:
    """Get suggested queries for network analysis"""
    return [
        "Analyze this network traffic for security threats and anomalies",
        "What are the most active IP addresses and what might they be doing?",
        "Identify any suspicious port usage or protocol patterns",
        "Look for signs of network scanning or reconnaissance",
        "Analyze the traffic for potential data exfiltration attempts",
        "What protocols are being used and are they appropriate for this network?",
        "Identify any unusual traffic patterns or timing anomalies",
        "Look for signs of malware communication or C&C traffic",
        "Analyze DNS requests for suspicious domains or patterns",
        "Check for any encrypted traffic that might be hiding malicious activity"
    ]

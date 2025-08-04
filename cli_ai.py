#!/usr/bin/env python3
"""
CLI Interface for Sniff Recon AI Analysis

This module provides a command-line interface for AI-powered packet analysis.
"""

import argparse
import sys
import os
from typing import List
from scapy.packet import Packet
import scapy.all as scapy
from ai_module import ai_engine, PacketSummary
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_banner():
    """Print the application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🔍 Sniff Recon AI                        ║
    ║              AI-Powered Network Packet Analyzer              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_colored(text: str, color: str = "cyan", end="\n"):
    """Print colored text to terminal"""
    colors = {
        "cyan": "\033[96m",
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "bold": "\033[1m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}", end=end)

def load_packets(file_path: str) -> List[Packet]:
    """Load packets from file"""
    try:
        if file_path.endswith(('.pcap', '.pcapng')):
            packets = scapy.rdpcap(file_path)
            return list(packets)
        else:
            print_colored(f"❌ Unsupported file format: {file_path}", "red")
            return []
    except Exception as e:
        print_colored(f"❌ Error loading packets: {e}", "red")
        return []

def display_packet_summary(packet_summary: PacketSummary):
    """Display packet summary statistics"""
    print_colored("\n📊 Packet Analysis Summary", "bold")
    print("=" * 50)
    
    print_colored(f"Total Packets: {packet_summary.total_packets}", "cyan")
    print_colored(f"Unique Source IPs: {len(packet_summary.unique_src_ips)}", "cyan")
    print_colored(f"Unique Destination IPs: {len(packet_summary.unique_dst_ips)}", "cyan")
    
    if packet_summary.packet_sizes:
        avg_size = sum(packet_summary.packet_sizes) / len(packet_summary.packet_sizes)
        print_colored(f"Average Packet Size: {avg_size:.1f} bytes", "cyan")
    
    print_colored("\n🔍 Protocol Distribution:", "yellow")
    for protocol, count in packet_summary.protocol_distribution.items():
        print(f"  {protocol}: {count}")
    
    print_colored("\n🌐 Top 5 Source IPs:", "yellow")
    for i, (ip, count) in enumerate(list(packet_summary.top_src_ips.items())[:5], 1):
        print(f"  {i}. {ip}: {count} packets")
    
    print_colored("\n🌐 Top 5 Destination IPs:", "yellow")
    for i, (ip, count) in enumerate(list(packet_summary.top_dst_ips.items())[:5], 1):
        print(f"  {i}. {ip}: {count} packets")
    
    if packet_summary.suspicious_patterns:
        print_colored("\n⚠️  Suspicious Patterns Detected:", "red")
        for pattern in packet_summary.suspicious_patterns:
            print(f"  • {pattern}")
    else:
        print_colored("\n✅ No suspicious patterns detected", "green")

def interactive_ai_mode(packets: List[Packet]):
    """Interactive AI query mode with Layered Filtering"""
    print_colored("\n🤖 AI Analysis Mode", "bold")
    print("=" * 50)
    print_colored("Ask questions about your network traffic. Type 'quit' to exit.", "cyan")
    print_colored("Type 'help' for suggested questions.", "cyan")

    # Layered filtering
    print_colored("\nFiltering suspicious packets for smart AI triage...", "yellow")
    suspicious = ai_engine.filter_suspicious_packets(packets)
    clusters = ai_engine.cluster_packets_by_ip(suspicious)
    triaged_summaries = ai_engine.summarize_clusters(clusters)
    
    if not triaged_summaries:
        print_colored("No suspicious packets found after triage. Falling back to classic summary.", "yellow")
        packet_summary = ai_engine.extract_packet_statistics(packets)
    else:
        print_colored(f"{len(triaged_summaries)} suspicious flows detected.", "yellow")
        # Flatten as text for LLM
def format_triaged_for_llm():
    out = []
    for group in triaged_summaries:
        out.append(f"Src: {group['src_ip']} → Dst: {group['dst_ip']} | Cnt: {group['packet_count']} | Ports: {group['ports']} | Proto: {group['protocols']}")
        for pat in group['suspicious_patterns']:
            out.append(f"  Pattern: {pat}")
    return '\n'.join(out)

    while True:
        try:
            print_colored("\n🤖 Question: ", "cyan", end="")
            user_query = input().strip()

            if user_query.lower() in ['quit', 'exit', 'q']:
                print_colored("👋 Goodbye!", "green")
                break

            if user_query.lower() == 'help':
                print_colored("\n💡 Suggested Questions:", "yellow")
                suggested = ai_engine.get_suggested_queries()
                for i, query in enumerate(suggested, 1):
                    print(f"  {i}. {query}")
                continue

            if not user_query:
                continue

            print_colored("🤖 Analyzing (triaged input)...", "cyan")
            llm_context = format_triaged_for_llm() if triaged_summaries else None

            if triaged_summaries:
                summary_obj = PacketSummary(
                    total_packets=sum(x['packet_count'] for x in triaged_summaries),
                    unique_src_ips=[x['src_ip'] for x in triaged_summaries],
                    unique_dst_ips=[x['dst_ip'] for x in triaged_summaries],
                    protocol_distribution={}, # skip for brevity
                    top_src_ips={},
                    top_dst_ips={},
                    port_analysis={},
                    packet_sizes=[],
                    time_range=(0, 0),
                    suspicious_patterns=[pat for x in triaged_summaries for pat in x['suspicious_patterns']],
                )
            else:
                summary_obj = packet_summary

            # Query AI
            result = ai_engine.query_ai(user_query, summary_obj)

            if result.get("success"):
                print_colored("\n💡 AI Response:", "green")
                print("-" * 30)
                print(result["response"])
                print("-" * 30)
            else:
                print_colored(f"\n❌ Error: {result.get('error', 'Unknown error')}", "red")

        except KeyboardInterrupt:
            print_colored("\n👋 Goodbye!", "green")
            break
        except Exception as e:
            print_colored(f"\n❌ Unexpected error: {e}", "red")

def batch_ai_mode(packets: List[Packet], queries: List[str]):
    """Batch AI query mode with Layered Filtering"""
    print_colored("\n🤖 Batch AI Analysis Mode (with triaged input)", "bold")
    print("=" * 50)
    
    # Layered filtering
    print_colored("Filtering suspicious packets for smart AI triage...", "yellow")
    suspicious = ai_engine.filter_suspicious_packets(packets)
    clusters = ai_engine.cluster_packets_by_ip(suspicious)
    triaged_summaries = ai_engine.summarize_clusters(clusters)

    if not triaged_summaries:
        print_colored("No suspicious packets found after triage. Using full summary for all queries.", "yellow")
        summary_obj = ai_engine.extract_packet_statistics(packets)
    else:
        print_colored(f"{len(triaged_summaries)} suspicious flows detected.", "yellow")
        summary_obj = PacketSummary(
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

    results = []

    for i, query in enumerate(queries, 1):
        print_colored(f"\n🔍 Processing query {i}/{len(queries)}: {query}", "cyan")
        # Query AI
        result = ai_engine.query_ai(query, summary_obj)
        if result.get("success"):
            print_colored("✅ Success", "green")
            results.append({
                "query": query,
                "response": result["response"],
                "success": True
            })
        else:
            print_colored(f"❌ Error: {result.get('error')}", "red")
            results.append({
                "query": query,
                "response": result.get("error"),
                "success": False
            })
    return results

def save_results(results: List[dict], output_file: str):
    """Save AI analysis results to file"""
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print_colored(f"\n💾 Results saved to: {output_file}", "green")
    except Exception as e:
        print_colored(f"\n❌ Error saving results: {e}", "red")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="AI-Powered Network Packet Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python cli_ai.py -f capture.pcap -i
  
  # Batch mode with specific queries
  python cli_ai.py -f capture.pcap -q "What are the top 5 IPs?" "Are there suspicious patterns?"
  
  # Save results to file
  python cli_ai.py -f capture.pcap -q "Analyze traffic" -o results.json
  
  # Show packet summary only
  python cli_ai.py -f capture.pcap --summary
        """
    )
    
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Path to packet capture file (.pcap, .pcapng)"
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Enable interactive AI query mode"
    )
    
    parser.add_argument(
        "-q", "--queries",
        nargs="+",
        help="List of AI queries to process"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file to save AI analysis results (JSON format)"
    )
    
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show packet summary statistics only"
    )
    
    parser.add_argument(
        "--suggested",
        action="store_true",
        help="Show suggested AI queries"
    )
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.file):
        print_colored(f"❌ File not found: {args.file}", "red")
        sys.exit(1)
    
    # Print banner
    print_banner()
    
    # Load packets
    print_colored(f"📁 Loading packets from: {args.file}", "cyan")
    packets = load_packets(args.file)
    
    if not packets:
        print_colored("❌ No packets loaded. Exiting.", "red")
        sys.exit(1)
    
    print_colored(f"✅ Loaded {len(packets)} packets", "green")
    
    # Show suggested queries
    if args.suggested:
        print_colored("\n💡 Suggested AI Queries:", "yellow")
        suggested = ai_engine.get_suggested_queries()
        for i, query in enumerate(suggested, 1):
            print(f"  {i}. {query}")
        return
    
    # Extract packet summary
    packet_summary = ai_engine.extract_packet_statistics(packets)
    
    # Show summary if requested
    if args.summary:
        display_packet_summary(packet_summary)
        return
    
    # Interactive mode
    if args.interactive:
        display_packet_summary(packet_summary)
        interactive_ai_mode(packets)
        return
    
    # Batch mode
    if args.queries:
        display_packet_summary(packet_summary)
        results = batch_ai_mode(packets, args.queries)
        
        # Save results if output file specified
        if args.output:
            save_results(results, args.output)
        
        # Display results
        print_colored("\n📊 AI Analysis Results:", "bold")
        print("=" * 50)
        
        for i, result in enumerate(results, 1):
            print_colored(f"\n🔍 Query {i}: {result['query']}", "cyan")
            if result['success']:
                print_colored("✅ Response:", "green")
                print(result['response'])
            else:
                print_colored("❌ Error:", "red")
                print(result['response'])
        
        return
    
    # Default: show summary and interactive mode
    display_packet_summary(packet_summary)
    interactive_ai_mode(packets)

if __name__ == "__main__":
    main() 
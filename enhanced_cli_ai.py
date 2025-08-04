#!/usr/bin/env python3
"""
Enhanced CLI Interface for Sniff Recon AI Analysis
Supports multi-agent AI, large file chunking, and improved error handling
"""

import argparse
import sys
import os
import time
from typing import List, Dict, Any
from scapy.packet import Packet
import scapy.all as scapy
from multi_agent_ai import multi_agent, query_ai, get_active_providers, get_suggested_queries
from ai_module import ai_engine, PacketSummary
import json
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.markdown import Markdown

# Load environment variables
load_dotenv()

console = Console()

def print_banner():
    """Print the enhanced application banner"""
    banner_text = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🔍 Sniff Recon AI Enhanced                ║
    ║           Multi-Agent Network Packet Analyzer v2.0           ║
    ║                                                              ║
    ║  🤖 Multi-AI Support  📊 Large File Handling  ⚡ Fast Analysis ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner_text, style="cyan bold"))

def print_system_status():
    """Print system status including active AI providers"""
    providers = get_active_providers()
    
    status_table = Table(title="🔧 System Status", show_header=True, header_style="bold magenta")
    status_table.add_column("Component", style="cyan")
    status_table.add_column("Status", style="green")
    status_table.add_column("Details", style="yellow")
    
    # AI Providers
    if providers:
        status_table.add_row("AI Providers", f"✅ Active ({len(providers)})", ", ".join(providers))
    else:
        status_table.add_row("AI Providers", "❌ None", "Check API keys in .env")
    
    # Multi-agent system
    if hasattr(multi_agent, 'active_providers') and multi_agent.active_providers:
        status_table.add_row("Multi-Agent", "✅ Enabled", f"Load balancing across {len(multi_agent.active_providers)} providers")
    else:
        status_table.add_row("Multi-Agent", "❌ Disabled", "Using fallback analysis")
    
    # Chunking capability
    chunk_size = getattr(multi_agent, 'chunk_size_mb', 5)
    max_packets = getattr(multi_agent, 'max_packets_per_chunk', 5000)
    status_table.add_row("Large File Support", "✅ Enabled", f"Chunks: {chunk_size}MB / {max_packets} packets")
    
    console.print(status_table)
    console.print()

def load_packets_with_progress(file_path: str) -> List[Packet]:
    """Load packets from file with progress indicator"""
    try:
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        console.print(f"📁 Loading packet file: {file_path}")
        console.print(f"📊 File size: {file_size_mb:.2f} MB")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            if file_path.endswith(('.pcap', '.pcapng')):
                task = progress.add_task("Loading packets...", total=None)
                
                # Use PcapReader for large files to avoid memory issues
                packets = []
                with scapy.PcapReader(file_path) as pcap_reader:
                    for i, pkt in enumerate(pcap_reader):
                        packets.append(pkt)
                        if i % 1000 == 0:  # Update every 1000 packets
                            progress.update(task, description=f"Loaded {i:,} packets...")
                
                progress.update(task, description=f"Completed! Loaded {len(packets):,} packets")
                return packets
            else:
                console.print(f"❌ Unsupported file format: {file_path}", style="red")
                return []
                
    except Exception as e:
        console.print(f"❌ Error loading packets: {e}", style="red")
        return []

def display_packet_summary(packets: List[Packet]):
    """Display comprehensive packet summary"""
    if not packets:
        console.print("⚠️ No packets to analyze", style="yellow")
        return
    
    # Extract statistics
    packet_summary = ai_engine.extract_packet_statistics(packets)
    
    # Create summary table
    summary_table = Table(title="📊 Packet Analysis Summary", show_header=True, header_style="bold blue")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="white")
    summary_table.add_column("Details", style="yellow")
    
    # Basic stats
    summary_table.add_row("Total Packets", f"{packet_summary.total_packets:,}", "")
    summary_table.add_row("Unique Source IPs", f"{len(packet_summary.unique_src_ips):,}", "")
    summary_table.add_row("Unique Destination IPs", f"{len(packet_summary.unique_dst_ips):,}", "")
    
    # File size estimation
    if packets:
        estimated_size = sum(len(pkt) for pkt in packets[:1000]) / 1000 * len(packets)
        estimated_mb = estimated_size / (1024 * 1024)
        summary_table.add_row("Estimated Size", f"{estimated_mb:.2f} MB", "Based on sampling")
    
    # Average packet size
    if packet_summary.packet_sizes:
        avg_size = sum(packet_summary.packet_sizes) / len(packet_summary.packet_sizes)
        summary_table.add_row("Average Packet Size", f"{avg_size:.1f} bytes", "")
    
    # Time range
    if packet_summary.time_range[0] != packet_summary.time_range[1]:
        duration = packet_summary.time_range[1] - packet_summary.time_range[0]
        summary_table.add_row("Time Duration", f"{duration:.2f} seconds", "")
    
    console.print(summary_table)
    
    # Protocol distribution
    if packet_summary.protocol_distribution:
        protocol_table = Table(title="🔍 Protocol Distribution", show_header=True, header_style="bold green")
        protocol_table.add_column("Protocol", style="cyan")
        protocol_table.add_column("Count", style="white")
        protocol_table.add_column("Percentage", style="yellow")
        
        total_packets = packet_summary.total_packets
        for protocol, count in sorted(packet_summary.protocol_distribution.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_packets) * 100 if total_packets > 0 else 0
            protocol_table.add_row(protocol, f"{count:,}", f"{percentage:.1f}%")
        
        console.print(protocol_table)
    
    # Top IPs
    if packet_summary.top_src_ips:
        ip_table = Table(title="🌐 Top Source IPs", show_header=True, header_style="bold magenta")
        ip_table.add_column("Rank", style="cyan")
        ip_table.add_column("IP Address", style="white")
        ip_table.add_column("Packet Count", style="yellow")
        
        for i, (ip, count) in enumerate(list(packet_summary.top_src_ips.items())[:10], 1):
            ip_table.add_row(str(i), ip, f"{count:,}")
        
        console.print(ip_table)
    
    # Suspicious patterns
    if packet_summary.suspicious_patterns:
        console.print("\n⚠️ Suspicious Patterns Detected:", style="bold red")
        for pattern in packet_summary.suspicious_patterns[:10]:
            console.print(f"  • {pattern}", style="red")
    else:
        console.print("\n✅ No suspicious patterns detected", style="green")

def interactive_ai_mode(packets: List[Packet]):
    """Enhanced interactive AI mode with multi-agent support"""
    console.print("\n🤖 Multi-Agent AI Analysis Mode", style="bold cyan")
    console.print("=" * 60)
    
    # Show active providers
    providers = get_active_providers()
    if providers:
        console.print(f"Active AI Providers: {', '.join(providers)}", style="green")
    else:
        console.print("No AI providers active - using local analysis", style="yellow")
    
    console.print("\nAsk questions about your network traffic. Type 'quit' to exit.")
    console.print("Type 'help' for suggested questions.", style="dim")
    console.print("Type 'status' to see system information.", style="dim")
    
    while True:
        try:
            # Get user input
            user_query = console.input("\n🤖 [bold cyan]Question:[/bold cyan] ").strip()
            
            if user_query.lower() in ['quit', 'exit', 'q']:
                console.print("👋 Goodbye!", style="green")
                break
            
            if user_query.lower() == 'help':
                console.print("\n💡 Suggested Questions:", style="bold yellow")
                suggested = get_suggested_queries()
                for i, query in enumerate(suggested, 1):
                    console.print(f"  {i:2d}. {query}")
                continue
            
            if user_query.lower() == 'status':
                print_system_status()
                continue
            
            if not user_query:
                continue
            
            # Show analysis progress
            with console.status("[bold green]🤖 Analyzing with multi-agent AI system...") as status:
                start_time = time.time()
                
                # Use multi-agent system
                result = query_ai(user_query, packets)
                
                analysis_time = time.time() - start_time
            
            # Display results
            if result.get("success"):
                console.print("\n💡 AI Analysis Results:", style="bold green")
                console.print("─" * 60)
                
                # Parse and display markdown if possible
                try:
                    response_md = Markdown(result["response"])
                    console.print(response_md)
                except:
                    console.print(result["response"])
                
                console.print("─" * 60)
                console.print(f"⏱️ Analysis time: {analysis_time:.2f}s", style="dim")
                
                # Show provider information if available
                if result.get("provider_responses"):
                    successful_providers = [r.provider for r in result["provider_responses"] if r.success and r.provider]
                    if successful_providers:
                        console.print(f"🤖 Providers used: {', '.join(set(successful_providers))}", style="dim")
                
            else:
                console.print(f"\n❌ Error: {result.get('error', 'Unknown error')}", style="red")
        
        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!", style="green")
            break
        except Exception as e:
            console.print(f"\n❌ Unexpected error: {e}", style="red")

def batch_analysis_mode(packets: List[Packet], queries: List[str]):
    """Batch analysis mode for multiple queries"""
    console.print(f"\n🔄 Batch Analysis Mode - Processing {len(queries)} queries", style="bold cyan")
    
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("Processing queries...", total=len(queries))
        
        for i, query in enumerate(queries, 1):
            progress.update(task, description=f"Query {i}/{len(queries)}: {query[:50]}...")
            
            result = query_ai(query, packets)
            results.append({
                "query": query,
                "result": result,
                "timestamp": time.time()
            })
            
            progress.advance(task)
    
    # Display results
    console.print(f"\n📊 Batch Analysis Results", style="bold green")
    console.print("=" * 80)
    
    for i, item in enumerate(results, 1):
        console.print(f"\n[bold cyan]Query {i}:[/bold cyan] {item['query']}")
        console.print("─" * 60)
        
        if item["result"].get("success"):
            try:
                response_md = Markdown(item["result"]["response"])
                console.print(response_md)
            except:
                console.print(item["result"]["response"])
        else:
            console.print(f"❌ Error: {item['result'].get('error', 'Unknown error')}", style="red")
        
        console.print("─" * 60)
    
    # Save results to file
    output_file = f"batch_analysis_{int(time.time())}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    console.print(f"\n💾 Results saved to: {output_file}", style="green")

def main():
    parser = argparse.ArgumentParser(
        description='Enhanced Sniff Recon - Multi-Agent Network Packet Analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_cli_ai.py -f capture.pcap -i                    # Interactive mode
  python enhanced_cli_ai.py -f capture.pcap -b queries.txt       # Batch mode
  python enhanced_cli_ai.py -f capture.pcap -q "Show threats"    # Single query
        """
    )
    
    parser.add_argument('-f', '--file', required=True,
                        help='Path to the packet capture file (.pcap, .pcapng)')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Start interactive AI analysis mode')
    parser.add_argument('-b', '--batch', 
                        help='Batch mode: file containing queries (one per line)')
    parser.add_argument('-q', '--query',
                        help='Single query to analyze')
    parser.add_argument('--no-summary', action='store_true',
                        help='Skip packet summary display')
    parser.add_argument('--chunk-size', type=int, default=5,
                        help='Chunk size in MB for large files (default: 5)')
    parser.add_argument('--max-packets', type=int, default=5000,
                        help='Maximum packets per chunk (default: 5000)')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Print system status
    print_system_status()
    
    # Validate file
    if not os.path.isfile(args.file):
        console.print(f"❌ Error: File '{args.file}' does not exist.", style="red")
        sys.exit(1)
    
    # Configure chunking parameters
    if hasattr(multi_agent, 'chunk_size_mb'):
        multi_agent.chunk_size_mb = args.chunk_size
    if hasattr(multi_agent, 'max_packets_per_chunk'):
        multi_agent.max_packets_per_chunk = args.max_packets
    
    # Load packets
    console.print(f"\n📂 Loading packet file: {args.file}")
    packets = load_packets_with_progress(args.file)
    
    if not packets:
        console.print("❌ No packets loaded. Exiting.", style="red")
        sys.exit(1)
    
    console.print(f"✅ Successfully loaded {len(packets):,} packets\n", style="green")
    
    # Display packet summary (unless disabled)
    if not args.no_summary:
        display_packet_summary(packets)
    
    # Execute based on mode
    if args.interactive:
        interactive_ai_mode(packets)
    elif args.batch:
        if not os.path.isfile(args.batch):
            console.print(f"❌ Error: Batch file '{args.batch}' does not exist.", style="red")
            sys.exit(1)
        
        with open(args.batch, 'r') as f:
            queries = [line.strip() for line in f if line.strip()]
        
        if not queries:
            console.print("❌ No queries found in batch file.", style="red")
            sys.exit(1)
        
        batch_analysis_mode(packets, queries)
    elif args.query:
        console.print(f"\n🤖 Processing single query: {args.query}")
        
        with console.status("[bold green]Analyzing..."):
            result = query_ai(args.query, packets)
        
        if result.get("success"):
            console.print("\n💡 AI Analysis Results:", style="bold green")
            console.print("─" * 60)
            try:
                response_md = Markdown(result["response"])
                console.print(response_md)
            except:
                console.print(result["response"])
            console.print("─" * 60)
        else:
            console.print(f"\n❌ Error: {result.get('error', 'Unknown error')}", style="red")
    else:
        console.print("⚠️ No analysis mode specified. Use -i, -b, or -q.", style="yellow")
        console.print("Use --help for more information.", style="dim")

if __name__ == '__main__':
    main()

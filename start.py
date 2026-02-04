#!/usr/bin/env python3
"""
Sniff-Recon Universal Launcher
Cross-platform launcher that works on Windows, Linux, and macOS.
Automatically detects Docker or Podman and handles everything.
"""

import subprocess
import sys
import os
import time
import webbrowser
import shutil
import platform
from pathlib import Path

# Configuration
APP_NAME = "sniff-recon"
CONTAINER_NAME = "sniff-recon-app"
IMAGE_NAME = "sniff-recon:latest"
PORT = 8501
URL = f"http://localhost:{PORT}"

# Colors for terminal output (cross-platform)
class Colors:
    if platform.system() == "Windows":
        # Enable ANSI on Windows
        os.system("")
    
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def print_banner():
    """Print the application banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🔍 SNIFF-RECON                                          ║
║   AI-Powered Network Packet Analyzer                      ║
║                                                           ║
║   Cross-Platform • Offline-First • Privacy-Focused        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{Colors.ENDC}"""
    print(banner)


def detect_container_runtime():
    """Detect available container runtime (Docker or Podman)."""
    # Check for Docker
    docker = shutil.which("docker")
    if docker:
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"{Colors.GREEN}✓{Colors.ENDC} Found Docker")
                return "docker", "docker-compose"
        except (subprocess.TimeoutExpired, Exception):
            pass
    
    # Check for Podman
    podman = shutil.which("podman")
    if podman:
        try:
            result = subprocess.run(
                ["podman", "info"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"{Colors.GREEN}✓{Colors.ENDC} Found Podman")
                # Check for podman-compose
                podman_compose = shutil.which("podman-compose")
                compose_cmd = "podman-compose" if podman_compose else "podman compose"
                return "podman", compose_cmd
        except (subprocess.TimeoutExpired, Exception):
            pass
    
    return None, None


def check_env_file():
    """Check if .env file exists, create from template if not."""
    env_path = Path(".env")
    template_path = Path(".env.template")
    
    if not env_path.exists():
        if template_path.exists():
            print(f"{Colors.YELLOW}!{Colors.ENDC} Creating .env from template...")
            shutil.copy(template_path, env_path)
            print(f"{Colors.GREEN}✓{Colors.ENDC} Created .env file")
            print(f"{Colors.CYAN}  → Edit .env to add your API keys (optional){Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}!{Colors.ENDC} No .env file found (AI features may be limited)")
    else:
        print(f"{Colors.GREEN}✓{Colors.ENDC} Found .env configuration")


def stop_existing_container(runtime):
    """Stop any existing container."""
    try:
        subprocess.run(
            [runtime, "stop", CONTAINER_NAME],
            capture_output=True,
            timeout=30
        )
        subprocess.run(
            [runtime, "rm", CONTAINER_NAME],
            capture_output=True,
            timeout=10
        )
    except Exception:
        pass  # Container might not exist


def build_image(runtime, compose_cmd):
    """Build the Docker/Podman image."""
    print(f"\n{Colors.BLUE}Building container image...{Colors.ENDC}")
    print(f"{Colors.CYAN}  This may take a few minutes on first run{Colors.ENDC}")
    
    try:
        # Use compose to build
        if "compose" in compose_cmd:
            cmd = compose_cmd.split() + ["build"]
        else:
            cmd = [compose_cmd, "build"]
        
        result = subprocess.run(
            cmd,
            timeout=600,  # 10 minutes timeout
            check=True
        )
        print(f"{Colors.GREEN}✓{Colors.ENDC} Image built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}✗{Colors.ENDC} Build failed: {e}")
        return False
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}✗{Colors.ENDC} Build timed out")
        return False


def start_container(runtime, compose_cmd):
    """Start the container."""
    print(f"\n{Colors.BLUE}Starting Sniff-Recon...{Colors.ENDC}")
    
    try:
        # Use compose to start
        if "compose" in compose_cmd:
            cmd = compose_cmd.split() + ["up", "-d"]
        else:
            cmd = [compose_cmd, "up", "-d"]
        
        result = subprocess.run(
            cmd,
            timeout=60,
            check=True
        )
        print(f"{Colors.GREEN}✓{Colors.ENDC} Container started")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}✗{Colors.ENDC} Failed to start: {e}")
        return False
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}✗{Colors.ENDC} Start timed out")
        return False


def wait_for_app(timeout=60):
    """Wait for the application to be ready."""
    print(f"\n{Colors.BLUE}Waiting for application to start...{Colors.ENDC}")
    
    import urllib.request
    import urllib.error
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = urllib.request.urlopen(f"{URL}/_stcore/health", timeout=2)
            if response.status == 200:
                print(f"{Colors.GREEN}✓{Colors.ENDC} Application is ready!")
                return True
        except (urllib.error.URLError, Exception):
            pass
        
        # Print progress
        elapsed = int(time.time() - start_time)
        print(f"  Waiting... ({elapsed}s)", end="\r")
        time.sleep(2)
    
    print(f"{Colors.YELLOW}!{Colors.ENDC} Timeout waiting for app (may still be starting)")
    return False


def open_browser():
    """Open the application in the default browser."""
    print(f"\n{Colors.CYAN}Opening browser at {URL}{Colors.ENDC}")
    try:
        webbrowser.open(URL)
    except Exception:
        print(f"{Colors.YELLOW}!{Colors.ENDC} Could not open browser automatically")
        print(f"  Please open manually: {URL}")


def print_usage_info(runtime, compose_cmd):
    """Print usage information."""
    compose = compose_cmd.split()[0] if " " in compose_cmd else compose_cmd
    
    print(f"""
{Colors.GREEN}{Colors.BOLD}═══════════════════════════════════════════════════════════{Colors.ENDC}
{Colors.GREEN}✓ Sniff-Recon is running!{Colors.ENDC}

{Colors.CYAN}Access the app:{Colors.ENDC}
  → {Colors.BOLD}{URL}{Colors.ENDC}

{Colors.CYAN}Useful commands:{Colors.ENDC}
  View logs:     {runtime} logs {CONTAINER_NAME} -f
  Stop:          {compose} down
  Restart:       {compose} restart
  Rebuild:       {compose} up -d --build

{Colors.CYAN}Features:{Colors.ENDC}
  • Upload PCAP, CSV, or TXT files for analysis
  • AI-powered packet analysis (Cloud or Offline with Ollama)
  • Interactive packet inspection
  • Export results as JSON

{Colors.YELLOW}Press Ctrl+C to exit this launcher (app keeps running){Colors.ENDC}
{Colors.GREEN}═══════════════════════════════════════════════════════════{Colors.ENDC}
""")


def run_local_mode():
    """Run in local Python mode (fallback if no container runtime)."""
    print(f"\n{Colors.YELLOW}No container runtime found. Running in local mode...{Colors.ENDC}")
    
    # Check for Python dependencies
    try:
        import streamlit
        import scapy
        import pandas
    except ImportError as e:
        print(f"{Colors.RED}✗{Colors.ENDC} Missing dependency: {e}")
        print(f"  Run: pip install -r requirements.txt")
        return False
    
    print(f"{Colors.GREEN}✓{Colors.ENDC} Dependencies found")
    print(f"\n{Colors.BLUE}Starting Streamlit server...{Colors.ENDC}")
    print(f"{Colors.CYAN}  Access at: {URL}{Colors.ENDC}")
    print(f"{Colors.YELLOW}  Press Ctrl+C to stop{Colors.ENDC}\n")
    
    # Open browser after short delay
    import threading
    threading.Timer(3.0, lambda: webbrowser.open(URL)).start()
    
    # Run Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", str(PORT),
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print(f"\n{Colors.CYAN}Goodbye!{Colors.ENDC}")
    
    return True


def main():
    """Main entry point."""
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print_banner()
    
    # Detect container runtime
    print(f"{Colors.BLUE}Detecting container runtime...{Colors.ENDC}")
    runtime, compose_cmd = detect_container_runtime()
    
    if not runtime:
        print(f"{Colors.YELLOW}!{Colors.ENDC} No Docker or Podman found")
        print(f"{Colors.CYAN}  Install Docker: https://docs.docker.com/get-docker/{Colors.ENDC}")
        print(f"{Colors.CYAN}  Install Podman: https://podman.io/getting-started/installation{Colors.ENDC}")
        
        # Fallback to local mode
        response = input(f"\n{Colors.YELLOW}Run in local Python mode? [y/N]: {Colors.ENDC}").strip().lower()
        if response == 'y':
            return run_local_mode()
        else:
            print(f"{Colors.RED}Exiting.{Colors.ENDC}")
            sys.exit(1)
    
    # Check .env file
    check_env_file()
    
    # Stop existing container
    print(f"\n{Colors.BLUE}Preparing environment...{Colors.ENDC}")
    stop_existing_container(runtime)
    
    # Build image
    if not build_image(runtime, compose_cmd):
        print(f"\n{Colors.RED}Failed to build image. Check errors above.{Colors.ENDC}")
        sys.exit(1)
    
    # Start container
    if not start_container(runtime, compose_cmd):
        print(f"\n{Colors.RED}Failed to start container. Check errors above.{Colors.ENDC}")
        sys.exit(1)
    
    # Wait for app to be ready
    wait_for_app()
    
    # Open browser
    open_browser()
    
    # Print usage info
    print_usage_info(runtime, compose_cmd)
    
    # Keep running until Ctrl+C
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.CYAN}Launcher stopped. App continues running in background.{Colors.ENDC}")
        print(f"  To stop: {compose_cmd.split()[0]} down")


if __name__ == "__main__":
    main()

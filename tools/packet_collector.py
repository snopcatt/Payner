#!/usr/bin/env python3
"""
Packet Collector - Network Packet Capture Tool
For authorized network monitoring and analysis only.
"""

from scapy.all import sniff, wrpcap, get_if_list
import os
import sys
import time
from datetime import datetime

class Colors:
    """Terminal colors for better output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

LOG_FILE = os.path.expanduser("~/.payner.log")
PCAP_FOLDER = os.path.expanduser("~/.payner_pcap/")
os.makedirs(PCAP_FOLDER, exist_ok=True)

captured_packets = []

def log_action(message):
    """Log actions to the payner log file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def packet_callback(packet):
    """Callback function for each captured packet"""
    captured_packets.append(packet)
    print(f"{Colors.GREEN}[{len(captured_packets)}] {packet.summary()}{Colors.ENDC}")

def display_banner():
    """Display packet collector banner"""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("═" * 60)
    print("📡 PACKET COLLECTOR v1.0")
    print("Network Packet Capture Tool")
    print("═" * 60)
    print(f"{Colors.ENDC}")
    print(f"{Colors.YELLOW}⚠️  Use only on networks you own or have permission to monitor{Colors.ENDC}")
    print()

def show_interfaces():
    """Display available network interfaces"""
    print(f"{Colors.CYAN}Available network interfaces:{Colors.ENDC}")
    interfaces = get_if_list()
    for i, iface in enumerate(interfaces, 1):
        print(f"  {i}. {iface}")
    return interfaces

def get_user_choice(prompt, max_val):
    """Get user choice with validation"""
    while True:
        try:
            choice = int(input(f"{Colors.YELLOW}{prompt}{Colors.ENDC}"))
            if 1 <= choice <= max_val:
                return choice
            else:
                print(f"{Colors.RED}Invalid choice. Please enter 1-{max_val}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number{Colors.ENDC}")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Exiting...{Colors.ENDC}")
            sys.exit(0)

def start_packet_collection():
    """Main packet collection function with interactive interface"""
    global captured_packets
    captured_packets = []
    
    display_banner()
    
    # Show available interfaces
    interfaces = show_interfaces()
    if not interfaces:
        print(f"{Colors.RED}No network interfaces found!{Colors.ENDC}")
        return
    
    # Select interface
    iface_choice = get_user_choice("Select interface number: ", len(interfaces))
    selected_interface = interfaces[iface_choice - 1]
    
    # Get packet count
    packet_count = get_user_choice("Enter number of packets to capture (1-1000): ", 1000)
    
    # Get timeout
    print(f"{Colors.CYAN}Capture timeout options:{Colors.ENDC}")
    print("  1. 30 seconds")
    print("  2. 60 seconds")
    print("  3. 120 seconds")
    print("  4. No timeout (capture until packet limit)")
    
    timeout_choice = get_user_choice("Select timeout option: ", 4)
    timeout_map = {1: 30, 2: 60, 3: 120, 4: None}
    timeout = timeout_map[timeout_choice]
    
    # Create timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    pcap_file = os.path.join(PCAP_FOLDER, f'capture_{timestamp}.pcap')
    
    print(f"\n{Colors.BOLD}Capture Configuration:{Colors.ENDC}")
    print(f"  Interface: {Colors.WHITE}{selected_interface}{Colors.ENDC}")
    print(f"  Packets: {Colors.WHITE}{packet_count}{Colors.ENDC}")
    print(f"  Timeout: {Colors.WHITE}{timeout if timeout else 'None'} seconds{Colors.ENDC}")
    print(f"  Output: {Colors.WHITE}{pcap_file}{Colors.ENDC}")
    
    input(f"\n{Colors.YELLOW}Press Enter to start capture or Ctrl+C to cancel...{Colors.ENDC}")
    
    print(f"\n{Colors.GREEN}🚀 Starting packet capture...{Colors.ENDC}")
    print(f"{Colors.CYAN}Capturing on {selected_interface}...{Colors.ENDC}")
    print("-" * 60)
    
    log_action(f"Started packet collection on {selected_interface}, capturing {packet_count} packets...")
    
    try:
        # Start packet capture
        start_time = time.time()
        sniff(
            iface=selected_interface,
            count=packet_count,
            prn=packet_callback,
            timeout=timeout,
            filter="ip"  # Only capture IP packets
        )
        
        capture_time = time.time() - start_time
        
        print("-" * 60)
        print(f"{Colors.GREEN}✅ Packet capture completed!{Colors.ENDC}")
        print(f"  Captured: {Colors.WHITE}{len(captured_packets)} packets{Colors.ENDC}")
        print(f"  Duration: {Colors.WHITE}{capture_time:.2f} seconds{Colors.ENDC}")
        
        if captured_packets:
            # Save packets to file
            wrpcap(pcap_file, captured_packets)
            print(f"  Saved to: {Colors.WHITE}{pcap_file}{Colors.ENDC}")
            log_action(f"Packet collection completed. Captured {len(captured_packets)} packets, saved to {pcap_file}")
        else:
            print(f"{Colors.YELLOW}⚠️  No packets were captured{Colors.ENDC}")
            log_action("Packet collection completed but no packets were captured")
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Capture interrupted by user{Colors.ENDC}")
        if captured_packets:
            wrpcap(pcap_file, captured_packets)
            print(f"  Partial capture saved: {Colors.WHITE}{pcap_file}{Colors.ENDC}")
        log_action(f"Packet collection interrupted. Captured {len(captured_packets)} packets")
    except Exception as e:
        print(f"{Colors.RED}❌ Capture failed: {e}{Colors.ENDC}")
        log_action(f"Packet collection failed: {e}")
    
    print(f"\n{Colors.BLUE}📊 Capture Summary:{Colors.ENDC}")
    print(f"  PCAP files location: {Colors.WHITE}{PCAP_FOLDER}{Colors.ENDC}")
    print(f"  Log file: {Colors.WHITE}{LOG_FILE}{Colors.ENDC}")

if __name__ == "__main__":
    try:
        start_packet_collection()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Goodbye!{Colors.ENDC}")
        sys.exit(0)


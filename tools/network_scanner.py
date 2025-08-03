#!/usr/bin/env python3
"""
Network Port Scanner
A legitimate security testing tool for authorized network assessment.
Use only on networks you own or have explicit permission to test.
"""

import socket
import threading
import argparse
import sys
import time
from datetime import datetime
import subprocess

class Colors:
    """Terminal colors for better output formatting"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PortScanner:
    def __init__(self, target, start_port=1, end_port=1024, threads=100, timeout=1, port_list=None):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.threads = threads
        self.timeout = timeout
        self.open_ports = []
        self.lock = threading.Lock()
        self.port_list = port_list  # Specific ports to scan
        
        # Common services dictionary
        self.services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            69: "TFTP", 80: "HTTP", 110: "POP3", 119: "NNTP", 123: "NTP",
            135: "RPC", 139: "NetBIOS", 143: "IMAP", 161: "SNMP", 194: "IRC",
            389: "LDAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
            1723: "PPTP", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
            5900: "VNC", 6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
        }

    def banner(self):
        """Display scanner banner"""
        print(f"{Colors.HEADER}{Colors.BOLD}")
        print("=" * 60)
        print("    NETWORK PORT SCANNER v1.0")
        print("    For Authorized Security Testing Only")
        print("=" * 60)
        print(f"{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Target: {Colors.BOLD}{self.target}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Port Range: {Colors.BOLD}{self.start_port}-{self.end_port}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Threads: {Colors.BOLD}{self.threads}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Timeout: {Colors.BOLD}{self.timeout}s{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Started: {Colors.BOLD}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
        print("-" * 60)

    def resolve_target(self):
        """Resolve hostname to IP if needed"""
        try:
            ip = socket.gethostbyname(self.target)
            if ip != self.target:
                print(f"{Colors.OKBLUE}Resolved {self.target} to {ip}{Colors.ENDC}")
            return ip
        except socket.gaierror:
            print(f"{Colors.FAIL}Error: Could not resolve hostname {self.target}{Colors.ENDC}")
            return None

    def scan_port(self, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                # Try to grab banner
                banner = self.grab_banner(sock, port)
                service = self.services.get(port, "Unknown")
                
                with self.lock:
                    self.open_ports.append({
                        'port': port,
                        'service': service,
                        'banner': banner
                    })
                    print(f"{Colors.OKGREEN}[+] Port {port:5d} - {service:15s} - OPEN{Colors.ENDC}")
                    if banner:
                        print(f"    {Colors.WARNING}Banner: {banner}{Colors.ENDC}")
            
            sock.close()
        except Exception as e:
            pass  # Port closed or filtered

    def grab_banner(self, sock, port):
        """Attempt to grab service banner"""
        try:
            if port in [21, 22, 23, 25, 110, 143]:  # Services that send banners
                sock.settimeout(2)
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                return banner[:100] if banner else None
            elif port == 80:  # HTTP
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                response = sock.recv(1024).decode('utf-8', errors='ignore')
                if 'Server:' in response:
                    server_line = [line for line in response.split('\n') if 'Server:' in line]
                    return server_line[0].strip() if server_line else None
        except:
            pass
        return None

    def worker(self, port_queue):
        """Worker thread for scanning ports"""
        while True:
            try:
                port = port_queue.get(timeout=1)
                self.scan_port(port)
                port_queue.task_done()
            except:
                break

    def scan(self):
        """Main scanning function"""
        # Resolve target
        resolved_ip = self.resolve_target()
        if not resolved_ip:
            return
        
        self.target = resolved_ip
        self.banner()
        
        # Create port queue
        import queue
        port_queue = queue.Queue()
        
        # Add ports to queue
        if self.port_list:
            # Use specific port list
            for port in self.port_list:
                port_queue.put(port)
            total_ports = len(self.port_list)
        else:
            # Use port range
            for port in range(self.start_port, self.end_port + 1):
                port_queue.put(port)
            total_ports = self.end_port - self.start_port + 1
        
        # Start worker threads
        threads_list = []
        for _ in range(min(self.threads, port_queue.qsize())):
            t = threading.Thread(target=self.worker, args=(port_queue,))
            t.daemon = True
            t.start()
            threads_list.append(t)
        
        # Wait for completion
        start_time = time.time()
        port_queue.join()
        scan_time = time.time() - start_time
        
        # Display results
        self.display_results(scan_time, total_ports)

    def display_results(self, scan_time, total_ports):
        """Display scan results summary"""
        print("\n" + "=" * 60)
        print(f"{Colors.HEADER}{Colors.BOLD}SCAN RESULTS{Colors.ENDC}")
        print("=" * 60)
        
        if self.open_ports:
            print(f"{Colors.OKGREEN}Found {len(self.open_ports)} open ports:{Colors.ENDC}\n")
            
            # Sort by port number
            self.open_ports.sort(key=lambda x: x['port'])
            
            print(f"{'PORT':<8} {'SERVICE':<15} {'BANNER'}")
            print("-" * 60)
            
            for port_info in self.open_ports:
                banner = port_info['banner'][:40] + "..." if port_info['banner'] and len(port_info['banner']) > 40 else port_info['banner'] or ""
                print(f"{port_info['port']:<8} {port_info['service']:<15} {banner}")
        else:
            print(f"{Colors.WARNING}No open ports found in the specified range.{Colors.ENDC}")
        
        print(f"\n{Colors.OKCYAN}Scan completed in {scan_time:.2f} seconds{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Ports scanned: {total_ports}{Colors.ENDC}")

def validate_ip(ip):
    """Validate IP address format"""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def validate_hostname(hostname):
    """Basic hostname validation"""
    if len(hostname) > 255:
        return False
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-")
    return all(c in allowed for c in hostname)

def main():
    parser = argparse.ArgumentParser(
        description="Network Port Scanner - For Authorized Security Testing Only",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 network_scanner.py -t 192.168.1.1
  python3 network_scanner.py -t example.com -p 1-1000
  python3 network_scanner.py -t 10.0.0.1 -p 80,443,22,21
  python3 network_scanner.py -t 192.168.1.0/24 --top-ports
        """
    )
    
    parser.add_argument('-t', '--target', required=True,
                       help='Target IP address or hostname')
    parser.add_argument('-p', '--ports', default='1-1024',
                       help='Port range (e.g., 1-1000, 80,443,22) or "all" for 1-65535')
    parser.add_argument('--top-ports', action='store_true',
                       help='Scan top 100 most common ports')
    parser.add_argument('--threads', type=int, default=100,
                       help='Number of threads (default: 100)')
    parser.add_argument('--timeout', type=float, default=1,
                       help='Connection timeout in seconds (default: 1)')
    parser.add_argument('--stealth', action='store_true',
                       help='Use slower, more stealthy scanning')
    
    args = parser.parse_args()
    
    # Validate target
    if not (validate_ip(args.target) or validate_hostname(args.target)):
        print(f"{Colors.FAIL}Error: Invalid target format{Colors.ENDC}")
        sys.exit(1)
    
    # Parse port range
    port_list = []
    if args.top_ports:
        # Top 100 ports
        port_list = [21,22,23,25,53,69,80,110,119,123,135,139,143,161,389,443,445,993,995,1723,3306,3389,5432,5900,6379,8080,8443]
        start_port, end_port = min(port_list), max(port_list)
        print(f"{Colors.WARNING}Top ports mode - scanning most common ports{Colors.ENDC}")
    elif args.ports == 'all':
        start_port, end_port = 1, 65535
    else:
        # Parse complex port specifications (ranges and individual ports)
        try:
            for part in args.ports.split(','):
                part = part.strip()
                if '-' in part:
                    # Port range
                    range_start, range_end = map(int, part.split('-'))
                    if range_start > range_end or range_start < 1 or range_end > 65535:
                        raise ValueError(f"Invalid range: {part}")
                    port_list.extend(range(range_start, range_end + 1))
                else:
                    # Single port
                    port = int(part)
                    if port < 1 or port > 65535:
                        raise ValueError(f"Invalid port: {port}")
                    port_list.append(port)
            
            if not port_list:
                raise ValueError("No valid ports specified")
            
            # Remove duplicates and sort
            port_list = sorted(list(set(port_list)))
            start_port, end_port = min(port_list), max(port_list)
            
        except ValueError as e:
            print(f"{Colors.FAIL}Error: Invalid port specification - {e}{Colors.ENDC}")
            sys.exit(1)
    
    # Adjust settings for stealth mode
    if args.stealth:
        args.threads = min(args.threads, 10)
        args.timeout = max(args.timeout, 3)
        print(f"{Colors.WARNING}Stealth mode enabled - slower but less detectable{Colors.ENDC}")
    
    # Warning message
    print(f"{Colors.WARNING}WARNING: Use this tool only on networks you own or have explicit permission to test.{Colors.ENDC}")
    print(f"{Colors.WARNING}Unauthorized port scanning may be illegal in your jurisdiction.{Colors.ENDC}")
    
    try:
        input(f"{Colors.OKCYAN}Press Enter to continue or Ctrl+C to abort...{Colors.ENDC}")
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Scan aborted by user{Colors.ENDC}")
        sys.exit(0)
    
    # Create and run scanner
    scanner = PortScanner(
        target=args.target,
        start_port=start_port,
        end_port=end_port,
        threads=args.threads,
        timeout=args.timeout,
        port_list=port_list if port_list else None
    )
    
    try:
        scanner.scan()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Scan interrupted by user{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Error during scan: {e}{Colors.ENDC}")

if __name__ == "__main__":
    main()

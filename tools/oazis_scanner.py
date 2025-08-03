#!/usr/bin/env python3
"""
O'Azis Network Security Scanner
A professional penetration testing suite for authorized security assessments.
Created for educational and legitimate security testing purposes only.
"""

import socket
import threading
import sys
import time
import os
import json
from datetime import datetime
import subprocess
import ipaddress
import re

class Colors:
    """Terminal colors for Ice Queen theme"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PURPLE = '\033[35m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    LIGHTBLUE = '\033[94m'
    LIGHTCYAN = '\033[96m'
    ICE = '\033[96m'

class OAzisScanner:
    def __init__(self):
        self.version = "2.0"
        self.author = "O'Azis Security Team"
        self.scan_results = []
        self.target_list = []
        self.port_list = []
        self.scan_config = {
            'threads': 100,
            'timeout': 1.0,
            'stealth_mode': False,
            'save_results': True,
            'output_format': 'table'
        }
        
        # Enhanced service detection
        self.services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            69: "TFTP", 80: "HTTP", 110: "POP3", 111: "RPC", 119: "NNTP",
            123: "NTP", 135: "RPC", 139: "NetBIOS", 143: "IMAP", 161: "SNMP",
            194: "IRC", 389: "LDAP", 443: "HTTPS", 445: "SMB", 465: "SMTPS",
            514: "Syslog", 587: "SMTP", 636: "LDAPS", 993: "IMAPS", 995: "POP3S",
            1433: "MSSQL", 1521: "Oracle", 1723: "PPTP", 3306: "MySQL", 
            3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
            8080: "HTTP-Alt", 8443: "HTTPS-Alt", 9200: "Elasticsearch",
            27017: "MongoDB", 5984: "CouchDB", 6667: "IRC", 1080: "SOCKS"
        }
        
        self.common_ports = [21,22,23,25,53,69,80,110,111,119,123,135,139,143,161,194,389,443,445,465,514,587,636,993,995,1433,1521,1723,3306,3389,5432,5900,6379,8080,8443,9200,27017,5984,6667,1080]
        self.lock = threading.Lock()

    def display_banner(self):
        """Display the Ice Queen themed O'Azis banner"""
        os.system('clear' if os.name == 'posix' else 'cls')
        banner = f"""
{Colors.LIGHTCYAN}╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║    {Colors.LIGHTBLUE}██████╗{Colors.ICE} █████╗{Colors.LIGHTBLUE}███████╗{Colors.ICE}██╗{Colors.LIGHTBLUE}███████╗    ❄️  {Colors.WHITE}ICE QUEEN{Colors.LIGHTBLUE}  ❄️     {Colors.LIGHTCYAN}║
║   {Colors.LIGHTBLUE}██╔═══██╗{Colors.ICE}██╔══██╗{Colors.LIGHTBLUE}╚══███╔╝{Colors.ICE}██║{Colors.LIGHTBLUE}██╔════╝                             {Colors.LIGHTCYAN}║
║   {Colors.LIGHTBLUE}██║   ██║{Colors.ICE}███████║{Colors.LIGHTBLUE}  ███╔╝ {Colors.ICE}██║{Colors.LIGHTBLUE}███████╗    {Colors.WHITE}Network Security Scanner{Colors.LIGHTCYAN}  ║
║   {Colors.LIGHTBLUE}██║   ██║{Colors.ICE}██╔══██║{Colors.LIGHTBLUE} ███╔╝  {Colors.ICE}██║{Colors.LIGHTBLUE}╚════██║                             {Colors.LIGHTCYAN}║
║   {Colors.LIGHTBLUE}╚██████╔╝{Colors.ICE}██║  ██║{Colors.LIGHTBLUE}███████╗{Colors.ICE}██║{Colors.LIGHTBLUE}███████║    {Colors.BOLD}{Colors.WHITE}Professional Edition v{self.version}{Colors.LIGHTCYAN}    ║
║    {Colors.LIGHTBLUE}╚═════╝ {Colors.ICE}╚═╝  ╚═╝{Colors.LIGHTBLUE}╚══════╝{Colors.ICE}╚═╝{Colors.LIGHTBLUE}╚══════╝                             {Colors.LIGHTCYAN}║
║                                                                               ║
║  {Colors.WHITE}❄️  {Colors.BOLD}Created by The Ice Queen{Colors.WHITE}  ❄️                                    {Colors.LIGHTCYAN}║
║                                                                               ║
║  {Colors.LIGHTBLUE}🔍 Advanced Port Scanner    {Colors.WHITE}│{Colors.LIGHTBLUE}  🎯 Service Detection         {Colors.LIGHTCYAN}║
║  {Colors.LIGHTBLUE}⚡ Multi-threaded Engine    {Colors.WHITE}│{Colors.LIGHTBLUE}  🛡️  Stealth Mode Available   {Colors.LIGHTCYAN}║
║  {Colors.LIGHTBLUE}🔒 Banner Grabbing          {Colors.WHITE}│{Colors.LIGHTBLUE}  📊 JSON Export & Analytics   {Colors.LIGHTCYAN}║
║                                                                               ║
║  {Colors.LIGHTBLUE}Build: {Colors.WHITE}{datetime.now().strftime('%d.%m.%Y')}{Colors.LIGHTBLUE}  │  Target Systems: {Colors.WHITE}TCP/IP Networks{Colors.LIGHTBLUE}  │  Status: {Colors.GREEN}READY{Colors.LIGHTCYAN}  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.LIGHTBLUE}❄️  {Colors.WHITE}FROST PROTOCOL ACTIVATED{Colors.LIGHTBLUE}  ❄️{Colors.ENDC}
{Colors.WARNING}⚠️  Authorization Required: Use only on networks you own or have permission to test{Colors.ENDC}
"""
        print(banner)

    def display_main_menu(self):
        """Display the main interactive menu"""
        menu = f"""
{Colors.BOLD}{Colors.OKCYAN}╔══════════════════════════════════════════════════════════════╗
║                      🎯 MAIN MENU                           ║
╠══════════════════════════════════════════════════════════════╣{Colors.ENDC}
{Colors.OKGREEN}║  [1] 🎯 Single Target Scan                                  ║
║  [2] 📋 Multi-Target Scan                                   ║
║  [3] ⚙️  Scan Configuration                                  ║
║  [4] 📊 View Previous Results                               ║
║  [5] 🔧 Advanced Tools                                      ║
║  [6] 📖 Help & Documentation                               ║
║  [7] ℹ️  About O'Azis Scanner                               ║
║  [0] 🚪 Exit                                                ║{Colors.ENDC}
{Colors.BOLD}{Colors.OKCYAN}╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        print(menu)

    def get_user_input(self, prompt, input_type="string", validation=None):
        """Enhanced input handling with validation"""
        while True:
            try:
                if input_type == "string":
                    value = input(f"{Colors.OKCYAN}{prompt}{Colors.ENDC}").strip()
                elif input_type == "int":
                    value = int(input(f"{Colors.OKCYAN}{prompt}{Colors.ENDC}").strip())
                elif input_type == "float":
                    value = float(input(f"{Colors.OKCYAN}{prompt}{Colors.ENDC}").strip())
                
                if validation and not validation(value):
                    print(f"{Colors.FAIL}❌ Invalid input. Please try again.{Colors.ENDC}")
                    continue
                    
                return value
            except (ValueError, KeyboardInterrupt):
                if input_type in ["int", "float"]:
                    print(f"{Colors.FAIL}❌ Please enter a valid number.{Colors.ENDC}")
                else:
                    print(f"{Colors.FAIL}❌ Invalid input.{Colors.ENDC}")
                continue
            except EOFError:
                print(f"\n{Colors.WARNING}Exiting...{Colors.ENDC}")
                sys.exit(0)

    def validate_ip(self, ip):
        """Validate IP address"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def validate_hostname(self, hostname):
        """Validate hostname format"""
        if len(hostname) > 255 or len(hostname) == 0:
            return False
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-")
        return all(c in allowed for c in hostname)

    def validate_target(self, target):
        """Validate if target is valid IP or hostname"""
        return self.validate_ip(target) or self.validate_hostname(target)

    def parse_port_input(self, port_input):
        """Parse flexible port input (ranges, lists, keywords)"""
        ports = []
        
        if port_input.lower() == "common":
            return self.common_ports
        elif port_input.lower() == "all":
            return list(range(1, 65536))
        elif port_input.lower() == "top1000":
            # Top 1000 ports (simplified)
            return list(range(1, 1001))
        
        try:
            for part in port_input.split(','):
                part = part.strip()
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    if start > end or start < 1 or end > 65535:
                        raise ValueError(f"Invalid range: {part}")
                    ports.extend(range(start, end + 1))
                else:
                    port = int(part)
                    if port < 1 or port > 65535:
                        raise ValueError(f"Invalid port: {port}")
                    ports.append(port)
            
            return sorted(list(set(ports)))
        except ValueError as e:
            print(f"{Colors.FAIL}❌ Port parsing error: {e}{Colors.ENDC}")
            return None

    def single_target_scan(self):
        """Interactive single target scanning"""
        print(f"\n{Colors.BOLD}{Colors.OKGREEN}🎯 SINGLE TARGET SCAN{Colors.ENDC}")
        print("=" * 60)
        
        # Get target
        target = self.get_user_input(
            "🎯 Enter target (IP or hostname): ",
            validation=self.validate_target
        )
        
        # Get ports
        print(f"\n{Colors.OKCYAN}Port Options:{Colors.ENDC}")
        print("  • Ranges: 1-1000, 8000-9000")
        print("  • Lists: 22,80,443,8080")
        print("  • Mixed: 20-25,80,443,8000-8090")
        print("  • Keywords: 'common', 'all', 'top1000'")
        
        port_input = self.get_user_input("🔍 Enter ports to scan: ")
        ports = self.parse_port_input(port_input)
        
        if not ports:
            return
        
        # Scan options
        print(f"\n{Colors.OKCYAN}Scan Options:{Colors.ENDC}")
        stealth = self.get_user_input("🥷 Enable stealth mode? (y/n): ").lower() == 'y'
        
        if stealth:
            threads = min(self.scan_config['threads'], 10)
            timeout = max(self.scan_config['timeout'], 3.0)
            print(f"{Colors.WARNING}🔒 Stealth mode enabled: {threads} threads, {timeout}s timeout{Colors.ENDC}")
        else:
            threads = self.scan_config['threads']
            timeout = self.scan_config['timeout']
        
        # Confirmation
        print(f"\n{Colors.BOLD}{Colors.WARNING}📋 SCAN SUMMARY:{Colors.ENDC}")
        print(f"  Target: {Colors.BOLD}{target}{Colors.ENDC}")
        print(f"  Ports: {Colors.BOLD}{len(ports)} ports{Colors.ENDC}")
        print(f"  Mode: {Colors.BOLD}{'Stealth' if stealth else 'Normal'}{Colors.ENDC}")
        
        confirm = self.get_user_input("\n🚀 Start scan? (y/n): ").lower()
        if confirm != 'y':
            print(f"{Colors.WARNING}Scan cancelled.{Colors.ENDC}")
            return
        
        # Execute scan
        self.execute_scan([target], ports, threads, timeout, stealth)

    def multi_target_scan(self):
        """Interactive multi-target scanning"""
        print(f"\n{Colors.BOLD}{Colors.OKGREEN}📋 MULTI-TARGET SCAN{Colors.ENDC}")
        print("=" * 60)
        
        targets = []
        print(f"{Colors.OKCYAN}Enter targets (one per line, empty line to finish):{Colors.ENDC}")
        
        while True:
            target = input(f"{Colors.OKCYAN}Target {len(targets)+1}: {Colors.ENDC}").strip()
            if not target:
                break
            if self.validate_target(target):
                targets.append(target)
                print(f"{Colors.OKGREEN}✅ Added: {target}{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}❌ Invalid target: {target}{Colors.ENDC}")
        
        if not targets:
            print(f"{Colors.WARNING}No valid targets provided.{Colors.ENDC}")
            return
        
        # Get ports (same as single target)
        port_input = self.get_user_input("🔍 Enter ports to scan: ")
        ports = self.parse_port_input(port_input)
        
        if not ports:
            return
        
        # Execute scan for all targets
        print(f"\n{Colors.BOLD}{Colors.WARNING}📋 MULTI-SCAN SUMMARY:{Colors.ENDC}")
        print(f"  Targets: {Colors.BOLD}{len(targets)}{Colors.ENDC}")
        print(f"  Ports per target: {Colors.BOLD}{len(ports)}{Colors.ENDC}")
        print(f"  Total scans: {Colors.BOLD}{len(targets) * len(ports)}{Colors.ENDC}")
        
        confirm = self.get_user_input("\n🚀 Start multi-target scan? (y/n): ").lower()
        if confirm == 'y':
            self.execute_scan(targets, ports, self.scan_config['threads'], 
                            self.scan_config['timeout'], self.scan_config['stealth_mode'])

    def scan_configuration(self):
        """Configure scan settings"""
        print(f"\n{Colors.BOLD}{Colors.OKGREEN}⚙️ SCAN CONFIGURATION{Colors.ENDC}")
        print("=" * 60)
        
        print(f"\n{Colors.OKCYAN}Current Configuration:{Colors.ENDC}")
        print(f"  Threads: {Colors.BOLD}{self.scan_config['threads']}{Colors.ENDC}")
        print(f"  Timeout: {Colors.BOLD}{self.scan_config['timeout']}s{Colors.ENDC}")
        print(f"  Stealth Mode: {Colors.BOLD}{'Enabled' if self.scan_config['stealth_mode'] else 'Disabled'}{Colors.ENDC}")
        print(f"  Save Results: {Colors.BOLD}{'Yes' if self.scan_config['save_results'] else 'No'}{Colors.ENDC}")
        
        while True:
            print(f"\n{Colors.OKCYAN}Configuration Options:{Colors.ENDC}")
            print("  [1] Set thread count")
            print("  [2] Set timeout")
            print("  [3] Toggle stealth mode")
            print("  [4] Toggle save results")
            print("  [0] Back to main menu")
            
            choice = self.get_user_input("Choose option: ")
            
            if choice == "1":
                threads = self.get_user_input(
                    "Enter thread count (1-500): ",
                    input_type="int",
                    validation=lambda x: 1 <= x <= 500
                )
                self.scan_config['threads'] = threads
                print(f"{Colors.OKGREEN}✅ Thread count set to {threads}{Colors.ENDC}")
                
            elif choice == "2":
                timeout = self.get_user_input(
                    "Enter timeout in seconds (0.1-30): ",
                    input_type="float",
                    validation=lambda x: 0.1 <= x <= 30
                )
                self.scan_config['timeout'] = timeout
                print(f"{Colors.OKGREEN}✅ Timeout set to {timeout}s{Colors.ENDC}")
                
            elif choice == "3":
                self.scan_config['stealth_mode'] = not self.scan_config['stealth_mode']
                status = "enabled" if self.scan_config['stealth_mode'] else "disabled"
                print(f"{Colors.OKGREEN}✅ Stealth mode {status}{Colors.ENDC}")
                
            elif choice == "4":
                self.scan_config['save_results'] = not self.scan_config['save_results']
                status = "enabled" if self.scan_config['save_results'] else "disabled"
                print(f"{Colors.OKGREEN}✅ Save results {status}{Colors.ENDC}")
                
            elif choice == "0":
                break

    def scan_port(self, target, port):
        """Scan a single port on target"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.scan_config['timeout'])
            result = sock.connect_ex((target, port))
            
            if result == 0:
                banner = self.grab_banner(sock, port)
                service = self.services.get(port, "Unknown")
                
                with self.lock:
                    scan_result = {
                        'target': target,
                        'port': port,
                        'service': service,
                        'banner': banner,
                        'timestamp': datetime.now().isoformat()
                    }
                    self.scan_results.append(scan_result)
                    
                    # Real-time output
                    banner_text = f" - {banner[:50]}..." if banner and len(banner) > 50 else f" - {banner}" if banner else ""
                    print(f"{Colors.OKGREEN}[+] {target}:{port:5d} - {service:15s} - OPEN{banner_text}{Colors.ENDC}")
            
            sock.close()
        except Exception:
            pass

    def grab_banner(self, sock, port):
        """Enhanced banner grabbing"""
        try:
            if port in [21, 22, 23, 25, 110, 143, 220, 993, 995]:
                sock.settimeout(2)
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                return banner[:200] if banner else None
            elif port in [80, 8080, 8443]:
                sock.send(b"HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n")
                response = sock.recv(1024).decode('utf-8', errors='ignore')
                server_lines = [line for line in response.split('\n') if 'Server:' in line]
                return server_lines[0].strip() if server_lines else None
        except:
            pass
        return None

    def worker_thread(self, target, port_queue):
        """Worker thread for port scanning"""
        while True:
            try:
                port = port_queue.get(timeout=1)
                self.scan_port(target, port)
                port_queue.task_done()
            except:
                break

    def execute_scan(self, targets, ports, threads, timeout, stealth):
        """Execute the actual scanning process"""
        import queue
        
        print(f"\n{Colors.BOLD}{Colors.HEADER}🚀 INITIATING O'AZIS SCAN{Colors.ENDC}")
        print("=" * 70)
        
        total_scans = len(targets) * len(ports)
        scan_start = time.time()
        
        for target_idx, target in enumerate(targets, 1):
            print(f"\n{Colors.OKCYAN}📡 Scanning target {target_idx}/{len(targets)}: {Colors.BOLD}{target}{Colors.ENDC}")
            print(f"{Colors.OKCYAN}Ports: {len(ports)} | Threads: {threads} | Timeout: {timeout}s{Colors.ENDC}")
            print("-" * 60)
            
            # Resolve target
            try:
                resolved_ip = socket.gethostbyname(target)
                if resolved_ip != target:
                    print(f"{Colors.OKBLUE}🔍 Resolved {target} → {resolved_ip}{Colors.ENDC}")
                target_ip = resolved_ip
            except socket.gaierror:
                print(f"{Colors.FAIL}❌ Could not resolve {target}{Colors.ENDC}")
                continue
            
            # Create port queue
            port_queue = queue.Queue()
            for port in ports:
                port_queue.put(port)
            
            # Start worker threads
            thread_list = []
            active_threads = min(threads, len(ports))
            
            for _ in range(active_threads):
                t = threading.Thread(target=self.worker_thread, args=(target_ip, port_queue))
                t.daemon = True
                t.start()
                thread_list.append(t)
            
            # Wait for completion
            target_start = time.time()
            port_queue.join()
            target_time = time.time() - target_start
            
            target_results = [r for r in self.scan_results if r['target'] == target_ip]
            print(f"\n{Colors.OKGREEN}✅ Target {target} complete: {len(target_results)} open ports in {target_time:.2f}s{Colors.ENDC}")
        
        total_time = time.time() - scan_start
        self.display_scan_results(total_time, total_scans)

    def display_scan_results(self, scan_time, total_scans):
        """Display comprehensive scan results"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}📊 O'AZIS SCAN RESULTS{Colors.ENDC}")
        print("=" * 70)
        
        if not self.scan_results:
            print(f"{Colors.WARNING}🔍 No open ports discovered in scan.{Colors.ENDC}")
            return
        
        # Group results by target
        targets = {}
        for result in self.scan_results:
            target = result['target']
            if target not in targets:
                targets[target] = []
            targets[target].append(result)
        
        # Display results per target
        for target, results in targets.items():
            print(f"\n{Colors.BOLD}{Colors.OKCYAN}🎯 Target: {target}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}Open Ports: {len(results)}{Colors.ENDC}")
            print("-" * 60)
            print(f"{'PORT':<8} {'SERVICE':<15} {'BANNER':<45}")
            print("-" * 60)
            
            for result in sorted(results, key=lambda x: x['port']):
                banner = result['banner'][:42] + "..." if result['banner'] and len(result['banner']) > 42 else result['banner'] or ""
                print(f"{result['port']:<8} {result['service']:<15} {banner:<45}")
        
        # Summary
        print(f"\n{Colors.BOLD}{Colors.OKGREEN}📈 SCAN SUMMARY{Colors.ENDC}")
        print(f"  Total Targets: {Colors.BOLD}{len(targets)}{Colors.ENDC}")
        print(f"  Open Ports: {Colors.BOLD}{len(self.scan_results)}{Colors.ENDC}")
        print(f"  Total Scans: {Colors.BOLD}{total_scans:,}{Colors.ENDC}")
        print(f"  Scan Time: {Colors.BOLD}{scan_time:.2f} seconds{Colors.ENDC}")
        print(f"  Rate: {Colors.BOLD}{total_scans/scan_time:.1f} scans/sec{Colors.ENDC}")
        
        # Save results
        if self.scan_config['save_results']:
            self.save_scan_results()

    def save_scan_results(self):
        """Save scan results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"oazis_scan_{timestamp}.json"
        
        scan_data = {
            'scan_info': {
                'scanner': 'O\'Azis Network Security Scanner',
                'version': self.version,
                'timestamp': datetime.now().isoformat(),
                'total_results': len(self.scan_results)
            },
            'configuration': self.scan_config,
            'results': self.scan_results
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(scan_data, f, indent=2)
            print(f"{Colors.OKGREEN}💾 Results saved to: {filename}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}❌ Failed to save results: {e}{Colors.ENDC}")

    def show_help(self):
        """Display help and documentation"""
        help_text = f"""
{Colors.BOLD}{Colors.OKGREEN}📖 O'AZIS SCANNER HELP{Colors.ENDC}
{'=' * 50}

{Colors.OKCYAN}🎯 SCANNING MODES:{Colors.ENDC}
  • Single Target  - Scan one IP/hostname
  • Multi-Target   - Scan multiple targets
  
{Colors.OKCYAN}🔍 PORT SPECIFICATIONS:{Colors.ENDC}
  • Ranges:   1-1000, 8000-9000
  • Lists:    22,80,443,8080
  • Mixed:    20-25,80,443,8000-8090
  • Keywords: 'common', 'all', 'top1000'
  
{Colors.OKCYAN}⚙️ CONFIGURATION OPTIONS:{Colors.ENDC}
  • Threads:      1-500 (default: 100)
  • Timeout:      0.1-30s (default: 1s)
  • Stealth Mode: Slower, less detectable
  • Save Results: Auto-save to JSON
  
{Colors.OKCYAN}🔧 ADVANCED FEATURES:{Colors.ENDC}
  • Service Detection: 50+ common services
  • Banner Grabbing:   Version identification
  • Multi-threading:   High-speed scanning
  • Real-time Output:  Live scan results
  • JSON Export:       Machine-readable results
  
{Colors.WARNING}⚠️ LEGAL NOTICE:{Colors.ENDC}
Use only on networks you own or have explicit permission to test.
Unauthorized scanning may violate laws and regulations.
        """
        print(help_text)
        input(f"{Colors.OKCYAN}Press Enter to continue...{Colors.ENDC}")

    def show_about(self):
        """Display about information"""
        about_text = f"""
{Colors.BOLD}{Colors.HEADER}ℹ️ ABOUT O'AZIS SCANNER{Colors.ENDC}
{'=' * 50}

{Colors.OKCYAN}Scanner Information:{Colors.ENDC}
  Name:     O'Azis Network Security Scanner
  Version:  {self.version}
  Author:   {self.author}
  Build:    {datetime.now().strftime('%Y.%m.%d')}
  
{Colors.OKCYAN}Technical Specifications:{Colors.ENDC}
  • Multi-threaded TCP port scanning
  • Service fingerprinting (50+ services)
  • Banner grabbing and version detection
  • Flexible target and port specification
  • JSON result export
  • Stealth scanning capabilities
  
{Colors.OKCYAN}Supported Protocols:{Colors.ENDC}
  TCP, HTTP/HTTPS, SSH, FTP, SMTP, POP3, IMAP,
  Telnet, DNS, LDAP, SMB, RDP, VNC, MySQL,
  PostgreSQL, MongoDB, Redis, Elasticsearch
  
{Colors.OKGREEN}🔒 Built for legitimate security professionals and ethical hackers.{Colors.ENDC}
        """
        print(about_text)
        input(f"{Colors.OKCYAN}Press Enter to continue...{Colors.ENDC}")

    def main_loop(self):
        """Main application loop"""
        while True:
            self.display_banner()
            self.display_main_menu()
            
            choice = self.get_user_input("🎯 Select option: ")
            
            if choice == "1":
                self.single_target_scan()
            elif choice == "2":
                self.multi_target_scan()
            elif choice == "3":
                self.scan_configuration()
            elif choice == "4":
                print(f"{Colors.WARNING}📊 Results viewing feature coming soon!{Colors.ENDC}")
                time.sleep(2)
            elif choice == "5":
                print(f"{Colors.WARNING}🔧 Advanced tools coming soon!{Colors.ENDC}")
                time.sleep(2)
            elif choice == "6":
                self.show_help()
            elif choice == "7":
                self.show_about()
            elif choice == "0":
                print(f"\n{Colors.OKGREEN}👋 Thank you for using O'Azis Scanner!{Colors.ENDC}")
                print(f"{Colors.OKCYAN}Stay secure! 🔒{Colors.ENDC}\n")
                sys.exit(0)
            else:
                print(f"{Colors.FAIL}❌ Invalid option. Please try again.{Colors.ENDC}")
                time.sleep(1)

def main():
    """Main application entry point"""
    try:
        scanner = OAzisScanner()
        scanner.main_loop()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}🛑 Scan interrupted by user.{Colors.ENDC}")
        print(f"{Colors.OKGREEN}👋 Goodbye!{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.FAIL}❌ Critical error: {e}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()

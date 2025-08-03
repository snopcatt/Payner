#!/usr/bin/env python3
"""
Batman Load Testing Tool
An authorized stress testing suite for web servers.
Created for legitimate and authorized load testing purposes.
"""

import requests
import threading
import time
import sys
import os
from datetime import datetime

class Colors:
    """Terminal colors for Batman theme"""
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
    DARK = '\033[90m'

class Batman:
    def __init__(self):
        self.version = "1.0"
        self.author = "The Dark Knight"
        self.target_url = ""
        self.request_count = 0
        self.thread_count = 10
        self.successful_requests = 0
        self.failed_requests = 0
        self.lock = threading.Lock()

    def display_banner(self):
        """Display the themed banner"""
        os.system('clear' if os.name == 'posix' else 'cls')
        banner = f"""
{Colors.YELLOW}╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║    {Colors.BOLD}{Colors.YELLOW}██████╗  █████╗ ████████╗███╗   ███╗ █████╗ ███╗   ██╗{Colors.ENDC}{Colors.YELLOW}                ║
║    {Colors.BOLD}{Colors.YELLOW}██╔══██╗██╔══██╗╚══██╔══╝████╗ ████║██╔══██╗████╗  ██║{Colors.ENDC}{Colors.YELLOW}                ║
║    {Colors.BOLD}{Colors.YELLOW}██████╔╝███████║   ██║   ██╔████╔██║███████║██╔██╗ ██║{Colors.ENDC}{Colors.YELLOW}  🦇 {Colors.BOLD}{Colors.WHITE}THE DARK KNIGHT{Colors.ENDC}{Colors.YELLOW} 🦇  ║
║    {Colors.BOLD}{Colors.YELLOW}██╔══██╗██╔══██║   ██║   ██║╚██╔╝██║██╔══██║██║╚██╗██║{Colors.ENDC}{Colors.YELLOW}                ║
║    {Colors.BOLD}{Colors.YELLOW}██████╔╝██║  ██║   ██║   ██║ ╚═╝ ██║██║  ██║██║ ╚████║{Colors.ENDC}{Colors.YELLOW}                ║
║    {Colors.BOLD}{Colors.YELLOW}╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝{Colors.ENDC}{Colors.YELLOW}                ║
║                                                                               ║
║  {Colors.BOLD}{Colors.WHITE}🦇 BATMAN LOAD TESTING TOOL v{self.version} - WEB STRESS TESTER 🦇{Colors.ENDC}{Colors.YELLOW}            ║
║                                                                               ║  
║  {Colors.CYAN}🔧 Multi-threaded HTTP Requests  {Colors.WHITE}│{Colors.CYAN}  ⚡ Concurrent Load Testing{Colors.ENDC}{Colors.YELLOW}        ║
║  {Colors.CYAN}📊 Real-time Statistics         {Colors.WHITE}│{Colors.CYAN}  🎯 Target Performance Analysis{Colors.ENDC}{Colors.YELLOW}   ║
║  {Colors.CYAN}🚀 Customizable Request Patterns{Colors.WHITE}│{Colors.CYAN}  📈 Response Time Monitoring{Colors.ENDC}{Colors.YELLOW}     ║
║                                                                               ║
║  {Colors.OKBLUE}Author: {Colors.WHITE}{self.author}{Colors.ENDC}{Colors.YELLOW}  │  Build: {Colors.WHITE}{datetime.now().strftime('%d.%m.%Y')}{Colors.ENDC}{Colors.YELLOW}  │  Status: {Colors.GREEN}READY{Colors.ENDC}{Colors.YELLOW}           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.YELLOW}🦇  {Colors.WHITE}GOTHAM PROTOCOL INITIATED{Colors.YELLOW}  🦇{Colors.ENDC}
{Colors.WARNING}⚠️  AUTHORIZATION REQUIRED: Use only on websites you own or have explicit permission to test{Colors.ENDC}
"""
        print(banner)

    def display_main_menu(self):
        """Display the main menu"""
        menu = f"""
{Colors.BOLD}{Colors.OKBLUE}╔══════════════════════════════════════════════════════════════╗
║                      🦇 MAIN MENU                           ║
╠══════════════════════════════════════════════════════════════╣{Colors.ENDC}
{Colors.OKGREEN}║  [1] 🎯 Set Target URL                                    ║
║  [2] ⚙️  Configure Load Testing                             ║
║  [3] 🚀 Start Load Test                                    ║
║  [4] 📊 View Test Results                                  ║
║  [0] 🚪 Exit                                               ║{Colors.ENDC}
{Colors.BOLD}{Colors.OKBLUE}╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        print(menu)

    def get_user_input(self, prompt, input_type="string", validation=None):
        """Enhanced input handling with validation"""
        while True:
            try:
                if input_type == "string":
                    value = input(f"{Colors.OKBLUE}{prompt}{Colors.ENDC}").strip()
                elif input_type == "int":
                    value = int(input(f"{Colors.OKBLUE}{prompt}{Colors.ENDC}").strip())

                if validation and not validation(value):
                    print(f"{Colors.FAIL}❌ Invalid input. Please try again.{Colors.ENDC}")
                    continue

                return value
            except (ValueError, KeyboardInterrupt):
                print(f"{Colors.FAIL}❌ Invalid input.{Colors.ENDC}")
                continue
            except EOFError:
                print(f"\n{Colors.WARNING}Exiting...{Colors.ENDC}")
                sys.exit(0)


    def configure_load_test(self):
        """Configure load testing parameters"""
        print(f"\n{Colors.BOLD}{Colors.OKGREEN}⚙️ LOAD TEST CONFIGURATION{Colors.ENDC}")
        print("=" * 60)

        # Request count
        self.request_count = self.get_user_input(
            "📦 Enter number of requests (e.g., 1000): ",
            input_type="int",
            validation=lambda x: x > 0
        )

        # Threads
        self.thread_count = self.get_user_input(
            "⚙️ Enter number of threads (e.g., 10): ",
            input_type="int",
            validation=lambda x: 1 <= x <= 500
        )

    def perform_request(self, thread_id):
        """Execute HTTP requests in a separate thread"""
        while True:
            if self.successful_requests + self.failed_requests >= self.request_count:
                break

            try:
                response = requests.get(self.target_url, timeout=5)
                with self.lock:
                    if response.status_code == 200:
                        self.successful_requests += 1
                        print(f"{Colors.OKGREEN}[Thread {thread_id}] 🚀 Success {self.successful_requests}{Colors.ENDC}")
                    else:
                        self.failed_requests += 1
                        print(f"{Colors.WARNING}[Thread {thread_id}] ⚠️ HTTP {response.status_code} - Failed {self.failed_requests}{Colors.ENDC}")
            except requests.RequestException as e:
                with self.lock:
                    self.failed_requests += 1
                    print(f"{Colors.FAIL}[Thread {thread_id}] ❌ Failed {self.failed_requests} - {str(e)[:50]}{Colors.ENDC}")

    def start_load_test(self):
        """Start performing load test on the target URL"""
        if not self.target_url:
            print(f"{Colors.WARNING}❌ No target URL set. Please set the target URL first.{Colors.ENDC}")
            return

        print(f"\n{Colors.BOLD}{Colors.OKCYAN}🚀 STARTING LOAD TEST{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Target: {self.target_url} | Requests: {self.request_count} | Threads: {self.thread_count}{Colors.ENDC}")
        print("-" * 60)

        threads = []
        self.successful_requests = 0
        self.failed_requests = 0

        # Start threads
        for i in range(self.thread_count):
            thread = threading.Thread(target=self.perform_request, args=(i+1,))
            thread.start()
            threads.append(thread)

        # Wait for completion
        for thread in threads:
            thread.join()

        print(f"\n{Colors.OKGREEN}✅ Load test completed.{Colors.ENDC}")

    def view_test_results(self):
        """Display test results"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}📊 LOAD TEST RESULTS{Colors.ENDC}")
        print("=" * 60)
        print(f"Successful requests: {Colors.OKGREEN}{self.successful_requests}{Colors.ENDC}")
        print(f"Failed requests: {Colors.FAIL}{self.failed_requests}{Colors.ENDC}")

    def main_loop(self):
        """Main application loop"""
        while True:
            self.display_banner()
            self.display_main_menu()

            choice = self.get_user_input("⚙️ Select option: ")

            if choice == "1":
                self.target_url = self.get_user_input("🎯 Enter target URL: ", validation=lambda x: x.startswith("http"))
            elif choice == "2":
                self.configure_load_test()
            elif choice == "3":
                self.start_load_test()
            elif choice == "4":
                self.view_test_results()
            elif choice == "0":
                print(f"\n{Colors.OKGREEN}👋 Thank you for using Batman Load Testing Tool!{Colors.ENDC}")
                print(f"{Colors.OKCYAN}Stay secure! 🔒{Colors.ENDC}\n")
                sys.exit(0)
            else:
                print(f"{Colors.FAIL}❌ Invalid option. Please try again.{Colors.ENDC}")


def main():
    """Main application entry point"""
    try:
        batman = Batman()
        batman.main_loop()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}🛑 Test interrupted by user.{Colors.ENDC}")
        print(f"{Colors.OKGREEN}👋 Goodbye!{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.FAIL}❌ Critical error: {e}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()


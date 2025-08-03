#!/bin/bash

# Payner - Professional Tool Suite
# Version: 2.0
# Author: Payner Development Team

# Color definitions for enhanced UI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
DIM='\033[2m'
UNDERLINE='\033[4m'
BLINK='\033[5m'
NC='\033[0m' # No Color

# Configuration
VERSION="3.0"
AUTHOR="Payner Development Team"
TOOLS_DIR="$(dirname "$0")/tools"
LOG_FILE="$HOME/.payner.log"
CONFIG_FILE="$HOME/.payner.conf"
REPORTS_DIR="$HOME/.payner_reports"
TEMP_DIR="/tmp/payner"

# Create necessary directories
mkdir -p "$REPORTS_DIR" "$TEMP_DIR"

# Load configuration if exists
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi

# Logging function
log_action() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Error handling function
handle_error() {
    echo -e "${RED}${BOLD}⚠️  ERROR: $1${NC}"
    log_action "ERROR: $1"
    echo -e "${YELLOW}Press Enter to continue...${NC}"
    read
}

# Success message function
show_success() {
    echo -e "${GREEN}${BOLD}✅ $1${NC}"
    log_action "SUCCESS: $1"
}

# Check if tool exists
check_tool() {
    local tool_path="$1"
    local tool_name="$2"
    
    if [ -f "$tool_path" ]; then
        return 0
    else
        handle_error "$tool_name not found at $tool_path"
        return 1
    fi
}

# Function to display Payner logo and menu
show_main_menu() {
    clear
    echo -e "${BOLD}${YELLOW}"
    echo "════════════════════════════════════════════════════════════════════════════"
    echo "║                                                                          ║"
    echo "║  ██████╗  █████╗ ██╗   ██╗███╗   ██╗███████╗██████╗                     ║"
    echo "║  ██╔══██╗██╔══██╗╚██╗ ██╔╝████╗  ██║██╔════╝██╔══██╗                    ║"
    echo "║  ██████╔╝███████║ ╚████╔╝ ██╔██╗ ██║█████╗  ██████╔╝                    ║"
    echo "║  ██╔═══╝ ██╔══██║  ╚██╔╝  ██║╚██╗██║██╔══╝  ██╔══██╗                    ║"
    echo "║  ██║     ██║  ██║   ██║   ██║ ╚████║███████╗██║  ██║                    ║"
    echo "║  ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝                    ║"
    echo "║                                                                          ║"
    echo "════════════════════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    
    echo -e "${BOLD}${CYAN}                    🎵 MEGA TOOL COLLECTION 🎵${NC}"
    echo -e "${YELLOW}                    ━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BOLD}${GREEN}┌─────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${BOLD}${GREEN}│${NC}  ${BOLD}${WHITE}🎯 CHOOSE YOUR WEAPON:${NC}                                    ${BOLD}${GREEN}│${NC}"
    echo -e "${BOLD}${GREEN}├─────────────────────────────────────────────────────────────┤${NC}"
    echo -e "${BOLD}${GREEN}│${NC}                                                             ${BOLD}${GREEN}│${NC}"
    echo -e "${BOLD}${GREEN}│${NC}  ${BOLD}${YELLOW}[1]${NC} ${CYAN}🦇 BATMAN${NC}      - ${WHITE}Load Testing Tool${NC}                   ${BOLD}${GREEN}│${NC}"
    echo -e "${BOLD}${GREEN}│${NC}  ${BOLD}${YELLOW}[2]${NC} ${CYAN}❄️  PRINCEFROST${NC} - ${WHITE}Network Security Scanner${NC}            ${BOLD}${GREEN}│${NC}"
    echo -e "${BOLD}${GREEN}│${NC}  ${BOLD}${YELLOW}[3]${NC} ${PURPLE}🔍 SPIDER-MAN${NC}  - ${WHITE}Network Diagnostics${NC}                  ${BOLD}${GREEN}│${NC}"
    echo -e "${BOLD}${GREEN}│${NC}  ${BOLD}${YELLOW}[4]${NC} ${GREEN}📊 HULK${NC}        - ${WHITE}System Monitor${NC}                       ${BOLD}${GREEN}│${NC}"
    echo -e "${BOLD}${GREEN}│${NC}  ${BOLD}${YELLOW}[5]${NC} ${RED}🔥 THOR${NC}        - ${WHITE}Web Analysis${NC}                         ${BOLD}${GREEN}│${NC}"
    echo -e "${BOLD}${GREEN}│${NC}  ${BOLD}${YELLOW}[6]${NC} ${BLUE}📡 PACKET COLLECTOR${NC} - ${WHITE}Network Packet Capture${NC}      ${BOLD}${GREEN}│${NC}"
    echo -e "${BOLD}${GREEN}│${NC}                                                             ${BOLD}${GREEN}│${NC}"
    echo -e "${BOLD}${GREEN}│${NC}  ${BOLD}${YELLOW}[8]${NC} ${BLUE}🔧 STATUS${NC}     - ${WHITE}Check Tool Availability${NC}               ${BOLD}${GREEN}│${NC}"
    echo -e "${BOLD}${GREEN}│${NC}  ${BOLD}${YELLOW}[9]${NC} ${CYAN}📊 REPORTS${NC}    - ${WHITE}View Generated Reports${NC}                ${BOLD}${GREEN}│${NC}"
    echo -e "${BOLD}${GREEN}│${NC}  ${BOLD}${YELLOW}[0]${NC} ${RED}🚪 EXIT${NC}       - ${WHITE}Exit Payner Suite${NC}                    ${BOLD}${GREEN}│${NC}"
    echo -e "${BOLD}${GREEN}│${NC}                                                             ${BOLD}${GREEN}│${NC}"
    echo -e "${BOLD}${GREEN}└─────────────────────────────────────────────────────────────┘${NC}"
    echo ""
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${WHITE}             🎶 Powered by Payner Technology 🎶${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Function to display tool status
show_tool_status() {
    echo -e "${BOLD}${BLUE}┌─────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${BOLD}${BLUE}│${NC}  ${BOLD}${WHITE}🔧 TOOL STATUS CHECK${NC}                                     ${BOLD}${BLUE}│${NC}"
    echo -e "${BOLD}${BLUE}├─────────────────────────────────────────────────────────────┤${NC}"
    
    local tools=(
        "$TOOLS_DIR/batman.py:BATMAN"
        "$TOOLS_DIR/oazis_scanner.py:OAZIS"
        "$TOOLS_DIR/Palavo-Oko/palavo_oko.sh:PALAVO OKO"
        "$TOOLS_DIR/network_scanner.py:MILKO"
        "$TOOLS_DIR/packet_collector.py:PACKET COLLECTOR"
    )
    
    for tool in "${tools[@]}"; do
        IFS=':' read -r path name <<< "$tool"
        if [ -f "$path" ]; then
            echo -e "${BOLD}${BLUE}│${NC}  ${GREEN}✅ $name${NC} - Ready                                       ${BOLD}${BLUE}│${NC}"
        else
            echo -e "${BOLD}${BLUE}│${NC}  ${RED}❌ $name${NC} - Not Found                                 ${BOLD}${BLUE}│${NC}"
        fi
    done
    
    echo -e "${BOLD}${BLUE}└─────────────────────────────────────────────────────────────┘${NC}"
    echo ""
}

# Function to launch Batman
launch_batman() {
    echo -e "${BOLD}${YELLOW}🦇 Initializing BATMAN Load Testing Tool...${NC}"
    log_action "Launching BATMAN tool"
    sleep 1
    
    if check_tool "$TOOLS_DIR/batman.py" "BATMAN"; then
        show_success "BATMAN tool found and launching..."
        echo -e "${DIM}${CYAN}Loading Batman's arsenal...${NC}"
        sleep 1
        python3 "$TOOLS_DIR/batman.py"
        log_action "BATMAN tool execution completed"
    fi
    
    echo -e "${YELLOW}Press Enter to return to main menu...${NC}"
    read
}

# Function to launch PrinceFrost
launch_princefrost() {
    echo -e "${BOLD}${CYAN}❄️  Initializing PRINCEFROST Security Scanner...${NC}"
    log_action "Launching PRINCEFROST tool"
    sleep 1
    
    if check_tool "$TOOLS_DIR/oazis_scanner.py" "PRINCEFROST"; then
        show_success "PRINCEFROST scanner ready for deployment..."
        echo -e "${DIM}${CYAN}Activating frost protocols...${NC}"
        sleep 1
        python3 "$TOOLS_DIR/oazis_scanner.py"
        log_action "PRINCEFROST tool execution completed"
    fi
    
    echo -e "${YELLOW}Press Enter to return to main menu...${NC}"
    read
}

# Function to launch Palavo Oko
launch_palavo_oko() {
    echo -e "${BOLD}${GREEN}🕵️  Initializing PALAVO OKO Network Scanner...${NC}"
    log_action "Launching PALAVO OKO tool"
    sleep 1
    
    if check_tool "$TOOLS_DIR/Palavo-Oko/palavo_oko.sh" "PALAVO OKO"; then
        show_success "PALAVO OKO surveillance system online..."
        echo -e "${DIM}${GREEN}Engaging reconnaissance mode...${NC}"
        sleep 1
        bash "$TOOLS_DIR/Palavo-Oko/palavo_oko.sh"
        log_action "PALAVO OKO tool execution completed"
    fi
}

# Function to launch Milko
launch_milko() {
    echo -e "${BOLD}${PURPLE}🎯 Initializing MILKO Advanced Port Scanner...${NC}"
    log_action "Launching MILKO tool"
    sleep 1
    
    if check_tool "$TOOLS_DIR/network_scanner.py" "MILKO"; then
        show_success "MILKO targeting system activated..."
        echo -e "${DIM}${PURPLE}Calibrating scanning modules...${NC}"
        sleep 1
        python3 "$TOOLS_DIR/network_scanner.py"
        log_action "MILKO tool execution completed"
    fi
}

# Function to launch Packet Collector
launch_packet_collector() {
    echo -e "${BOLD}${BLUE}📡 Initializing PACKET COLLECTOR...${NC}"
    log_action "Launching PACKET COLLECTOR"
    sleep 1
    
    if check_tool "$TOOLS_DIR/packet_collector.py" "PACKET COLLECTOR"; then
        show_success "PACKET COLLECTOR ready to capture packets..."
        echo -e "${DIM}${BLUE}Capturing packets, please wait...${NC}"
        sleep 1
        python3 "$TOOLS_DIR/packet_collector.py"
        log_action "PACKET COLLECTOR execution completed"
    fi
    
    echo -e "${YELLOW}Press Enter to return to main menu...${NC}"
    read
}

# Function to launch Spider-Man (Network Diagnostics)
launch_spiderman() {
    echo -e "${BOLD}${PURPLE}🔍 Initializing SPIDER-MAN Network Diagnostics...${NC}"
    log_action "Launching SPIDER-MAN diagnostics"
    sleep 1
    
    local report_file="$REPORTS_DIR/spiderman_$(date +%Y%m%d_%H%M%S).txt"
    
    echo -e "${BOLD}${PURPLE}┌─────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${BOLD}${PURPLE}│${NC}  ${BOLD}${WHITE}🔍 SPIDER-MAN NETWORK DIAGNOSTICS${NC}                       ${BOLD}${PURPLE}│${NC}"
    echo -e "${BOLD}${PURPLE}├─────────────────────────────────────────────────────────────────┤${NC}"
    echo -e "${BOLD}${PURPLE}│${NC}  ${YELLOW}[1]${NC} Ping Test          ${YELLOW}[2]${NC} Traceroute                     ${BOLD}${PURPLE}│${NC}"
    echo -e "${BOLD}${PURPLE}│${NC}  ${YELLOW}[3]${NC} DNS Lookup         ${YELLOW}[4]${NC} WHOIS Query                    ${BOLD}${PURPLE}│${NC}"
    echo -e "${BOLD}${PURPLE}│${NC}  ${YELLOW}[0]${NC} Back to Main Menu                                     ${BOLD}${PURPLE}│${NC}"
    echo -e "${BOLD}${PURPLE}└─────────────────────────────────────────────────────────────────┘${NC}"
    
    while true; do
        echo -ne "${BOLD}${PURPLE}Spider-Man> ${NC}"
        read spiderman_choice
        
        case $spiderman_choice in
            1)
                echo -ne "${CYAN}Enter target IP/hostname: ${NC}"
                read target
                if [ ! -z "$target" ]; then
                    echo -e "${GREEN}Ping test results for $target:${NC}" | tee -a "$report_file"
                    ping -c 4 "$target" 2>&1 | tee -a "$report_file"
                    log_action "Performed ping test on $target"
                fi
                ;;
            2)
                echo -ne "${CYAN}Enter target IP/hostname: ${NC}"
                read target
                if [ ! -z "$target" ]; then
                    echo -e "${GREEN}Traceroute results for $target:${NC}" | tee -a "$report_file"
                    traceroute "$target" 2>&1 | tee -a "$report_file"
                    log_action "Performed traceroute to $target"
                fi
                ;;
            3)
                echo -ne "${CYAN}Enter domain name: ${NC}"
                read domain
                if [ ! -z "$domain" ]; then
                    echo -e "${GREEN}DNS lookup results for $domain:${NC}" | tee -a "$report_file"
                    dig "$domain" 2>&1 | tee -a "$report_file"
                    log_action "Performed DNS lookup for $domain"
                fi
                ;;
            4)
                echo -ne "${CYAN}Enter domain name: ${NC}"
                read domain
                if [ ! -z "$domain" ]; then
                    echo -e "${GREEN}WHOIS results for $domain:${NC}" | tee -a "$report_file"
                    whois "$domain" 2>&1 | tee -a "$report_file"
                    log_action "Performed WHOIS lookup for $domain"
                fi
                ;;
            0)
                echo -e "${GREEN}Report saved to: $report_file${NC}"
                break
                ;;
            *)
                echo -e "${RED}Invalid choice!${NC}"
                ;;
        esac
        echo ""
    done
}

# Function to launch Hulk (System Monitor)
launch_hulk() {
    echo -e "${BOLD}${GREEN}📊 Initializing HULK System Monitor...${NC}"
    log_action "Launching HULK system monitor"
    sleep 1
    
    local report_file="$REPORTS_DIR/hulk_$(date +%Y%m%d_%H%M%S).txt"
    
    echo -e "${BOLD}${GREEN}\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510${NC}" 
    echo -e "${BOLD}${GREEN}\u2502${NC}  ${BOLD}${WHITE}\ud83d\udcca HULK SYSTEM MONITOR${NC}                             ${BOLD}${GREEN}\u2502${NC}"
    echo -e "${BOLD}${GREEN}\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524${NC}"
    
    echo -e "${GREEN}System Information:${NC}" | tee "$report_file"
    echo "Generated on: $(date)" | tee -a "$report_file"
    echo "" | tee -a "$report_file"
    
    echo -e "${CYAN}CPU Information:${NC}" | tee -a "$report_file"
    lscpu | tee -a "$report_file"
    echo "" | tee -a "$report_file"
    
    echo -e "${CYAN}Memory Usage:${NC}" | tee -a "$report_file"
    free -h | tee -a "$report_file"
    echo "" | tee -a "$report_file"
    
    echo -e "${CYAN}Disk Usage:${NC}" | tee -a "$report_file"
    df -h | tee -a "$report_file"
    echo "" | tee -a "$report_file"
    
    echo -e "${CYAN}Network Interfaces:${NC}" | tee -a "$report_file"
    ip addr show | tee -a "$report_file"
    echo "" | tee -a "$report_file"
    
    echo -e "${CYAN}Active Processes (Top 10):${NC}" | tee -a "$report_file"
    ps aux --sort=-%cpu | head -11 | tee -a "$report_file"
    
    echo -e "${GREEN}Report saved to: $report_file${NC}"
    log_action "Generated system report: $report_file"
    
    echo -e "${YELLOW}Press Enter to continue...${NC}"
    read
}

# Function to launch Thor (Web Analysis)
launch_thor() {
    echo -e "${BOLD}${RED}🔥 Initializing THOR Web Analysis...${NC}"
    log_action "Launching THOR web analysis"
    sleep 1
    
    local report_file="$REPORTS_DIR/thor_$(date +%Y%m%d_%H%M%S).txt"
    
    echo -e "${BOLD}${RED}\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510${NC}"
    echo -e "${BOLD}${RED}\u2502${NC}  ${BOLD}${WHITE}\ud83d\udd25 THOR WEB ANALYSIS${NC}                                ${BOLD}${RED}\u2502${NC}"
    echo -e "${BOLD}${RED}\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524${NC}"
    echo -e "${BOLD}${RED}\u2502${NC}  ${YELLOW}[1]${NC} HTTP Response Check  ${YELLOW}[2]${NC} SSL Certificate Info          ${BOLD}${RED}\u2502${NC}"
    echo -e "${BOLD}${RED}\u2502${NC}  ${YELLOW}[3]${NC} Website Headers      ${YELLOW}[0]${NC} Back to Main Menu             ${BOLD}${RED}\u2502${NC}"
    echo -e "${BOLD}${RED}\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518${NC}"
    
    while true; do
        echo -ne "${BOLD}${RED}Thor> ${NC}"
        read thor_choice
        
        case $thor_choice in
            1)
                echo -ne "${CYAN}Enter website URL: ${NC}"
                read url
                if [ ! -z "$url" ]; then
                    echo -e "${GREEN}HTTP response for $url:${NC}" | tee -a "$report_file"
                    curl -I "$url" 2>&1 | tee -a "$report_file"
                    log_action "Checked HTTP response for $url"
                fi
                ;;
            2)
                echo -ne "${CYAN}Enter website URL (https://): ${NC}"
                read url
                if [ ! -z "$url" ]; then
                    echo -e "${GREEN}SSL certificate info for $url:${NC}" | tee -a "$report_file"
                    echo | openssl s_client -connect "${url#https://}:443" -servername "${url#https://}" 2>/dev/null | openssl x509 -noout -text | tee -a "$report_file"
                    log_action "Checked SSL certificate for $url"
                fi
                ;;
            3)
                echo -ne "${CYAN}Enter website URL: ${NC}"
                read url
                if [ ! -z "$url" ]; then
                    echo -e "${GREEN}Headers for $url:${NC}" | tee -a "$report_file"
                    curl -s -D - "$url" -o /dev/null | tee -a "$report_file"
                    log_action "Retrieved headers for $url"
                fi
                ;;
            0)
                echo -e "${GREEN}Report saved to: $report_file${NC}"
                break
                ;;
            *)
                echo -e "${RED}Invalid choice!${NC}"
                ;;
        esac
        echo ""
    done
}

# Function to view reports
view_reports() {
    echo -e "${BOLD}${CYAN}📊 Viewing Generated Reports...${NC}"
    log_action "Viewing reports"
    
    if [ ! -d "$REPORTS_DIR" ] || [ -z "$(ls -A "$REPORTS_DIR" 2>/dev/null)" ]; then
        echo -e "${YELLOW}No reports found in $REPORTS_DIR${NC}"
        echo -e "${YELLOW}Press Enter to continue...${NC}"
        read
        return
    fi
    
    echo -e "${BOLD}${CYAN}Available Reports:${NC}"
    echo ""
    ls -la "$REPORTS_DIR" | grep -v "^total" | nl -v0
    echo ""
    echo -ne "${CYAN}Enter report number to view (or 0 to go back): ${NC}"
    read report_num
    
    if [ "$report_num" = "0" ]; then
        return
    fi
    
    local report_files=("$REPORTS_DIR"/*)  
    if [ "$report_num" -ge 1 ] && [ "$report_num" -le "${#report_files[@]}" ]; then
        local selected_file="${report_files[$((report_num-1))]}"
        echo -e "${GREEN}Viewing: $(basename "$selected_file")${NC}"
        echo ""
        less "$selected_file"
    else
        echo -e "${RED}Invalid report number!${NC}"
    fi
    
    echo -e "${YELLOW}Press Enter to continue...${NC}"
    read
}

# Initialize log file
log_action "Payner Tool Suite v$VERSION started by $USER"

# Main loop
while true; do
    show_main_menu
    
    # Show current date/time and system info
    echo -e "${DIM}${WHITE}Current Time: $(date '+%Y-%m-%d %H:%M:%S') | User: $USER | System: $(uname -s)${NC}"
    echo -e "${DIM}${WHITE}Version: $VERSION | Log: $LOG_FILE${NC}"
    echo ""
    
    echo -ne "${BOLD}${YELLOW}🎵 Select your choice [0-9]: ${NC}"
    read choice
    
    case $choice in
        1)
            clear
            launch_batman
            ;;
        2)
            clear
            launch_princefrost
            ;;
        3)
            clear
            launch_spiderman
            ;;
        4)
            clear
            launch_hulk
            ;;
        5)
            clear
            launch_thor
            ;;
        6)
            clear
            launch_packet_collector
            ;;
        8)
            clear
            show_tool_status
            echo -e "${YELLOW}Press Enter to return to main menu...${NC}"
            read
            ;;
        9)
            clear
            view_reports
            ;;
        0)
            clear
            echo -e "${BOLD}${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
            echo -e "${BOLD}${GREEN}║${NC}  ${YELLOW}👋 Thank you for using Payner Suite! 👋${NC}            ${BOLD}${GREEN}║${NC}"
            echo -e "${BOLD}${GREEN}║${NC}  ${CYAN}🎵 Session completed successfully! 🎵${NC}                     ${BOLD}${GREEN}║${NC}"
            echo -e "${BOLD}${GREEN}║${NC}  ${WHITE}Total session time: $(date '+%H:%M:%S')${NC}                        ${BOLD}${GREEN}║${NC}"
            echo -e "${BOLD}${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
            echo ""
            log_action "Payner Tool Suite session ended by $USER"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Invalid choice! Please select from the available options${NC}"
            echo -e "${YELLOW}Available: 1-5 (Tools), 8 (Status), 9 (Reports), 0 (Exit)${NC}"
            sleep 2
            ;;
    esac
done

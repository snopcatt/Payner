#!/bin/bash

# Payner Toolkit Installation Script
# For Linux systems (tested on Kali Linux)

echo "🎵 Payner Toolkit Installation Script 🎵"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${YELLOW}Warning: Running as root. Some tools may require root privileges anyway.${NC}"
fi

# Check Python version
echo -e "${BLUE}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python3 found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python3 not found. Please install Python 3.7 or higher.${NC}"
    exit 1
fi

# Check pip
echo -e "${BLUE}Checking pip installation...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✅ pip3 found${NC}"
else
    echo -e "${YELLOW}Installing pip3...${NC}"
    sudo apt-get update && sudo apt-get install -y python3-pip
fi

# Install Python dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip3 install -r requirements.txt

# Check for required system tools
echo -e "${BLUE}Checking system dependencies...${NC}"

# Check for nmap
if command -v nmap &> /dev/null; then
    echo -e "${GREEN}✅ nmap found${NC}"
else
    echo -e "${YELLOW}Installing nmap...${NC}"
    sudo apt-get update && sudo apt-get install -y nmap
fi

# Check for other network tools
TOOLS=("ping" "traceroute" "dig" "whois" "netstat")
for tool in "${TOOLS[@]}"; do
    if command -v $tool &> /dev/null; then
        echo -e "${GREEN}✅ $tool found${NC}"
    else
        echo -e "${YELLOW}⚠️  $tool not found - some features may not work${NC}"
    fi
done

# Make scripts executable
echo -e "${BLUE}Setting executable permissions...${NC}"
chmod +x payner.sh
chmod +x tools/Palavo-Oko/palavo_oko.sh

# Create symlink for global access (optional)
echo -e "${BLUE}Do you want to create a global symlink? (y/n)${NC}"
read -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo ln -sf "$(pwd)/payner.sh" /usr/local/bin/payner
    echo -e "${GREEN}✅ Global symlink created. You can now run 'payner' from anywhere.${NC}"
fi

# Create desktop entry (optional)
echo -e "${BLUE}Do you want to create a desktop entry? (y/n)${NC}"
read -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    DESKTOP_FILE="$HOME/.local/share/applications/payner.desktop"
    mkdir -p "$HOME/.local/share/applications"
    
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Payner Toolkit
Comment=Professional Network Security Suite
Exec=$(pwd)/payner.sh
Icon=utilities-terminal
Terminal=true
Categories=Network;Security;
EOF
    
    echo -e "${GREEN}✅ Desktop entry created.${NC}"
fi

echo
echo -e "${GREEN}🎉 Installation completed successfully!${NC}"
echo
echo -e "${BLUE}To run the toolkit:${NC}"
echo -e "  ${YELLOW}./payner.sh${NC} (from this directory)"
if [[ -L /usr/local/bin/payner ]]; then
    echo -e "  ${YELLOW}payner${NC} (from anywhere)"
fi
echo
echo -e "${YELLOW}⚠️  Remember: Use only on authorized networks and systems!${NC}"
echo -e "${BLUE}📖 Check README.md for detailed usage instructions.${NC}"
echo
echo -e "${GREEN}🎵 Happy ethical hacking! 🎵${NC}"

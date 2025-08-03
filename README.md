# 🎵 Payner Toolkit - Professional Network Security Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://www.linux.org/)

A comprehensive network security testing suite designed for authorized penetration testing and network analysis. The Payner Toolkit combines multiple specialized tools into a unified interface for security professionals and ethical hackers.

## 🎯 Features

- **🦇 Batman Load Testing Tool** - Professional web server stress testing
- **❄️ O'Azis Network Scanner** - Advanced port scanning with service detection
- **🔍 MILKO Port Scanner** - Lightweight and fast port scanning utility  
- **📡 Packet Collector** - Network packet capture and analysis
- **🕵️ Palavo Oko** - Network reconnaissance and diagnostics
- **🕸️ Spider-Man Diagnostics** - Network connectivity testing
- **📊 Hulk System Monitor** - Comprehensive system monitoring
- **🔥 Thor Web Analysis** - HTTP/HTTPS analysis and SSL certificate inspection

## 🚀 Quick Start

### Prerequisites

- Linux operating system (tested on Kali Linux)
- Python 3.7 or higher
- Root privileges for some network operations

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/payner-toolkit.git
cd payner-toolkit
```

2. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

3. Make the main script executable:
```bash
chmod +x payner.sh
```

4. Run the toolkit:
```bash
./payner.sh
```

## 🛠️ Tools Overview

### Batman Load Testing Tool
- Multi-threaded HTTP load testing
- Configurable request patterns
- Real-time performance monitoring
- Detailed response analysis

### O'Azis Network Scanner
- Advanced TCP port scanning
- Service fingerprinting (50+ services)
- Banner grabbing capabilities
- JSON export functionality
- Stealth scanning mode

### MILKO Port Scanner
- High-speed port scanning
- Flexible port range specification  
- Service detection
- Banner grabbing

### Packet Collector
- Real-time packet capture
- Protocol filtering
- PCAP file generation
- Network traffic analysis

### Palavo Oko Network Scanner
- Network discovery
- Port scanning capabilities
- Network interface management
- Ping testing utilities

## 📖 Usage Examples

### Basic Network Scan
```bash
# Launch main interface
./payner.sh

# Select option 2 for O'Azis Scanner
# Enter target: 192.168.1.1
# Enter ports: common
```

### Load Testing
```bash
# Launch main interface
./payner.sh

# Select option 1 for Batman
# Configure target URL and test parameters
```

### Individual Tool Usage
```bash
# Run O'Azis Scanner directly
python3 tools/oazis_scanner.py

# Run Batman Load Tester directly  
python3 tools/batman.py

# Run MILKO Port Scanner directly
python3 tools/network_scanner.py -t 192.168.1.1 -p 1-1000
```

## ⚠️ Legal Disclaimer

**IMPORTANT**: This toolkit is designed for authorized security testing only. Users must ensure they have explicit permission before testing any networks or systems that they do not own.

- ✅ Use on your own networks and systems
- ✅ Use in authorized penetration testing engagements  
- ✅ Use for educational purposes in controlled environments
- ❌ Do not use on networks without explicit permission
- ❌ Do not use for malicious purposes
- ❌ Do not use to disrupt services or networks

Unauthorized network scanning and testing may violate local laws and regulations. Users are solely responsible for ensuring compliance with applicable laws.

## 🔧 Configuration

The toolkit supports various configuration options:

- **Threads**: Adjust scanning thread count (1-500)
- **Timeout**: Configure connection timeouts (0.1-30s)
- **Stealth Mode**: Enable slower, less detectable scanning
- **Output Formats**: JSON export and custom reporting
- **Logging**: Comprehensive activity logging

## 📊 Output and Reporting

- Real-time scan results display
- Comprehensive scan summaries
- JSON export for further analysis
- Automatic report generation
- Activity logging for audit trails

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest new features.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛡️ Security

If you discover any security vulnerabilities, please report them responsibly by emailing [security@example.com] instead of opening a public issue.

## 📞 Support

- GitHub Issues: Report bugs and request features
- Documentation: Check the `/docs` folder for detailed documentation
- Community: Join our discussions in the Issues section

## 🏆 Acknowledgments

- Built for the cybersecurity community
- Inspired by industry-standard penetration testing tools
- Designed with ethical hacking principles in mind

---

**Remember**: With great power comes great responsibility. Use these tools ethically and legally.

🎵 *Powered by Payner Technology* 🎵

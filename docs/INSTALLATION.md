# Installation Guide

This guide covers the installation process for the Payner Toolkit on various Linux distributions.

## System Requirements

- **Operating System**: Linux (Ubuntu, Debian, Kali Linux, CentOS, etc.)
- **Python**: Version 3.7 or higher
- **Memory**: Minimum 512 MB RAM
- **Storage**: At least 100 MB free space
- **Privileges**: Root access for some network operations

## Automatic Installation

The easiest way to install Payner Toolkit is using the automated installation script:

```bash
git clone https://github.com/yourusername/payner-toolkit.git
cd payner-toolkit
chmod +x install.sh
./install.sh
```

The installation script will:
- Check Python and pip installation
- Install required Python packages
- Install system dependencies (nmap, network tools)
- Set executable permissions
- Optionally create global symlinks and desktop entries

## Manual Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/payner-toolkit.git
cd payner-toolkit
```

### 2. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Install System Dependencies

#### On Ubuntu/Debian/Kali:
```bash
sudo apt-get update
sudo apt-get install -y nmap traceroute dnsutils whois net-tools openssl curl
```

#### On CentOS/RHEL/Fedora:
```bash
sudo yum install -y nmap traceroute bind-utils whois net-tools openssl curl
# Or for newer versions:
sudo dnf install -y nmap traceroute bind-utils whois net-tools openssl curl
```

### 4. Set Permissions

```bash
chmod +x payner.sh
chmod +x tools/Palavo-Oko/palavo_oko.sh
```

## Verification

Test your installation:

```bash
# Run the main toolkit
./payner.sh

# Test individual tools
python3 tools/batman.py
python3 tools/oazis_scanner.py
python3 tools/network_scanner.py --help
```

## Common Issues

### Permission Denied
If you encounter permission errors:
```bash
chmod +x payner.sh
chmod +x install.sh
```

### Python Module Not Found
If Python modules are missing:
```bash
pip3 install --user -r requirements.txt
```

### Network Tools Missing
Install missing network utilities:
```bash
# Ubuntu/Debian
sudo apt-get install -y nmap traceroute dnsutils whois

# CentOS/RHEL
sudo yum install -y nmap traceroute bind-utils whois
```

### Root Privileges Required
Some network operations require root privileges:
```bash
sudo python3 tools/packet_collector.py
```

## Optional: Global Installation

To make Payner available system-wide:

```bash
sudo ln -sf $(pwd)/payner.sh /usr/local/bin/payner
```

Now you can run `payner` from anywhere in the terminal.

## Uninstallation

To remove Payner Toolkit:

```bash
# Remove global symlink (if created)
sudo rm -f /usr/local/bin/payner

# Remove desktop entry (if created)
rm -f ~/.local/share/applications/payner.desktop

# Remove the toolkit directory
rm -rf payner-toolkit

# Remove user data (optional)
rm -f ~/.payner.log
rm -f ~/.payner.conf
rm -rf ~/.payner_reports
rm -rf ~/.payner_pcap
```

## Next Steps

After installation, check out:
- [Usage Guide](USAGE.md) - Learn how to use each tool
- [Configuration](CONFIGURATION.md) - Customize your toolkit
- [Examples](EXAMPLES.md) - See practical examples

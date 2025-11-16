# PHANTOM PROTOCOL - One-Line Installation

## 🚀 INSTANT INSTALLATION & SETUP

Copy and paste this single command to automatically install everything:

```bash
curl -fsSL https://raw.githubusercontent.com/husion84-svg/Turn/phantom-protocol-military-grade-pentest-system/auto_install.sh | sudo bash
```

## 🔧 ALTERNATIVE INSTALLATION METHODS

### Method 1: Direct Download & Run
```bash
wget https://raw.githubusercontent.com/husion84-svg/Turn/phantom-protocol-military-grade-pentest-system/auto_install.sh
chmod +x auto_install.sh
sudo ./auto_install.sh
```

### Method 2: Git Clone & Install
```bash
git clone https://github.com/husion84-svg/Turn.git
cd Turn
git checkout phantom-protocol-military-grade-pentest-system
chmod +x auto_install.sh
sudo ./auto_install.sh
```

### Method 3: Manual Setup (if auto-install fails)
```bash
# Clone repository
git clone https://github.com/husion84-svg/Turn.git
cd Turn
git checkout phantom-protocol-military-grade-pentest-system

# Run manual installer
chmod +x installer.sh
sudo ./installer.sh

# Install additional dependencies
pip install psutil aiohttp requests beautifulsoup4 cryptography lz4 zstandard blosc networkx paramiko scapy dnspython python-whois selenium webdriver-manager psycopg2-binary pymongo redis sqlalchemy flask fastapi pyyaml click colorama tqdm tabulate python-nmap shodan censys virustotal-api
```

## 🎯 WHAT THE AUTO-INSTALLER DOES

### System Setup
- ✅ Updates all system packages
- ✅ Installs 100+ penetration testing tools
- ✅ Configures Tor, proxychains, Docker
- ✅ Sets up memory optimization for 4GB RAM systems
- ✅ Installs Google Chrome + ChromeDriver

### Python Environment
- ✅ Creates isolated virtual environment
- ✅ Installs 150+ Python security packages
- ✅ Configures all PHANTOM PROTOCOL modules

### Security Tools
- ✅ Installs Metasploit Framework
- ✅ Installs Go-based tools (ffuf, subfinder, httpx, nuclei, etc.)
- ✅ Downloads wordlists (SecLists, FuzzDB, PayloadsAllTheThings)
- ✅ Configures nation-state level frameworks

### System Optimization
- ✅ Applies Chinese/Japanese memory optimization
- ✅ Sets up ZRAM compressed swap
- ✅ Configures kernel parameters for performance
- ✅ Enables temperature monitoring

## 🚀 QUICK START AFTER INSTALLATION

### Option 1: Guided Launch
```bash
cd phantom_protocol_auto/Turn
./quick_launch.sh
```

### Option 2: Direct Launch
```bash
cd phantom_protocol_auto/Turn
./start_phantom.sh https://target.com --auth authorization.txt
```

### Option 3: System Test
```bash
cd phantom_protocol_auto/Turn
./system_test.sh
```

## 🔐 REQUIRED PASSPHRASE

The system requires this exact passphrase for decryption:

```
WILL TOOL KILL OPEN NEVER WILL AGAIN NEVER ZERO WELCOME DUE AND NEVER
```

## 📋 SYSTEM REQUIREMENTS

### Minimum Requirements
- **OS**: Debian/Ubuntu Linux
- **RAM**: 2GB (optimized for 4GB systems)
- **Storage**: 10GB free space
- **Network**: Internet connection
- **Permissions**: sudo access

### Recommended Requirements
- **RAM**: 8GB or more
- **Storage**: 20GB+ free space
- **CPU**: 4+ cores
- **Network**: High-speed internet

## ⚠️ LEGAL NOTICE

**AUTHORIZED USE ONLY**

This system is designed for:
- ✅ Authorized penetration testing
- ✅ Bug bounty programs
- ✅ Security research with proper authorization
- ✅ Educational purposes in controlled environments

**Unauthorized use is illegal and prohibited.**

Always ensure you have written authorization before testing any system you do not own.

## 🛠️ TROUBLESHOOTING

### If installation fails:
1. Check internet connection
2. Ensure you have sudo privileges
3. Try manual installation method
4. Check system logs: `tail -f /var/log/syslog`

### If system doesn't start:
1. Run system test: `./system_test.sh`
2. Check Python environment: `source phantom_env/bin/activate`
3. Verify dependencies: `pip list`
4. Check logs: `tail -f logs/phantom_protocol.log`

### Common Issues:
- **Memory errors**: System includes 4GB RAM optimization
- **Permission errors**: Ensure proper sudo access
- **Network errors**: Check proxy and Tor configuration
- **Import errors**: Reinstall Python dependencies

## 📞 SUPPORT

For issues or questions:
1. Run system diagnostics: `./system_test.sh`
2. Check installation logs
3. Verify all dependencies are installed
4. Ensure proper authorization before testing

---

**🎯 PHANTOM PROTOCOL v1.0 - Military-Grade Edition**
**Ready for nation-state level penetration testing**
#!/bin/bash

# PHANTOM PROTOCOL - Installation Script
# Military-grade penetration testing system installer for Debian/Ubuntu

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║                           PHANTOM PROTOCOL v1.0                              ║"
echo "║                    Military-Grade Penetration Testing System                 ║"
echo "║                              INSTALLER                                       ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root for system packages
if [[ $EUID -eq 0 ]]; then
   echo -e "${YELLOW}Warning: Running as root. This is recommended for system package installation.${NC}"
fi

# Detect OS
if [[ -f /etc/debian_version ]]; then
    OS="debian"
    echo -e "${GREEN}✓ Detected Debian/Ubuntu system${NC}"
elif [[ -f /etc/redhat-release ]]; then
    OS="redhat"
    echo -e "${YELLOW}⚠ Red Hat/CentOS detected. Some packages may need manual installation.${NC}"
else
    echo -e "${RED}✗ Unsupported operating system. This installer is designed for Debian/Ubuntu.${NC}"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install package with error handling
install_package() {
    local package=$1
    echo -e "${BLUE}Installing $package...${NC}"
    
    if [[ $OS == "debian" ]]; then
        if ! apt-get install -y "$package"; then
            echo -e "${RED}✗ Failed to install $package${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠ Please manually install: $package${NC}"
    fi
    
    echo -e "${GREEN}✓ $package installed${NC}"
}

# Update package lists
echo -e "${BLUE}Updating package lists...${NC}"
if [[ $OS == "debian" ]]; then
    apt-get update
fi

# Install system dependencies
echo -e "${BLUE}Installing system dependencies...${NC}"

SYSTEM_PACKAGES=(
    "python3"
    "python3-pip"
    "python3-venv"
    "git"
    "curl"
    "wget"
    "nmap"
    "tor"
    "proxychains4"
    "build-essential"
    "libssl-dev"
    "libffi-dev"
    "python3-dev"
    "postgresql-client"
    "redis-tools"
    "docker.io"
    "openjdk-11-jdk"
    "golang-go"
    "ruby"
    "nodejs"
    "npm"
)

for package in "${SYSTEM_PACKAGES[@]}"; do
    if ! command_exists "${package%%-*}"; then
        install_package "$package"
    else
        echo -e "${GREEN}✓ $package already installed${NC}"
    fi
done

# Install additional security tools
echo -e "${BLUE}Installing additional security tools...${NC}"

SECURITY_TOOLS=(
    "sqlmap"
    "nikto"
    "dirb"
    "gobuster"
    "hydra"
    "john"
    "hashcat"
    "aircrack-ng"
    "wireshark-common"
    "tcpdump"
)

for tool in "${SECURITY_TOOLS[@]}"; do
    if ! command_exists "$tool"; then
        install_package "$tool"
    else
        echo -e "${GREEN}✓ $tool already installed${NC}"
    fi
done

# Create Python virtual environment
echo -e "${BLUE}Creating Python virtual environment...${NC}"
if [[ ! -d "venv" ]]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip

# Install Python dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"

PYTHON_PACKAGES=(
    "asyncio"
    "aiohttp"
    "requests"
    "beautifulsoup4"
    "lxml"
    "selenium"
    "cryptography"
    "pycryptodome"
    "psutil"
    "loguru"
    "colorama"
    "tqdm"
    "click"
    "pyyaml"
    "jinja2"
    "sqlalchemy"
    "pymongo"
    "psycopg2-binary"
    "redis"
    "celery"
    "flask"
    "fastapi"
    "uvicorn"
    "websockets"
    "paramiko"
    "scapy"
    "python-nmap"
    "dnspython"
    "python-whois"
    "shodan"
    "censys"
    "virustotal-api"
    "web3"
    "bitcoin"
    "ecdsa"
    "pyjwt"
    "passlib"
    "bcrypt"
    "pyotp"
    "qrcode"
    "pillow"
    "matplotlib"
    "seaborn"
    "pandas"
    "numpy"
    "scipy"
    "scikit-learn"
    "tensorflow"
    "torch"
    "transformers"
)

echo "Installing Python packages..."
pip install "${PYTHON_PACKAGES[@]}"

# Install specialized penetration testing tools
echo -e "${BLUE}Installing specialized penetration testing tools...${NC}"

# Install Metasploit (if not already installed)
if ! command_exists msfconsole; then
    echo -e "${BLUE}Installing Metasploit Framework...${NC}"
    curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
    chmod 755 msfinstall
    ./msfinstall
    rm msfinstall
    echo -e "${GREEN}✓ Metasploit Framework installed${NC}"
else
    echo -e "${GREEN}✓ Metasploit Framework already installed${NC}"
fi

# Install additional Go tools
echo -e "${BLUE}Installing Go-based security tools...${NC}"
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

GO_TOOLS=(
    "github.com/ffuf/ffuf@latest"
    "github.com/OWASP/Amass/v3/...@latest"
    "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
    "github.com/projectdiscovery/httpx/cmd/httpx@latest"
    "github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest"
    "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest"
)

for tool in "${GO_TOOLS[@]}"; do
    echo "Installing $tool..."
    go install "$tool"
done

# Create directory structure
echo -e "${BLUE}Creating directory structure...${NC}"
mkdir -p config
mkdir -p logs
mkdir -p encrypted_data
mkdir -p frameworks/custom
mkdir -p reports
mkdir -p temp
mkdir -p data

# Create configuration files
echo -e "${BLUE}Creating configuration files...${NC}"

# AI Coordinator config
cat > config/ai_config.json << 'EOF'
{
    "reasoning_depth": 10,
    "framework_timeout": 300,
    "max_concurrent_frameworks": 5,
    "custom_framework_creation": true,
    "performance_monitoring": true,
    "decision_logging": true
}
EOF

# Proxy Manager config
cat > config/proxy_config.json << 'EOF'
{
    "max_concurrent_verifications": 50,
    "verification_timeout": 15,
    "rotation_interval": 300,
    "min_anonymity_level": 2,
    "min_speed_threshold": 5000,
    "blacklist_threshold": 0.7,
    "tor_integration": true
}
EOF

# Extraction Engine config
cat > config/extraction_config.json << 'EOF'
{
    "max_concurrent_extractions": 5,
    "stealth_mode": true,
    "validation_required": true,
    "proof_collection": true,
    "pattern_timeout": 30,
    "memory_limit_mb": 1024
}
EOF

# Main system config
cat > config/phantom_config.json << 'EOF'
{
    "system": {
        "version": "1.0",
        "debug_mode": false,
        "max_memory_usage": 0.8,
        "max_cpu_usage": 0.8,
        "temp_cleanup": true
    },
    "security": {
        "authorization_required": true,
        "nda_acknowledgment": true,
        "activity_logging": true,
        "encrypted_storage": true,
        "secure_deletion": true
    },
    "networking": {
        "proxy_rotation": true,
        "tor_integration": true,
        "max_connections": 100,
        "connection_timeout": 30,
        "retry_attempts": 3
    },
    "reporting": {
        "cvss_scoring": true,
        "executive_summary": true,
        "technical_details": true,
        "remediation_steps": true,
        "timeline_reconstruction": true
    }
}
EOF

# Create sample authorization file template
cat > authorization_template.txt << 'EOF'
AUTHORIZED PENETRATION TEST

TARGET: [INSERT TARGET URL/IP]
SCOPE: [INSERT TESTING SCOPE AND LIMITATIONS]
AUTHORIZED BY: [INSERT AUTHORIZER NAME AND TITLE]
ORGANIZATION: [INSERT CLIENT ORGANIZATION]
DATE: [INSERT AUTHORIZATION DATE]
VALID UNTIL: [INSERT EXPIRATION DATE]

TESTING PARAMETERS:
- Type: Authorized Security Assessment
- Methodology: PHANTOM PROTOCOL Military-Grade Testing
- Impact Level: Read-only, Non-destructive
- Reporting: Encrypted, Confidential

LEGAL ACKNOWLEDGMENTS:
- This authorization covers only the specified target and scope
- Testing must remain within defined boundaries
- No data exfiltration or system damage permitted
- All findings are confidential under NDA
- Penalties for unauthorized disclosure apply

SIGNATURE: [INSERT DIGITAL SIGNATURE OR AUTHORIZATION CODE]

---
This authorization must be present and valid before any testing begins.
Modify this template with actual authorization details.
EOF

# Set up Tor configuration
echo -e "${BLUE}Configuring Tor...${NC}"
if [[ -f /etc/tor/torrc ]]; then
    # Backup original torrc
    cp /etc/tor/torrc /etc/tor/torrc.backup
    
    # Add PHANTOM PROTOCOL specific configuration
    cat >> /etc/tor/torrc << 'EOF'

# PHANTOM PROTOCOL Configuration
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
MaxCircuitDirtiness 300
NewCircuitPeriod 30
MaxClientCircuitsPending 32
EOF
    
    echo -e "${GREEN}✓ Tor configured${NC}"
fi

# Set up system optimizations
echo -e "${BLUE}Applying system optimizations...${NC}"

# Increase file descriptor limits
echo "* soft nofile 65536" >> /etc/security/limits.conf
echo "* hard nofile 65536" >> /etc/security/limits.conf

# Network optimizations
sysctl -w net.core.rmem_max=134217728
sysctl -w net.core.wmem_max=134217728
sysctl -w net.ipv4.tcp_rmem="4096 87380 134217728"
sysctl -w net.ipv4.tcp_wmem="4096 65536 134217728"

# Memory optimizations for low-RAM systems
echo "vm.swappiness=10" >> /etc/sysctl.conf
echo "vm.vfs_cache_pressure=50" >> /etc/sysctl.conf

# Create startup script
cat > start_phantom.sh << 'EOF'
#!/bin/bash

# PHANTOM PROTOCOL Startup Script

echo "Starting PHANTOM PROTOCOL..."

# Activate virtual environment
source venv/bin/activate

# Start Tor service
sudo service tor start

# Check system resources
echo "System Resources:"
echo "Memory: $(free -h | grep Mem | awk '{print $3 "/" $2}')"
echo "CPU: $(nproc) cores"
echo "Disk: $(df -h . | tail -1 | awk '{print $4}') available"

# Start PHANTOM PROTOCOL
python3 phantom_protocol.py "$@"
EOF

chmod +x start_phantom.sh

# Create decryption utility script
cat > decrypt_results.sh << 'EOF'
#!/bin/bash

# PHANTOM PROTOCOL Results Decryption Utility

if [ $# -eq 0 ]; then
    echo "Usage: $0 <encrypted_file_or_folder>"
    echo "Example: $0 encrypted_data/phantom_results_example_com_1234567890.phantom"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run decryption tool
python3 core/encryption_manager.py "$1"
EOF

chmod +x decrypt_results.sh

# Create system health check script
cat > health_check.sh << 'EOF'
#!/bin/bash

# PHANTOM PROTOCOL System Health Check

echo "PHANTOM PROTOCOL - System Health Check"
echo "======================================"

# Check Python environment
echo "Python Version: $(python3 --version)"
echo "Virtual Environment: $(which python3)"

# Check system resources
echo "Memory Usage: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "Disk Usage: $(df -h . | tail -1 | awk '{print $5}')"

# Check network connectivity
echo "Network Connectivity:"
if ping -c 1 google.com &> /dev/null; then
    echo "  ✓ Internet connection active"
else
    echo "  ✗ No internet connection"
fi

# Check Tor service
if systemctl is-active --quiet tor; then
    echo "  ✓ Tor service running"
else
    echo "  ✗ Tor service not running"
fi

# Check required tools
echo "Required Tools:"
TOOLS=("nmap" "sqlmap" "python3" "tor" "curl" "wget")
for tool in "${TOOLS[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo "  ✓ $tool"
    else
        echo "  ✗ $tool (missing)"
    fi
done

# Check Python packages
echo "Python Packages:"
source venv/bin/activate
PACKAGES=("aiohttp" "cryptography" "requests" "psutil")
for package in "${PACKAGES[@]}"; do
    if python3 -c "import $package" &> /dev/null; then
        echo "  ✓ $package"
    else
        echo "  ✗ $package (missing)"
    fi
done

echo "======================================"
echo "Health check completed."
EOF

chmod +x health_check.sh

# Set proper permissions
echo -e "${BLUE}Setting file permissions...${NC}"
chmod +x phantom_protocol.py
chmod +x core/*.py
chmod 700 encrypted_data
chmod 600 config/*.json

# Final system test
echo -e "${BLUE}Running system test...${NC}"
source venv/bin/activate

# Test Python imports
python3 -c "
import asyncio
import aiohttp
import cryptography
import psutil
print('✓ All critical Python packages imported successfully')
"

# Test core modules
python3 -c "
from core.ai_coordinator import AICoordinator
from core.proxy_manager import ProxyManager
from core.extraction_engine import ExtractionEngine
from core.encryption_manager import EncryptionManager
print('✓ All core modules imported successfully')
"

echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║                        INSTALLATION COMPLETED                                ║"
echo "╠═══════════════════════════════════════════════════════════════════════════════╣"
echo "║  PHANTOM PROTOCOL v1.0 has been successfully installed!                      ║"
echo "║                                                                               ║"
echo "║  Usage:                                                                       ║"
echo "║    ./start_phantom.sh --target <URL> --auth-file <authorization.txt>         ║"
echo "║                                                                               ║"
echo "║  Example:                                                                     ║"
echo "║    ./start_phantom.sh --target https://example.com --auth-file auth.txt      ║"
echo "║                                                                               ║"
echo "║  Utilities:                                                                   ║"
echo "║    ./health_check.sh          - Check system health                          ║"
echo "║    ./decrypt_results.sh       - Decrypt test results                         ║"
echo "║                                                                               ║"
echo "║  Authorization:                                                               ║"
echo "║    Edit 'authorization_template.txt' with proper authorization details       ║"
echo "║                                                                               ║"
echo "║  ⚠️  IMPORTANT: This system is for authorized use only!                      ║"
echo "║      Ensure you have written authorization before any testing.               ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Edit 'authorization_template.txt' with proper authorization details"
echo "2. Run './health_check.sh' to verify system status"
echo "3. Start testing with './start_phantom.sh --target <URL> --auth-file <auth.txt>'"
echo ""
echo -e "${RED}⚠️  Remember: Always ensure you have proper written authorization before testing!${NC}"
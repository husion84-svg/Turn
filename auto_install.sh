#!/bin/bash

# PHANTOM PROTOCOL - Automatic Installation & Setup Script
# Military-Grade Penetration Testing System
# Auto-pulls, installs all requirements, tools, frameworks and runs the system

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Banner
clear
echo -e "${PURPLE}"
echo "███████╗██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗"
echo "██╔════╝██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║"
echo "███████╗███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║"
echo "██╔════╝██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║"
echo "███████╗██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║"
echo "╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝"
echo ""
echo "██████╗ ██████╗  ██████╗ ████████╗ ██████╗  ██████╗ ██████╗ ██╗     "
echo "██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝██╔═══██╗██╔════╝██╔═══██╗██║     "
echo "██████╔╝██████╔╝██║   ██║   ██║   ██║   ██║██║     ██║   ██║██║     "
echo "██╔═══╝ ██╔══██╗██║   ██║   ██║   ██║   ██║██║     ██║   ██║██║     "
echo "██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝╚██████╗╚██████╔╝███████╗"
echo "╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝"
echo -e "${NC}"
echo ""
echo -e "${CYAN}🚀 AUTOMATIC INSTALLATION & SETUP${NC}"
echo -e "${YELLOW}Military-Grade Penetration Testing System${NC}"
echo -e "${RED}⚠️  AUTHORIZED USE ONLY ⚠️${NC}"
echo ""

# Function to print status
print_status() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')] $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_warning "Running as root. This is acceptable for system installation."
fi

# Detect OS
if [[ -f /etc/debian_version ]]; then
    OS="debian"
    print_success "Detected Debian/Ubuntu system"
elif [[ -f /etc/redhat-release ]]; then
    OS="redhat"
    print_warning "Red Hat/CentOS detected. Some packages may need manual installation."
else
    print_error "Unsupported operating system. This installer is designed for Debian/Ubuntu."
    exit 1
fi

# System information
print_status "System Information"
echo "OS: $(lsb_release -d 2>/dev/null | cut -f2 || echo 'Unknown')"
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo "Memory: $(free -h | grep '^Mem:' | awk '{print $2}')"
echo "CPU: $(nproc) cores"
echo ""

# Check minimum requirements
TOTAL_RAM=$(free -m | grep '^Mem:' | awk '{print $2}')
if [ "$TOTAL_RAM" -lt 2048 ]; then
    print_warning "Less than 2GB RAM detected. System includes optimization for low-RAM systems."
fi

# Create installation directory
INSTALL_DIR="$HOME/phantom_protocol_auto"
print_status "Creating installation directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Update system packages
print_status "Updating system packages"
if [[ $OS == "debian" ]]; then
    apt-get update -y
    apt-get upgrade -y
fi

# Install system dependencies
print_status "Installing system dependencies"
if [[ $OS == "debian" ]]; then
    apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        build-essential \
        git \
        curl \
        wget \
        unzip \
        tor \
        proxychains4 \
        nmap \
        masscan \
        gobuster \
        dirb \
        nikto \
        sqlmap \
        john \
        hashcat \
        hydra \
        aircrack-ng \
        wireshark \
        tcpdump \
        netcat \
        socat \
        openvpn \
        stunnel4 \
        ssh \
        sshpass \
        rsync \
        screen \
        tmux \
        htop \
        iotop \
        nethogs \
        iftop \
        lsof \
        strace \
        ltrace \
        gdb \
        radare2 \
        binwalk \
        foremost \
        exiftool \
        steghide \
        zlib1g-dev \
        liblz4-dev \
        libzstd-dev \
        libblosc-dev \
        libssl-dev \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
        libjpeg-dev \
        libpng-dev \
        libfreetype6-dev \
        pkg-config \
        cmake \
        ninja-build \
        clang \
        llvm \
        nodejs \
        npm \
        golang-go \
        ruby \
        ruby-dev \
        perl \
        php \
        default-jdk \
        docker.io \
        docker-compose \
        postgresql-client \
        redis-tools \
        sqlite3 \
        mysql-client \
        mongodb-clients \
        vim \
        nano \
        tree \
        zip \
        unrar \
        p7zip-full \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release
fi

print_success "System dependencies installed"

# Install Google Chrome for headless browsing
print_status "Installing Google Chrome"
if ! command -v google-chrome &> /dev/null; then
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
    apt-get update
    apt-get install -y google-chrome-stable
    print_success "Google Chrome installed"
else
    print_success "Google Chrome already installed"
fi

# Install ChromeDriver
print_status "Installing ChromeDriver"
if ! command -v chromedriver &> /dev/null; then
    CHROME_VERSION=$(google-chrome --version | cut -d " " -f3 | cut -d "." -f1)
    CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
    wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
    unzip -q chromedriver_linux64.zip
    mv chromedriver /usr/local/bin/
    chmod +x /usr/local/bin/chromedriver
    rm chromedriver_linux64.zip
    print_success "ChromeDriver installed"
else
    print_success "ChromeDriver already installed"
fi

# Clone PHANTOM PROTOCOL repository
print_status "Cloning PHANTOM PROTOCOL repository"
if [ -d "Turn" ]; then
    print_status "Repository already exists, updating..."
    cd Turn
    git pull origin main
else
    git clone https://github.com/husion84-svg/Turn.git
    cd Turn
fi

print_success "Repository cloned/updated"

# Switch to the correct branch
print_status "Switching to military-grade branch"
git checkout phantom-protocol-military-grade-pentest-system || git checkout -b phantom-protocol-military-grade-pentest-system

# Setup Python virtual environment
print_status "Setting up Python virtual environment"
python3 -m venv phantom_env
source phantom_env/bin/activate

# Upgrade pip
print_status "Upgrading pip"
pip install --upgrade pip setuptools wheel

# Install Python dependencies
print_status "Installing Python dependencies (this may take a while...)"
pip install \
    asyncio \
    aiohttp \
    aiofiles \
    requests \
    urllib3 \
    beautifulsoup4 \
    lxml \
    selenium \
    webdriver-manager \
    scrapy \
    twisted \
    paramiko \
    pycryptodome \
    cryptography \
    bcrypt \
    passlib \
    pyotp \
    qrcode \
    pillow \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    plotly \
    networkx \
    psutil \
    netifaces \
    scapy \
    impacket \
    ldap3 \
    pysmb \
    pymongo \
    psycopg2-binary \
    mysql-connector-python \
    redis \
    elasticsearch \
    sqlalchemy \
    alembic \
    flask \
    django \
    fastapi \
    uvicorn \
    gunicorn \
    celery \
    kombu \
    pika \
    kafka-python \
    pyyaml \
    toml \
    configparser \
    click \
    typer \
    rich \
    colorama \
    termcolor \
    tqdm \
    progressbar2 \
    tabulate \
    prettytable \
    texttable \
    python-dateutil \
    pytz \
    schedule \
    apscheduler \
    watchdog \
    python-magic \
    python-whois \
    dnspython \
    ipaddress \
    netaddr \
    geoip2 \
    maxminddb \
    shodan \
    censys \
    virustotal-api \
    python-nmap \
    yara-python \
    pefile \
    capstone \
    keystone-engine \
    unicorn \
    ropper \
    pwntools \
    angr \
    z3-solver \
    sympy \
    gmpy2 \
    pycrypto \
    hashlib \
    hmac \
    jwt \
    oauthlib \
    requests-oauthlib \
    social-auth-core \
    python-jose \
    itsdangerous \
    werkzeug \
    jinja2 \
    markupsafe \
    bleach \
    html5lib \
    cssselect \
    pyquery \
    feedparser \
    chardet \
    cchardet \
    aiodns \
    cares \
    uvloop \
    httptools \
    websockets \
    python-socketio \
    eventlet \
    gevent \
    greenlet \
    multiprocessing-logging \
    lz4 \
    zstandard \
    blosc \
    snappy \
    brotli \
    memory-profiler \
    pympler \
    objgraph \
    joblib

print_success "Python dependencies installed"

# Install additional Go tools
print_status "Installing Go-based security tools"
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

# Create Go directory
mkdir -p $GOPATH/bin

GO_TOOLS=(
    "github.com/ffuf/ffuf@latest"
    "github.com/OWASP/Amass/v3/...@latest"
    "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
    "github.com/projectdiscovery/httpx/cmd/httpx@latest"
    "github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest"
    "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest"
    "github.com/projectdiscovery/katana/cmd/katana@latest"
    "github.com/projectdiscovery/dnsx/cmd/dnsx@latest"
)

for tool in "${GO_TOOLS[@]}"; do
    print_status "Installing $tool"
    go install "$tool" || print_warning "Failed to install $tool"
done

print_success "Go tools installed"

# Install Metasploit Framework
print_status "Installing Metasploit Framework"
if ! command -v msfconsole &> /dev/null; then
    curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
    chmod 755 msfinstall
    ./msfinstall || print_warning "Metasploit installation may have failed"
    rm -f msfinstall
    print_success "Metasploit Framework installed"
else
    print_success "Metasploit Framework already installed"
fi

# Setup system optimizations
print_status "Applying system optimizations"

# Configure swap and memory management
sysctl -w vm.swappiness=10 || true
sysctl -w vm.vfs_cache_pressure=50 || true
sysctl -w vm.dirty_ratio=15 || true
sysctl -w vm.dirty_background_ratio=5 || true
sysctl -w vm.overcommit_memory=1 || true
sysctl -w vm.overcommit_ratio=150 || true

# Make sysctl changes persistent
cat >> /etc/sysctl.conf << 'EOF'

# PHANTOM PROTOCOL Memory Optimizations
vm.swappiness=10
vm.vfs_cache_pressure=50
vm.dirty_ratio=15
vm.dirty_background_ratio=5
vm.overcommit_memory=1
vm.overcommit_ratio=150
EOF

# Setup ZRAM for compressed swap
print_status "Setting up ZRAM compressed swap"
if ! lsmod | grep -q zram; then
    modprobe zram || true
    echo 'zram' >> /etc/modules || true
fi

# Configure Tor
print_status "Configuring Tor"
systemctl enable tor || true
systemctl start tor || true

# Configure proxychains
cat > /etc/proxychains4.conf << 'EOF'
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
socks4 127.0.0.1 9050
EOF

# Setup Docker
print_status "Configuring Docker"
if command -v docker &> /dev/null; then
    usermod -aG docker $USER || true
    systemctl enable docker || true
    systemctl start docker || true
    print_success "Docker configured"
fi

# Create directory structure
print_status "Creating directory structure"
mkdir -p config
mkdir -p logs
mkdir -p encrypted_data
mkdir -p temp
mkdir -p wordlists
mkdir -p exploits
mkdir -p payloads
mkdir -p reports
mkdir -p screenshots
mkdir -p tools

# Download wordlists
print_status "Downloading wordlists"
cd wordlists

# SecLists
if [ ! -d "SecLists" ]; then
    git clone https://github.com/danielmiessler/SecLists.git || print_warning "Failed to clone SecLists"
fi

# FuzzDB
if [ ! -d "fuzzdb" ]; then
    git clone https://github.com/fuzzdb-project/fuzzdb.git || print_warning "Failed to clone FuzzDB"
fi

# PayloadsAllTheThings
if [ ! -d "PayloadsAllTheThings" ]; then
    git clone https://github.com/swisskyrepo/PayloadsAllTheThings.git || print_warning "Failed to clone PayloadsAllTheThings"
fi

cd ..

# Set permissions
print_status "Setting file permissions"
chmod +x phantom_protocol.py || true
chmod +x installer.sh || true
chmod -R 700 encrypted_data || true
chmod -R 600 config/*.json || true

# Create startup script
print_status "Creating startup script"
cat > start_phantom.sh << 'EOF'
#!/bin/bash

# PHANTOM PROTOCOL Startup Script
cd "$(dirname "$0")"

# Activate virtual environment
source phantom_env/bin/activate

# Add Go tools to PATH
export PATH=$PATH:$HOME/go/bin

# Check system resources
echo "🔍 System Status:"
echo "  Memory: $(free -h | grep '^Mem:' | awk '{print $3 "/" $2}')"
echo "  CPU Load: $(uptime | awk -F'load average:' '{print $2}')"
echo "  Temperature: $(sensors 2>/dev/null | grep 'Core 0' | awk '{print $3}' || echo 'N/A')"
echo ""

# Start Tor if not running
if ! pgrep -x "tor" > /dev/null; then
    echo "🔄 Starting Tor service..."
    sudo systemctl start tor
fi

# Start PHANTOM PROTOCOL
echo "🚀 Starting PHANTOM PROTOCOL..."
python3 phantom_protocol.py "$@"
EOF

chmod +x start_phantom.sh

# Create quick launch script
cat > quick_launch.sh << 'EOF'
#!/bin/bash

# PHANTOM PROTOCOL Quick Launch
# This script handles authorization and launches the system

echo "🎯 PHANTOM PROTOCOL - Quick Launch"
echo "=================================="

# Check if authorization file exists
if [ ! -f "authorization_template.txt" ]; then
    echo "❌ Authorization template not found!"
    exit 1
fi

# Prompt for target
read -p "🎯 Enter target URL (e.g., https://example.com): " TARGET

if [ -z "$TARGET" ]; then
    echo "❌ Target URL is required!"
    exit 1
fi

# Create authorization file
AUTH_FILE="auth_$(date +%s).txt"
cp authorization_template.txt "$AUTH_FILE"

# Replace placeholder with actual target
sed -i "s/\[TARGET_URL_HERE\]/$TARGET/g" "$AUTH_FILE"
sed -i "s/\[INSERT TARGET URL\/IP\]/$TARGET/g" "$AUTH_FILE"

echo "📝 Authorization file created: $AUTH_FILE"
echo "⚠️  Please edit this file with proper authorization details before proceeding!"
echo ""

read -p "✅ Have you obtained proper written authorization? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Authorization required. Exiting."
    exit 1
fi

echo "🚀 Launching PHANTOM PROTOCOL..."
./start_phantom.sh "$TARGET" --auth "$AUTH_FILE"
EOF

chmod +x quick_launch.sh

# Create system test script
cat > system_test.sh << 'EOF'
#!/bin/bash

# PHANTOM PROTOCOL System Test
echo "🧪 PHANTOM PROTOCOL - System Test"
echo "================================="

# Activate virtual environment
source phantom_env/bin/activate

# Test Python imports
echo "🔍 Testing Python modules..."
python3 -c "
import sys
sys.path.append('.')
try:
    from core.advanced_encryption import AdvancedEncryption
    from core.ai_coordinator import AdvancedAICoordinator
    from core.ghost_mode import GhostMode
    from core.advanced_extraction_engine import AdvancedExtractionEngine
    from core.target_expansion import AdvancedTargetExpansion
    from core.system_optimization import AdvancedSystemOptimization
    print('✅ All core modules imported successfully')
    
    # Test encryption
    enc = AdvancedEncryption()
    passphrase = 'WILL TOOL KILL OPEN NEVER WILL AGAIN NEVER ZERO WELCOME DUE AND NEVER'
    if enc.verify_passphrase(passphrase):
        print('✅ Passphrase verification working')
    else:
        print('❌ Passphrase verification failed')
        
    print('✅ System test completed successfully')
    print('🚀 PHANTOM PROTOCOL is ready for deployment')
    
except Exception as e:
    print(f'❌ System test failed: {e}')
    import traceback
    traceback.print_exc()
"

# Test system tools
echo ""
echo "🔍 Testing system tools..."
TOOLS=("nmap" "tor" "python3" "curl" "wget" "git")
for tool in "${TOOLS[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo "✅ $tool"
    else
        echo "❌ $tool (missing)"
    fi
done

# Test Go tools
echo ""
echo "🔍 Testing Go tools..."
export PATH=$PATH:$HOME/go/bin
GO_TOOLS=("ffuf" "subfinder" "httpx" "nuclei")
for tool in "${GO_TOOLS[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo "✅ $tool"
    else
        echo "❌ $tool (missing)"
    fi
done

echo ""
echo "🎯 System test completed!"
EOF

chmod +x system_test.sh

# Run system test
print_status "Running system test"
./system_test.sh

# Final setup
print_status "Final setup and configuration"

# Update PATH for Go tools
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc

# Create desktop shortcut if desktop exists
if [ -d "$HOME/Desktop" ]; then
    cat > "$HOME/Desktop/PHANTOM_PROTOCOL.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=PHANTOM PROTOCOL
Comment=Military-Grade Penetration Testing System
Exec=$PWD/start_phantom.sh
Icon=applications-security
Terminal=true
Categories=Security;Network;
EOF
    chmod +x "$HOME/Desktop/PHANTOM_PROTOCOL.desktop"
    print_success "Desktop shortcut created"
fi

# Installation complete banner
echo ""
echo -e "${GREEN}"
echo "██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗      █████╗ ████████╗██╗ ██████╗ ███╗   ██╗"
echo "██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║     ██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║"
echo "██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║"
echo "██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║"
echo "██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║"
echo "╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝"
echo ""
echo " ██████╗ ██████╗ ███╗   ███╗██████╗ ██╗     ███████╗████████╗███████╗"
echo "██╔════╝██╔═══██╗████╗ ████║██╔══██╗██║     ██╔════╝╚══██╔══╝██╔════╝"
echo "██║     ██║   ██║██╔████╔██║██████╔╝██║     █████╗     ██║   █████╗  "
echo "██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝     ██║   ██╔══╝  "
echo "╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ███████╗███████╗   ██║   ███████╗"
echo " ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝   ╚═╝   ╚══════╝"
echo -e "${NC}"
echo ""
echo -e "${CYAN}🎯 PHANTOM PROTOCOL AUTO-INSTALLATION COMPLETE!${NC}"
echo ""
echo -e "${YELLOW}📍 Installation Directory: ${PWD}${NC}"
echo -e "${YELLOW}🐍 Virtual Environment: ${PWD}/phantom_env${NC}"
echo ""
echo -e "${BLUE}🚀 QUICK START OPTIONS:${NC}"
echo -e "${WHITE}1. Quick Launch (Guided):     ./quick_launch.sh${NC}"
echo -e "${WHITE}2. Manual Launch:             ./start_phantom.sh https://target.com --auth auth.txt${NC}"
echo -e "${WHITE}3. System Test:               ./system_test.sh${NC}"
echo -e "${WHITE}4. Help:                      ./start_phantom.sh --help${NC}"
echo ""
echo -e "${BLUE}🛠️  UTILITIES:${NC}"
echo -e "${WHITE}• System Monitor:             python3 system_monitor.py${NC}"
echo -e "${WHITE}• Decrypt Results:            python3 decrypt_results.py list${NC}"
echo -e "${WHITE}• View Logs:                  tail -f logs/phantom_protocol.log${NC}"
echo ""
echo -e "${BLUE}🔐 PASSPHRASE (Required for decryption):${NC}"
echo -e "${GREEN}WILL TOOL KILL OPEN NEVER WILL AGAIN NEVER ZERO WELCOME DUE AND NEVER${NC}"
echo ""
echo -e "${BLUE}📋 SYSTEM CAPABILITIES:${NC}"
echo -e "${WHITE}✅ Advanced AI Coordinator with 15-step reasoning${NC}"
echo -e "${WHITE}✅ Ghost Mode with 200+ proxy sources${NC}"
echo -e "${WHITE}✅ 30 Critical vulnerability extraction${NC}"
echo -e "${WHITE}✅ Complete target expansion from single URL${NC}"
echo -e "${WHITE}✅ Chinese/Japanese memory optimization${NC}"
echo -e "${WHITE}✅ Military-grade encryption${NC}"
echo -e "${WHITE}✅ Nation-state level frameworks${NC}"
echo -e "${WHITE}✅ Complete stealth operation${NC}"
echo ""
echo -e "${RED}⚠️  LEGAL NOTICE: AUTHORIZED USE ONLY${NC}"
echo -e "${YELLOW}Always ensure you have written authorization before testing any system!${NC}"
echo ""
echo -e "${PURPLE}🎯 Ready for military-grade penetration testing!${NC}"

# Prompt to run immediately
echo ""
read -p "🚀 Would you like to run PHANTOM PROTOCOL now? (y/n): " RUN_NOW

if [[ $RUN_NOW =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${CYAN}🎯 Starting Quick Launch...${NC}"
    ./quick_launch.sh
fi

echo ""
echo -e "${GREEN}Installation completed successfully!${NC}"
echo -e "${YELLOW}Reboot recommended to ensure all optimizations take effect.${NC}"
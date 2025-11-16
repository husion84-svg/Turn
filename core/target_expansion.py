#!/usr/bin/env python3
"""
PHANTOM PROTOCOL - Advanced Target Expansion System
Military-grade target discovery and attack surface mapping
Auto-expand single URL to complete infrastructure footprint
"""

import asyncio
import aiohttp
import logging
import json
import time
import re
import socket
import ssl
import subprocess
import dns.resolver
import whois
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from urllib.parse import urlparse, urljoin
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import nmap
import requests
from bs4 import BeautifulSoup
import shodan
import censys.search
import threading
import hashlib

class TargetType(Enum):
    MAIN_DOMAIN = "main_domain"
    SUBDOMAIN = "subdomain"
    IP_ADDRESS = "ip_address"
    API_ENDPOINT = "api_endpoint"
    MOBILE_APP = "mobile_app"
    CLOUD_RESOURCE = "cloud_resource"
    CDN_ENDPOINT = "cdn_endpoint"
    THIRD_PARTY_SERVICE = "third_party_service"

class DiscoveryMethod(Enum):
    DNS_ENUMERATION = "dns_enumeration"
    CERTIFICATE_TRANSPARENCY = "certificate_transparency"
    SEARCH_ENGINE_DORKING = "search_engine_dorking"
    SHODAN_SCANNING = "shodan_scanning"
    CENSYS_SCANNING = "censys_scanning"
    SUBDOMAIN_BRUTEFORCE = "subdomain_bruteforce"
    PORT_SCANNING = "port_scanning"
    WEB_CRAWLING = "web_crawling"
    MOBILE_APP_ANALYSIS = "mobile_app_analysis"
    CLOUD_ENUMERATION = "cloud_enumeration"

@dataclass
class ExpandedTarget:
    url: str
    ip_addresses: List[str]
    target_type: TargetType
    discovery_method: DiscoveryMethod
    technologies: List[str]
    services: List[Dict[str, Any]]
    security_headers: Dict[str, str]
    certificates: List[Dict[str, Any]]
    subdomains: List[str]
    endpoints: List[str]
    mobile_apps: List[Dict[str, Any]]
    cloud_resources: List[Dict[str, Any]]
    third_party_integrations: List[str]
    confidence_score: float
    last_updated: float

class AdvancedTargetExpansion:
    """
    Military-grade target expansion system
    Discovers complete attack surface from single URL
    """
    
    def __init__(self, config_path: str = "config/expansion_config.json"):
        self.config_path = config_path
        
        # Core components
        self.discovered_targets = {}
        self.expansion_queue = asyncio.Queue()
        self.processed_targets = set()
        
        # Discovery tools
        self.nmap_scanner = None
        self.shodan_api = None
        self.censys_api = None
        
        # Wordlists and patterns
        self.subdomain_wordlist = []
        self.endpoint_wordlist = []
        self.technology_patterns = {}
        
        # Configuration
        self.max_depth = 3
        self.max_targets = 1000
        self.stealth_mode = True
        self.parallel_workers = 20
        
        # Initialize components
        self.load_wordlists()
        self.setup_discovery_tools()
        self.load_technology_patterns()
        
        logging.info("Advanced Target Expansion System initialized")
    
    def load_wordlists(self):
        """Load wordlists for subdomain and endpoint discovery"""
        # Comprehensive subdomain wordlist
        self.subdomain_wordlist = [
            # Common subdomains
            "www", "mail", "ftp", "admin", "api", "app", "blog", "cdn", "dev", "test",
            "staging", "prod", "production", "demo", "beta", "alpha", "mobile", "m",
            "secure", "ssl", "vpn", "remote", "portal", "dashboard", "panel", "control",
            
            # Technical subdomains
            "ns1", "ns2", "mx", "mx1", "mx2", "smtp", "pop", "imap", "webmail",
            "autodiscover", "autoconfig", "cpanel", "whm", "plesk", "directadmin",
            
            # Service-specific
            "jenkins", "gitlab", "github", "bitbucket", "jira", "confluence",
            "wiki", "docs", "help", "support", "status", "monitoring", "grafana",
            "kibana", "elasticsearch", "prometheus", "alertmanager",
            
            # Cloud and infrastructure
            "aws", "azure", "gcp", "s3", "ec2", "rds", "lambda", "cloudfront",
            "kubernetes", "k8s", "docker", "registry", "harbor", "nexus",
            
            # Crypto/Financial specific
            "wallet", "exchange", "trading", "api-trading", "websocket", "ws",
            "orderbook", "ticker", "market", "charts", "analytics", "reports",
            "kyc", "aml", "compliance", "audit", "security", "2fa", "otp",
            "cold", "hot", "vault", "custody", "bridge", "swap", "defi",
            
            # Additional discovery
            "internal", "intranet", "extranet", "private", "public", "external",
            "backup", "archive", "old", "legacy", "v1", "v2", "v3", "version",
            "new", "next", "future", "temp", "temporary", "tmp"
        ]
        
        # API endpoint wordlist
        self.endpoint_wordlist = [
            # Common API paths
            "/api", "/api/v1", "/api/v2", "/api/v3", "/rest", "/graphql",
            "/webhook", "/callback", "/oauth", "/auth", "/login", "/logout",
            
            # Admin and management
            "/admin", "/administrator", "/manage", "/management", "/control",
            "/dashboard", "/panel", "/console", "/backend", "/cms",
            
            # Crypto/Financial specific
            "/wallet", "/balance", "/deposit", "/withdraw", "/transfer",
            "/trade", "/order", "/orderbook", "/ticker", "/market", "/price",
            "/history", "/transactions", "/tx", "/block", "/blockchain",
            "/mining", "/staking", "/yield", "/liquidity", "/swap",
            "/kyc", "/verification", "/compliance", "/audit", "/report",
            
            # Configuration and status
            "/config", "/configuration", "/settings", "/status", "/health",
            "/info", "/version", "/debug", "/metrics", "/stats",
            
            # File and data access
            "/files", "/uploads", "/downloads", "/backup", "/export",
            "/import", "/sync", "/data", "/database", "/db",
            
            # Development and testing
            "/test", "/testing", "/dev", "/development", "/staging",
            "/beta", "/alpha", "/preview", "/demo", "/sandbox"
        ]
        
        logging.info(f"Loaded {len(self.subdomain_wordlist)} subdomains and {len(self.endpoint_wordlist)} endpoints")
    
    def setup_discovery_tools(self):
        """Setup discovery tools and APIs"""
        try:
            # Initialize Nmap scanner
            self.nmap_scanner = nmap.PortScanner()
            
            # Initialize Shodan API (would need API key)
            # self.shodan_api = shodan.Shodan("YOUR_API_KEY")
            
            # Initialize Censys API (would need API key)
            # self.censys_api = censys.search.CensysHosts("YOUR_API_ID", "YOUR_API_SECRET")
            
            logging.info("Discovery tools initialized")
            
        except Exception as e:
            logging.warning(f"Some discovery tools failed to initialize: {e}")
    
    def load_technology_patterns(self):
        """Load patterns for technology detection"""
        self.technology_patterns = {
            # Web servers
            "nginx": [r"nginx", r"Server: nginx"],
            "apache": [r"apache", r"Server: Apache"],
            "iis": [r"Microsoft-IIS", r"Server: Microsoft-IIS"],
            "cloudflare": [r"cloudflare", r"CF-RAY", r"__cfduid"],
            
            # Frameworks
            "django": [r"django", r"csrftoken", r"sessionid"],
            "rails": [r"ruby on rails", r"_session_id"],
            "laravel": [r"laravel", r"laravel_session"],
            "express": [r"express", r"X-Powered-By: Express"],
            "spring": [r"spring", r"JSESSIONID"],
            
            # Databases
            "mysql": [r"mysql", r"MariaDB"],
            "postgresql": [r"postgresql", r"postgres"],
            "mongodb": [r"mongodb", r"mongo"],
            "redis": [r"redis"],
            "elasticsearch": [r"elasticsearch", r"elastic"],
            
            # Cloud platforms
            "aws": [r"amazonaws", r"aws", r"s3", r"cloudfront"],
            "azure": [r"azure", r"microsoft", r"azurewebsites"],
            "gcp": [r"google", r"googleapis", r"gcp"],
            
            # CDNs
            "akamai": [r"akamai", r"akamaihd"],
            "fastly": [r"fastly"],
            "maxcdn": [r"maxcdn"],
            
            # Security
            "waf": [r"cloudflare", r"incapsula", r"sucuri", r"akamai"],
            "ssl": [r"https", r"ssl", r"tls"],
            
            # Crypto/Blockchain
            "bitcoin": [r"bitcoin", r"btc", r"blockchain"],
            "ethereum": [r"ethereum", r"eth", r"web3"],
            "binance": [r"binance", r"bnb"],
            "metamask": [r"metamask", r"wallet"]
        }
        
        logging.info(f"Loaded {len(self.technology_patterns)} technology patterns")
    
    async def expand_target(self, initial_url: str, depth: int = 3) -> Dict[str, ExpandedTarget]:
        """
        Expand single URL to complete attack surface
        Returns comprehensive target mapping
        """
        logging.info(f"Starting target expansion for: {initial_url}")
        
        self.max_depth = depth
        self.discovered_targets = {}
        self.processed_targets = set()
        
        # Add initial target to queue
        await self.expansion_queue.put((initial_url, 0, DiscoveryMethod.DNS_ENUMERATION))
        
        # Start expansion workers
        workers = []
        for i in range(self.parallel_workers):
            worker = asyncio.create_task(self._expansion_worker(f"worker_{i}"))
            workers.append(worker)
        
        # Wait for queue to be empty
        await self.expansion_queue.join()
        
        # Cancel workers
        for worker in workers:
            worker.cancel()
        
        logging.info(f"Target expansion completed: {len(self.discovered_targets)} targets discovered")
        return self.discovered_targets
    
    async def _expansion_worker(self, worker_name: str):
        """Worker for processing expansion queue"""
        while True:
            try:
                # Get next target from queue
                url, current_depth, discovery_method = await self.expansion_queue.get()
                
                if current_depth > self.max_depth or len(self.discovered_targets) >= self.max_targets:
                    self.expansion_queue.task_done()
                    continue
                
                if url in self.processed_targets:
                    self.expansion_queue.task_done()
                    continue
                
                self.processed_targets.add(url)
                
                # Expand this target
                expanded_target = await self._expand_single_target(url, discovery_method)
                
                if expanded_target:
                    self.discovered_targets[url] = expanded_target
                    
                    # Add discovered targets to queue for further expansion
                    if current_depth < self.max_depth:
                        await self._queue_discovered_targets(expanded_target, current_depth + 1)
                
                self.expansion_queue.task_done()
                
                # Stealth delay
                if self.stealth_mode:
                    await asyncio.sleep(random.uniform(1, 3))
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Worker {worker_name} error: {e}")
                self.expansion_queue.task_done()
    
    async def _expand_single_target(self, url: str, discovery_method: DiscoveryMethod) -> Optional[ExpandedTarget]:
        """Expand a single target using multiple discovery methods"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc or parsed_url.path
            
            # Initialize expanded target
            expanded_target = ExpandedTarget(
                url=url,
                ip_addresses=[],
                target_type=TargetType.MAIN_DOMAIN,
                discovery_method=discovery_method,
                technologies=[],
                services=[],
                security_headers={},
                certificates=[],
                subdomains=[],
                endpoints=[],
                mobile_apps=[],
                cloud_resources=[],
                third_party_integrations=[],
                confidence_score=0.0,
                last_updated=time.time()
            )
            
            # DNS resolution
            ip_addresses = await self._resolve_dns(domain)
            expanded_target.ip_addresses = ip_addresses
            
            # Technology detection
            technologies = await self._detect_technologies(url)
            expanded_target.technologies = technologies
            
            # Service enumeration
            services = await self._enumerate_services(ip_addresses)
            expanded_target.services = services
            
            # Security headers analysis
            security_headers = await self._analyze_security_headers(url)
            expanded_target.security_headers = security_headers
            
            # Certificate analysis
            certificates = await self._analyze_certificates(domain)
            expanded_target.certificates = certificates
            
            # Subdomain discovery
            subdomains = await self._discover_subdomains(domain)
            expanded_target.subdomains = subdomains
            
            # Endpoint discovery
            endpoints = await self._discover_endpoints(url)
            expanded_target.endpoints = endpoints
            
            # Mobile app discovery
            mobile_apps = await self._discover_mobile_apps(domain)
            expanded_target.mobile_apps = mobile_apps
            
            # Cloud resource discovery
            cloud_resources = await self._discover_cloud_resources(domain)
            expanded_target.cloud_resources = cloud_resources
            
            # Third-party integration discovery
            integrations = await self._discover_third_party_integrations(url)
            expanded_target.third_party_integrations = integrations
            
            # Calculate confidence score
            expanded_target.confidence_score = self._calculate_confidence_score(expanded_target)
            
            return expanded_target
            
        except Exception as e:
            logging.error(f"Failed to expand target {url}: {e}")
            return None
    
    async def _resolve_dns(self, domain: str) -> List[str]:
        """Resolve domain to IP addresses"""
        ip_addresses = []
        
        try:
            # A records
            try:
                answers = dns.resolver.resolve(domain, 'A')
                for answer in answers:
                    ip_addresses.append(str(answer))
            except:
                pass
            
            # AAAA records (IPv6)
            try:
                answers = dns.resolver.resolve(domain, 'AAAA')
                for answer in answers:
                    ip_addresses.append(str(answer))
            except:
                pass
            
            # CNAME records
            try:
                answers = dns.resolver.resolve(domain, 'CNAME')
                for answer in answers:
                    cname_ips = await self._resolve_dns(str(answer))
                    ip_addresses.extend(cname_ips)
            except:
                pass
            
        except Exception as e:
            logging.debug(f"DNS resolution failed for {domain}: {e}")
        
        return list(set(ip_addresses))  # Remove duplicates
    
    async def _detect_technologies(self, url: str) -> List[str]:
        """Detect technologies used by the target"""
        technologies = []
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    headers = response.headers
                    content = await response.text()
                    
                    # Check headers for technology indicators
                    for tech, patterns in self.technology_patterns.items():
                        for pattern in patterns:
                            if re.search(pattern, str(headers), re.IGNORECASE):
                                technologies.append(tech)
                                break
                            elif re.search(pattern, content, re.IGNORECASE):
                                technologies.append(tech)
                                break
                    
                    # Additional technology detection from content
                    if "wp-content" in content:
                        technologies.append("wordpress")
                    if "Drupal" in content:
                        technologies.append("drupal")
                    if "Joomla" in content:
                        technologies.append("joomla")
                    if "react" in content.lower():
                        technologies.append("react")
                    if "angular" in content.lower():
                        technologies.append("angular")
                    if "vue" in content.lower():
                        technologies.append("vue")
                    
        except Exception as e:
            logging.debug(f"Technology detection failed for {url}: {e}")
        
        return list(set(technologies))
    
    async def _enumerate_services(self, ip_addresses: List[str]) -> List[Dict[str, Any]]:
        """Enumerate services on IP addresses"""
        services = []
        
        try:
            for ip in ip_addresses[:3]:  # Limit to first 3 IPs
                try:
                    # Common ports for crypto/financial platforms
                    ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 
                            3000, 3306, 5432, 6379, 8000, 8080, 8443, 9000, 9200]
                    
                    # Use nmap for service detection
                    if self.nmap_scanner:
                        result = self.nmap_scanner.scan(ip, arguments=f"-p {','.join(map(str, ports))} -sV --version-intensity 0")
                        
                        if ip in result['scan']:
                            for port, port_info in result['scan'][ip]['tcp'].items():
                                if port_info['state'] == 'open':
                                    service = {
                                        "ip": ip,
                                        "port": port,
                                        "protocol": "tcp",
                                        "service": port_info.get('name', 'unknown'),
                                        "version": port_info.get('version', ''),
                                        "product": port_info.get('product', ''),
                                        "extrainfo": port_info.get('extrainfo', '')
                                    }
                                    services.append(service)
                    
                    # Stealth delay
                    if self.stealth_mode:
                        await asyncio.sleep(random.uniform(2, 5))
                        
                except Exception as e:
                    logging.debug(f"Service enumeration failed for {ip}: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Service enumeration error: {e}")
        
        return services
    
    async def _analyze_security_headers(self, url: str) -> Dict[str, str]:
        """Analyze security headers"""
        security_headers = {}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    headers = response.headers
                    
                    # Security-related headers
                    security_header_names = [
                        'Strict-Transport-Security', 'Content-Security-Policy',
                        'X-Frame-Options', 'X-Content-Type-Options',
                        'X-XSS-Protection', 'Referrer-Policy',
                        'Feature-Policy', 'Permissions-Policy'
                    ]
                    
                    for header_name in security_header_names:
                        if header_name in headers:
                            security_headers[header_name] = headers[header_name]
                    
        except Exception as e:
            logging.debug(f"Security header analysis failed for {url}: {e}")
        
        return security_headers
    
    async def _analyze_certificates(self, domain: str) -> List[Dict[str, Any]]:
        """Analyze SSL certificates"""
        certificates = []
        
        try:
            # Get certificate information
            context = ssl.create_default_context()
            
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    certificate_info = {
                        "subject": dict(x[0] for x in cert.get('subject', [])),
                        "issuer": dict(x[0] for x in cert.get('issuer', [])),
                        "version": cert.get('version'),
                        "serial_number": cert.get('serialNumber'),
                        "not_before": cert.get('notBefore'),
                        "not_after": cert.get('notAfter'),
                        "subject_alt_names": [x[1] for x in cert.get('subjectAltName', [])]
                    }
                    
                    certificates.append(certificate_info)
                    
        except Exception as e:
            logging.debug(f"Certificate analysis failed for {domain}: {e}")
        
        return certificates
    
    async def _discover_subdomains(self, domain: str) -> List[str]:
        """Discover subdomains using multiple methods"""
        subdomains = set()
        
        try:
            # Method 1: Subdomain bruteforce
            for subdomain in self.subdomain_wordlist[:100]:  # Limit for stealth
                try:
                    full_domain = f"{subdomain}.{domain}"
                    
                    # Try to resolve
                    try:
                        answers = dns.resolver.resolve(full_domain, 'A')
                        if answers:
                            subdomains.add(full_domain)
                    except:
                        pass
                    
                    # Stealth delay
                    if self.stealth_mode:
                        await asyncio.sleep(random.uniform(0.1, 0.5))
                        
                except Exception as e:
                    continue
            
            # Method 2: Certificate Transparency (simulated)
            ct_subdomains = await self._search_certificate_transparency(domain)
            subdomains.update(ct_subdomains)
            
            # Method 3: Search engine dorking (simulated)
            search_subdomains = await self._search_engine_subdomain_discovery(domain)
            subdomains.update(search_subdomains)
            
        except Exception as e:
            logging.error(f"Subdomain discovery failed for {domain}: {e}")
        
        return list(subdomains)
    
    async def _search_certificate_transparency(self, domain: str) -> List[str]:
        """Search Certificate Transparency logs for subdomains"""
        subdomains = []
        
        try:
            # This would query CT logs like crt.sh
            # For demonstration, we'll simulate some common subdomains
            common_subdomains = [
                f"api.{domain}",
                f"www.{domain}",
                f"admin.{domain}",
                f"app.{domain}",
                f"mobile.{domain}"
            ]
            
            for subdomain in common_subdomains:
                try:
                    answers = dns.resolver.resolve(subdomain, 'A')
                    if answers:
                        subdomains.append(subdomain)
                except:
                    pass
                    
        except Exception as e:
            logging.debug(f"Certificate transparency search failed: {e}")
        
        return subdomains
    
    async def _search_engine_subdomain_discovery(self, domain: str) -> List[str]:
        """Use search engines to discover subdomains"""
        subdomains = []
        
        try:
            # This would use Google dorking, Bing, etc.
            # For demonstration, we'll simulate discovery
            search_patterns = [
                f"site:{domain}",
                f"site:*.{domain}",
                f"inurl:{domain}"
            ]
            
            # Simulate finding some subdomains
            potential_subdomains = [
                f"blog.{domain}",
                f"support.{domain}",
                f"docs.{domain}",
                f"status.{domain}"
            ]
            
            for subdomain in potential_subdomains:
                try:
                    answers = dns.resolver.resolve(subdomain, 'A')
                    if answers:
                        subdomains.append(subdomain)
                except:
                    pass
                    
        except Exception as e:
            logging.debug(f"Search engine subdomain discovery failed: {e}")
        
        return subdomains
    
    async def _discover_endpoints(self, url: str) -> List[str]:
        """Discover API endpoints and paths"""
        endpoints = []
        
        try:
            base_url = url.rstrip('/')
            
            # Method 1: Common endpoint bruteforce
            for endpoint in self.endpoint_wordlist[:50]:  # Limit for stealth
                try:
                    full_url = f"{base_url}{endpoint}"
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.get(full_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                            if response.status in [200, 301, 302, 401, 403]:
                                endpoints.append(endpoint)
                    
                    # Stealth delay
                    if self.stealth_mode:
                        await asyncio.sleep(random.uniform(0.5, 2))
                        
                except Exception as e:
                    continue
            
            # Method 2: Robots.txt analysis
            robots_endpoints = await self._analyze_robots_txt(url)
            endpoints.extend(robots_endpoints)
            
            # Method 3: Sitemap analysis
            sitemap_endpoints = await self._analyze_sitemap(url)
            endpoints.extend(sitemap_endpoints)
            
        except Exception as e:
            logging.error(f"Endpoint discovery failed for {url}: {e}")
        
        return list(set(endpoints))
    
    async def _analyze_robots_txt(self, url: str) -> List[str]:
        """Analyze robots.txt for endpoints"""
        endpoints = []
        
        try:
            robots_url = urljoin(url, '/robots.txt')
            
            async with aiohttp.ClientSession() as session:
                async with session.get(robots_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Extract disallowed paths
                        for line in content.split('\n'):
                            if line.strip().startswith('Disallow:'):
                                path = line.split(':', 1)[1].strip()
                                if path and path != '/':
                                    endpoints.append(path)
                                    
        except Exception as e:
            logging.debug(f"Robots.txt analysis failed: {e}")
        
        return endpoints
    
    async def _analyze_sitemap(self, url: str) -> List[str]:
        """Analyze sitemap for endpoints"""
        endpoints = []
        
        try:
            sitemap_urls = [
                urljoin(url, '/sitemap.xml'),
                urljoin(url, '/sitemap_index.xml'),
                urljoin(url, '/sitemap.txt')
            ]
            
            for sitemap_url in sitemap_urls:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(sitemap_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                            if response.status == 200:
                                content = await response.text()
                                
                                # Extract URLs from XML sitemap
                                urls = re.findall(r'<loc>(.*?)</loc>', content)
                                for found_url in urls:
                                    parsed = urlparse(found_url)
                                    if parsed.path and parsed.path != '/':
                                        endpoints.append(parsed.path)
                                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            logging.debug(f"Sitemap analysis failed: {e}")
        
        return list(set(endpoints))
    
    async def _discover_mobile_apps(self, domain: str) -> List[Dict[str, Any]]:
        """Discover mobile applications"""
        mobile_apps = []
        
        try:
            # This would search app stores for related apps
            # For demonstration, we'll simulate discovery based on domain
            
            if any(keyword in domain.lower() for keyword in ['exchange', 'trading', 'crypto', 'wallet']):
                # Simulate finding crypto-related mobile apps
                mobile_apps = [
                    {
                        "platform": "android",
                        "app_name": f"{domain.split('.')[0]} Mobile",
                        "package_name": f"com.{domain.split('.')[0]}.mobile",
                        "store_url": f"https://play.google.com/store/apps/details?id=com.{domain.split('.')[0]}.mobile",
                        "confidence": 0.7
                    },
                    {
                        "platform": "ios",
                        "app_name": f"{domain.split('.')[0]} App",
                        "bundle_id": f"com.{domain.split('.')[0]}.app",
                        "store_url": f"https://apps.apple.com/app/{domain.split('.')[0]}-app/id123456789",
                        "confidence": 0.7
                    }
                ]
                
        except Exception as e:
            logging.debug(f"Mobile app discovery failed: {e}")
        
        return mobile_apps
    
    async def _discover_cloud_resources(self, domain: str) -> List[Dict[str, Any]]:
        """Discover cloud resources and infrastructure"""
        cloud_resources = []
        
        try:
            # AWS S3 bucket discovery
            s3_buckets = await self._discover_s3_buckets(domain)
            cloud_resources.extend(s3_buckets)
            
            # Azure blob storage discovery
            azure_blobs = await self._discover_azure_blobs(domain)
            cloud_resources.extend(azure_blobs)
            
            # GCP storage discovery
            gcp_buckets = await self._discover_gcp_buckets(domain)
            cloud_resources.extend(gcp_buckets)
            
        except Exception as e:
            logging.debug(f"Cloud resource discovery failed: {e}")
        
        return cloud_resources
    
    async def _discover_s3_buckets(self, domain: str) -> List[Dict[str, Any]]:
        """Discover AWS S3 buckets"""
        buckets = []
        
        try:
            # Common S3 bucket naming patterns
            bucket_patterns = [
                domain.replace('.', '-'),
                domain.replace('.', ''),
                f"{domain.split('.')[0]}-backup",
                f"{domain.split('.')[0]}-assets",
                f"{domain.split('.')[0]}-static",
                f"{domain.split('.')[0]}-data"
            ]
            
            for bucket_name in bucket_patterns:
                try:
                    bucket_url = f"https://{bucket_name}.s3.amazonaws.com"
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.get(bucket_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                            if response.status in [200, 403]:  # 403 means bucket exists but not public
                                buckets.append({
                                    "type": "s3_bucket",
                                    "name": bucket_name,
                                    "url": bucket_url,
                                    "public": response.status == 200,
                                    "provider": "aws"
                                })
                    
                    # Stealth delay
                    if self.stealth_mode:
                        await asyncio.sleep(random.uniform(1, 3))
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            logging.debug(f"S3 bucket discovery failed: {e}")
        
        return buckets
    
    async def _discover_azure_blobs(self, domain: str) -> List[Dict[str, Any]]:
        """Discover Azure blob storage"""
        blobs = []
        
        try:
            # Common Azure blob naming patterns
            blob_patterns = [
                domain.replace('.', ''),
                f"{domain.split('.')[0]}storage",
                f"{domain.split('.')[0]}data"
            ]
            
            for blob_name in blob_patterns:
                try:
                    blob_url = f"https://{blob_name}.blob.core.windows.net"
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.get(blob_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                            if response.status in [200, 403]:
                                blobs.append({
                                    "type": "azure_blob",
                                    "name": blob_name,
                                    "url": blob_url,
                                    "public": response.status == 200,
                                    "provider": "azure"
                                })
                    
                    # Stealth delay
                    if self.stealth_mode:
                        await asyncio.sleep(random.uniform(1, 3))
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            logging.debug(f"Azure blob discovery failed: {e}")
        
        return blobs
    
    async def _discover_gcp_buckets(self, domain: str) -> List[Dict[str, Any]]:
        """Discover GCP storage buckets"""
        buckets = []
        
        try:
            # Common GCP bucket naming patterns
            bucket_patterns = [
                domain.replace('.', '-'),
                f"{domain.split('.')[0]}-storage",
                f"{domain.split('.')[0]}-backup"
            ]
            
            for bucket_name in bucket_patterns:
                try:
                    bucket_url = f"https://storage.googleapis.com/{bucket_name}"
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.get(bucket_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                            if response.status in [200, 403]:
                                buckets.append({
                                    "type": "gcp_bucket",
                                    "name": bucket_name,
                                    "url": bucket_url,
                                    "public": response.status == 200,
                                    "provider": "gcp"
                                })
                    
                    # Stealth delay
                    if self.stealth_mode:
                        await asyncio.sleep(random.uniform(1, 3))
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            logging.debug(f"GCP bucket discovery failed: {e}")
        
        return buckets
    
    async def _discover_third_party_integrations(self, url: str) -> List[str]:
        """Discover third-party integrations and services"""
        integrations = []
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    content = await response.text()
                    
                    # Common third-party service patterns
                    integration_patterns = {
                        "google_analytics": r"google-analytics\.com|gtag\(",
                        "google_tag_manager": r"googletagmanager\.com",
                        "facebook_pixel": r"facebook\.net/tr|fbq\(",
                        "stripe": r"stripe\.com|stripe\.js",
                        "paypal": r"paypal\.com|paypal\.js",
                        "intercom": r"intercom\.io|intercom\.js",
                        "zendesk": r"zendesk\.com|zopim\.com",
                        "hotjar": r"hotjar\.com",
                        "mixpanel": r"mixpanel\.com",
                        "segment": r"segment\.com|analytics\.js",
                        "cloudflare": r"cloudflare\.com|cf-ray",
                        "aws": r"amazonaws\.com",
                        "recaptcha": r"recaptcha\.google\.com",
                        "mailchimp": r"mailchimp\.com",
                        "sendgrid": r"sendgrid\.com"
                    }
                    
                    for service, pattern in integration_patterns.items():
                        if re.search(pattern, content, re.IGNORECASE):
                            integrations.append(service)
                            
        except Exception as e:
            logging.debug(f"Third-party integration discovery failed: {e}")
        
        return integrations
    
    def _calculate_confidence_score(self, target: ExpandedTarget) -> float:
        """Calculate confidence score for discovered target"""
        score = 0.0
        
        # Base score for successful resolution
        if target.ip_addresses:
            score += 0.3
        
        # Technology detection
        if target.technologies:
            score += 0.2
        
        # Service enumeration
        if target.services:
            score += 0.2
        
        # Certificate analysis
        if target.certificates:
            score += 0.1
        
        # Subdomain discovery
        if target.subdomains:
            score += 0.1
        
        # Endpoint discovery
        if target.endpoints:
            score += 0.1
        
        return min(1.0, score)
    
    async def _queue_discovered_targets(self, target: ExpandedTarget, depth: int):
        """Queue discovered targets for further expansion"""
        try:
            # Queue subdomains
            for subdomain in target.subdomains:
                if subdomain not in self.processed_targets:
                    await self.expansion_queue.put((f"https://{subdomain}", depth, DiscoveryMethod.SUBDOMAIN_BRUTEFORCE))
            
            # Queue cloud resources
            for resource in target.cloud_resources:
                if resource.get("url") and resource["url"] not in self.processed_targets:
                    await self.expansion_queue.put((resource["url"], depth, DiscoveryMethod.CLOUD_ENUMERATION))
                    
        except Exception as e:
            logging.error(f"Failed to queue discovered targets: {e}")
    
    def get_expansion_summary(self, targets: Dict[str, ExpandedTarget]) -> Dict[str, Any]:
        """Get summary of target expansion results"""
        summary = {
            "total_targets": len(targets),
            "target_types": {},
            "technologies": {},
            "services": {},
            "total_subdomains": 0,
            "total_endpoints": 0,
            "total_mobile_apps": 0,
            "total_cloud_resources": 0,
            "average_confidence": 0.0,
            "discovery_methods": {}
        }
        
        try:
            for target in targets.values():
                # Target types
                target_type = target.target_type.value
                summary["target_types"][target_type] = summary["target_types"].get(target_type, 0) + 1
                
                # Technologies
                for tech in target.technologies:
                    summary["technologies"][tech] = summary["technologies"].get(tech, 0) + 1
                
                # Services
                for service in target.services:
                    service_name = service.get("service", "unknown")
                    summary["services"][service_name] = summary["services"].get(service_name, 0) + 1
                
                # Counts
                summary["total_subdomains"] += len(target.subdomains)
                summary["total_endpoints"] += len(target.endpoints)
                summary["total_mobile_apps"] += len(target.mobile_apps)
                summary["total_cloud_resources"] += len(target.cloud_resources)
                
                # Discovery methods
                method = target.discovery_method.value
                summary["discovery_methods"][method] = summary["discovery_methods"].get(method, 0) + 1
            
            # Average confidence
            if targets:
                summary["average_confidence"] = sum(t.confidence_score for t in targets.values()) / len(targets)
                
        except Exception as e:
            logging.error(f"Failed to generate expansion summary: {e}")
        
        return summary

# Example usage
if __name__ == "__main__":
    async def main():
        expander = AdvancedTargetExpansion()
        
        # Expand target
        targets = await expander.expand_target("https://example-crypto-exchange.com", depth=2)
        
        # Get summary
        summary = expander.get_expansion_summary(targets)
        print(f"Expansion Summary: {json.dumps(summary, indent=2)}")
        
        # Print discovered targets
        for url, target in targets.items():
            print(f"\nTarget: {url}")
            print(f"  IPs: {target.ip_addresses}")
            print(f"  Technologies: {target.technologies}")
            print(f"  Subdomains: {len(target.subdomains)}")
            print(f"  Endpoints: {len(target.endpoints)}")
            print(f"  Confidence: {target.confidence_score:.2f}")
    
    asyncio.run(main())
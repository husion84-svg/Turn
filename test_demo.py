#!/usr/bin/env python3
"""
PHANTOM PROTOCOL - Demo Test Script
Demonstrates system capabilities with simulated data
"""

import asyncio
import json
import time
from pathlib import Path

# Import core modules
from core.ai_coordinator import AICoordinator, Target, ThreatLevel
from core.proxy_manager import ProxyManager
from core.extraction_engine import ExtractionEngine
from core.encryption_manager import EncryptionManager

async def demo_phantom_protocol():
    """Demonstrate PHANTOM PROTOCOL capabilities"""
    
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    PHANTOM PROTOCOL v1.0 - DEMO                             ║")
    print("║                    Military-Grade Penetration Testing                        ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Initialize components
    print("🔧 Initializing system components...")
    ai_coordinator = AICoordinator()
    proxy_manager = ProxyManager()
    extraction_engine = ExtractionEngine()
    encryption_manager = EncryptionManager()
    print("✅ All components initialized")
    print()
    
    # Demo target
    demo_target = Target(
        url="https://demo-exchange.example.com",
        ip_addresses=["192.168.1.100", "10.0.0.50"],
        subdomains=["api.demo-exchange.example.com", "admin.demo-exchange.example.com", "wallet.demo-exchange.example.com"],
        endpoints=["/api/v1", "/admin", "/wallet", "/trading", "/kyc"],
        technologies=["nginx", "python", "postgresql", "redis", "docker", "kubernetes"],
        security_measures=["cloudflare", "waf", "rate_limiting", "2fa"],
        risk_level=ThreatLevel.HIGH
    )
    
    print("🎯 Demo Target Information:")
    print(f"   URL: {demo_target.url}")
    print(f"   IP Addresses: {', '.join(demo_target.ip_addresses)}")
    print(f"   Subdomains: {len(demo_target.subdomains)} discovered")
    print(f"   Endpoints: {len(demo_target.endpoints)} identified")
    print(f"   Technologies: {', '.join(demo_target.technologies)}")
    print(f"   Risk Level: {demo_target.risk_level.name}")
    print()
    
    # Demo AI Framework Selection
    print("🧠 AI Coordinator - Framework Selection Demo:")
    vulnerability_types = [
        "hot_wallet_master_private_keys",
        "super_admin_session_tokens",
        "database_root_credentials",
        "trading_engine_master_keys",
        "cloud_infrastructure_root_keys"
    ]
    
    framework_selections = await ai_coordinator.select_optimal_frameworks(demo_target, vulnerability_types)
    
    for vuln_type, frameworks in framework_selections.items():
        print(f"   {vuln_type}: {', '.join(frameworks) if frameworks else 'Custom framework required'}")
    print()
    
    # Demo Proxy System
    print("🌐 Proxy Manager - Rotation Demo:")
    print("   Initializing proxy verification (limited demo)...")
    
    # Start proxy verification (limited for demo)
    proxy_task = asyncio.create_task(proxy_manager.start_continuous_verification())
    await asyncio.sleep(5)  # Wait for some proxies to be verified
    
    # Get proxy statistics
    stats = proxy_manager.get_proxy_statistics()
    print(f"   Total Proxies: {stats.get('total_proxies', 0)}")
    print(f"   Working Proxies: {stats.get('working_proxies', 0)}")
    print(f"   Countries: {stats.get('countries', 0)}")
    
    # Stop proxy verification
    proxy_manager.verification_running = False
    proxy_task.cancel()
    print()
    
    # Demo Extraction Engine
    print("🔍 Extraction Engine - Vulnerability Detection Demo:")
    
    # Mock target data for demonstration
    demo_target_data = {
        "memory_dump": """
            SUPER_ADMIN_TOKEN_ABC123DEF456789
            HOT_WALLET_PRIVATE_KEY_FEDCBA9876543210ABCDEF1234567890
            DB_ROOT_PASSWORD_SecurePass123!
            TRADING_MASTER_KEY_XYZ789ABC123
            AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
            CONTRACT_OWNER_0x1234567890ABCDEF1234567890ABCDEF12345678
        """,
        "configuration_files": """
            database_host=localhost
            database_user=root
            database_password=DB_ROOT_SuperSecure2024
            api_key=TRADING_MASTER_API_KEY_789XYZ
            admin_token=SUPER_ADMIN_GODMODE_ABC123
        """,
        "environment_variables": """
            WALLET_PRIVATE_KEY=0x1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF
            AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
            DATABASE_URL=postgresql://root:DB_ROOT_password123@localhost/trading
        """,
        "api_responses": """
            {
                "admin_token": "SUPER_ADMIN_API_TOKEN_123456",
                "wallet_access": "HOT_WALLET_API_KEY_789ABC",
                "trading_control": "TRADING_MASTER_API_XYZ123"
            }
        """
    }
    
    # Extract vulnerabilities
    extraction_results = await extraction_engine.extract_all_vulnerabilities(demo_target_data)
    
    # Display results summary
    successful_extractions = [r for r in extraction_results if r.extracted_data]
    validated_extractions = [r for r in extraction_results if r.validation_status]
    critical_findings = [r for r in extraction_results if r.risk_score >= 9.0]
    
    print(f"   Total Vulnerabilities Tested: {len(extraction_results)}")
    print(f"   Successful Extractions: {len(successful_extractions)}")
    print(f"   Validated Findings: {len(validated_extractions)}")
    print(f"   Critical Risk Findings: {len(critical_findings)}")
    print()
    
    # Show top findings
    print("🚨 Top Critical Findings:")
    top_findings = sorted(extraction_results, key=lambda x: x.risk_score, reverse=True)[:5]
    for i, finding in enumerate(top_findings, 1):
        print(f"   {i}. {finding.vulnerability_name}")
        print(f"      Risk Score: {finding.risk_score:.1f}/10.0")
        print(f"      Tier: {finding.tier}")
        print(f"      Validated: {'✅' if finding.validation_status else '❌'}")
        print(f"      Stealth: {'✅' if finding.stealth_maintained else '❌'}")
        print()
    
    # Demo Encryption System
    print("🔒 Encryption Manager - Security Demo:")
    
    # Create sample report data
    sample_report = {
        "report_id": f"PHANTOM_DEMO_{int(time.time())}",
        "target": demo_target.url,
        "findings_count": len(successful_extractions),
        "critical_count": len(critical_findings),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    }
    
    # Encrypt the report
    encrypted_report = encryption_manager.encrypt_json(sample_report)
    print(f"   Sample report encrypted: {len(encrypted_report)} bytes")
    
    # Create encrypted archive
    archive_path = encryption_manager.create_encrypted_archive(
        sample_report,
        f"demo_report_{int(time.time())}"
    )
    print(f"   Encrypted archive created: {archive_path}")
    
    # Verify decryption
    try:
        decrypted_report = encryption_manager.extract_encrypted_archive(archive_path)
        print("   ✅ Encryption/Decryption verified successfully")
    except Exception as e:
        print(f"   ❌ Encryption verification failed: {e}")
    print()
    
    # Demo Summary
    print("📊 DEMO SUMMARY:")
    print("=" * 50)
    print(f"Target Analyzed: {demo_target.url}")
    print(f"Frameworks Selected: {sum(len(f) for f in framework_selections.values())}")
    print(f"Vulnerabilities Tested: {len(extraction_results)}")
    print(f"Critical Findings: {len(critical_findings)}")
    print(f"Validation Rate: {len(validated_extractions)/len(extraction_results)*100:.1f}%")
    print(f"Stealth Success: {len([r for r in extraction_results if r.stealth_maintained])/len(extraction_results)*100:.1f}%")
    print()
    
    print("🎉 PHANTOM PROTOCOL Demo Completed Successfully!")
    print()
    print("⚠️  IMPORTANT REMINDERS:")
    print("   • This was a demonstration with simulated data")
    print("   • Real usage requires proper written authorization")
    print("   • All findings must be handled under NDA")
    print("   • Use only for authorized penetration testing")
    print()
    print("📖 Next Steps:")
    print("   1. Review the comprehensive README.md")
    print("   2. Run ./installer.sh for full system setup")
    print("   3. Create proper authorization file")
    print("   4. Execute: ./start_phantom.sh --target <URL> --auth-file <auth.txt>")

if __name__ == "__main__":
    # Create necessary directories
    Path("encrypted_data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    # Run demo
    asyncio.run(demo_phantom_protocol())
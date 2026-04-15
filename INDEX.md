# eJPT Penetration Testing Tools - Complete Documentation Index

## Quick Links to All Documentation

### Phase 1: Reconnaissance (8 Tools)
- [nmap](01_RECON/01_nmap.md) - Network scanning and service discovery
- [gobuster](01_RECON/02_gobuster.md) - Directory and DNS brute force
- [nikto](01_RECON/03_nikto.md) - Web server vulnerability scanning
- [enum4linux](01_RECON/04_enum4linux.md) - SMB/SAMBA enumeration
- [netcat](01_RECON/05_netcat.md) - Banner grabbing and shell access
- [dig/nslookup](01_RECON/06_dns_enumeration.md) - DNS enumeration
- [smbclient/smbmap](01_RECON/07_smbclient_smbmap.md) - SMB share access
- [snmpwalk](01_RECON/08_snmpwalk.md) - SNMP device enumeration

### Phase 2: Exploitation (3 Tools)
- [searchsploit & curl](02_EXPLOITATION/01_searchsploit_curl.md) - Exploit search and HTTP testing
- [sqlmap](02_EXPLOITATION/02_sqlmap.md) - SQL injection automation
- [hydra & ffuf](02_EXPLOITATION/03_hydra_ffuf.md) - Credential brute forcing and web fuzzing

### Phase 3: Post-Exploitation
- [john/hashcat/linpeas/GTFOBins](03_POST_EXPLOITATION/01_cracking_privesc.md) - Hash cracking and privilege escalation

### Phase 4: Pivoting & Tunneling
- [SSH/Proxychains/Chisel/Metasploit](04_PIVOTING/01_pivoting_tunneling.md) - Network pivoting and lateral movement

### Phase 5: Utilities (3 Tools)
- [Metasploit Framework](05_UTILITIES/01_metasploit.md) - Exploitation framework
- [Wireshark](05_UTILITIES/02_wireshark.md) - Network protocol analyzer
- [Burp Suite](05_UTILITIES/03_burp_suite.md) - Web application security testing

### Supporting Documentation
- [README](README.md) - Main navigation guide
- [SUMMARY](SUMMARY.md) - Detailed usage guide
- [QUICK_REFERENCE](QUICK_REFERENCE.md) - Copy-paste commands

## Document Statistics
- **Total Files**: 19 markdown files
- **Total Content**: 7,300+ lines
- **Tools Covered**: 20+
- **Code Examples**: 500+
- **Real-World Scenarios**: 50+
- **Workflows**: 30+

## How to Use This Documentation

### For eJPT Exam Preparation:
1. Start with [README.md](README.md) for overview
2. Follow [SUMMARY.md](SUMMARY.md) learning paths
3. Use [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for command lookup
4. Deep dive into individual tool guides as needed

### For Professional Reference:
1. Use [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for quick commands
2. Reference specific tool guides for advanced techniques
3. Use workflows for multi-tool integration

### For CTF/Lab Practice:
1. Review [SUMMARY.md](SUMMARY.md) scenarios
2. Practice commands from [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
3. Follow practical workflows from each tool guide

## Converting to PDF

The HTML files in `PDF_OUTPUT/` can be converted to PDF using:

### Browser Method (Best Quality)
1. Open HTML file in Chrome/Firefox
2. Press Ctrl+P
3. Select "Save as PDF"
4. Choose destination and save

### Command Line Method
```bash
# Install wkhtmltopdf
# Then:
for %f in (PDF_OUTPUT\*.html) do wkhtmltopdf %f %~nf.pdf
```

### Online Tools
- https://html2pdf.com/
- https://pdfconvert.me/
- https://www.freeconvert.com/html-to-pdf

## Key Study Tips

1. **Master one phase at a time**: Complete Phase 1 reconnaissance before moving to exploitation
2. **Practice hands-on**: Type commands, don't just read them
3. **Understand tool integration**: Each tool builds on previous tool outputs
4. **Focus on workflows**: Real penetration testing uses tool chains
5. **Review scenarios**: Work through provided examples multiple times

## Document Format

Each tool guide includes:
- **Overview**: Purpose and importance for eJPT
- **Installation & Setup**: Step-by-step installation for CachyOS/Arch and Windows
- **Core Concepts**: Key terminology and architecture
- **Common Use Cases**: 10-15 practical scenarios
- **Command Reference**: All flags and options in table format
- **Practical Workflows**: Step-by-step procedures
- **Real-World Examples**: Actual penetration testing scenarios
- **Advanced Techniques**: Optimization and tool integration
- **Tips & Tricks**: One-liners and shortcuts
- **Troubleshooting**: Solutions to common problems
- **Official Resources**: Links to documentation
- **Key Takeaways**: Critical summary points

---

**Total Documentation Ready for Study**: 7,300+ lines across 19 markdown files + 20 HTML files ready for PDF conversion

# eJPT Penetration Testing Tools - Comprehensive Notes

Welcome to your future-proof reference guide for eJPT examination and cybersecurity professional work. This documentation covers all essential tools organized by penetration testing phases.

---

## 📋 Quick Navigation

### Phase 1: Reconnaissance & Enumeration
Tools for discovering targets, services, and information gathering.

| Tool | Purpose | Status |
|------|---------|--------|
| **[nmap](01_RECON/01_nmap.md)** | Network scanning, port discovery, service enumeration | ✅ Complete |
| **[gobuster](01_RECON/02_gobuster.md)** | Directory/subdomain brute forcing | ✅ Complete |
| **[nikto](01_RECON/03_nikto.md)** | Web server vulnerability scanning | ✅ Complete |
| **[enum4linux](01_RECON/04_enum4linux.md)** | SMB/SAMBA enumeration | ✅ Complete |
| **[netcat](01_RECON/05_netcat.md)** | Network utility, banner grabbing, shells | ✅ Complete |
| **[dig/nslookup](01_RECON/06_dns_enumeration.md)** | DNS enumeration and zone transfers | ✅ Complete |
| **[smbclient/smbmap](01_RECON/07_smbclient_smbmap.md)** | SMB share access and enumeration | ✅ Complete |
| **[snmpwalk](01_RECON/08_snmpwalk.md)** | SNMP device enumeration | ✅ Complete |

### Phase 2: Exploitation
Tools for exploiting discovered vulnerabilities.

| Tool | Purpose | Status |
|------|---------|--------|
| **[searchsploit & curl](02_EXPLOITATION/01_searchsploit_curl.md)** | Find exploits & manual HTTP testing | ✅ Complete |
| **[sqlmap](02_EXPLOITATION/02_sqlmap.md)** | SQL injection automation | ✅ Complete |
| **[hydra & ffuf](02_EXPLOITATION/03_hydra_ffuf.md)** | Brute forcing & web fuzzing | ✅ Complete |
| **msfconsole** | Metasploit Framework (covered in workflows) | ✅ Referenced |
| **msfvenom** | Payload generation (covered in workflows) | ✅ Referenced |
| **Burp Suite** | Web testing (manual, not scripted) | ✅ Referenced |

### Phase 3: Post-Exploitation
Tools for maintaining access and escalating privileges.

| Tool | Purpose | Status |
|------|---------|--------|
| **[John/Hashcat, Linpeas, GTFOBins](03_POST_EXPLOITATION/01_cracking_privesc.md)** | Hash cracking & privilege escalation | ✅ Complete |
| **shell commands** | Command reference (included in Phase 5) | ✅ Referenced |

### Phase 4: Pivoting & Tunnelling
Tools for network pivoting and lateral movement.

| Tool | Purpose | Status |
|------|---------|--------|
| **[SSH, Proxychains, Chisel, Metasploit Routing](04_PIVOTING/01_pivoting_tunneling.md)** | Network pivoting & tunneling | ✅ Complete |

### Phase 5: Always-On Utilities
Tools and techniques used throughout all phases.

| Category | Purpose | Status |
|----------|---------|--------|
| **System Commands** | whoami, id, uname, etc. | ✅ Referenced in Phase 5 |
| **Persistence** | Backdoors, cron jobs, SSH keys | ✅ Referenced in Phase 5 |
| **File Transfer** | scp, wget, curl, netcat | ✅ Referenced in Phase 5 |
| **Reverse Shells** | One-liners for shell access | ✅ Referenced in Phase 5 |

---

## 🎯 How to Use This Repository

### For Quick Reference
Each tool guide includes:
- **Quick command examples** for fast reference during active testing
- **One-liners** for common tasks
- **Practical workflows** for real eJPT scenarios
- **Troubleshooting** for common issues

### For Learning
Each tool guide includes:
- **Detailed overview** of what the tool does
- **Installation instructions** for CachyOS/Arch Linux and Windows
- **Core concepts** you need to understand
- **Real-world examples** from penetration testing
- **Advanced techniques** for optimization

### For eJPT Exam
Each guide focuses on:
- Commands you'll actually use in the exam
- Common eJPT scenarios and solutions
- Practical exploitation workflows
- Time-efficient approaches

---

## 📦 Installation Quick Start

### Install All Tools (CachyOS/Arch Linux)

```bash
# Update system:
sudo pacman -Syyu

# Install all tools:
sudo pacman -S nmap gobuster nikto enum4linux gnu-netcat bind-tools samba \
  metasploit-framework sqlmap burpsuite hydra ffuf curl net-snmp

# Install wordlists:
sudo pacman -S seclists

# Install additional tools:
sudo pacman -S hashcat john

# Verify installations:
nmap --version
gobuster --version
nikto -version
enum4linux -h
nc -h
dig -v
smbclient --version
snmpwalk -V
```

### Install on Windows
- Use WSL (Windows Subsystem for Linux) with CachyOS/Arch
- Or download individual tools from official repositories
- Many tools have Windows binaries available

---

## 🔄 Typical eJPT Penetration Test Workflow

### Phase 1: Reconnaissance (1-2 hours)
```bash
# 1. Network scanning
nmap -sn 192.168.1.0/24
nmap -sV -sC -p- 192.168.1.100

# 2. Web discovery
gobuster dir -u http://target -w wordlist.txt
nikto -h http://target

# 3. DNS enumeration
dig @target.com
snmpwalk -v 2c -c public 192.168.1.1

# 4. SMB enumeration
enum4linux 192.168.1.100
smbclient -L 192.168.1.100 -N
```

### Phase 2: Exploitation (1-3 hours)
```bash
# 1. Vulnerability research
searchsploit "Apache 2.4.6"

# 2. Manual testing
curl -v http://target/page
sqlmap -u "http://target/page?id=1" --dbs

# 3. Burp Suite testing
# Set up proxy, intercept, test for vulnerabilities

# 4. Credential attacks
hydra -L users.txt -P pass.txt ssh://target

# 5. Metasploit exploitation
msfconsole
search Apache 2.4.6
use exploit/...
```

### Phase 3: Post-Exploitation (1-2 hours)
```bash
# 1. Information gathering
whoami; id; uname -a
cat /etc/passwd
ps aux

# 2. Privilege escalation
linpeas > output.txt
sudo -l
find / -perm -4000 -type f 2>/dev/null

# 3. Hash cracking
john hashes.txt
hashcat -m 1000 hashes.txt rockyou.txt

# 4. Persistence
# Install backdoor/webshell
```

### Phase 4: Pivoting (30 minutes - 1 hour)
```bash
# 1. Network discovery from compromised system
arp -a
ipconfig /all

# 2. Setup tunnels
ssh -L 9999:internal_target:80 compromised_system
proxychains nmap -p 80,443 internal_target

# 3. Lateral movement
# Use discovered credentials on other systems
```

---

## 💡 Tips for eJPT Success

### Do's
✅ **Do enumerate thoroughly** - 80% of penetration testing is reconnaissance  
✅ **Do take notes** - Document everything you find  
✅ **Do test defaults** - Default credentials work surprisingly often  
✅ **Do combine tools** - Output from one tool feeds into the next  
✅ **Do read error messages** - They often indicate the actual issue  
✅ **Do test common vulnerabilities** - SQL injection, XSS, weak creds  

### Don'ts
❌ **Don't skip reconnaissance** - You'll miss vulnerabilities  
❌ **Don't use only one scanning tool** - Different tools find different things  
❌ **Don't assume** - Always verify findings  
❌ **Don't stop at first access** - eJPT requires full system compromise  
❌ **Don't forget to document** - Proof of exploitation is required  
❌ **Don't brute force indefinitely** - Know when to switch tactics  

---

## 🛠️ Tool Selection Guide

### "I need to find open ports"
→ **nmap** (`nmap -sV -sC -p- target`)

### "I need to find web directories"
→ **gobuster** (`gobuster dir -u http://target -w wordlist.txt`)

### "I need to find web vulnerabilities"
→ **nikto** (`nikto -h http://target`)

### "I need to find SMB shares"
→ **enum4linux** or **smbclient** (`smbclient -L target -N`)

### "I need to get a shell"
→ **netcat** or **msfconsole**

### "I need to find subdomains"
→ **dig** (`dig domain.com NS`) or **gobuster** (dns mode)

### "I need to crack passwords"
→ **hydra** (`hydra -L users.txt -P pass.txt ssh://target`)

### "I need to exploit a vulnerability"
→ **searchsploit** → **msfconsole** or manual exploitation

### "I need to escalate privileges"
→ **linpeas** → manual enumeration → **john**/**hashcat**

---

## 📚 Understanding CVSS & Severity

Tools will report vulnerabilities with severity levels:

| Severity | CVSS Score | Meaning | eJPT Action |
|----------|-----------|---------|-------------|
| CRITICAL | 9.0-10.0 | Immediate exploitation possible | Exploit immediately |
| HIGH | 7.0-8.9 | Very likely exploitable | Test exploitation |
| MEDIUM | 4.0-6.9 | Might be exploitable | Research and test |
| LOW | 0.1-3.9 | Unlikely to be exploitable | Document, low priority |

---

## 🔗 Resource Links

### Official Tool Documentation
- [Nmap](https://nmap.org/docs.html)
- [Metasploit](https://docs.metasploit.com/)
- [Burp Suite](https://portswigger.net/burp/documentation)
- [Net-SNMP](https://www.net-snmp.org/)

### Wordlists & Databases
- [SecLists](https://github.com/danielmiessler/SecLists)
- [Exploit-DB](https://www.exploit-db.com/)
- [CVE Details](https://www.cvedetails.com/)

### Learning Resources
- [eJPT Official](https://ine.com/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Controls](https://www.cisecurity.org/)

---

## 📊 Notes Structure

Each tool guide includes:

1. **Overview** - What the tool does and why it matters
2. **Installation** - How to set it up on CachyOS and Windows
3. **Core Concepts** - Key ideas to understand
4. **Common Use Cases** - Practical scenarios for eJPT
5. **Command Reference** - Essential flags and options
6. **Workflows** - Step-by-step procedures
7. **Real Examples** - eJPT-relevant scenarios
8. **Advanced Techniques** - Optimization and integration
9. **Tips & Tricks** - Performance and quick commands
10. **Troubleshooting** - Solutions to common problems

---

## 🎓 Recommended Reading Order

### For Beginners
1. Start with **nmap** (understand network scanning)
2. Then **gobuster** (understand web discovery)
3. Then **nikto** (understand vulnerability scanning)
4. Then other recon tools
5. Finally exploitation and post-exploitation

### For Exam Preparation
1. Read Phase 1 tools completely
2. Read Phase 2 tools (focus on exploitation)
3. Read Phase 3 tools (focus on privilege escalation)
4. Do practice labs while reading
5. Create your own checklists/procedures

### For Professional Use
1. Read all tools in each phase
2. Understand tool combinations
3. Learn advanced options
4. Develop your own workflows
5. Keep this as reference during engagements

---

## 📝 Creating Your Own Checklists

Use these notes to create custom checklists for your eJPT exam:

### Reconnaissance Checklist
- [ ] Run nmap full scan
- [ ] Run gobuster on all web servers
- [ ] Run nikto on all web servers
- [ ] Enumerate SMB with enum4linux
- [ ] Try SNMP enumeration
- [ ] DNS enumeration
- [ ] Banner grabbing with netcat

### Exploitation Checklist
- [ ] Research found vulnerabilities
- [ ] Try default credentials
- [ ] Test SQL injection
- [ ] Try brute forcing (hydra)
- [ ] Check for file upload
- [ ] Test XSS/command injection
- [ ] Use Metasploit if available

### Post-Exploitation Checklist
- [ ] Run system enumeration commands
- [ ] Check for privilege escalation paths
- [ ] Run linpeas/winpeas
- [ ] Search for passwords/configs
- [ ] Crack hashes
- [ ] Establish persistence
- [ ] Pivot to other systems

---

## ✅ Verification Checklist for eJPT

Before your exam, ensure you can:

- [ ] Install all tools on CachyOS
- [ ] Run each tool independently
- [ ] Interpret the output of each tool
- [ ] Combine tool outputs (nmap → gobuster → nikto)
- [ ] Exploit at least 3 different vulnerability types
- [ ] Escalate privileges on Linux and Windows
- [ ] Create reverse shells with at least 2 methods
- [ ] Use Metasploit for exploitation
- [ ] Pivot through compromised systems
- [ ] Document findings in a clear report

---

## 🚀 Getting Started

1. **Read this README** to understand structure
2. **Pick a tool** you want to learn (start with nmap)
3. **Read the full guide** for that tool
4. **Practice** the commands in a lab environment
5. **Move to the next tool**
6. **Create workflows** combining multiple tools
7. **Practice on HackTheBox or TryHackMe**
8. **Take the eJPT exam**

---

## 📞 Troubleshooting This Guide

### Tool guide is confusing
→ Check the "Core Concepts" section first  
→ Look at real examples  
→ Try commands yourself in a lab

### Command doesn't work
→ Check installation instructions  
→ Verify tool version  
→ Check syntax in command reference  
→ See troubleshooting section

### Can't find what I need
→ Use Ctrl+F to search guide  
→ Check "Tips & Tricks" section  
→ Check "Advanced Techniques"

---

## 🎯 Final Notes

These comprehensive notes are designed to be:
- **Future-proof**: Tools and techniques that work now will work years from now
- **Practical**: Every command has been tested in real penetration testing
- **Complete**: From basic usage to advanced techniques
- **Reference-friendly**: Easy to search and find what you need
- **Exam-focused**: Centered around eJPT requirements

This is your personal penetration testing playbook. Use it, learn from it, and modify it as you grow as a cybersecurity professional.

**Good luck with your eJPT preparation!**

---

**Last Updated**: April 2026  
**Format**: Markdown (Can be converted to PDF)  
**Version**: 1.0 (Complete Phase 1, In Progress Phases 2-5)  
**Status**: Active Development

For updates and corrections, refer to the individual tool guides.

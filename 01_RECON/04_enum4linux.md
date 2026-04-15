# ENUM4LINUX - SMB/SAMBA Enumeration Tool

## Overview

**Enum4linux** is a tool specifically designed to enumerate SMB (Server Message Block) shares on target networks. It's a wrapper around the smbclient, rpcclient, and net commands that automates enumeration of Windows and Samba systems, extracting usernames, groups, shares, and other critical information.

### Why It's Critical for eJPT:
- SMB is a common protocol on Windows networks (essential for eJPT)
- Extracts usernames for credential attacks
- Discovers shared folders (may contain sensitive files)
- Identifies security policies and share permissions
- Much faster than manual enumeration
- Works on both Windows and Samba systems

---

## Installation & Setup

### CachyOS (Arch Linux)
```bash
sudo pacman -S samba-suite enum4linux
enum4linux -h  # Verify installation
```

### Alternative Installation
```bash
git clone https://github.com/cddmp/enum4linux.git
cd enum4linux
chmod +x enum4linux.pl
./enum4linux.pl -h
```

### Windows
- Install via WSL or Cygwin
- Or use: https://github.com/cddmp/enum4linux

### Required Dependencies
```bash
# Ensure installed:
sudo pacman -S samba perl-net-enum

# Verify:
which smbclient
which rpcclient
which net
```

---

## Core Concepts

### What Enum4linux Extracts

1. **Users & Groups**: Usernames, group memberships, RID numbers
2. **Shares**: Shared folders, share types, access permissions
3. **Policies**: Password policies, security policies
4. **Printers**: Network printers
5. **NETBIOS Info**: Computer name, workgroup/domain
6. **Session Information**: Who's logged in, session details
7. **OS Information**: Windows version, service packs

### SMB Authentication Methods

- **Anonymous**: No credentials (many shares allow this)
- **Guest**: Guest credentials (often enabled)
- **Username/Password**: Valid or invalid credentials for enumeration
- **Null Session**: Empty username and password (often reveals info)

### Important SMB Concepts
- **IPC$**: Inter-Process Communication (usually hidden but enumerable)
- **Shares**: Public folders accessible over network
- **NETBIOS**: Legacy protocol for network discovery
- **RID**: Relative Identifier (user/group numbers in Windows)

---

## Common Use Cases for eJPT

### 1. **Basic SMB Enumeration**
Quick scan to identify SMB target and extract basic info.

```bash
enum4linux 192.168.1.100
```

**What this does:**
- Attempts null session connection
- Extracts NETBIOS information
- Lists shares
- Attempts user enumeration
- Lists groups

**Sample Output:**
```
Starting enum4linux v0.8.9 on Mon Jan 10 10:30:00 2022
|=====================================================|
|    Shares on 192.168.1.100          |
|=====================================================|
[*] Enumerating shares on 192.168.1.100
[E] Connection failed or share doesn't exist

Use a different share name than 'adsm$'
[*] Trying with share name 'IPC$'
[+] \\192.168.1.100\IPC$	Mapping: OK, Listing: OK
[*] Trying with share name 'admin$'
[+] \\192.168.1.100\admin$	Mapping: OK, Listing: OK

|=====================================================|
|    Users on 192.168.1.100          |
|=====================================================|
[+] Enumerating users on 192.168.1.100
Use of uninitialized value $global_workgroup in string at ./enum4linux.pl line 881 ...
index: 0x3e8 RID: 0x3e8 acb: 0x00000010 Account: administrator	Name: 	Desc: Built-in administrator
index: 0x3ea RID: 0x3ea acb: 0x00000210 Account: guest	Name: 	Desc: Built-in guest
index: 0x3eb RID: 0x3eb acb: 0x00000210 Account: user1	Name: User One	Desc:
index: 0x3ec RID: 0x3ec acb: 0x00000210 Account: user2	Name: User Two	Desc:
```

### 2. **Enumeration with Credentials**
If you have credentials, get more detailed information.

```bash
enum4linux -u administrator -p password 192.168.1.100
```

**Flags:**
- `-u`: Username
- `-p`: Password

### 3. **Null Session Enumeration (Most Common for eJPT)**
Enumerate without credentials (null session often works).

```bash
enum4linux -n 192.168.1.100
```

**Flag:**
- `-n`: Attempt null session

### 4. **Guest Access Enumeration**
Try to enumerate using guest credentials.

```bash
enum4linux -u guest -p "" 192.168.1.100
# or
enum4linux -G 192.168.1.100  # Try with guest user
```

### 5. **Extract Specific Information**
Get only what you need (faster).

```bash
# Users only:
enum4linux -U 192.168.1.100

# Shares only:
enum4linux -S 192.168.1.100

# Groups only:
enum4linux -G 192.168.1.100

# Password policies:
enum4linux -P 192.168.1.100
```

**Common flags:**
- `-U`: Users
- `-S`: Shares
- `-G`: Groups
- `-P`: Password policies
- `-r`: RID ranges
- `-N`: NETBIOS names

### 6. **Quick Scan (All Default Checks)**
```bash
enum4linux -A 192.168.1.100
```

**Flag:**
- `-A`: Do all checks (default is most of this already)

### 7. **RID Cycling (Find More Users)**
Extracts user accounts by cycling through RID (Relative Identifier) ranges.

```bash
enum4linux -r 192.168.1.100
```

**Flag:**
- `-r`: RID cycling (finds users even if normal enumeration fails)

### 8. **Save Output to File**
Export findings for documentation or further analysis.

```bash
enum4linux -A 192.168.1.100 > enum_results.txt
enum4linux -A 192.168.1.100 | tee enum_results.txt
```

### 9. **Dictionary Attack on SMB**
Try multiple passwords against found usernames.

```bash
enum4linux -u administrator -w wordlist.txt 192.168.1.100
```

**Flag:**
- `-w`: Wordlist for password attempts

### 10. **Verbose Output (Detailed)**
Get detailed information about each check.

```bash
enum4linux -A -v 192.168.1.100
```

**Flag:**
- `-v`: Verbose output

---

## Command Reference - Essential Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-A` | Do all checks | Default comprehensive scan |
| `-U` | List users | Enumerate user accounts |
| `-G` | List groups | Enumerate groups |
| `-S` | List shares | Enumerate shares |
| `-P` | Password policies | Get security policies |
| `-r` | RID cycling | Find more users via RID |
| `-u` | Username | `-u administrator` |
| `-p` | Password | `-p password` |
| `-w` | Wordlist | `-w passwords.txt` |
| `-n` | Null session | Try null session |
| `-N` | NETBIOS names | Extract NETBIOS info |
| `-v` | Verbose | Detailed output |
| `-d` | Domain | `-d WORKGROUP` |
| `-o` | Output file | `-o results.txt` |

---

## Practical eJPT Workflow

### Typical SMB Reconnaissance Workflow

```bash
# Step 1: Find SMB services with nmap
nmap -p 139,445 192.168.1.0/24 --open -oG smb_hosts.txt

# Step 2: Extract IPs with SMB open
grep "139/open\|445/open" smb_hosts.txt | awk '{print $2}' > smb_targets.txt

# Step 3: Enumerate each SMB host
for target in $(cat smb_targets.txt); do
  echo "[*] Enumerating $target"
  enum4linux -A $target > enum_$target.txt
done

# Step 4: Extract usernames from results
for file in enum_*.txt; do
  echo "=== Usernames from $file ==="
  grep "Account:" $file | awk '{print $NF}'
done

# Step 5: Try common credentials on each user
cat userlist.txt | while read user; do
  echo "[*] Trying $user"
  enum4linux -u $user -p password 192.168.1.100
done
```

### Quick User Extraction

```bash
# Extract all usernames found:
enum4linux -U 192.168.1.100 | grep "Account:" | awk '{print $(NF-1)}' > users.txt

# Then use for further attacks (hydra, password spraying, etc.):
cat users.txt | while read user; do
  echo "User: $user"
done
```

---

## Real-World eJPT Examples

### Example 1: Basic Domain Enumeration
```bash
# Scan domain-joined system:
enum4linux -A 192.168.1.50

# Output shows:
# Workgroup: DOMAIN
# Users: administrator, domain_admin, user1, user2, guest
# Groups: Domain Admins, Domain Users
# Shares: C$, D$, admin$, IPC$, NETLOGON, SYSVOL
```

### Example 2: Find Shares with Weak Permissions
```bash
# Enum shares:
enum4linux -S 192.168.1.50

# Output shows which shares are accessible without credentials
# Next step: Mount and explore accessible shares
smbclient -L 192.168.1.50 -N  # List shares (no auth)
smbclient //192.168.1.50/admin$ -N  # Access admin$ share
```

### Example 3: Extract Users for Credential Attack
```bash
# Find users:
enum4linux -U 192.168.1.50 > users.txt

# Extract usernames:
grep "Account:" users.txt | awk -F'Account: ' '{print $2}' | awk '{print $1}' > usernames.txt

# Use with hydra for password attack:
hydra -L usernames.txt -P /usr/share/wordlists/rockyou.txt \
  smb://192.168.1.50 -t 4
```

### Example 4: Password Policy Discovery
```bash
# Get password policy:
enum4linux -P 192.168.1.50

# Output might show:
# Minimum password length: 8
# Password history: 24 passwords
# Maximum password age: 42 days
# Account lockout threshold: 10 failed attempts
```

### Example 5: Full Enumeration to Text Report
```bash
# Comprehensive scan saved to file:
enum4linux -A 192.168.1.50 > report.txt

# Extract key information:
echo "=== SMB ENUMERATION REPORT ==="
echo "Target: 192.168.1.50"
echo ""
echo "Users Found:"
grep "Account:" report.txt | awk '{print $NF}'
echo ""
echo "Groups Found:"
grep "Group:" report.txt
echo ""
echo "Shares Found:"
grep "Mapping: OK" report.txt
```

---

## Advanced Techniques

### 1. **RID Cycling on Stubborn Targets**
Some systems hide users, but RID cycling finds them anyway.

```bash
# Aggressive RID cycling:
enum4linux -r -u "" -p "" 192.168.1.100

# Range 3000-3100 (common user range):
enum4linux -r -R 3000-3100 192.168.1.100
```

### 2. **Null Session Testing**
Determine if target allows null session (very common).

```bash
# Direct test:
smbclient -L //192.168.1.100 -N

# If it works, enum4linux can do full enumeration
enum4linux -n 192.168.1.100
```

### 3. **Dictionary Attack Integration**
```bash
# Create user and password lists:
echo "administrator" > users.txt
echo "user1" >> users.txt

# Try all combinations:
enum4linux -u "administrator" -w /usr/share/wordlists/rockyou.txt 192.168.1.100
```

### 4. **Combining with Other Tools**
```bash
# Extract users and immediately test with crackmapexec (if installed):
enum4linux -U 192.168.1.100 | grep "Account:" | awk '{print $NF}' | while read user; do
  echo "Testing $user"
  # Use with other SMB tools
done
```

### 5. **Policy-Based Attacks**
```bash
# Get password policy:
enum4linux -P 192.168.1.100

# Use policy info to craft targeted attacks:
# If lockout threshold is 10, stop at 9 attempts per user
# If minimum length is 8, adjust wordlist filters
```

---

## Tips & Tricks for eJPT

### Quick Reference One-Liners

```bash
# Get just usernames:
enum4linux 192.168.1.100 | grep "Account:" | awk '{print $(NF-1)}'

# Get just shares:
enum4linux -S 192.168.1.100 | grep "\\\\" | grep -v "IPC\|ADMIN\|C\$"

# Find accessible shares:
smbclient -L 192.168.1.100 -N | grep "Disk\|Printer"

# Test null session:
smbclient -L 192.168.1.100 -N  # If this works, enum4linux will succeed

# Extract password policy:
enum4linux -P 192.168.1.100 | grep -i "policy"

# Combined with nmap for SMB network sweep:
nmap -p 445 --script smb-os-discovery 192.168.1.0/24

# Find all SMB hosts then enum all:
for ip in $(nmap -p 445 --open 192.168.1.0/24 -oG - | grep "Up" | awk '{print $2}'); do
  enum4linux -A $ip | grep -E "User|Share|Group"
done
```

### Common Enum4linux Findings & Exploitation

| Finding | Implication | Next Step |
|---------|-------------|-----------|
| Null session works | Can enumerate without auth | Full enumeration possible |
| Accessible admin$ | System misconfig | May be able to access files/executables |
| Many users found | Social engineering possible | Use users in credential attacks |
| Guest enabled | Weak security | Try guest account access |
| Old OS (XP, Server 2003) | Legacy vulnerabilities | Check for EternalBlue (MS17-010) |
| Share permissions weak | File access possible | Mount share and explore |

### Performance Tips

```bash
# Fast basic enumeration:
enum4linux -U -S -G 192.168.1.100

# Skip slow checks:
enum4linux -A -q 192.168.1.100  # Quiet mode (faster)

# Limit to specific checks:
enum4linux -U -G 192.168.1.100  # Only users and groups (fast)
```

---

## Combining Enum4linux with Other Tools

### Enum4linux → SMBclient
```bash
# Enum4linux finds accessible shares
enum4linux -S 192.168.1.100

# Then access with smbclient:
smbclient //192.168.1.100/accessible_share -N
smbclient //192.168.1.100/admin$ -u administrator -p password
```

### Enum4linux → Hydra
```bash
# Extract usernames:
enum4linux -U 192.168.1.100 | grep "Account:" | awk '{print $NF}' > users.txt

# Brute force with hydra:
hydra -L users.txt -P /usr/share/wordlists/rockyou.txt \
  smb://192.168.1.100 -t 4 -v
```

### Enum4linux → Smbmap
```bash
# Enum4linux finds users
# Smbmap shows share permissions with those users:

enum4linux -U 192.168.1.100  # Find users
smbmap -u user1 -p password -d DOMAIN -H 192.168.1.100  # Test permissions
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Check SMB service is running, port 139/445 open |
| "No users enumerated" | Try `-r` for RID cycling, system may restrict enumeration |
| "Authentication failed" | Wrong credentials or null session disabled |
| "Timeout" | Network latency, try without `-v` for faster output |
| "Perl errors" | Ensure Perl installed: `sudo pacman -S perl` |
| "Module not found" | Install: `sudo pacman -S perl-net-enum` |

---

## Official Documentation & Resources

- **GitHub Repository**: https://github.com/cddmp/enum4linux
- **SMB Protocol Info**: https://wiki.wireshark.org/SMB
- **Windows RID Documentation**: https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-relative-id--rid--allocation
- **Samba Documentation**: https://www.samba.org/

---

## Key Takeaways for eJPT

1. **Basic enum**: `enum4linux 192.168.1.100`
2. **Get users**: `enum4linux -U 192.168.1.100`
3. **Get shares**: `enum4linux -S 192.168.1.100`
4. **Try harder**: Use `-r` for RID cycling
5. **Use credentials**: If available: `-u user -p pass`
6. **Combine with nmap**: Find SMB first, then enum
7. **Extract users**: Use for hydra/credential attacks
8. **Check null session**: `smbclient -L target -N`

---

**Next Steps**: Use extracted usernames for credential attacks with hydra, and accessible shares for file exfiltration or malware placement.

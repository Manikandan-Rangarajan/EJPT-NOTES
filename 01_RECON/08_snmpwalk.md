# SNMPWALK - SNMP Enumeration

## Overview

**SNMPWALK** is a command-line tool for querying SNMP (Simple Network Management Protocol) enabled devices. It's used to gather information about networked devices like routers, switches, printers, and servers. SNMP often reveals critical system information.

### Why It's Critical for eJPT:
- Many devices expose SNMP (routers, printers, servers)
- Often uses weak default credentials (public/private)
- Reveals system information, running processes, installed software
- Can be exploited for information gathering
- Often overlooked but extremely informative

---

## Installation & Setup

### CachyOS (Arch Linux)
```bash
sudo pacman -S net-snmp
snmpwalk -V  # Verify installation
which snmpwalk snmpclient snmpgetnext
```

### Alternative Installation
```bash
# If not in repos:
sudo pacman -S net-snmp net-snmp-utils
```

### Windows
- Download from: https://www.net-snmp.org/download.html
- Or use WSL with net-snmp

### Verify Installation
```bash
snmpwalk -h
snmpget -h
snmpbulkwalk -h
```

---

## Core SNMP Concepts

### SNMP Versions
- **SNMPv1**: Basic, no encryption (default, most common in eJPT)
- **SNMPv2c**: Improved, still no encryption
- **SNMPv3**: Encrypted, secure

### Community Strings (Credentials)
Default community strings (often not changed):
- **public**: Read-only access (default)
- **private**: Read-write access (sometimes set)
- **guest**: Guest access

### MIB (Management Information Base)
- **OID (Object Identifier)**: Address to data on device
- **Common OID**: 1.3.6.1.2.1.1
- **System info**: 1.3.6.1.2.1.1 (sysDescr, sysUptime, etc.)
- **Interfaces**: 1.3.6.1.2.1.2 (network interfaces)
- **Processes**: 1.3.6.1.2.1.25.4 (running processes)
- **Files**: 1.3.6.1.2.1.25.3.4.1 (mounted disks)

### Common Information Accessible
- System description and version
- Hostname
- Uptime
- Running processes
- Disk usage
- Network interfaces and traffic
- Installed software
- Routing tables

---

## Common Use Cases for eJPT

### 1. **Basic SNMP Enumeration**
Attempt to enumerate a device using default community string.

```bash
snmpwalk -v 2c -c public 192.168.1.1
```

**Output:**
```
SNMPv2-MIB::sysDescr.0 = STRING: "Cisco IOS Software, C3750 Software, Version 12.2(58)SE2"
SNMPv2-MIB::sysObjectID.0 = OID: SNMPv2-SMI::enterprises.9.9.46.1
SNMPv2-MIB::sysUpTimeInstance.0 = Timeticks: (595968000) 68 days, 22:41:08.00
SNMPv2-MIB::sysContact.0 = STRING: "admin@company.com"
SNMPv2-MIB::sysName.0 = STRING: "router1"
SNMPv2-MIB::sysLocation.0 = STRING: "Building A"
SNMPv2-MIB::sysServices.0 = INTEGER: 72
SNMPv2-MIB::sysORLastChange.0 = Timeticks: (1) 0:00:00.01
```

**Flags:**
- `-v 2c`: SNMP version 2c (most common)
- `-c public`: Community string (default)

### 2. **Try Different Community Strings**
```bash
# Try common strings:
snmpwalk -v 2c -c public 192.168.1.1
snmpwalk -v 2c -c private 192.168.1.1
snmpwalk -v 2c -c guest 192.168.1.1
snmpwalk -v 2c -c "" 192.168.1.1  # Empty string
```

### 3. **Get Specific System Information**
Query specific OID sections for targeted data.

```bash
# System description and version:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.1.1

# Hostname:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.1.5

# Uptime:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.1.3

# System contact:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.1.4

# System location:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.1.6
```

### 4. **Enumerate Network Interfaces**
```bash
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.2
```

**Output shows:**
- Interface names
- Network interface statistics
- Traffic data

### 5. **List Running Processes**
```bash
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.25.4.2
```

**Output shows:**
- Running process names
- Process PIDs
- Memory usage

### 6. **Check Disk Usage**
```bash
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.25.2
```

**Output shows:**
- Storage/disk names
- Total disk size
- Used disk space
- Available space

### 7. **Get File/Directory Information**
```bash
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.25.3.4.1
```

### 8. **List Installed Software**
```bash
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.25.6.3
```

**Output shows:**
- Installed applications
- Application versions

### 9. **SNMPv1 Enumeration**
```bash
snmpwalk -v 1 -c public 192.168.1.1
```

**Flag:**
- `-v 1`: Use SNMPv1 (older devices)

### 10. **Walk Entire MIB Tree**
Get everything the device will show (might be slow).

```bash
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1
```

### 11. **Specific Value Query (Single OID)**
```bash
snmpget -v 2c -c public 192.168.1.1 1.3.6.1.2.1.1.1.0
```

**Flag:**
- `snmpget`: Get specific value instead of walking tree

### 12. **Bulk Walk (Faster)**
```bash
snmpbulkwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1
```

### 13. **Set SNMP Value (Read-Write)**
If community string has write access:

```bash
snmpset -v 2c -c private 192.168.1.1 1.3.6.1.2.1.1.4.0 s "new value"
```

**Flag:**
- `snmpset`: Set a value
- `s`: String type

---

## Command Reference - Essential Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-v` | SNMP version | `-v 2c` or `-v 1` |
| `-c` | Community string | `-c public` |
| `1.3.6.1...` | OID to query | System info, processes, etc. |
| `-Cc` | Character output | Better formatting |
| `-Ln` | Show only values | Clean output |
| `-On` | Numeric OID output | More detailed |

---

## Practical eJPT Workflows

### Complete SNMP Enumeration Workflow

```bash
# Step 1: Check if SNMP is open:
nmap -p 161 -u 192.168.1.0/24 -sU

# Step 2: Try to enumerate each device:
for host in 192.168.1.{1,5,10,15}; do
  echo "[*] Checking $host"
  
  # Try different community strings:
  for community in public private guest ""; do
    result=$(snmpwalk -v 2c -c "$community" $host 1.3.6.1.2.1.1.1.0 2>&1)
    if [[ $result != *"Timeout"* ]] && [[ ! -z $result ]]; then
      echo "[+] SUCCESS: $community"
      snmpwalk -v 2c -c "$community" $host 1.3.6.1.2.1.1 > snmp_$host.txt
      break
    fi
  done
done

# Step 3: Analyze results:
cat snmp_*.txt
```

---

## Real-World eJPT Examples

### Example 1: Cisco Router Enumeration
```bash
snmpwalk -v 2c -c public 192.168.1.1

# Typical output:
# Cisco IOS Software, Version 12.2(58)SE2
# Hostname: router1
# Uptime: 68 days, 22:41:08
# Location: Building A, Floor 3
# Contact: admin@company.com
```

### Example 2: Find and Identify All SNMP Devices
```bash
#!/bin/bash
# snmp_scan.sh

for host in 192.168.1.{1..254}; do
  (
    result=$(snmpget -v 2c -c public -O qv $host 1.3.6.1.2.1.1.1.0 2>&1)
    if [[ $result != *"Timeout"* ]] && [[ ! -z $result ]]; then
      echo "$host: $result"
    fi
  ) &
done
wait
```

### Example 3: Extract Sensitive Information
```bash
SNMP_HOST="192.168.1.1"

echo "=== SNMP Enumeration Results ==="
echo ""
echo "System Description:"
snmpget -v 2c -c public -Oqv $SNMP_HOST 1.3.6.1.2.1.1.1.0

echo -e "\nHostname:"
snmpget -v 2c -c public -Oqv $SNMP_HOST 1.3.6.1.2.1.1.5.0

echo -e "\nContact:"
snmpget -v 2c -c public -Oqv $SNMP_HOST 1.3.6.1.2.1.1.4.0

echo -e "\nLocation:"
snmpget -v 2c -c public -Oqv $SNMP_HOST 1.3.6.1.2.1.1.6.0

echo -e "\nUptime:"
snmpget -v 2c -c public -Oqv $SNMP_HOST 1.3.6.1.2.1.1.3.0

echo -e "\nRunning Processes:"
snmpwalk -v 2c -c public -Oqv $SNMP_HOST 1.3.6.1.2.1.25.4.2 | head -20

echo -e "\nDisk Usage:"
snmpwalk -v 2c -c public -Oqv $SNMP_HOST 1.3.6.1.2.1.25.2.3.1.3
```

### Example 4: SNMP Community String Brute Force
```bash
#!/bin/bash
# snmp_brute.sh

HOST=$1
WORDLIST=$2

echo "[*] SNMP Community String Brute Force on $HOST"

cat $WORDLIST | while read community; do
  result=$(snmpget -v 2c -c "$community" -O qv $HOST 1.3.6.1.2.1.1.1.0 2>&1)
  
  if [[ $result != *"Timeout"* ]] && [[ ! -z $result ]]; then
    echo "[+] Found: $community"
    echo "    Response: $result"
  fi
done

# Run:
# ./snmp_brute.sh 192.168.1.1 /usr/share/wordlists/snmp.txt
```

---

## Advanced Techniques

### 1. **SNMP Version Detection**
```bash
# Try SNMPv1:
snmpwalk -v 1 -c public 192.168.1.1 1.3.6.1.2.1.1.1

# Try SNMPv2c:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.1.1

# Try SNMPv3 (encrypted):
snmpwalk -v 3 -u username -A password 192.168.1.1
```

### 2. **Extract Routing Table**
```bash
# Learn network topology:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.4.21.1
# Shows all routes known by device
```

### 3. **ARP Table Enumeration**
```bash
# Discover all devices on network:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.3.1.1.2
# Shows MAC -> IP mappings
```

### 4. **Installed Software Discovery**
```bash
# Find what software is running:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.25.6.3.1.2
# Useful for searching CVEs
```

---

## Tips & Tricks for eJPT

### Quick Reference One-Liners

```bash
# Test if SNMP responds:
snmpget -v 2c -c public -O qv 192.168.1.1 1.3.6.1.2.1.1.1.0

# Get system description:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.1.1

# Get hostname:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.1.5

# List processes:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.25.4.2

# Check disk space:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1.2.1.25.2

# Test multiple hosts:
for host in 192.168.1.{1,2,5,10}; do
  echo "=== $host ==="
  snmpget -v 2c -c public -O qv $host 1.3.6.1.2.1.1.5.0
done

# Full walk to file:
snmpwalk -v 2c -c public 192.168.1.1 1.3.6.1 > snmp_dump.txt
```

### Default Community Strings to Try
```bash
public        # Most common, read-only
private       # Sometimes set, read-write
guest         # Sometimes set
comunidad     # Spanish
manager       # Sometimes set
snmp          # Sometimes set
""            # Empty string
1234          # Weak password
12345         # Weak password
```

### Common Findings

| Data | Importance | Action |
|------|-----------|--------|
| OS Version | HIGH | Search for CVE |
| Running Processes | MEDIUM | Identify services |
| Hostname | MEDIUM | Target identification |
| Disk Space | LOW | Environment info |
| Network Interfaces | MEDIUM | Network mapping |
| Installed Software | HIGH | Vulnerability assessment |
| Contact Info | LOW | Social engineering |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Timeout" | SNMP service not running or port 161 filtered |
| "NoSuchObject" | OID doesn't exist on this device |
| "Access Denied" | Wrong community string or version mismatch |
| "Unknown Object Identifier" | OID syntax error |
| "Command not found" | Install net-snmp: `sudo pacman -S net-snmp` |

---

## Official Documentation & Resources

- **Net-SNMP Manual**: `man snmpwalk`
- **Net-SNMP Homepage**: https://www.net-snmp.org/
- **SNMP MIB Reference**: https://oidref.com/
- **Common OIDs**: https://www.cisco.com/en/US/tech/tk648/tk362/technologies_tech_note09186a00800945e9.shtml

---

## Key Takeaways for eJPT

1. **Basic enum**: `snmpwalk -v 2c -c public target`
2. **Try multiple community strings**: public, private, guest
3. **Get system info**: OID 1.3.6.1.2.1.1
4. **List processes**: OID 1.3.6.1.2.1.25.4
5. **Check disk**: OID 1.3.6.1.2.1.25.2
6. **Extract hostname**: OID 1.3.6.1.2.1.1.5
7. **Find on network**: nmap port 161 UDP
8. **Use snmpget for single value**: Faster than walk

---

**Next Steps**: Use SNMP information to identify software versions for CVE research, or discovered processes to find exploitation paths.

# DNS ENUMERATION - DIG & NSLOOKUP

## Overview

**Dig** (Domain Information Groper) and **nslookup** are command-line tools for querying DNS servers. They're essential for domain reconnaissance, uncovering subdomains, understanding DNS infrastructure, and finding MX records, NS records, and other DNS information.

### Why It's Critical for eJPT:
- Find subdomains of target domain
- Identify DNS infrastructure
- Discover mail servers (MX records)
- Find DNS servers (NS records)
- DNS zone transfer attempts (can leak entire DNS info)
- Identify IP ranges from DNS records

### Dig vs Nslookup

| Feature | Dig | Nslookup |
|---------|-----|----------|
| Development | Modern (developed by ISC) | Legacy (older) |
| Output | Verbose, detailed | Simple, concise |
| Features | More options, scripting | Basic queries |
| Availability | Most Linux systems | Windows & Linux |
| Preferred for eJPT | Yes | Yes (especially Windows) |

---

## Installation & Setup

### CachyOS (Arch Linux)
```bash
sudo pacman -S bind-tools  # Includes dig, nslookup, host
dig -v  # Verify installation
which dig nslookup
```

### Windows
- Built into Windows (nslookup)
- Or download: https://www.isc.org/bind/

### Verify Installation
```bash
dig --version
nslookup
```

---

## Core DNS Concepts

### DNS Record Types

| Record | Purpose | Example |
|--------|---------|---------|
| **A** | IPv4 address | example.com → 93.184.216.34 |
| **AAAA** | IPv6 address | example.com → 2606:2800:220:1:248:1893:25c8:1946 |
| **CNAME** | Alias | www.example.com → example.com |
| **MX** | Mail server | mail.example.com (priority 10) |
| **NS** | Name server | ns1.example.com |
| **TXT** | Text records | Verification, SPF, DKIM |
| **SOA** | Start of Authority | Admin info, serial number |
| **SRV** | Service records | _ldap._tcp.example.com |
| **PTR** | Reverse DNS | IP → domain name |

### DNS Query Types

- **Standard Query (@)**: Regular DNS lookup
- **ANY Query**: Get all records (often blocked now)
- **Zone Transfer (axfr)**: Get entire DNS zone
- **Reverse Query (ptr)**: Find domain from IP

---

## Common Use Cases for eJPT

### DIG Commands

### 1. **Basic Domain Lookup**
Get A record (IP address) for a domain.

```bash
dig example.com
```

**Output:**
```
; <<>> DiG 9.16.1-Ubuntu <<>> example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345

;; QUESTION SECTION:
;example.com.			IN	A

;; ANSWER SECTION:
example.com.		3599	IN	A	93.184.216.34

;; Query time: 50 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
```

**Key Info:**
- `A 93.184.216.34`: IPv4 address
- Query time: DNS response time
- SERVER: Which DNS server answered

### 2. **Query Specific Record Type**
```bash
# Get A records (IPv4):
dig example.com A

# Get AAAA records (IPv6):
dig example.com AAAA

# Get MX records (Mail servers):
dig example.com MX

# Get NS records (Nameservers):
dig example.com NS

# Get TXT records (Text info):
dig example.com TXT

# Get SOA record (DNS zone info):
dig example.com SOA

# Get ALL records:
dig example.com ANY
```

### 3. **Short Output Format**
```bash
# Simple answer only (useful for scripts):
dig example.com +short

# Output:
# 93.184.216.34

# Or for mail servers:
dig example.com MX +short

# Output:
# 10 mail.example.com.
```

### 4. **Specify DNS Server**
Query a specific DNS server.

```bash
# Query Google's DNS:
dig @8.8.8.8 example.com

# Query target's nameserver:
dig @ns1.example.com example.com

# Query corporate DNS:
dig @192.168.1.1 internal.local
```

**Flag:**
- `@server`: Use specific DNS server

### 5. **Reverse DNS Lookup**
Find domain name from IP address.

```bash
dig -x 93.184.216.34
dig -x 192.168.1.100
```

**Flag:**
- `-x`: Reverse DNS lookup

### 6. **DNS Zone Transfer**
Attempt to get entire DNS zone (often blocked but worth trying).

```bash
# Try zone transfer (AXFR):
dig @ns1.example.com example.com AXFR

# Output might show all subdomains:
# example.com         3600  IN SOA
# www.example.com     3600  IN A
# mail.example.com    3600  IN A
# admin.example.com   3600  IN A
# ...
```

**Flag:**
- `AXFR`: Zone transfer query

### 7. **Trace DNS Resolution**
Follow complete DNS resolution path.

```bash
dig +trace example.com
```

**Output shows:**
1. Root nameservers
2. TLD nameservers
3. Authoritative nameservers
4. Final answer

### 8. **Find All Subdomains (via MX, TXT, etc.)**
```bash
# Get mail servers (may list subdomains):
dig example.com MX

# Get text records (may contain subdomains):
dig example.com TXT

# Get service records:
dig _service._proto.example.com SRV
```

### 9. **Verbose Output**
```bash
dig example.com +comments
dig example.com +stats
dig example.com +noall +answer  # Just the answer section
```

### 10. **Bulk DNS Queries**
Query multiple domains.

```bash
# Query file of domains:
dig -f domains.txt

# File format (domains.txt):
# example1.com
# example2.com
# example3.com
```

---

### NSLOOKUP Commands

### 1. **Basic Lookup**
```bash
nslookup example.com
```

**Output:**
```
Server:         8.8.8.8
Address:        8.8.8.8#53

Non-authoritative answer:
Name:   example.com
Address: 93.184.216.34
```

### 2. **Query Specific Record**
```bash
# A record:
nslookup example.com

# Mail servers:
nslookup -query=MX example.com
# or
nslookup -type=MX example.com

# Nameservers:
nslookup -query=NS example.com

# Text records:
nslookup -query=TXT example.com
```

### 3. **Use Specific DNS Server**
```bash
nslookup example.com 8.8.8.8
nslookup example.com 1.1.1.1
```

### 4. **Reverse DNS**
```bash
nslookup 93.184.216.34
```

### 5. **Interactive Mode**
```bash
# Enter nslookup prompt:
nslookup

# Then type queries:
> example.com
> set type=MX
> example.com
> set server 8.8.8.8
> another.com
> exit
```

---

## Command Reference - Dig Essential Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `@server` | DNS server | `dig @8.8.8.8 example.com` |
| `-x` | Reverse lookup | `dig -x 192.168.1.100` |
| `+short` | Short output | Show just answers |
| `+trace` | Trace path | Follow resolution chain |
| `AXFR` | Zone transfer | `dig @ns1 example.com AXFR` |
| `ANY` | All records | `dig example.com ANY` |
| `MX` | Mail servers | `dig example.com MX` |
| `NS` | Nameservers | `dig example.com NS` |
| `TXT` | Text records | `dig example.com TXT` |
| `+noall +answer` | Only answer | Clean output |
| `-f` | File input | `dig -f domains.txt` |

---

## Practical eJPT Workflows

### Domain Reconnaissance Workflow

```bash
# Step 1: Get basic domain info:
dig example.com +short
dig example.com NS +short
dig example.com MX +short

# Step 2: Query nameserver directly:
NAMESERVER=$(dig example.com NS +short | head -1)
dig @$NAMESERVER example.com

# Step 3: Try zone transfer:
dig @$NAMESERVER example.com AXFR

# Step 4: Reverse lookup on discovered IPs:
for ip in $(dig example.com +short); do
  dig -x $ip +short
done

# Step 5: Find subdomains from various records:
dig example.com MX | grep "mail"
dig example.com TXT | grep "@"
```

### Subdomain Discovery

```bash
# Find mail-related subdomains:
dig example.com MX +short | awk '{print $NF}' | tr -d '.'

# Find all referenced domains in TXT:
dig example.com TXT +short | grep -o '[a-zA-Z0-9-]*\.example\.com'

# Query common subdomains:
for subdomain in www mail ftp admin api staging dev; do
  echo "=== $subdomain.example.com ==="
  dig $subdomain.example.com +short
done
```

---

## Real-World eJPT Examples

### Example 1: Complete Domain Information Gathering
```bash
#!/bin/bash
# domain_recon.sh - Complete DNS enumeration

DOMAIN=$1

echo "[*] Enumerating $DOMAIN"
echo ""

echo "=== A Records ==="
dig $DOMAIN A +short

echo -e "\n=== AAAA Records (IPv6) ==="
dig $DOMAIN AAAA +short

echo -e "\n=== MX Records (Mail) ==="
dig $DOMAIN MX +short

echo -e "\n=== NS Records (Nameservers) ==="
dig $DOMAIN NS +short

echo -e "\n=== TXT Records ==="
dig $DOMAIN TXT +short

echo -e "\n=== SOA Record ==="
dig $DOMAIN SOA +short

echo -e "\n=== Attempting Zone Transfer ==="
for ns in $(dig $DOMAIN NS +short); do
  echo "Trying zone transfer on $ns:"
  dig @$ns $DOMAIN AXFR +short
done

# Run:
# ./domain_recon.sh example.com
```

### Example 2: Subdomain Enumeration via DNS
```bash
#!/bin/bash
# subdomain_enum.sh

DOMAIN=$1
WORDLIST=$2

echo "[*] Enumerating subdomains for $DOMAIN"

# Simple wordlist method (doesn't always work, but try):
cat $WORDLIST | while read subdomain; do
  result=$(dig $subdomain.$DOMAIN +short 2>/dev/null)
  if [ ! -z "$result" ]; then
    echo "$subdomain.$DOMAIN: $result"
  fi
done

# Better method: Use DNS records for hints
echo -e "\n[*] Finding subdomains from DNS records:"
dig $DOMAIN MX +short | awk '{print $NF}' | sed 's/\.$//'
dig $DOMAIN NS +short

# Run:
# ./subdomain_enum.sh example.com wordlist.txt
```

### Example 3: Finding Mail Servers
```bash
DOMAIN="example.com"

echo "Mail servers for $DOMAIN:"
dig $DOMAIN MX +short | sort -n | awk '{print $NF}'

# Try reverse DNS on mail server IP:
MAIL_IP=$(dig mail.example.com +short)
echo "Mail server IP: $MAIL_IP"
dig -x $MAIL_IP +short
```

### Example 4: Zone Transfer Attempt
```bash
DOMAIN="example.com"

# Get nameserver:
NS=$(dig $DOMAIN NS +short | head -1)

# Try zone transfer:
echo "[*] Attempting zone transfer on $NS for $DOMAIN"
dig @$NS $DOMAIN AXFR

# If successful, all subdomains/records revealed!
# If failed, shows "Transfer failed" or similar
```

---

## Advanced Techniques

### 1. **DNS Brute Force Subdomains**
```bash
# Using common subdomains:
for subdomain in www mail ftp admin api staging dev test prod; do
  dig $subdomain.example.com +short 2>/dev/null && echo "$subdomain.example.com: FOUND"
done

# Using wordlist (with timeout):
cat subdomains.txt | while read sub; do
  timeout 0.5 dig $sub.example.com +short 2>/dev/null && echo "$sub.example.com found"
done
```

### 2. **DNS Cache Snooping**
```bash
# Query for popular sites to check cache:
dig @target.com google.com
# If cached, faster response; if not cached, may reveal info
```

### 3. **DNS Amplification Testing**
```bash
# Test DNS server for amplification (security check):
dig @target.com . ANY +stats

# Response larger than query = amplification possible
```

### 4. **DNSSEC Validation**
```bash
# Check DNSSEC status:
dig example.com +dnssec

# If shows "ad" flag, DNSSEC is validated
```

---

## Tips & Tricks for eJPT

### Quick Reference One-Liners

```bash
# Get just the IP:
dig example.com +short

# Get mail servers:
dig example.com MX +short

# Get nameservers:
dig example.com NS +short

# Reverse DNS on IP:
dig -x 192.168.1.100 +short

# Find all subdomains via MX:
dig example.com MX +short | awk '{print $NF}' | tr -d '.'

# Try zone transfer:
dig @ns1.example.com example.com AXFR +short

# Trace DNS path:
dig example.com +trace +short

# Query multiple domains:
for domain in site1.com site2.com site3.com; do
  echo "$domain: $(dig $domain +short)"
done

# Get all DNS records (if allowed):
dig example.com ANY +short

# Check multiple DNS servers:
for dns in 8.8.8.8 1.1.1.1 208.67.222.222; do
  echo "=== DNS Server $dns ==="
  dig @$dns example.com +short
done
```

### Common Findings

| Finding | Value |
|---------|-------|
| MX Records | Mail servers (attack target) |
| NS Records | DNS servers (attack target) |
| TXT Records | SPF, DKIM, DMARC policies |
| CNAME | Alias hosts (more targets) |
| A/AAAA | IP addresses (reconnaissance) |
| SOA | DNS admin contact info |
| Zone Transfer Success | Complete DNS data leaked |

---

## Combining DNS Enumeration with Other Tools

### Dig → Nmap
```bash
# Get DNS records, then scan those IPs:
dig example.com MX +short | awk '{print $NF}' | while read mailserver; do
  ip=$(dig $mailserver +short)
  nmap -p 25,110,143 $ip
done
```

### Dig → Gobuster
```bash
# Find subdomains from DNS, then enumerate web:
dig example.com NS +short
dig @ns1.example.com example.com AXFR | grep -o '[a-zA-Z0-9-]*\.example\.com' | while read subdomain; do
  gobuster dir -u http://$subdomain -w common.txt
done
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Query refused" | DNS server blocking queries |
| "NXDOMAIN" | Domain doesn't exist |
| "SERVFAIL" | DNS server error |
| "Zone transfer failed" | Server blocks zone transfers (secure) |
| "Timeout" | DNS server not responding |
| "no nameservers found" | Misconfigured DNS or network issue |

---

## Official Documentation & Resources

- **Dig Manual**: `man dig`
- **Nslookup Manual**: `man nslookup`
- **BIND Documentation**: https://www.isc.org/bind/
- **DNS Record Types**: https://en.wikipedia.org/wiki/List_of_DNS_record_types

---

## Key Takeaways for eJPT

1. **Basic lookup**: `dig example.com`
2. **Get mail servers**: `dig example.com MX +short`
3. **Get nameservers**: `dig example.com NS +short`
4. **Reverse DNS**: `dig -x 192.168.1.100`
5. **Try zone transfer**: `dig @ns1 example.com AXFR`
6. **Query specific server**: `dig @8.8.8.8 example.com`
7. **Short output**: Add `+short` for clean results
8. **Use nslookup on Windows**: Alternative if dig unavailable

---

**Next Steps**: Use discovered IPs and subdomains for nmap scanning and further reconnaissance.

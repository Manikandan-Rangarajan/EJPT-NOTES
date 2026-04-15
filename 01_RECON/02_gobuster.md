# GOBUSTER - Directory & DNS Brute Force

## Overview

**Gobuster** is a fast, powerful tool for brute-forcing URIs, DNS subdomains, virtual hostnames, and S3 buckets. It's essential for web reconnaissance and discovering hidden directories and files on web servers during penetration tests.

### Why It's Critical for eJPT:
- Uncovers hidden web directories and files
- Finds sensitive paths (admin panels, backups, config files)
- DNS mode discovers subdomains that may be overlooked
- Much faster than older tools like dirb
- Effective against web applications with directory indexing disabled

---

## Installation & Setup

### CachyOS (Arch Linux)
```bash
sudo pacman -S gobuster
gobuster --version  # Verify installation
```

### Install from Source
```bash
git clone https://github.com/OJ/gobuster.git
cd gobuster
go build -o gobuster
sudo mv gobuster /usr/local/bin/
```

### Windows
- Download from: https://github.com/OJ/gobuster/releases
- Extract .exe file
- Run from command line or PowerShell

### Installing Wordlists (Critical!)

**CachyOS/Arch Linux:**
```bash
# Install SecLists (comprehensive wordlist collection)
sudo pacman -S seclists

# WordLists location:
/usr/share/seclists/
```

**Common wordlist paths:**
```bash
# On Kali/Arch:
/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
/usr/share/seclists/Discovery/Web-Content/

# Alternative download:
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt
```

---

## Core Concepts

### Three Main Modes

1. **dir**: Directory/file brute force on web servers
2. **dns**: DNS subdomain enumeration
3. **vhost**: Virtual host discovery
4. **s3**: AWS S3 bucket enumeration

### How It Works

- Gobuster takes a wordlist of potential directories/subdomains
- Sends HTTP requests (or DNS queries) for each word
- Reports successful hits based on HTTP status codes or DNS resolution
- Uses threading for speed (default: 10 threads)

### Status Codes (What matters for dir mode)
- **200**: Found and accessible
- **301/302**: Redirect (still useful)
- **403**: Forbidden (directory exists but not accessible)
- **404**: Not found (skip, unless you care about 404s)
- **401**: Authentication required (found but needs credentials)

---

## Installation Verification & First Run

```bash
# Check installation:
which gobuster
gobuster help

# View available modes:
gobuster --help
# Output shows: dir, dns, vhost, s3 modes
```

---

## Common Use Cases for eJPT

### 1. **Basic Directory Brute Force**
Find common directories on a web server.

```bash
gobuster dir -u http://192.168.1.50 -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

**What each flag does:**
- `dir`: Directory brute force mode
- `-u`: Target URL
- `-w`: Wordlist file path

**Output:**
```
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://192.168.1.50
[+] Threads:        10
[+] Wordlist:       /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2021/11/15 10:30:45 Found: /admin (Status: 200)
2021/11/15 10:30:46 Found: /backup (Status: 301)
2021/11/15 10:30:47 Found: /login (Status: 200)
2021/11/15 10:30:48 Found: /uploads (Status: 403)
```

### 2. **Faster Scan with Better Wordlist**
Use a larger, more comprehensive wordlist with increased threads.

```bash
gobuster dir -u http://192.168.1.50 \
  -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
  -t 50 \
  -v
```

**Flags:**
- `-t 50`: 50 concurrent threads (faster but more network traffic)
- `-v`: Verbose (shows all attempts, not just hits)

### 3. **Look for Specific File Extensions**
Often files like .php, .txt, .config are gold.

```bash
gobuster dir -u http://192.168.1.50 \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -x php,txt,html,config,bak
```

**Flags:**
- `-x`: File extensions to append to wordlist entries

**Example output:**
```
Found: /config.php (Status: 200)
Found: /backup.txt (Status: 200)
Found: /admin.html (Status: 200)
Found: /database.config (Status: 200)
```

### 4. **DNS Subdomain Enumeration**
Find subdomains of a target domain.

```bash
gobuster dns -d example.com \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

**Flags:**
- `dns`: Switch to DNS mode
- `-d`: Domain to enumerate

**Output:**
```
Found: admin.example.com
Found: api.example.com
Found: blog.example.com
Found: dev.example.com
Found: mail.example.com
Found: staging.example.com
```

### 5. **Custom Status Code Filtering**
Only report specific status codes you care about.

```bash
gobuster dir -u http://192.168.1.50 \
  -w common.txt \
  -s 200,403,401 \
  --no-error
```

**Flags:**
- `-s`: Status codes to treat as success (default: 200,204,301,302,307,401,403)
- `--no-error`: Don't print errors

### 6. **Virtual Host Discovery**
Find different websites hosted on the same IP.

```bash
gobuster vhost -u http://192.168.1.50 \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

### 7. **Add Custom Headers**
Some servers need specific headers (User-Agent, etc.).

```bash
gobuster dir -u http://192.168.1.50 \
  -w common.txt \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
```

### 8. **Follow Redirects**
Automatically follow 301/302 redirects.

```bash
gobuster dir -u http://192.168.1.50 \
  -w common.txt \
  -L
```

**Flag:**
- `-L`: Follow redirects

### 9. **Ignore Certificate Issues (HTTPS)**
For self-signed or invalid SSL certificates.

```bash
gobuster dir -u https://192.168.1.50 \
  -w common.txt \
  -k
```

**Flag:**
- `-k`: Skip SSL certificate verification

### 10. **Save Results to File**
Export findings for documentation.

```bash
gobuster dir -u http://192.168.1.50 \
  -w common.txt \
  -o results.txt
```

---

## Command Reference - Essential Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-u` | Target URL | `-u http://example.com` |
| `-w` | Wordlist | `-w common.txt` |
| `-t` | Thread count | `-t 50` (default: 10) |
| `-x` | File extensions | `-x php,txt,html` |
| `-s` | Status codes | `-s 200,403` |
| `-o` | Output file | `-o results.txt` |
| `-H` | Custom header | `-H "User-Agent: Chrome"` |
| `-v` | Verbose | Show all attempts |
| `-k` | Skip SSL verify | For HTTPS with bad certs |
| `-L` | Follow redirects | Follow 301/302/307 |
| `-d` | Domain (DNS mode) | `-d example.com` |
| `--no-error` | Suppress errors | Don't show error messages |
| `-a` | User-Agent | `-a "custom agent"` |
| `-p` | Proxy | `-p http://proxy:8080` |

---

## Practical eJPT Workflow

### Web Reconnaissance Workflow

```bash
# Step 1: Basic scan with common paths
gobuster dir -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -t 30 -o initial_results.txt

# Step 2: If successful, try PHP files
gobuster dir -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt \
  -x php \
  -t 30 -o php_results.txt

# Step 3: Look for admin/backup paths
gobuster dir -u http://target.com \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -x php,bak,backup,old,zip,tar \
  -t 30 -o sensitive_results.txt

# Step 4: Check DNS subdomains (if domain name is available)
gobuster dns -d target.com \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  -o subdomains.txt
```

---

## Real-World eJPT Examples

### Example 1: Wordpress Admin Discovery
```bash
# Look for wp-admin and other Wordpress paths:
gobuster dir -u http://192.168.1.50 \
  -w /usr/share/seclists/Discovery/Web-Content/wordpress.txt \
  -t 50 -v

# Output might show:
# Found: /wp-admin/ (Status: 302)
# Found: /wp-login.php (Status: 200)
# Found: /wp-content/ (Status: 200)
# Found: /wp-includes/ (Status: 200)
```

### Example 2: API Endpoint Discovery
```bash
# Find API endpoints:
gobuster dir -u http://192.168.1.50 \
  -w /usr/share/seclists/Discovery/Web-Content/api/ \
  -t 50 -o api_endpoints.txt

# Then test with tools like curl or Burp Suite
```

### Example 3: Backup & Config File Hunting
```bash
# Search for sensitive files:
gobuster dir -u http://192.168.1.50 \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -x php,bak,backup,config,old,txt,sql,zip,tar,gz,7z \
  -t 50 -s 200 -o sensitive_files.txt

# Then download interesting files:
# curl http://192.168.1.50/config.php
# curl http://192.168.1.50/backup.sql
# curl http://192.168.1.50/database.bak
```

### Example 4: Multi-step Enumeration
```bash
#!/bin/bash
# Comprehensive web enumeration script

TARGET="http://192.168.1.50"
WORDLIST="/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt"

echo "[*] Starting comprehensive enumeration of $TARGET"

# Basic directory scan
echo "[+] Step 1: Basic directory scan"
gobuster dir -u $TARGET -w $WORDLIST -t 50 -o results_basic.txt

# PHP files
echo "[+] Step 2: PHP file scan"
gobuster dir -u $TARGET -w $WORDLIST -x php -t 50 -o results_php.txt

# Backup files
echo "[+] Step 3: Backup file scan"
gobuster dir -u $TARGET -w $WORDLIST -x bak,backup,old,zip -t 50 -o results_backup.txt

# Results summary
echo "[+] Results saved"
echo "Basic: $(wc -l < results_basic.txt) findings"
echo "PHP: $(wc -l < results_php.txt) findings"
echo "Backup: $(wc -l < results_backup.txt) findings"
```

---

## Advanced Techniques

### 1. **Pattern-Based Wordlist Generation**
Create custom wordlists for specific scenarios.

```bash
# Generate numbers for common patterns:
gobuster dir -u http://target.com \
  -w <(seq 1 1000 | sed 's/^/page-/')  # Generate page-1, page-2, etc.

# Generate dates:
gobuster dir -u http://target.com \
  -w <(for year in 2020 2021 2022; do for month in 01 02 03; do echo "$year-$month"; done; done)
```

### 2. **Combining Multiple Wordlists**
```bash
# Merge multiple wordlists:
cat wordlist1.txt wordlist2.txt wordlist3.txt | sort -u > merged.txt
gobuster dir -u http://target.com -w merged.txt
```

### 3. **Recursive Directory Brute Force**
```bash
# Find subdirectories in discovered directories:
gobuster dir -u http://target.com/admin \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt

# Then scan deeper:
gobuster dir -u http://target.com/admin/users \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

### 4. **Timing Evasion**
```bash
# Slower scan to evade WAF/IDS:
gobuster dir -u http://target.com \
  -w common.txt \
  -t 5 \
  --delay 100ms  # Add delay between requests
```

### 5. **Using Gobuster with Other Tools**
```bash
# Get nmap-discovered HTTP servers and scan them:
for ip in $(nmap -p 80 --open 192.168.1.0/24 -oG - | grep "80/open" | awk '{print $2}'); do
  gobuster dir -u http://$ip -w common.txt -o results_$ip.txt &
done
wait  # Wait for all background jobs to complete
```

---

## Tips & Tricks for eJPT

### Performance Optimization
```bash
# Maximum speed (but may be detected):
gobuster dir -u http://target.com -w wordlist.txt -t 200

# Balanced (fast but not too aggressive):
gobuster dir -u http://target.com -w wordlist.txt -t 50

# Stealthy (slow, less likely to trigger IDS):
gobuster dir -u http://target.com -w wordlist.txt -t 5 --delay 500ms
```

### Effective Wordlist Selection
```bash
# For quick scan:
/usr/share/seclists/Discovery/Web-Content/common.txt (4,607 entries)

# For thorough scan:
/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt (220,546 entries)

# For API endpoints:
/usr/share/seclists/Discovery/Web-Content/api/

# For Wordpress:
/usr/share/seclists/Discovery/Web-Content/wordpress.txt
```

### Common Discoveries in eJPT
- `/admin` - Admin panel
- `/login` - Login page
- `/uploads` - Uploaded files (often 403 but important)
- `/api` - API endpoints
- `/config` - Configuration files
- `/backup` - Backup files
- `/test` - Test pages with debug info
- `/.git` - Exposed Git repository
- `/.env` - Environment variables (sensitive!)
- `/shell.php` - Web shells left by previous attackers

### One-Liners for Quick Results
```bash
# Scan and extract only 200 status codes:
gobuster dir -u http://target.com -w common.txt | grep "200"

# Scan multiple targets:
for target in 192.168.1.{10..20}; do
  echo "[*] Scanning http://$target"
  gobuster dir -u http://$target -w common.txt -t 50
done

# Extract URLs from results:
grep "Found" results.txt | awk '{print $2}'
```

---

## Combining Gobuster with Other Tools

### Gobuster → Nikto
```bash
# Find directories with gobuster, then check with nikto:
gobuster dir -u http://target.com -w common.txt -o dirs.txt
cat dirs.txt | grep "Found" | awk '{print "http://target.com" $2}' | while read url; do
  nikto -url $url
done
```

### Gobuster → Burp Suite
```bash
# Export results as URLs for Burp Suite import:
gobuster dir -u http://target.com -w common.txt -o results.txt
grep "Found" results.txt | awk '{print "http://target.com" $2}' > urls.txt

# Then load urls.txt into Burp Suite
```

### Gobuster → Manual Testing
```bash
# Find interesting endpoints then test manually:
gobuster dir -u http://target.com -w common.txt -x php,txt -t 50

# Manually test found URLs with curl:
curl -v http://target.com/admin
curl -v http://target.com/config.txt
curl -v http://target.com/backup.zip
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Check target URL, ensure service is running |
| "No results found" | Try different wordlist, add `-s 200,403,401` to check non-200 codes |
| "Too many false positives" | Use `-s 200` to only accept 200 status codes |
| "Scan is very slow" | Reduce `-t` (threads) or check network/target responsiveness |
| "SSL certificate error" | Use `-k` to skip certificate verification |
| "Gobuster not found" | Ensure installed: `sudo pacman -S gobuster` or build from source |

---

## Official Documentation & Resources

- **GitHub Repository**: https://github.com/OJ/gobuster
- **Official Documentation**: https://github.com/OJ/gobuster/wiki
- **SecLists WordLists**: https://github.com/danielmiessler/SecLists
- **Web Content Discovery**: https://github.com/danielmiessler/SecLists/tree/master/Discovery/Web-Content

---

## Key Takeaways for eJPT

1. **Basic scan**: `gobuster dir -u http://target -w common.txt`
2. **Always try multiple extensions**: `-x php,txt,html,bak`
3. **Increase threads for speed**: `-t 50` (default: 10)
4. **Save results**: `-o results.txt`
5. **Try DNS subdomains**: `gobuster dns -d domain -w wordlist.txt`
6. **Filter status codes**: `-s 200,403` (important!)
7. **Use good wordlists**: Quality > Quantity
8. **Combine with other tools**: Findings feed into other recon tools

---

**Next Steps**: Use findings from gobuster to identify vulnerable paths, misconfigurations, or exposed files for exploitation.

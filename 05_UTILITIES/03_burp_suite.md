# Burp Suite - Web Application Security Testing

## Overview

Burp Suite is the industry standard tool for web application penetration testing. It's a Java-based framework containing multiple tools for finding vulnerabilities in web applications. For eJPT, Burp Suite is essential for:

- **Web vulnerability scanning** - Automated detection of SQL injection, XSS, CSRF, etc.
- **Manual testing** - Proxy interception to modify requests/responses
- **HTTP request manipulation** - Repeater tool for testing modifications
- **Authentication bypass** - Intruder for credential brute forcing
- **API testing** - Analyze and test REST/SOAP APIs
- **Session management analysis** - Identify flawed authentication logic
- **Information gathering** - Site map shows all discovered endpoints

Burp integrates with browsers via proxy, allowing real-time interception and analysis of all HTTP/HTTPS traffic.

## Installation & Setup

### CachyOS/Arch Linux Installation

```bash
# Install Burp Suite Community Edition
yay -S burp-suite-community

# Or via pacman if available
sudo pacman -S burp-suite-community

# Verify installation
burpsuite --version

# Launch
burpsuite
```

### Windows Installation

```powershell
# Option 1: Chocolatey
choco install burpsuite-community

# Option 2: Direct download
# Visit: https://portswigger.net/burp/communitydownload
# Download and run installer

# Option 3: Docker
docker run -it --rm -p 8080:8080 portswigger/burpsuite-community
```

### Browser Proxy Configuration

**Firefox Setup**:
```
1. Settings > Network Settings > Manual proxy configuration
2. HTTP Proxy: 127.0.0.1, Port: 8080
3. Check "Use this proxy for all protocols"
4. Import Burp CA certificate (see below)
```

**Chrome Setup**:
```bash
# Use with proxy
google-chrome --proxy-server="http://127.0.0.1:8080"

# Or configure system-wide proxy
```

### Burp CA Certificate Installation

```bash
# Export CA certificate from Burp
# 1. In Burp: Settings > Certificates > Export certificate
# 2. Save as burp.crt

# Firefox import
# 1. Preferences > Advanced > Certificates > View Certificates
# 2. Authorities tab > Import > Select burp.crt

# Linux system-wide
sudo cp burp.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

## Core Concepts

### Burp Suite Architecture

```
┌─────────────────────────────────┐
│     WEB BROWSER (User)          │
├─────────────────────────────────┤
│  Proxy (Port 8080)              │
│  - Intercept requests/responses │
│  - Modify headers/body          │
├─────────────────────────────────┤
│  Repeater (Manual testing)      │
│  - Modify and resend requests   │
├─────────────────────────────────┤
│  Intruder (Fuzzing/Brute Force) │
│  - Automated parameter testing  │
├─────────────────────────────────┤
│  Scanner (Vulnerability scan)   │
│  - Active/passive scanning      │
├─────────────────────────────────┤
│  HTTPS/HTTP SERVERS             │
└─────────────────────────────────┘
```

### Key Terminology

| Term | Definition |
|------|-----------|
| **Proxy** | Intercepts traffic between browser and server |
| **Interception** | Pause traffic to modify before forwarding |
| **Repeater** | Tool to send modified HTTP requests multiple times |
| **Intruder** | Tool for automated parameter fuzzing/brute force |
| **Scanner** | Automated vulnerability detection tool |
| **Site Map** | Visual representation of all discovered endpoints |
| **Target scope** | Define which URLs to test (include/exclude) |
| **Payloads** | Fuzzing strings tested against parameters |
| **Active scan** | Send requests to discover vulnerabilities |
| **Passive scan** | Analyze responses without sending new requests |

### Burp Tools Overview

| Tool | Purpose | Use Case |
|------|---------|----------|
| **Proxy** | Intercept traffic | Modify requests, understand application flow |
| **Repeater** | Resend requests | Test SQL injection, XSS, CSRF |
| **Intruder** | Fuzzing/brute force | Parameter values, usernames, passwords |
| **Scanner** | Vulnerability scan | Find common web vulnerabilities |
| **Decoder** | Encode/decode | Base64, URL, HTML entities |
| **Comparer** | Compare responses | Identify differences between requests |
| **Collaborator** | Out-of-band testing | XXE, SSRF, blind XSS detection |

## Common Use Cases

### 1. Basic Proxy Setup and Interception

**Scenario**: Configure Burp as proxy and intercept first request.

```bash
# Step 1: Start Burp Suite
burpsuite &

# Step 2: Configure proxy (Proxy > Intercept > Intercept is on)

# Step 3: Configure browser proxy to 127.0.0.1:8080

# Step 4: Navigate to website in browser
# http://vulnerable.site.com/login

# Step 5: In Burp, intercept appears
# GET /login HTTP/1.1
# Host: vulnerable.site.com
# User-Agent: Mozilla/5.0...

# Step 6: Modify or forward
# Click "Forward" to send to server
# Or modify and click "Forward"
```

### 2. Modify Request Parameters (SQLi Testing)

**Scenario**: Test login form for SQL injection vulnerability.

```bash
# Step 1: Intercept login request
# POST /login HTTP/1.1
# username=admin&password=password

# Step 2: Modify in Repeater
# Tools > Repeater > Send to Repeater

# Step 3: Modify username parameter with SQLi payload
# username=admin' OR '1'='1&password=anything

# Step 4: Click "Send" to test
# Analyze response for successful authentication

# Step 5: Try other SQLi payloads
# username=admin'--&password=test
# username=admin' #&password=test
```

### 3. Directory and Parameter Discovery

**Scenario**: Find hidden endpoints and parameters via brute force.

```bash
# Step 1: Capture request in Repeater
# GET /index.php?user=test&id=1 HTTP/1.1

# Step 2: Use Intruder > Send to Intruder

# Step 3: Set attack type
# Intruder > Attack type: Cluster bomb

# Step 4: Mark positions (highlight parameters)
# Positions: user=§test§&id=§1§

# Step 5: Configure payloads
# Payload set 1: Common usernames
# Payload set 2: Common IDs
# Load from built-in wordlists

# Step 6: Start attack
# Intruder > Start attack

# Step 7: Analyze results
# Look for different response codes/sizes
```

### 4. Cookie and Session Analysis

**Scenario**: Test authentication by analyzing session cookies.

```bash
# Step 1: Intercept login request

# Step 2: Forward through login process
# Watch for Set-Cookie header

# Step 3: In Repeater, modify cookie
# GET /admin HTTP/1.1
# Cookie: session=ORIGINAL_COOKIE

# Step 4: Test various modifications
# Change session cookie value (even one character)
# Observe if server accepts modified session

# Step 5: Test cookie expiration
# Remove cookie entirely
# Send request - should be denied

# Step 6: Test cookie randomness
# Make multiple logins
# Analyze cookie values for predictability
```

### 5. XSS (Cross-Site Scripting) Testing

**Scenario**: Test user input fields for XSS vulnerability.

```bash
# Step 1: Find input parameter (search, comment, profile, etc.)
# GET /search?q=test HTTP/1.1

# Step 2: Send to Repeater

# Step 3: Test with XSS payload
# GET /search?q=<script>alert('XSS')</script> HTTP/1.1

# Step 4: In response, look for:
# - Unescaped <script> tag
# - No Content Security Policy header

# Step 5: Test encoded payloads
# GET /search?q=%3Cscript%3Ealert('XSS')%3C/script%3E HTTP/1.1

# Step 6: Test other contexts
# HTML: <img src=x onerror="alert('XSS')">
# JavaScript: ";alert('XSS');//
# Event handler: <svg onload="alert('XSS')">
```

### 6. Active Vulnerability Scanning

**Scenario**: Automated scan for common vulnerabilities.

```bash
# Step 1: Define target scope
# Target > Scope > Add
# URL: http://vulnerable.site.com

# Step 2: Right-click target
# Scan > Active scan

# Step 3: Configure scan type
# Crawl > Choose crawling options
# Scan type: Full audit

# Step 4: Start scan
# Monitor progress in Scan queue

# Step 5: Review results
# Target > Site map
# Items with red indicators = vulnerabilities found

# Step 6: Analyze each finding
# Vulnerability > Details > Proof of concept
```

### 7. Intruder Brute Force (Credentials)

**Scenario**: Brute force login credentials.

```bash
# Step 1: Capture login POST request
# POST /login HTTP/1.1
# username=test&password=test

# Step 2: Send to Intruder
# Tools > Intruder > Send to Intruder

# Step 3: Mark parameters
# Positions: username=§admin§&password=§password§

# Step 4: Select attack type
# Intruder > Attack type: Pitchfork
# (Pitchfork uses n:1, Cluster bomb uses all combinations)

# Step 5: Load payload lists
# Payloads > Payload type: Simple list
# Load usernames.txt
# Load passwords.txt for payload 2

# Step 6: Start attack
# Intruder > Start attack

# Step 7: Monitor for successful login
# Look for Status 302 (redirect) or different response size
```

### 8. CSRF Token Manipulation

**Scenario**: Test if CSRF tokens are properly validated.

```bash
# Step 1: Capture request with CSRF token
# POST /change-password HTTP/1.1
# csrf_token=abc123def456&password=newpass

# Step 2: Send to Repeater multiple times

# Step 3: Test modifications:
# - Change csrf_token value
# - Remove csrf_token entirely
# - Reuse old csrf_token from previous request

# Step 4: Analyze responses
# If any work (not rejected), CSRF vulnerability exists

# Step 5: Test token generation
# Multiple requests > Do tokens match?
# Test predictability of token generation
```

### 9. Authentication Bypass Testing

**Scenario**: Test various authentication bypass techniques.

```bash
# Step 1: Intercept authentication request
# GET /admin HTTP/1.1
# Authorization: Bearer token123

# Step 2: Test methods of bypass:
# - Remove Authorization header entirely
# - Change Bearer to bearer (lowercase)
# - Add duplicate Authorization header
# - Modify token value slightly
# - Test null/empty token

# Step 3: Test bypassing with HTTP method
# Try OPTIONS, HEAD instead of GET
# Try X-Original-Method header
# Try X-Rewrite-URL header

# Step 4: Analyze responses
# 200 OK = potential bypass
# 401/403 = proper denial
```

### 10. API Endpoint Testing

**Scenario**: Test REST API for vulnerabilities.

```bash
# Step 1: Monitor API calls in Proxy
# Browser makes API requests to /api/users/1

# Step 2: Send to Repeater
# GET /api/users/1 HTTP/1.1

# Step 3: Test parameter manipulation
# GET /api/users/2 (access other user)
# GET /api/users/admin (enumerate endpoints)
# GET /api/users/999999 (error handling)

# Step 4: Test missing authentication
# Remove Authorization header
# Send request - should fail

# Step 5: Test method manipulation
# Try DELETE, PUT, PATCH methods
# POST /api/users/1 with body {"role":"admin"}
# See if privilege escalation possible

# Step 6: Test injection in API
# GET /api/users?search=admin' OR '1'='1
# Test SQL injection in API parameters
```

### 11. Decoder Usage (Manual Encoding/Decoding)

**Scenario**: Decode captured data or encode payloads.

```bash
# In Burp: Tools > Decoder

# Example 1: Decode Base64
Input: dXNlcm5hbWU6cGFzc3dvcmQ=
Click Decode
Output: username:password

# Example 2: URL encode payload
Input: <script>alert('XSS')</script>
Smart decode > URL
Output: %3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E

# Example 3: HTML encode
Input: <b>test</b>
Smart decode > HTML
Output: &lt;b&gt;test&lt;/b&gt;

# Example 4: Chain encoding (Double encoding)
Input: <script>alert('XSS')</script>
Encode to: %3Cscript%3E...
Encode again: %253Cscript%253E...
```

### 12. Response Comparison (Comparer)

**Scenario**: Identify differences between two responses.

```bash
# Step 1: Capture two similar requests
# Request A: GET /page?id=1
# Request B: GET /page?id=2

# Step 2: Send both to Repeater
# Get responses for each

# Step 3: Select Response A in Repeater
# Copy response
# Tools > Comparer > Paste

# Step 4: Select Response B in Repeater
# Copy response
# Tools > Comparer > Paste (in second pane)

# Step 5: Compare side-by-side
# Comparer shows differences highlighted
# Identify timing differences, content variations
```

### 13. Collaborator for Out-of-Band Testing

**Scenario**: Test blind vulnerabilities (XXE, SSRF, blind XSS).

```bash
# Step 1: Generate Collaborator payload
# Collaborator > Copy to clipboard
# Generates: xxxx.burpcollaborator.net

# Step 2: Use in XXE payload
# POST /upload HTTP/1.1
# <?xml version="1.0"?>
# <!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://xxxx.burpcollaborator.net/">]>
# <foo>&xxe;</foo>

# Step 3: Send request

# Step 4: Poll Collaborator
# Collaborator > Poll now
# Shows any DNS/HTTP callbacks

# Step 5: Analyze callback details
# Shows DNS lookup, HTTP request, details
# Confirms vulnerability even without direct response
```

### 14. Site Map Exploration

**Scenario**: Discover all application endpoints.

```bash
# Step 1: Enable proxy interception
# Browse application normally, click links, fill forms

# Step 2: In Target > Site map, view all discovered URLs

# Step 3: Expand tree structure
# Example:
# http://vulnerable.site.com/
#  ├── login
#  ├── admin/
#  │   ├── dashboard
#  │   ├── users
#  │   └── settings
#  ├── api/
#  │   ├── users
#  │   └── posts
#  └── uploads

# Step 4: Right-click items
# - Send to Scanner (active scan)
# - Send to Repeater (manual testing)
# - Send to Intruder (fuzzing)

# Step 5: Use Scope to focus testing
# Target > Scope > Add
# Include: http://vulnerable.site.com
# Exclude: /logout
```

### 15. Passive Scan Analysis

**Scenario**: Identify potential issues without active scanning.

```bash
# Step 1: Set passive scan status
# Dashboard > Settings > Passive scanning: On

# Step 2: Browse application normally

# Step 3: Proxy analyzes all requests/responses
# Looks for:
# - Missing security headers
# - Weak cookie flags
# - Information disclosure
# - Unencrypted communication

# Step 4: View findings
# Dashboard > Issue activity
# Shows passive scan results

# Step 5: Review each finding
# Severity: High/Medium/Low/Info
# Confidence: Certain/Firm/Tentative
```

## Command Reference

### Burp Proxy Key Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+U` | URL decode selected text |
| `Ctrl+Shift+U` | URL encode selected text |
| `Ctrl+B` | Base64 decode selected text |
| `Ctrl+Shift+B` | Base64 encode selected text |
| `Ctrl+H` | HTML decode selected text |
| `Ctrl+Shift+H` | HTML encode selected text |
| `Right-click packet` | Send to other tools (Repeater, Scanner, Intruder) |
| `Ctrl+Shift+R` | Open history (search past requests) |

### Intruder Attack Types

| Attack Type | Purpose | Use Case |
|-------------|---------|----------|
| **Sniper** | 1 payload set, vary one position | Single parameter fuzzing |
| **Battering ram** | 1 payload set, same for all positions | Multiple field brute force (username=payload, password=payload) |
| **Pitchfork** | Multiple payload sets, iterate together | Username/password pairs simultaneously |
| **Cluster bomb** | Multiple payload sets, all combinations | Comprehensive parameter fuzzing |

### Scanner Finding Severities

| Severity | Meaning |
|----------|---------|
| **Critical** | Leads to immediate compromise |
| **High** | Significant security risk |
| **Medium** | Potential exploitation possible |
| **Low** | Minor vulnerability |
| **Info** | Informational finding |

## Practical Workflows

### Workflow 1: Full Web Application Penetration Test

**Goal**: Complete security assessment of web application.

```bash
# Step 1: Passive reconnaissance
# Set scope: Target > Scope
# Add URL: http://vulnerable.app
# Browse application normally (without active scanning)
# Allow 10+ minutes of passive scanning

# Step 2: Site map exploration
# Target > Site map
# Identify all endpoints
# Document important URLs

# Step 3: Manual testing
# Focus on:
# - Login functionality (authentication bypass)
# - Search functionality (SQL injection)
# - File upload (file type bypass)
# - User input forms (XSS)

# Step 4: Active vulnerability scanning
# Target > Scope items > Right-click
# Scan > Active scan
# Let complete (may take 30+ minutes)

# Step 5: Intruder-based fuzzing
# High-value parameters:
# - user ID parameter (access control)
# - Search terms (injection)
# - File names (traversal)

# Step 6: Report findings
# Dashboard > Issue activity
# Review all findings by severity
# Document proof of concept for each
```

### Workflow 2: SQL Injection Testing

**Goal**: Discover and confirm SQL injection vulnerability.

```bash
# Step 1: Identify database-connected input
# Intruder > Look for:
# - Search boxes
# - Filter parameters
# - User lookup functions

# Step 2: Test with basic payloads
# Repeater > Parameter:
# id=1' OR '1'='1
# id=1; DROP TABLE users;--
# id=1 UNION SELECT NULL--

# Step 3: Analyze responses
# Different response length = potential SQLi
# Error messages = confirm SQLi

# Step 4: Use Scanner for detection
# Active scanner has SQLi module
# Right-click parameter > Send to Scanner

# Step 5: Alternative: Use sqlmap integration
# Export request from Repeater
# Run: sqlmap -r request.txt
# More automated SQLi detection
```

### Workflow 3: Authentication Bypass Testing

**Goal**: Test various authentication mechanisms.

```bash
# Step 1: Capture login request
# Proxy > Intercept login POST

# Step 2: Test methods:
# A) Direct access without login
#    GET /admin without cookies

# B) Cookie manipulation
#    Modify session cookie
#    Use old/expired cookies

# C) Authentication header bypass
#    Remove Authorization header
#    Change Bearer token

# D) Parameter bypass
#    Add admin=true parameter
#    Change role parameter

# E) HTTP method override
#    Change POST to GET
#    Add X-HTTP-Method-Override

# Step 3: Use Intruder for systematic testing
# Intruder > Mark parameter positions
# Attack type: Sniper
# Payloads: Common bypass values

# Step 4: Analyze 200 OK responses
# Unexpected successful responses = bypass found
```

### Workflow 4: API Security Testing

**Goal**: Test REST/SOAP API endpoints.

```bash
# Step 1: Monitor API calls
# Proxy > Browse application
# Watch for /api/ calls
# Examine POST/GET requests to API

# Step 2: Test authorization
# Capture: GET /api/users/1
# Modify to: GET /api/users/2
# If accessible without explicit authorization = IDOR

# Step 3: Test authentication
# Remove Authorization header
# Add Authorization: Bearer invalid
# Observe if denied properly

# Step 4: Test data exposure
# GET /api/users (list all users?)
# GET /api/users/1 (leaks email/phone?)

# Step 5: Test mutation operations
# POST /api/users/1 (can modify other users?)
# DELETE /api/users/1 (can delete?)
# PUT /api/users/1/role with {"role":"admin"}

# Step 6: Test rate limiting
# Intruder > Rapid API calls
# Observe for rate limiting responses (429)
```

## Real-World Examples

### Example 1: SQL Injection in Login Form

**Scenario**: Test login vulnerable to SQL injection.

```
Request:
POST /login HTTP/1.1
Host: vulnerable.site
Content-Type: application/x-www-form-urlencoded

username=admin' OR '1'='1'--&password=test

Response:
HTTP/1.1 302 Found
Location: /dashboard
Set-Cookie: session=abc123def456

Result: Successful login without correct password
Vulnerability: SQL injection in authentication
```

### Example 2: CSRF Token Missing

**Scenario**: Change password without CSRF protection.

```
Intercept:
POST /change-password HTTP/1.1
Host: vulnerable.site

new_password=hacker123&confirm=hacker123

(No csrf_token parameter)

Test:
Remove both password fields, only send parameter tampering
Response: 200 OK - Password changed

Vulnerability: Missing CSRF token allows unauthorized password change
```

### Example 3: Access Control - Insecure Direct Object Reference (IDOR)

**Scenario**: Access other user's data by modifying ID.

```
Intercept:
GET /user/profile?id=123 HTTP/1.1

Response:
{
  "id": 123,
  "name": "Current User",
  "email": "user@site.com",
  "role": "user"
}

Modify to:
GET /user/profile?id=1 HTTP/1.1

Response:
{
  "id": 1,
  "name": "Administrator",
  "email": "admin@site.com",
  "role": "admin"
}

Vulnerability: IDOR - access other users' data without authorization
```

## Advanced Techniques

### Technique 1: Macro Automation

Automate multi-step workflows (login, CSRF token refresh, request).

```
Proxy > Options > Macros
Record macro:
1. Login request (POST /login)
2. Capture session cookie
3. Extract CSRF token from response
4. Use in subsequent requests

Intruder will auto-login and refresh tokens
```

### Technique 2: Session Handling Rules

Automatically update session tokens during Intruder attacks.

```
Intruder > Options > Session handling rules
Add rule:
- Before each request: Execute macro (login)
- Extract session from Set-Cookie header
- Use in subsequent Intruder requests
```

### Technique 3: Custom Burp Extensions

Extend Burp with Python/Java plugins for specialized testing.

```
Extender > Add extension
Example: Custom SQL injection detector
- Monitor Repeater requests
- Automatically test SQLi payloads
- Alert on successful injections
```

## Tips & Tricks

### Tip 1: Scope Limiting for Faster Testing

```
Target > Scope > Include only target domain
Reduces noise and focuses scanning on relevant endpoints
```

### Tip 2: Exclude Logout from Scanning

```
Target > Scope > Exclude
Pattern: /logout, /signout
Prevents active scan from logging you out repeatedly
```

### Tip 3: Use Repeater History

```
Repeater > History
Shows all previous Repeater requests
Useful for comparing payloads and responses
```

### Tip 4: Keyboard Shortcuts for Payload Encoding

```
Ctrl+U = URL decode
Ctrl+Shift+U = URL encode
Ctrl+B = Base64 decode
Ctrl+Shift+B = Base64 encode
```

### Tip 5: Grep-based Search

```
Intruder > Grep > Extract
Extract specific strings from all responses
Example: Extract all session IDs to analyze predictability
```

### Tip 6: Burp Community vs Professional

```
Community Edition Limitations:
- No active vulnerability scanning
- No Burp Collaborator
- Scanner limited to passive analysis

Work-around: Use sqlmap, manual testing for active scanning
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `Browser not connecting through proxy` | Proxy not configured | Check browser settings, verify 127.0.0.1:8080 |
| `SSL certificate error` | CA certificate not installed | Import burp.crt into browser |
| `No traffic captured` | Interception off | Proxy > Intercept > Turn on |
| `Intruder very slow` | Too many threads | Intruder > Options > Thread pool size (lower = slower but stable) |
| `Out of memory` | Large capture/scan | Restart Burp, or use Community edition on weaker system |
| `Scan hangs on single request` | Timeout on slow endpoint | Settings > Scanner > Timeout: Increase value |
| `Cannot access local application` | Application only on localhost | Configure browser to connect through proxy for localhost |
| `Scanner not finding vulnerabilities` | Passive only (Community) | Use manual testing + Intruder for active testing |

## Official Resources

- **Documentation**: https://portswigger.net/burp/documentation
- **Web Security Academy**: https://portswigger.net/web-security
- **Community Forum**: https://forum.portswigger.net/
- **Burp Extensions (BApp Store)**: https://portswigger.net/bappstore
- **Community Edition**: https://portswigger.net/burp/communitydownload

## Key Takeaways

1. **Proxy interception** - Real-time request/response modification for deep testing
2. **Active scanning** - Automated detection of 1000+ vulnerability types (Professional only)
3. **Intruder fuzzing** - Systematic parameter testing with payload dictionaries
4. **Session handling** - Analyze authentication mechanisms for bypass opportunities
5. **API testing** - Dedicated tools for REST/SOAP API security assessment
6. **Out-of-band testing** - Collaborator confirms blind vulnerabilities (XXE, SSRF)
7. **Scope management** - Focus testing on target application, exclude non-targets
8. **Repeater modification** - Manual request crafting for edge case testing
9. **Encoding/decoding** - Built-in tools for payload preparation
10. **Integration with sqlmap** - Export requests for automated SQL injection testing

---

**Next Steps**: Combine Burp Suite with Metasploit for full exploitation (find vulnerability with Burp, exploit with Metasploit). Use Wireshark to verify Burp modifications reach target unchanged.

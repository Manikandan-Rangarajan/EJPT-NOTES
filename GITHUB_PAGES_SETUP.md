# GitHub Pages Setup Guide

## 🚀 Quick Start to Host Your Hacker Docs Online

### Step 1: Create GitHub Repository

```bash
# Create a new repository on GitHub
# Name: ejpt-tools-docs (or your preferred name)
# Make it PUBLIC (required for free GitHub Pages)
# Don't initialize with README (we have our own)
```

### Step 2: Push Files to GitHub

```bash
# Navigate to your project root
cd C:\Users\Manikandan Rangarjan\Documents\EJPT\ai-notes

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: eJPT Penetration Testing Documentation with hacker-themed index"

# Add remote (replace USERNAME and REPO)
git remote add origin https://github.com/USERNAME/ejpt-tools-docs.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (gear icon)
3. Scroll to **Pages** section (left sidebar)
4. Under "Source", select:
   - Branch: `main`
   - Folder: `/PDF_OUTPUT` (Important!)
5. Click **Save**

GitHub will display your site URL (usually: `https://USERNAME.github.io/ejpt-tools-docs`)

### Step 4: Access Your Site

Your documentation is now live! Visit:
```
https://USERNAME.github.io/ejpt-tools-docs
```

The main entry point is `index.html` - a beautiful hacker-themed dashboard with:
- ✨ Glitch text effects
- 🌟 Neon glow animations
- 🎯 Matrix background
- 🔍 Search functionality (Ctrl+K)
- 📊 Statistics dashboard
- 🎨 Responsive design
- ⚡ Hover effects

---

## 📋 What's Included

### In PDF_OUTPUT/:
- **index.html** - Main hacker-themed dashboard (THE ENTRY POINT)
- **20 HTML files** - All documentation files organized by phase
- Each file links back to the index for easy navigation

### Features of the Index:

#### 🎮 Interactive Elements
- Click any tool card to open the documentation
- Search box with Ctrl+K shortcut
- Smooth animations and transitions
- Responsive design for mobile/tablet/desktop

#### 📊 Dashboard Stats
- 23 tools documented
- 15K+ lines of code
- 60+ real-world scenarios
- 5 penetration testing phases

#### 🎨 Hacker Aesthetics
- Neon green (#00ff00) and pink (#ff0099) color scheme
- Glitch text effects on title
- Matrix-like background
- Smooth hover effects
- Glowing shadows

#### 🔍 Search Functionality
- Type to filter tools
- Ctrl+K to focus search
- Real-time filtering

---

## 🛠️ Customization

### Change Colors
Edit the `--primary-color`, `--secondary-color`, and `--accent-color` in the CSS:

```css
:root {
    --primary-color: #00ff00;      /* Neon green */
    --secondary-color: #00cc00;    /* Green */
    --accent-color: #ff0099;       /* Hot pink */
    --dark-bg: #0a0e27;           /* Dark blue */
}
```

### Add More Tools
Edit the `tools` object in the JavaScript section:

```javascript
phase1: [
    { name: 'Tool Name', file: 'filename.html', icon: '🔍', 
      desc: 'Description', lines: 409 },
    // ... add more
]
```

### Modify Animations
- Glitch effect: `.glitch::before` and `.glitch::after`
- Hover effects: `.tool-card:hover`
- Background animation: `@keyframes backgroundShift`

---

## 📁 Repository Structure for GitHub

```
ejpt-tools-docs/
├── PDF_OUTPUT/
│   ├── index.html (MAIN ENTRY POINT)
│   ├── 01_nmap.html
│   ├── 02_gobuster.html
│   ├── ... (all 20 HTML files)
│   └── QUICK_REFERENCE.html
├── 01_RECON/
│   └── *.md (markdown source files)
├── 02_EXPLOITATION/
│   └── *.md
├── ... (other phase directories)
├── README.md
├── SUMMARY.md
├── QUICK_REFERENCE.md
└── .gitignore (optional)
```

---

## 🔒 GitIgnore (Optional)

Create `.gitignore` to exclude unnecessary files:

```
# Dependencies
node_modules/
.git/

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Large files (if any)
*.pdf
```

---

## 🎯 Domain (Optional)

To use a custom domain instead of GitHub's default:

1. Register a domain (e.g., ejpt-tools.com)
2. In GitHub Pages settings, add custom domain
3. Point domain DNS to GitHub Pages IP
4. Wait 24 hours for DNS propagation

---

## 📊 GitHub Pages Limits

**Free GitHub Pages includes:**
- ✅ Unlimited bandwidth
- ✅ Unlimited deployments
- ✅ HTTPS enabled by default
- ✅ Custom domains supported
- ✅ Jekyll support
- ⚠️ No server-side code (static files only)

**Perfect for this project!** All HTML/CSS/JavaScript is client-side.

---

## 🚀 Advanced: Auto-Deploy

Use GitHub Actions to auto-build from markdown → HTML:

Create `.github/workflows/build.yml`:

```yaml
name: Build Documentation

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build markdown to HTML
        run: |
          for f in *.md; do
            pandoc "$f" -o "PDF_OUTPUT/${f%.md}.html"
          done
      - name: Commit changes
        run: |
          git add PDF_OUTPUT/
          git commit -m "Auto-build: Generated HTML from markdown"
          git push
```

---

## 🔗 Sharing Your Site

Share the link with:
- **Friends**: Direct GitHub Pages URL
- **Resume**: Add to projects section
- **Job interviews**: Showcase your pentesting knowledge
- **Study group**: Complete eJPT prep material
- **Social media**: Portfolio of work

Example:
```
Check out my comprehensive eJPT Penetration Testing Documentation:
https://USERNAME.github.io/ejpt-tools-docs

Includes 23 tools, 15K+ lines of code, 60+ real-world scenarios
Built with hacker vibes! 🔓
```

---

## ✅ Verification Checklist

- [ ] Repository created and public
- [ ] All files pushed to GitHub
- [ ] GitHub Pages enabled in Settings
- [ ] Source set to `/PDF_OUTPUT` branch
- [ ] Visit URL and see the hacker dashboard
- [ ] Click through to verify all links work
- [ ] Search functionality works (Ctrl+K)
- [ ] Mobile responsive (test on phone)

---

## 🆘 Troubleshooting

### "404 Not Found"
- Ensure GitHub Pages is enabled
- Check source is set to `/PDF_OUTPUT`
- Wait 1-2 minutes for deployment

### "Links not working"
- All files must be in `PDF_OUTPUT/`
- File names must match exactly (case-sensitive)
- Verify `index.html` exists

### "Slow loading"
- Normal - GitHub Pages might take a few seconds
- Check browser cache (Ctrl+Shift+Delete)

### "Styling looks wrong"
- Check GitHub Pages settings
- Try different branch
- Clear browser cache

---

## 📚 Resources

- **GitHub Pages Docs**: https://pages.github.com/
- **GitHub Markdown Guide**: https://guides.github.com/
- **GitHub Actions**: https://docs.github.com/en/actions

---

## 🎉 You're All Set!

Your eJPT Penetration Testing Documentation is now:
- ✅ Professionally hosted on GitHub Pages
- ✅ Accessible to anyone via link
- ✅ Free and unlimited bandwidth
- ✅ Auto-HTTPS encrypted
- ✅ Searchable and interactive
- ✅ Mobile-responsive
- ✅ Amazing hacker aesthetics

**Total Documentation:**
- 23 cybersecurity tools
- 15,000+ lines of code
- 60+ real-world scenarios
- 40+ practical workflows
- Beautiful, functional dashboard

Happy hacking! 🔓

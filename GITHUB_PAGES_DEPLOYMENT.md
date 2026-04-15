# GitHub Pages Deployment Guide

## Quick Start (TL;DR)

```bash
# 1. Create a GitHub repository
# Go to https://github.com/new and create a repository named "ejpt-notes" (or any name)

# 2. Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main

# 3. Enable GitHub Pages
# Go to: Settings → Pages
# Source: Deploy from a branch
# Branch: main
# Folder: /PDF_OUTPUT
# Save

# 4. Site will be live at:
# https://YOUR_USERNAME.github.io/YOUR_REPO_NAME
```

---

## Detailed Setup Instructions

### Step 1: Create a GitHub Repository

1. Go to [GitHub New Repository](https://github.com/new)
2. Fill in the details:
   - **Repository name**: `ejpt-notes` (or your preferred name)
   - **Description**: "eJPT Penetration Testing Learning Platform with Anime-Themed CSS"
   - **Public** (required for GitHub Pages free tier)
   - Leave other options as default
3. Click **Create repository**

### Step 2: Configure Git Remote

```bash
# Add the GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Rename default branch to main (if needed)
git branch -M main

# Verify remote is set correctly
git remote -v
```

Expected output:
```
origin  https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git (fetch)
origin  https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git (push)
```

### Step 3: Push to GitHub

```bash
# Push all commits to GitHub
git push -u origin main

# Verify push was successful
git status
```

You should see: `Your branch is up to date with 'origin/main'.`

### Step 4: Enable GitHub Pages

1. Go to your GitHub repository
2. Click **Settings** (top right)
3. Scroll to **Pages** section (left sidebar)
4. Configure:
   - **Source**: Select "Deploy from a branch"
   - **Branch**: Select "main"
   - **Folder**: Select "/PDF_OUTPUT"
   - Click **Save**

5. GitHub will show a message:
   ```
   Your site is published at https://YOUR_USERNAME.github.io/YOUR_REPO_NAME
   ```

### Step 5: Wait & Verify

- GitHub Pages typically deploys within 1-2 minutes
- Check the **Deployments** section to see status
- Once "Active", visit the URL to see your site live

---

## Your Deployment URL

After enabling GitHub Pages with `/PDF_OUTPUT` as the source, your site will be available at:

```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME
```

**Example:**
- If your username is `john-doe`
- And repo is `ejpt-notes`
- Then URL is: `https://john-doe.github.io/ejpt-notes`

---

## What Gets Deployed

From `/PDF_OUTPUT` directory:

| File | Purpose |
|------|---------|
| `index.html` | Main dashboard (entry point) |
| `01_nmap.html` - `08_snmpwalk.html` | Tool documentation pages |
| `01_metasploit.html`, etc. | Specialized tool guides |
| `README.html`, `SUMMARY.html`, `QUICK_REFERENCE.html` | Reference pages |
| `anime-vibes.css` | Anime-themed CSS framework |

All files are self-contained - no external dependencies!

---

## Verification Checklist

After deployment, verify everything works:

- [ ] Landing page loads at `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME`
- [ ] Dashboard theme toggle works (🌙/☀️ button)
- [ ] Dark mode shows cyan/purple neon colors
- [ ] Light mode shows professional styling
- [ ] Tool pages load with anime styling
- [ ] Code blocks have cyan glowing borders
- [ ] All links work correctly
- [ ] Mobile responsive on small screens
- [ ] No console errors in browser DevTools

---

## Troubleshooting

### Site shows 404 or "Not Found"

**Solution:**
1. Verify Pages source is set to `/PDF_OUTPUT`
2. Go to **Settings → Pages** and check:
   - Branch is set to `main`
   - Folder is set to `/PDF_OUTPUT`
3. Wait 2-3 minutes for deployment
4. Hard refresh browser (Ctrl+Shift+R)

### CSS not loading / Styling looks wrong

**Solution:**
1. Open browser DevTools (F12)
2. Check Network tab for `anime-vibes.css`
3. If file shows 404:
   - Verify `anime-vibes.css` exists in `PDF_OUTPUT/`
   - Check `index.html` has correct path: `href="anime-vibes.css"`
4. If CSS loads but styling is missing:
   - Hard refresh (Ctrl+Shift+R)
   - Clear browser cache

### Theme toggle doesn't work

**Solution:**
1. Check browser console for JavaScript errors (F12 → Console)
2. Verify localStorage is enabled
3. Try in incognito/private window
4. Check that the theme toggle script is in HTML files

### Site takes too long to load

**Solution:**
1. GitHub Pages caches content
2. Try hard refresh (Ctrl+Shift+R)
3. Wait a few minutes
4. Check site status at https://www.githubstatus.com/

---

## Updates & Changes

### To update the site after deployment:

```bash
# 1. Make changes locally
# Edit files, test them

# 2. Stage and commit changes
git add .
git commit -m "Update: describe your changes"

# 3. Push to GitHub
git push origin main

# 4. GitHub Pages auto-deploys within 1-2 minutes
# No additional configuration needed!
```

---

## Advanced Configuration (Optional)

### Custom Domain

If you want to use your own domain:

1. Go to **Settings → Pages**
2. Scroll to "Custom domain"
3. Enter your domain (e.g., `ejpt.yoursite.com`)
4. Click **Save**
5. GitHub will display DNS records to configure
6. Add DNS records to your domain provider
7. GitHub Pages will verify and enable HTTPS automatically

### Custom 404 Page

Create a `PDF_OUTPUT/404.html` file, and GitHub will show it for missing pages.

### HTTPS (Automatic)

GitHub Pages automatically provides:
- Free HTTPS certificate
- Auto-renewal
- Force HTTPS option (Settings → Pages → Enforce HTTPS)

---

## File Structure for GitHub Pages

```
your-repo/
├── .git/                          # Git repository (automatic)
├── .gitignore                     # Files to ignore
├── PDF_OUTPUT/                    # GitHub Pages source ⭐
│   ├── index.html                # Landing page (entry point)
│   ├── anime-vibes.css           # CSS framework
│   ├── 01_nmap.html              # Tool pages
│   ├── 02_gobuster.html
│   ├── ... (other HTML files)
│   ├── README.html
│   ├── SUMMARY.html
│   └── QUICK_REFERENCE.html
├── 01_RECON/                      # Source markdown (optional)
├── 02_EXPLOITATION/               # Source markdown (optional)
├── ... (other markdown directories)
├── anime-vibes.css                # Source CSS (for reference)
├── README.md                      # Repository README
├── QUICK_START.md
└── ... (other documentation)
```

**Note:** Only files in `/PDF_OUTPUT/` are deployed to GitHub Pages. Source files (markdown, etc.) stay in the repository but aren't published to the web.

---

## Performance Optimization

Your site is already optimized:

- ✅ **CSS Framework**: 35 KB (gzipped ~10 KB)
- ✅ **No External Dependencies**: Pure HTML/CSS/JavaScript
- ✅ **CDN Delivery**: GitHub Pages uses Fastly CDN for fast global delivery
- ✅ **Caching**: Browsers cache CSS and static assets
- ✅ **GPU Acceleration**: Animations use transforms for 60 FPS

Expected load times:
- First load: 200-500ms (after CDN cache warms)
- Subsequent loads: 50-100ms
- CSS: 20-50ms

---

## Support & Next Steps

### If You Need Help:

1. **GitHub Pages Official Docs**: https://pages.github.com/
2. **GitHub Troubleshooting**: https://docs.github.com/en/pages/getting-started-with-github-pages
3. **Check Deployment Status**: Go to repository → Deployments tab

### Potential Enhancements:

- [ ] Add progress tracking for learning paths
- [ ] Create interactive quiz system
- [ ] Add video tutorial links
- [ ] Build PWA version for offline access
- [ ] Add user accounts with bookmarks
- [ ] Create community forum
- [ ] Add search functionality
- [ ] Create API for progress tracking

---

## Summary

| Step | Time | Status |
|------|------|--------|
| Create GitHub repo | 1 min | ⏳ Next |
| Configure git remote | 1 min | ⏳ Next |
| Push to GitHub | 2-5 min | ⏳ Next |
| Enable GitHub Pages | 1 min | ⏳ Next |
| Deployment completes | 1-2 min | ⏳ Next |
| **Total Time** | **~15 minutes** | 🚀 |

---

**Everything is ready! Follow the Quick Start section above to go live.** 🎉

Last Updated: April 15, 2026

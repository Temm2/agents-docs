# Public Sharing Guide - Get a Shareable Link

## ✅ Color Fix Applied

All test result boxes now use:
- **Background**: Grey (#3a3a3a)
- **Text**: White (#ffffff)
- **Borders**: Colored (purple/red) for visual distinction

This makes all text easily readable! ✅

---

## 🌐 Option 1: GitHub Pages (Recommended - Permanent & Free)

**Best for:** Long-term sharing, professional use

### Quick Setup

```bash
# Run the setup script
./setup_github_pages.sh

# Then follow the instructions it prints
```

### Manual Setup

1. **Create docs folder:**
   ```bash
   mkdir -p docs
   cp test_report.html docs/index.html
   ```

2. **Initialize git (if not already):**
   ```bash
   git init
   git add .
   git commit -m "Add test report"
   ```

3. **Create GitHub repository:**
   - Go to: https://github.com/new
   - Name it (e.g., "ramm-test-report")
   - Make it **PUBLIC** (required for free GitHub Pages)
   - Click "Create repository"

4. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git branch -M main
   git push -u origin main
   ```

5. **Enable GitHub Pages:**
   - Go to your repo → **Settings** → **Pages**
   - **Source**: Deploy from a branch
   - **Branch**: `main`, **Folder**: `/docs`
   - Click **Save**

6. **Your public URL:**
   ```
   https://YOUR_USERNAME.github.io/YOUR_REPO/
   ```

**⏱️ Takes 1-2 minutes to go live**

---

## 🚀 Option 2: Ngrok (Temporary - Instant)

**Best for:** Quick sharing, temporary links

### Setup

1. **Install ngrok:**
   ```bash
   # macOS
   brew install ngrok
   
   # Or download from: https://ngrok.com/download
   ```

2. **Run the sharing script:**
   ```bash
   python share_public.py
   ```

3. **Choose option 2 (ngrok)**

4. **Share the URL it gives you!**

**⚠️ Note:** Free ngrok URLs expire after 2 hours. Keep the terminal open while sharing.

---

## 🏠 Option 3: Local Server (Same Network)

**Best for:** Team members on same WiFi

```bash
# Start server
python3 -m http.server 8000

# Share your IP address:
# macOS: ifconfig | grep "inet "
# Then share: http://YOUR_IP:8000/test_report.html
```

---

## 📧 Option 4: Direct File Sharing

**Simplest:** Just share the HTML file directly

1. **Generate report:**
   ```bash
   python -m app.report_generator
   ```

2. **Share `test_report.html`:**
   - Email it
   - Upload to Google Drive/Dropbox → Share link
   - Use WeTransfer, SendAnywhere, etc.

**Works offline** - recipient just opens the file in browser!

---

## 🎯 Quick Start (Easiest)

**For permanent link:**
```bash
./setup_github_pages.sh
# Follow the printed instructions
```

**For instant temporary link:**
```bash
python share_public.py
# Choose ngrok option
```

---

## 💡 Recommendation

- **GitHub Pages**: Best for permanent, professional sharing
- **Ngrok**: Best for quick demos or temporary sharing
- **File sharing**: Best for offline viewing or one-time sharing

All options work great - choose based on your needs! 🚀

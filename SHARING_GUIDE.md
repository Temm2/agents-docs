# Sharing RAMM Agent Tests - Guide

## Quick Share Options

### Option 1: Simplest Sharing (Recommended)

**One command:**
```bash
python share_simple.py
```

This will:
- ✅ Generate the report
- ✅ Show you the file path
- ✅ Open it in your browser
- ✅ Give you 4 simple sharing options

**Or use the shell script:**
```bash
./share_tests.sh
```

**Manual generation:**
```bash
cd /Users/admin/Documents/rammagents
source .venv/bin/activate
python -m app.report_generator
```

**Generated files:**
- `test_report.html` - Self-contained HTML report (~21KB)
- `test_report.md` - Markdown version

**Location:** `/Users/admin/Documents/rammagents/test_report.html`

**Share the HTML file:**
- Email it
- Upload to Google Drive/Dropbox and share link
- Host on GitHub Pages (see below)
- Share via file sharing service

**The HTML file includes:**
- ✅ All logic test results (16 scenarios)
- ✅ All business logic test results (11 calculations)
- ✅ Graph validation results
- ✅ Beautiful styling (no external dependencies)
- ✅ Self-contained (works offline)

---

### Option 2: Streamlit Cloud (Interactive Dashboard)

Deploy the dashboard to Streamlit Cloud for interactive sharing:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add RAMM agent tests"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `ramm_dashboard.py`
   - Click "Deploy"

3. **Share the link:**
   - Streamlit Cloud provides a public URL like: `https://your-app.streamlit.app`
   - Share this URL with anyone
   - They can interact with all tests in real-time

**Requirements:**
- GitHub account
- Streamlit Cloud account (free)
- Repository must be public (or you need Streamlit Cloud for Teams)

---

### Option 3: GitHub Pages (Static HTML)

Host the HTML report on GitHub Pages:

1. **Generate report:**
   ```bash
   python -m app.report_generator
   ```

2. **Create `docs` folder and move report:**
   ```bash
   mkdir -p docs
   cp test_report.html docs/index.html
   ```

3. **Push to GitHub:**
   ```bash
   git add docs/
   git commit -m "Add test report"
   git push origin main
   ```

4. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: `main` branch, `/docs` folder
   - Save

5. **Share the link:**
   - Your report will be at: `https://yourusername.github.io/rammagents/`
   - Share this URL

---

### Option 4: Local Network Sharing

Share via local network (for team members on same network):

1. **Start a simple HTTP server:**
   ```bash
   cd /Users/admin/Documents/rammagents
   python3 -m http.server 8000
   ```

2. **Share your IP address:**
   - Find your IP: `ifconfig | grep "inet "`
   - Share: `http://YOUR_IP:8000/test_report.html`

3. **Team members access:**
   - Open browser: `http://YOUR_IP:8000/test_report.html`

---

### Option 5: Export to PDF

Convert HTML report to PDF for document sharing:

1. **Using browser:**
   - Open `test_report.html` in browser
   - Print → Save as PDF

2. **Using command line (requires wkhtmltopdf):**
   ```bash
   wkhtmltopdf test_report.html test_report.pdf
   ```

---

## What's Included in Reports

### Logic Tests (16 scenarios)
- ✅ Happy Path (3): Campaign creation, purchase flow, redemption flow
- ✅ Security (10): Unauthorized access, replay attacks, race conditions, etc.
- ✅ Resilience (3): Partial failures, concurrent operations, etc.

### Business Logic Tests (11 calculations)
- ✅ Bonding Curves: Linear, exponential, logarithmic pricing
- ✅ Rewards: Tier-based and attribution calculations
- ✅ Yield: Simple and compound interest
- ✅ ROI: Campaign ROI and PVT velocity metrics

### Graph Validation
- ✅ Agent reachability
- ✅ Edge integrity
- ✅ Isolation checks

---

## Recommended Sharing Method

**For quick sharing:** Use Option 1 (HTML file) - just email or upload the file.

**For interactive sharing:** Use Option 2 (Streamlit Cloud) - best for demos and collaboration.

**For permanent hosting:** Use Option 3 (GitHub Pages) - best for documentation.

---

## Example Share Message

```
Hi team,

I've generated a comprehensive test report for the RAMM agent system.

📊 Report includes:
- 16 logic test scenarios (agent behavior & security)
- 11 business logic tests (calculations & math)
- Graph validation results

📁 Files:
- test_report.html (open in browser)
- test_report.md (markdown version)

Or view interactive dashboard:
[Streamlit Cloud URL]

Let me know if you have questions!

Best,
[Your Name]
```

---

## Updating Reports

To regenerate reports with latest test results:

```bash
cd /Users/admin/Documents/rammagents
source .venv/bin/activate
python -m app.report_generator
```

This overwrites the existing `test_report.html` and `test_report.md` files.

---

## Troubleshooting

**HTML file won't open:**
- Make sure file has `.html` extension
- Try different browser
- Check file permissions

**Streamlit Cloud deployment fails:**
- Check `requirements.txt` includes all dependencies
- Verify `ramm_dashboard.py` exists
- Check Streamlit Cloud logs for errors

**GitHub Pages not showing:**
- Wait 5-10 minutes after enabling
- Check repository is public
- Verify `/docs` folder exists with `index.html`

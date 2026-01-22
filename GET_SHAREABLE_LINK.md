# Get Your Shareable Link - Quick Guide

## 🚀 Fastest Way to Get a Public Link

### Step 1: Run Setup Script
```bash
./setup_docs_hosting.sh
```

This copies all your documentation files to the `docs/` folder.

### Step 2: Push to GitHub

**If you already have a GitHub repo:**
```bash
git add docs/
git commit -m "Add documentation"
git push
```

**If you need to create a new repo:**
```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Add RAMM agents documentation"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Pages

1. Go to your GitHub repository
2. Click **Settings** → **Pages**
3. Under **Source**:
   - Select: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/docs**
4. Click **Save**

### Step 4: Get Your Link

**Your documentation will be live at:**
```
https://YOUR_USERNAME.github.io/YOUR_REPO/
```

**Example:**
```
https://johndoe.github.io/ramm-docs/
```

⏱️ **Wait 1-2 minutes** for GitHub to deploy your site.

---

## 📁 What's Included

Your shareable link will have access to:

- ✅ **test_report.html** - Complete test results
- ✅ **All .md files** - All documentation
- ✅ **index.html** - Navigation page

**All files are accessible via:**
```
https://YOUR_USERNAME.github.io/YOUR_REPO/FILENAME.md
https://YOUR_USERNAME.github.io/YOUR_REPO/test_report.html
```

---

## 🔗 Share the Link

Once live, share this link with anyone:
```
https://YOUR_USERNAME.github.io/YOUR_REPO/
```

They can:
- ✅ View the test report
- ✅ Read all markdown documentation
- ✅ Download any file
- ✅ Access everything from anywhere

---

## 💡 Pro Tips

1. **Bookmark the link** - It's permanent
2. **Update anytime** - Just push new changes to GitHub
3. **Free forever** - GitHub Pages is free for public repos
4. **Works on mobile** - Responsive design

---

## 🆘 Troubleshooting

**Link not working?**
- Wait 2-3 minutes (GitHub needs time to deploy)
- Check Settings → Pages shows "Your site is live at..."
- Make sure repo is **PUBLIC** (required for free hosting)

**Files not showing?**
- Make sure files are in `docs/` folder
- Check file names are correct
- Try refreshing the page

**Need help?**
- Check `PUBLIC_SHARING.md` for more options
- Or use `python share_public.py` for alternative methods

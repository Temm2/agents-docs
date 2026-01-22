#!/bin/bash
# Quick setup script for GitHub Pages hosting

echo "📦 Setting up GitHub Pages for test report..."
echo ""

# Create docs folder
mkdir -p docs

# Copy report to docs/index.html
cp test_report.html docs/index.html

echo "✅ Created docs/index.html"
echo ""
echo "📤 Next steps:"
echo ""
echo "1. If you haven't initialized git:"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit'"
echo ""
echo "2. Create a GitHub repository (or use existing)"
echo "   - Go to: https://github.com/new"
echo "   - Create a new repository (make it PUBLIC for free hosting)"
echo ""
echo "3. Push to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Enable GitHub Pages:"
echo "   - Go to your repo → Settings → Pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: main, Folder: /docs"
echo "   - Click Save"
echo ""
echo "5. Your report will be live at:"
echo "   https://YOUR_USERNAME.github.io/YOUR_REPO/"
echo ""
echo "⏱️  It may take 1-2 minutes for the site to go live."
echo ""

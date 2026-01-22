#!/bin/bash
# Setup GitHub Pages hosting for all documentation

echo "📦 Setting up documentation hosting..."
echo ""

# Create docs folder
mkdir -p docs

# Copy test report to docs
if [ -f "test_report.html" ]; then
    cp test_report.html docs/
    echo "✅ Copied test_report.html"
fi

# Copy all markdown files to docs
echo "📄 Copying markdown files..."
for file in *.md; do
    if [ -f "$file" ]; then
        cp "$file" docs/
        echo "  ✅ Copied $file"
    fi
done

# Copy index.html if it exists
if [ -f "docs/index.html" ]; then
    echo "✅ Using existing docs/index.html"
else
    echo "⚠️  docs/index.html not found - creating basic one..."
    cat > docs/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>RAMM Agents Documentation</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: sans-serif; background: #1a1a1a; color: #e0e0e0; padding: 40px; }
        h1 { color: #667eea; }
        a { color: #2ecc71; text-decoration: none; }
        a:hover { text-decoration: underline; }
        ul { list-style: none; padding: 0; }
        li { margin: 10px 0; padding: 10px; background: #2a2a2a; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🚀 RAMM Agents Documentation</h1>
    <p>All documentation files are available below:</p>
    <ul>
        <li><a href="test_report.html">📊 Test Report</a></li>
        <li><a href="NOVICE_GUIDE.md">🎓 Novice Guide</a></li>
        <li><a href="SHARING_GUIDE.md">📤 Sharing Guide</a></li>
        <li><a href="SHOPI_VALET_CONNECTION.md">🔗 SHOPI-VALET Connection</a></li>
        <li><a href="TESTING.md">🧪 Testing Guide</a></li>
        <li><a href="TEST_SCENARIOS.md">📋 Test Scenarios</a></li>
        <li><a href="STATE_ANALYSIS.md">🔍 State Analysis</a></li>
        <li><a href="ANALYSIS_SUMMARY.md">📊 Analysis Summary</a></li>
        <li><a href="TEST_TYPES.md">📚 Test Types</a></li>
        <li><a href="PUBLIC_SHARING.md">🌐 Public Sharing</a></li>
    </ul>
</body>
</html>
EOF
    echo "✅ Created docs/index.html"
fi

echo ""
echo "✅ Documentation setup complete!"
echo ""
echo "📤 Next steps for GitHub Pages:"
echo ""
echo "1. Initialize git (if not already):"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Add documentation'"
echo ""
echo "2. Create GitHub repository:"
echo "   - Go to: https://github.com/new"
echo "   - Name it (e.g., 'ramm-docs')"
echo "   - Make it PUBLIC"
echo "   - Click 'Create repository'"
echo ""
echo "3. Push to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Enable GitHub Pages:"
echo "   - Go to repo → Settings → Pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: main, Folder: /docs"
echo "   - Click Save"
echo ""
echo "5. Your documentation will be live at:"
echo "   https://YOUR_USERNAME.github.io/YOUR_REPO/"
echo ""
echo "⏱️  Takes 1-2 minutes to go live"
echo ""

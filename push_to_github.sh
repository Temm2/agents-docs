#!/bin/bash
# Push documentation to GitHub and get shareable link

echo "🚀 Pushing to GitHub repository: agents-docs"
echo ""

# Check if remote already exists
if git remote get-url origin > /dev/null 2>&1; then
    echo "✅ Remote 'origin' already configured"
    git remote -v
else
    echo "📝 Please enter your GitHub username:"
    read -r GITHUB_USERNAME
    
    if [ -z "$GITHUB_USERNAME" ]; then
        echo "❌ GitHub username is required"
        exit 1
    fi
    
    echo ""
    echo "🔗 Adding remote: https://github.com/$GITHUB_USERNAME/agents-docs.git"
    git remote add origin "https://github.com/$GITHUB_USERNAME/agents-docs.git"
    echo "✅ Remote added"
fi

echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🌐 Next step: Enable GitHub Pages"
    echo ""
    echo "1. Go to: https://github.com/$GITHUB_USERNAME/agents-docs/settings/pages"
    echo "2. Under 'Source':"
    echo "   - Select: Deploy from a branch"
    echo "   - Branch: main"
    echo "   - Folder: /docs"
    echo "3. Click 'Save'"
    echo ""
    echo "⏱️  Wait 1-2 minutes, then your site will be live at:"
    echo "   https://$GITHUB_USERNAME.github.io/agents-docs/"
    echo ""
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo "   - Repository doesn't exist (create it first)"
    echo "   - Wrong username"
    echo "   - Authentication required (use GitHub CLI or SSH)"
    echo ""
    echo "💡 Alternative: Use GitHub CLI"
    echo "   gh repo create agents-docs --public --source=. --remote=origin --push"
fi

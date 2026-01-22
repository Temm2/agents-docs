#!/bin/bash
# Preview documentation locally and get sharing instructions

echo "📚 RAMM Agents Documentation Preview"
echo ""

# Check if docs folder exists
if [ ! -d "docs" ]; then
    echo "⚠️  docs/ folder not found. Running setup..."
    ./setup_docs_hosting.sh
fi

echo "🌐 Starting local preview server..."
echo ""
echo "📖 Documentation will be available at:"
echo "   http://localhost:8000/"
echo ""
echo "📁 Files included:"
ls -1 docs/*.md docs/*.html 2>/dev/null | wc -l | xargs echo "   Total files:"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start server
cd docs
python3 -m http.server 8000

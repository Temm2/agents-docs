#!/bin/bash
# Quick script to generate and open/share test reports

cd "$(dirname "$0")"

echo "🚀 Generating RAMM Agent Test Reports..."
source .venv/bin/activate
python -m app.report_generator

echo ""
echo "✅ Reports generated successfully!"
echo ""
echo "📁 Files created:"
echo "   - test_report.html (21KB)"
echo "   - test_report.md"
echo ""
echo "📤 Share options:"
echo "   1. Open in browser: open test_report.html"
echo "   2. Email the HTML file"
echo "   3. Upload to Google Drive/Dropbox"
echo "   4. Share via file sharing service"
echo ""
read -p "Open HTML report in browser now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open test_report.html
    echo "✅ Opened in browser!"
fi

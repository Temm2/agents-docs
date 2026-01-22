#!/usr/bin/env python3
"""
Generate a public shareable link for the test report.

Options:
1. GitHub Pages (permanent, free)
2. Python HTTP server + ngrok (temporary, requires ngrok)
3. Local server with instructions
"""

import os
import subprocess
import sys
from pathlib import Path

def check_ngrok():
    """Check if ngrok is installed."""
    try:
        result = subprocess.run(["ngrok", "version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def start_ngrok_tunnel(port=8000):
    """Start ngrok tunnel and return public URL."""
    print("🌐 Starting ngrok tunnel...")
    try:
        # Start ngrok in background
        process = subprocess.Popen(
            ["ngrok", "http", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for ngrok to start
        import time
        time.sleep(3)
        
        # Try to get the URL from ngrok API
        import urllib.request
        import json
        try:
            response = urllib.request.urlopen("http://localhost:4040/api/tunnels")
            data = json.loads(response.read())
            if data.get("tunnels"):
                public_url = data["tunnels"][0]["public_url"]
                return public_url, process
        except:
            pass
        
        print("⚠️  Could not get ngrok URL automatically.")
        print("   Check http://localhost:4040 for your ngrok dashboard")
        return None, process
        
    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")
        return None, None

def setup_github_pages():
    """Set up GitHub Pages hosting."""
    print("\n📦 GitHub Pages Setup (Permanent, Free)")
    print("=" * 60)
    print("\nSteps:")
    print("1. Create a GitHub repository (or use existing)")
    print("2. Create a 'docs' folder in your repo")
    print("3. Copy test_report.html to docs/index.html")
    print("4. Push to GitHub")
    print("5. Go to Settings → Pages → Source: /docs")
    print("6. Your report will be at: https://YOUR_USERNAME.github.io/REPO_NAME/")
    print("\nQuick commands:")
    print("  mkdir -p docs")
    print("  cp test_report.html docs/index.html")
    print("  git add docs/")
    print("  git commit -m 'Add test report'")
    print("  git push")
    print("\nThen enable GitHub Pages in repository settings!")

def start_local_server():
    """Start local HTTP server."""
    import http.server
    import socketserver
    import threading
    
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"\n🌐 Local server started on http://localhost:{PORT}")
        print(f"   Report: http://localhost:{PORT}/test_report.html")
        print("\n⚠️  This is only accessible on your local network.")
        print("   For public sharing, use GitHub Pages or ngrok.")
        print("\nPress Ctrl+C to stop the server.")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

def main():
    """Main function to generate shareable link."""
    
    # First, generate the report
    print("📊 Generating test report...")
    os.system("python -m app.report_generator")
    
    report_path = Path("test_report.html")
    if not report_path.exists():
        print("❌ Report generation failed!")
        return
    
    print(f"✅ Report generated: {report_path.absolute()}\n")
    
    print("=" * 60)
    print("🌐 PUBLIC SHARING OPTIONS")
    print("=" * 60)
    
    print("\n1️⃣  GitHub Pages (Recommended - Permanent & Free)")
    print("   - Best for long-term sharing")
    print("   - Free, permanent URL")
    print("   - Requires GitHub account")
    setup_github_pages()
    
    print("\n" + "=" * 60)
    
    if check_ngrok():
        print("\n2️⃣  Ngrok (Temporary - Quick Setup)")
        print("   - Instant public URL")
        print("   - Temporary (free tier)")
        print("   - Good for quick sharing")
        
        response = input("\nStart ngrok tunnel? (y/n): ")
        if response.lower() == 'y':
            # Start local server first
            import threading
            import http.server
            import socketserver
            
            PORT = 8000
            Handler = http.server.SimpleHTTPRequestHandler
            
            def start_server():
                with socketserver.TCPServer(("", PORT), Handler) as httpd:
                    httpd.serve_forever()
            
            server_thread = threading.Thread(target=start_server, daemon=True)
            server_thread.start()
            
            # Start ngrok
            public_url, ngrok_process = start_ngrok_tunnel(PORT)
            
            if public_url:
                print(f"\n✅ Public URL: {public_url}/test_report.html")
                print(f"\n📤 Share this link with anyone!")
                print(f"\n⚠️  This tunnel will close when you stop ngrok (Ctrl+C)")
                print("   Keep this terminal open while sharing.")
                
                try:
                    input("\nPress Enter to stop ngrok and server...")
                except KeyboardInterrupt:
                    pass
                
                if ngrok_process:
                    ngrok_process.terminate()
            else:
                print("\n⚠️  Check http://localhost:4040 for ngrok dashboard")
                input("\nPress Enter to stop...")
    else:
        print("\n2️⃣  Ngrok (Not Installed)")
        print("   Install: brew install ngrok (macOS) or download from ngrok.com")
        print("   Then run this script again for instant public URL")
    
    print("\n" + "=" * 60)
    print("\n3️⃣  Local Server (Same Network Only)")
    print("   - Only accessible on your local network")
    print("   - Good for team members on same WiFi")
    
    response = input("\nStart local server? (y/n): ")
    if response.lower() == 'y':
        start_local_server()
    
    print("\n" + "=" * 60)
    print("\n💡 TIP: For easiest sharing, use GitHub Pages!")
    print("   It's free, permanent, and works from anywhere.")

if __name__ == "__main__":
    main()

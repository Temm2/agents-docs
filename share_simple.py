#!/usr/bin/env python3
"""
Simplest way to share test reports - generates a shareable link or file.
"""

import os
import sys
from pathlib import Path

def main():
    """Generate report and provide simplest sharing options."""
    
    # Generate report
    print("📊 Generating test report...")
    os.system("python -m app.report_generator")
    
    report_path = Path("test_report.html")
    if not report_path.exists():
        print("❌ Report generation failed!")
        return
    
    print(f"\n✅ Report generated: {report_path.absolute()}")
    print(f"   Size: {report_path.stat().st_size / 1024:.1f} KB")
    
    print("\n" + "="*60)
    print("📤 SIMPLEST WAYS TO SHARE:")
    print("="*60)
    
    print("\n1️⃣  EMAIL (Easiest)")
    print(f"   Just attach: {report_path.name}")
    print("   Works in any email client")
    
    print("\n2️⃣  GOOGLE DRIVE / DROPBOX")
    print(f"   Upload: {report_path.name}")
    print("   Right-click → Share → Copy link")
    
    print("\n3️⃣  COPY FILE PATH")
    print(f"   Path: {report_path.absolute()}")
    print("   Share this path if on same network")
    
    print("\n4️⃣  VIEW LOCALLY")
    print("   Open in browser:")
    print(f"   file://{report_path.absolute()}")
    
    print("\n" + "="*60)
    
    # Try to open automatically
    try:
        import subprocess
        import platform
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", str(report_path)])
            print("\n✅ Opened in browser!")
        elif platform.system() == "Windows":
            os.startfile(str(report_path))
            print("\n✅ Opened in browser!")
        else:  # Linux
            subprocess.run(["xdg-open", str(report_path)])
            print("\n✅ Opened in browser!")
    except:
        pass

if __name__ == "__main__":
    main()

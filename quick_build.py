#!/usr/bin/env python3
"""
Quick build script for testing Nuitka compilation
"""

import subprocess
import sys
import os

def quick_build():
    """Quick build test with Nuitka"""
    print("🚀 Quick Nuitka Build Test")
    print("=" * 30)
    
    # Test with main.py only
    cmd = [
        "python", "-m", "nuitka",
        "--standalone",
        "--onefile", 
        "--enable-plugin=tk-inter",
        "--assume-yes-for-downloads",
        "--output-dir=test_dist",
        "--output-filename=ChessGame-Test.exe" if os.name == 'nt' else "--output-filename=ChessGame-Test",
        "main.py"
    ]
    
    if os.name == 'nt':  # Windows
        cmd.extend(["--msvc=latest", "--windows-console-mode=disable"])
    
    print(f"🔨 Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, text=True)
        print("✅ Quick build successful!")
        
        # Check if file exists
        test_file = "test_dist/ChessGame-Test.exe" if os.name == 'nt' else "test_dist/ChessGame-Test"
        if os.path.exists(test_file):
            size = os.path.getsize(test_file) / (1024 * 1024)  # MB
            print(f"📦 Executable created: {test_file} ({size:.1f} MB)")
        else:
            print("⚠️ Executable not found in expected location")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    quick_build()
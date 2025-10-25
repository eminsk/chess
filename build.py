#!/usr/bin/env python3
"""
Build script for Professional Chess Game

Creates standalone executables for the chess game using PyInstaller.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n🔨 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False


def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        return run_command(f"{sys.executable} -m pip install pyinstaller", "PyInstaller installation")


def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Cleaning {dir_name}/")
            shutil.rmtree(dir_name)


def get_platform_name():
    """Get platform-specific name"""
    system = platform.system().lower()
    if system == 'darwin':
        return 'macos'
    return system


def build_executables():
    """Build all executables"""
    platform_name = get_platform_name()
    
    # Common PyInstaller options
    common_opts = [
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm"
    ]
    
    # Add icon if available (Windows)
    icon_path = "assets/icon.ico"
    if os.path.exists(icon_path) and platform.system() == "Windows":
        common_opts.append(f"--icon={icon_path}")
    
    builds = [
        {
            'script': 'main.py',
            'name': f'ChessGame-{platform_name}',
            'description': 'Main game launcher'
        },
        {
            'script': 'chess_game.py',
            'name': f'ChessGame-SinglePlayer-{platform_name}',
            'description': 'Single player vs AI'
        },
        {
            'script': 'chess_multiplayer.py',
            'name': f'ChessGame-Multiplayer-{platform_name}',
            'description': 'Two player mode'
        }
    ]
    
    success_count = 0
    
    for build in builds:
        cmd_parts = [
            "pyinstaller",
            *common_opts,
            f"--name={build['name']}",
            build['script']
        ]
        
        cmd = " ".join(cmd_parts)
        
        if run_command(cmd, f"Building {build['description']}"):
            success_count += 1
        else:
            print(f"❌ Failed to build {build['description']}")
    
    return success_count == len(builds)


def create_portable_package():
    """Create a portable package"""
    platform_name = get_platform_name()
    package_name = f"ChessGame-{platform_name.title()}-Portable"
    
    print(f"\n📦 Creating portable package: {package_name}")
    
    # Create package directory
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    os.makedirs(package_name)
    
    # Copy executables
    dist_path = Path("dist")
    if dist_path.exists():
        for exe_file in dist_path.glob("*"):
            if exe_file.is_file():
                shutil.copy2(exe_file, package_name)
                print(f"📄 Copied {exe_file.name}")
    
    # Copy documentation
    docs_to_copy = ["README.md", "LICENSE"]
    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy2(doc, package_name)
            print(f"📄 Copied {doc}")
    
    # Create platform-specific README
    readme_content = f"""# Professional Chess Game - {platform_name.title()} Portable

## Quick Start

### Game Mode Selector (Recommended)
Run `ChessGame-{platform_name}` to open the game mode selector.

### Direct Launch
- `ChessGame-SinglePlayer-{platform_name}` - Play against AI
- `ChessGame-Multiplayer-{platform_name}` - Two player mode

## System Requirements
- No additional software required
- Fully portable - no installation needed

## Features
- Complete chess implementation with all rules
- Beautiful modern GUI with dark theme
- AI opponent for single player mode
- Local multiplayer for two players
- Move history and undo functionality

Enjoy playing chess! ♔♕♖♗♘♙
"""
    
    with open(f"{package_name}/README-Portable.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ Portable package created: {package_name}/")
    return package_name


def create_archive(package_name):
    """Create ZIP archive of the portable package"""
    archive_name = f"{package_name}.zip"
    
    print(f"\n🗜️ Creating archive: {archive_name}")
    
    try:
        shutil.make_archive(package_name, 'zip', package_name)
        print(f"✅ Archive created: {archive_name}")
        
        # Show archive size
        size = os.path.getsize(archive_name) / (1024 * 1024)  # MB
        print(f"📊 Archive size: {size:.1f} MB")
        
        return archive_name
    except Exception as e:
        print(f"❌ Failed to create archive: {e}")
        return None


def main():
    """Main build process"""
    print("🎯 Professional Chess Game - Build Script")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"🐍 Python version: {sys.version}")
    print(f"💻 Platform: {platform.system()} {platform.machine()}")
    
    # Install dependencies
    if not install_pyinstaller():
        print("❌ Failed to install PyInstaller")
        sys.exit(1)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build executables
    if not build_executables():
        print("❌ Build failed")
        sys.exit(1)
    
    # Create portable package
    package_name = create_portable_package()
    
    # Create archive
    archive_name = create_archive(package_name)
    
    print("\n🎉 Build completed successfully!")
    print(f"📦 Portable package: {package_name}/")
    if archive_name:
        print(f"🗜️ Archive: {archive_name}")
    
    print("\n🚀 Ready to distribute!")


if __name__ == "__main__":
    main()
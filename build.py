#!/usr/bin/env python3
"""
Build script for Professional Chess Game

Creates standalone executables for the chess game using Nuitka.
Nuitka compiles Python to C++ for better performance and smaller executables.
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
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        return False


def install_nuitka():
    """Install Nuitka and required dependencies"""
    try:
        import nuitka
        print("✅ Nuitka is already installed")
        return True
    except ImportError:
        print("📦 Installing Nuitka...")
        
        # Check if uv is available
        try:
            subprocess.run("uv --version", shell=True, check=True, capture_output=True)
            print("🚀 Using uv for package installation")
            return run_command("uv add nuitka ordered-set", "Installing Nuitka with uv")
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to pip
            print("📦 Using pip for package installation")
            packages = ["nuitka", "ordered-set"]
            for package in packages:
                if not run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}"):
                    return False
            return True


def install_compiler():
    """Check and install C++ compiler if needed"""
    system = platform.system()
    
    if system == "Windows":
        print("🔧 Checking for C++ compiler on Windows...")
        # Try to find Visual Studio Build Tools or MinGW
        try:
            result = subprocess.run("where cl", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Visual Studio C++ compiler found")
                return True
        except:
            pass
        
        try:
            result = subprocess.run("where gcc", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MinGW GCC compiler found")
                return True
        except:
            pass
        
        print("⚠️ No C++ compiler found. Nuitka will try to download MinGW automatically.")
        print("   If build fails, install Visual Studio Build Tools or MinGW manually.")
        return True
        
    elif system == "Linux":
        print("🔧 Checking for C++ compiler on Linux...")
        try:
            result = subprocess.run("which gcc", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ GCC compiler found")
                return True
            else:
                print("❌ GCC not found. Please install: sudo apt-get install gcc g++ (Ubuntu/Debian)")
                return False
        except:
            return False
            
    elif system == "Darwin":  # macOS
        print("🔧 Checking for C++ compiler on macOS...")
        try:
            result = subprocess.run("which clang", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Clang compiler found")
                return True
            else:
                print("❌ Clang not found. Please install Xcode Command Line Tools: xcode-select --install")
                return False
        except:
            return False
    
    return True


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
    """Build all executables using Nuitka"""
    platform_name = get_platform_name()
    
    # Create dist directory if it doesn't exist
    os.makedirs("dist", exist_ok=True)
    
    # Common Nuitka options
    common_opts = [
        "--standalone",
        "--onefile",
        "--enable-plugin=tk-inter",
        "--assume-yes-for-downloads",
        "--output-dir=dist"
    ]
    
    # Add icon if available (Windows)
    icon_path = "assets/icon.ico"
    if os.path.exists(icon_path) and platform.system() == "Windows":
        common_opts.append(f"--windows-icon-from-ico={icon_path}")
    
    # Platform-specific optimizations
    if platform.system() == "Windows":
        common_opts.extend([
            "--mingw64",  # Use MinGW64 compiler (auto-download)
            "--windows-console-mode=disable"
        ])
    
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
        # Build with Nuitka
        cmd_parts = [
            f"{sys.executable} -m nuitka",
            *common_opts,
            f"--output-filename={build['name']}",
            build['script']
        ]
        
        cmd = " ".join(cmd_parts)
        
        if run_command(cmd, f"Building {build['description']} with Nuitka"):
            success_count += 1
            
            # Move the executable to dist folder with correct name
            source_name = build['script'].replace('.py', '.exe' if platform.system() == "Windows" else '')
            target_name = f"{build['name']}.exe" if platform.system() == "Windows" else build['name']
            
            # Find the generated executable
            for root, dirs, files in os.walk("dist"):
                for file in files:
                    if file.startswith(build['script'].replace('.py', '')):
                        source_path = os.path.join(root, file)
                        target_path = os.path.join("dist", target_name)
                        if source_path != target_path:
                            shutil.move(source_path, target_path)
                        break
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
    print("🎯 Professional Chess Game - Build Script (Nuitka)")
    print("=" * 55)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"🐍 Python version: {sys.version}")
    print(f"💻 Platform: {platform.system()} {platform.machine()}")
    
    # Check and install C++ compiler
    if not install_compiler():
        print("❌ C++ compiler not available")
        sys.exit(1)
    
    # Install Nuitka
    if not install_nuitka():
        print("❌ Failed to install Nuitka")
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
    print("\n💡 Nuitka Benefits:")
    print("   ✨ Faster startup and execution")
    print("   📦 Smaller executable size")
    print("   🔒 Better code protection")
    print("   🚀 Native C++ compilation")


if __name__ == "__main__":
    main()
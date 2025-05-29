#!/usr/bin/env python3
"""
Test script to verify AI Helper setup
"""

import sys
import subprocess

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import textual
        print("✅ textual imported successfully")
    except ImportError:
        print("❌ textual not found - run: pip install textual")
        return False
    
    try:
        from google import genai
        print("✅ google-genai imported successfully")
    except ImportError:
        print("❌ google-genai not found - run: pip install google-genai")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError:
        print("❌ python-dotenv not found - run: pip install python-dotenv")
        return False
    
    try:
        import pydantic
        print("✅ pydantic imported successfully")
    except ImportError:
        print("❌ pydantic not found - run: pip install pydantic")
        return False
    
    return True

def test_system_tools():
    """Test if required system tools are available"""
    print("\nTesting system tools...")
    
    tools = ["xdotool", "xclip"]
    all_available = True
    
    for tool in tools:
        try:
            subprocess.run([tool, "--version"], 
                         capture_output=True, check=True)
            print(f"✅ {tool} is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"⚠️ {tool} not found - install with: sudo apt install {tool}")
            all_available = False
    
    return all_available

def test_env_file():
    """Test if .env file exists and has API key"""
    print("\nTesting environment setup...")
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
            if 'GEMINI_API_KEY' in content:
                print("✅ .env file found with GEMINI_API_KEY")
                return True
            else:
                print("❌ .env file found but no GEMINI_API_KEY")
                return False
    except FileNotFoundError:
        print("❌ .env file not found")
        print("Create it with: echo 'GEMINI_API_KEY=your_key_here' > .env")
        return False

def main():
    """Run all tests"""
    print("🧪 AI Helper Setup Test\n")
    
    imports_ok = test_imports()
    tools_ok = test_system_tools()
    env_ok = test_env_file()
    
    print("\n" + "="*50)
    
    if imports_ok and tools_ok and env_ok:
        print("🎉 All tests passed! You're ready to use the AI Helper.")
        print("Run: python ai_helper.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        
        if not imports_ok:
            print("\n📦 To install Python dependencies:")
            print("pip install -r requirements.txt")
        
        if not tools_ok:
            print("\n🔧 To install system tools:")
            print("sudo apt install xdotool xclip  # Ubuntu/Debian")
        
        if not env_ok:
            print("\n🔑 To set up API key:")
            print("echo 'GEMINI_API_KEY=your_actual_key' > .env")

if __name__ == "__main__":
    main() 
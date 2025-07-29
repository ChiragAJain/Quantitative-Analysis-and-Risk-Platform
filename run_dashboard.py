#!/usr/bin/env python3
"""
Stock Market Analysis Dashboard Runner

This script launches the interactive stock market analysis dashboard.
Make sure to install requirements first: pip install -r requirements.txt
"""

import sys
import subprocess
import importlib.util

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'yfinance', 'pandas', 'numpy', 'plotly', 
        'dash', 'dash_bootstrap_components', 'scipy'
    ]
    
    missing_packages = []
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   • {package}")
        print("\n💡 Install them with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    print("🔍 Checking requirements...")
    
    if not check_requirements():
        sys.exit(1)
    
    print("✅ All requirements satisfied!")
    print("🚀 Launching Stock Market Analysis Dashboard...\n")
    
    try:
        # Import and run the dashboard
        from dashboard import app
        app.run(debug=False, host='127.0.0.1', port=8050)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Quick deployment script for Stock Market Analysis Dashboard
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_git_status():
    """Check if we're in a git repository"""
    if not os.path.exists('.git'):
        print("❌ Not in a git repository. Please run 'git init' first.")
        return False
    return True

def deploy_heroku():
    """Deploy to Heroku"""
    print("\n🚀 Deploying to Heroku...")
    
    if not check_git_status():
        return False
    
    # Check if heroku CLI is installed
    if not run_command("heroku --version", "Checking Heroku CLI"):
        print("💡 Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # Check if logged in
    if not run_command("heroku auth:whoami", "Checking Heroku login"):
        print("💡 Please login: heroku login")
        return False
    
    # Get app name
    app_name = input("Enter your Heroku app name (or press Enter to create new): ").strip()
    
    if app_name:
        # Check if app exists
        if run_command(f"heroku apps:info {app_name}", f"Checking app {app_name}"):
            print(f"📱 Using existing app: {app_name}")
        else:
            print(f"❌ App {app_name} not found")
            return False
    else:
        # Create new app
        app_name = input("Enter name for new app: ").strip()
        if not app_name:
            print("❌ App name required")
            return False
        
        if not run_command(f"heroku create {app_name}", f"Creating app {app_name}"):
            return False
    
    # Add, commit, and push
    run_command("git add .", "Adding files")
    run_command('git commit -m "Deploy stock market dashboard"', "Committing changes")
    
    if run_command("git push heroku main", "Deploying to Heroku"):
        print(f"\n🎉 Deployment successful!")
        print(f"🌐 Your dashboard is available at: https://{app_name}.herokuapp.com")
        return True
    
    return False

def deploy_docker():
    """Build and test Docker image"""
    print("\n🐳 Building Docker image...")
    
    if not run_command("docker --version", "Checking Docker"):
        print("💡 Install Docker: https://docs.docker.com/get-docker/")
        return False
    
    # Build image
    if not run_command("docker build -t stock-dashboard .", "Building Docker image"):
        return False
    
    print("\n✅ Docker image built successfully!")
    print("🔧 To run locally: docker run -p 8080:8080 stock-dashboard")
    print("🌐 Then visit: http://localhost:8080")
    
    # Ask if user wants to run locally
    if input("\nRun locally now? (y/n): ").lower() == 'y':
        print("🚀 Starting container... (Press Ctrl+C to stop)")
        os.system("docker run -p 8080:8080 stock-dashboard")
    
    return True

def main():
    print("🎯 Stock Market Dashboard Deployment Tool")
    print("=" * 50)
    
    print("\nAvailable deployment options:")
    print("1. Heroku (recommended for beginners)")
    print("2. Docker (for any cloud provider)")
    print("3. Show deployment guide")
    print("4. Exit")
    
    while True:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            deploy_heroku()
            break
        elif choice == '2':
            deploy_docker()
            break
        elif choice == '3':
            print("\n📖 Check DEPLOYMENT.md for detailed instructions")
            print("🌐 Supported platforms: Heroku, Railway, Render, Docker")
            break
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()
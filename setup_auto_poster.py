#!/usr/bin/env python3
"""
TikTok & YouTube Auto-Poster Setup Script
Helps you configure the auto-poster for your accounts

Setup: python setup_auto_poster.py

⚠️ IMPORTANT: Read the setup instructions carefully before proceeding!
"""

import os
import json

def print_header():
    print("""
╔══════════════════════════════════════════════════════════════╗
║     🎬 TikTok & YouTube Auto-Poster Setup                     ║
║        Reddit Video Maker Bot - Auto Upload                  ║
╚══════════════════════════════════════════════════════════════╝
""")

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required = ["google-api-python-client", "google-auth-httplib2", "google-auth-oauthlib"]
    missing = []
    
    for package in required:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages! Install with:")
        print(f"    pip install {' '.join(missing)}")
        return False
    
    return True

def setup_youtube():
    """Guide user through YouTube API setup"""
    print("\n" + "="*60)
    print("📺 YOUTUBE API SETUP")
    print("="*60)
    
    print("""
To post to YouTube automatically, you need to:

1️⃣  Go to: https://console.cloud.google.com/

2️⃣  Create a new project (or select existing)

3️⃣  Enable YouTube Data API v3:
    - Search "YouTube Data API v3"
    - Click "Enable"

4️⃣  Create OAuth 2.0 credentials:
    - Go to "APIs & Services" → "Credentials"
    - Click "Create Credentials" → "OAuth client ID"
    - Application type: "Desktop app"
    - Name it: "Reddit Video Auto-Poster"

5️⃣  Download the JSON file:
    - Download the client_secret.json
    - Rename it to: client_secrets.json
    - Place it in the same folder as this script

6️⃣  First run will prompt you to authorize:
    - Visit the URL shown
    - Grant permissions
    - Copy the code back
""")
    
    input("\nPress ENTER when you've downloaded client_secrets.json...")

def setup_tiktok():
    """Guide user through TikTok setup"""
    print("\n" + "="*60)
    print("📱 TIKTOK SETUP")
    print("="*60)
    
    print("""
⚠️  TikTok does NOT have an official API for posting videos.

You have these options:

🎯 OPTION 1: Third-Party Services (RECOMMENDED)
    - Buffer (buffer.com)
    - Later (later.com)
    - SocialBee (socialbee.com)
    - These have built-in TikTok integration

🎯 OPTION 2: Browser Automation
    - Can automate posting via Selenium/Playwright
    - Requires session cookies
    - More complex setup

🎯 OPTION 3: Manual Posting
    - Download videos locally
    - Post manually to TikTok app

For now, we'll set up YouTube which is fully supported.
You can add TikTok automation later.
""")
    
    input("\nPress ENTER to continue...")

def create_cron_job():
    """Create cron job for daily posting"""
    print("\n" + "="*60)
    print("⏰ AUTOMATION SETUP (Linux/Mac)")
    print("="*60)
    
    print("""
To run automatically every day, add a cron job:

1️⃣  Open terminal and type:
    crontab -e

2️⃣  Add this line for 9 AM daily:
    0 9 * * * cd /path/to/RedditVideoMakerBot && python3 auto_poster.py

3️⃣  Save and exit

For Windows, use Task Scheduler:
    1. Open Task Scheduler
    2. Create Basic Task
    3. Set trigger to daily at 9 AM
    4. Set action to run: python auto_poster.py
""")

def update_config():
    """Update the auto poster configuration"""
    config = {
        "videos_folder": "./video_output",
        "posted_folder": "./posted_videos",
        "drafts_folder": "./drafts",
        "daily_limit": 5,
        "min_interval_hours": 2,
        "youtube": {
            "enabled": True,
            "client_secrets_file": "client_secrets.json",
            "schedule": "12:00"
        },
        "tiktok": {
            "enabled": False,  # Disabled until user sets up
            "session_cookies": "",
            "schedule": "09:00"
        },
        "accounts": {
            "tiktok": "@casper.black07",
            "youtube": "@sinname2015"
        }
    }
    
    with open("auto_post_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ Configuration saved to auto_post_config.json")
    print("   Update the paths and credentials as needed")

def print_summary():
    """Print setup summary"""
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    
    print("""
📋 NEXT STEPS:

1️⃣  Configure YouTube API:
    - Download client_secrets.json
    - Place it in this folder

2️⃣  Update video folder:
    - Point videos_folder to where RedditVideoMakerBot saves videos
    - Default: ./video_output

3️⃣  Run the poster:
    - python auto_poster.py

4️⃣  Schedule automation:
    - Use cron (Linux/Mac) or Task Scheduler (Windows)

📱 Your accounts:
    TikTok: @casper.black07
    YouTube: @sinname2015

⚠️  REMEMBER:
    - Post quality content
    - Respect platform rules
    - Don't spam - 5 videos/day is a good limit
    - Engage with your audience!
""")

def main():
    print_header()
    
    print("\n🔧 Starting setup...\n")
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Setup YouTube
    setup_youtube()
    
    # Setup TikTok
    setup_tiktok()
    
    # Create folders
    print("\n📁 Creating folders...")
    for folder in ["video_output", "posted_videos", "drafts"]:
        os.makedirs(folder, exist_ok=True)
        print(f"  ✅ {folder}/")
    
    # Update configuration
    update_config()
    
    # Cron job info
    create_cron_job()
    
    # Summary
    print_summary()

if __name__ == "__main__":
    main()
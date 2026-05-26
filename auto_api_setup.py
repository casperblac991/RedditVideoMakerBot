#!/usr/bin/env python3
"""
🚀 AUTOMATED API SETUP SCRIPT
==============================
This script will help you get ALL APIs for your content factory

Your Accounts:
- YouTube: @sinname2015
- TikTok: @casper.black07
"""

import os
import json
import webbrowser
import time
from pathlib import Path

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🔑  COMPLETE API SETUP FOR CONTENT FACTORY                 ║
║                                                              ║
║   📺 YouTube: @sinname2015                                   ║
║   📱 TikTok: @casper.black07                                  ║
║   📱 Reddit: (need account)                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def open_links():
    """Open all necessary API setup pages in browser"""
    
    print("\n📌 Opening all necessary pages in your browser...\n")
    
    links = {
        "1. Reddit App Creation": "https://www.reddit.com/prefs/apps",
        "2. Google Cloud Console": "https://console.cloud.google.com/",
        "3. TikTok Developer": "https://developers.tiktok.com/",
    }
    
    for name, url in links.items():
        print(f"Opening: {name}")
        webbrowser.open(url)
        time.sleep(1)
    
    print("\n✅ All pages opened in your browser!")

def step_by_step_guide():
    """Print complete step-by-step guide"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    📱 REDDIT API SETUP                        ║
╚══════════════════════════════════════════════════════════════╝

🔗 URL: https://www.reddit.com/prefs/apps

STEP 1: Login to Reddit
   → Use any Reddit account (can be new)

STEP 2: Create New App
   → Click "Create App" button
   → Type: "script"

STEP 3: Fill Details
   name: ContentFactoryBot
   description: AI Content Factory for videos
   redirect uri: http://localhost:8080

STEP 4: Copy Credentials
   → CLIENT ID: (under app name, 12 chars)
   → CLIENT SECRET: (long string)

STEP 5: Save to api_config.json

══════════════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════════╗
║                    📺 YOUTUBE API SETUP                      ║
╚══════════════════════════════════════════════════════════════╝

🔗 URL: https://console.cloud.google.com/

STEP 1: Login to Google
   → Use the Google account for @sinname2015

STEP 2: Create New Project
   → Click "Select a project" (top bar)
   → Click "New Project"
   → Name: "ContentFactory"
   → Click "Create"

STEP 3: Enable YouTube API
   → In sidebar: "APIs & Services" → "Library"
   → Search: "YouTube Data API v3"
   → Click "Enable"

STEP 4: Create OAuth Credentials
   → "APIs & Services" → "Credentials"
   → Click "Create Credentials" → "OAuth client ID"
   → Type: "Desktop app"
   → Name: "ContentFactoryUploader"
   → Click "Create"

STEP 5: Download JSON
   → Click "Download JSON" button
   → Rename to: youtube_credentials.json
   → Place in this project folder

STEP 6: First Run Auth
   → Run: python ai_content_factory.py
   → Browser will open for auth
   → Copy code and paste back

══════════════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════════╗
║                    📱 TIKTOK API SETUP                        ║
╚══════════════════════════════════════════════════════════════╝

⚠️ IMPORTANT: TikTok has VERY LIMITED API access

OPTIONS:

Option A: Official TikTok API (Requires Application)
   🔗 URL: https://developers.tiktok.com/
   → Apply for Creator API access
   → May take weeks for approval
   → Limited to approved partners

Option B: Browser Automation (Recommended)
   ✅ Already configured in our system!
   → No API key needed
   → Uses saved browser session

To use Browser Automation:
   1. Run: python ai_content_factory.py
   2. First time: Login to TikTok manually
   3. Session is saved automatically
   4. Future posts are automatic

Option C: Third-Party Tools
   → Buffer.com (free tier)
   → Later.com (free tier)
   → SocialBee.com (trial)

══════════════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════════╗
║                    📋 CONFIG FILE SETUP                      ║
╚══════════════════════════════════════════════════════════════╝

Create a file called: api_config.json

Paste this template:

{
  "reddit": {
    "client_id": "YOUR_REDDIT_CLIENT_ID",
    "client_secret": "YOUR_REDDIT_CLIENT_SECRET",
    "user_agent": "ContentFactoryBot/1.0"
  },
  "youtube": {
    "credentials_file": "youtube_credentials.json"
  },
  "tiktok": {
    "enabled": true,
    "session_file": "tiktok_session.json"
  },
  "accounts": {
    "youtube_channel": "@sinname2015",
    "tiktok_username": "@casper.black07"
  }
}

══════════════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════════╗
║                    🚀 QUICK START                            ║
╚══════════════════════════════════════════════════════════════╝

After getting credentials:

1. Create api_config.json with Reddit credentials

2. Download youtube_credentials.json from Google Cloud

3. Run the demo (works without APIs):
   python ai_demo_mode.py

4. For full automation:
   python ai_content_factory.py

5. For TikTok:
   - First run opens browser
   - Login @casper.black07
   - Session auto-saves

══════════════════════════════════════════════════════════════════
    """)

def create_config_template():
    """Create template config file"""
    
    config = {
        "reddit": {
            "client_id": "",
            "client_secret": "",
            "user_agent": "ContentFactoryBot/1.0"
        },
        "youtube": {
            "credentials_file": "youtube_credentials.json"
        },
        "tiktok": {
            "enabled": True,
            "session_file": "tiktok_session.json"
        },
        "accounts": {
            "youtube_channel": "@sinname2015",
            "tiktok_username": "@casper.black07"
        }
    }
    
    with open("api_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ Created api_config.json template")
    print("   Please edit this file and add your credentials!")

def main():
    print_banner()
    
    print("""
What would you like to do?

1️⃣  Open all API setup pages in browser
2️⃣  Show step-by-step guide
3️⃣  Create config template
4️⃣  All of the above (recommended)

Enter number (1-4):
    """)
    
    choice = input("> ").strip()
    
    if choice == "1":
        open_links()
    elif choice == "2":
        step_by_step_guide()
    elif choice == "3":
        create_config_template()
    elif choice == "4":
        open_links()
        time.sleep(2)
        step_by_step_guide()
        create_config_template()
        print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ All done! 

Next steps:
1. Open browser tabs (already opened)
2. Get your API credentials
3. Add them to api_config.json
4. Download youtube_credentials.json
5. Run: python ai_demo_mode.py

Good luck! 🚀
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
    else:
        print("Invalid choice. Running all options...")
        choice = "4"
    
    input("\nPress ENTER to exit...")

if __name__ == "__main__":
    main()
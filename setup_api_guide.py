#!/usr/bin/env python3
"""
🔑 API SETUP GUIDE & CREDENTIALS CONFIGURATOR
=============================================
Complete step-by-step guide to get all APIs for your content factory

Your Accounts:
- YouTube: @sinname2015
- TikTok: @casper.black07
"""

import os
import json
import webbrowser
from pathlib import Path
from datetime import datetime

# ============================================
# COLORS FOR TERMINAL
# ============================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.HEADER}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.HEADER}{'='*60}{Colors.END}\n")

def print_step(num, text):
    print(f"{Colors.CYAN}📌 Step {num}: {text}{Colors.END}")

def print_link(url, description=""):
    print(f"{Colors.GREEN}  🔗 {url}{Colors.END}")
    if description:
        print(f"     {description}")

def print_note(text):
    print(f"{Colors.YELLOW}  ℹ️  {text}{Colors.END}")

def print_success(text):
    print(f"{Colors.GREEN}  ✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}  ❌ {text}{Colors.END}")

# ============================================
# REDDIT API SETUP
# ============================================

def setup_reddit_api():
    """Guide user through Reddit API setup"""
    
    print_header("📱 REDDIT API SETUP")
    
    print("""
To fetch stories from Reddit automatically, you need Reddit API credentials.

Follow these steps:
    """)
    
    print_step(1, "Go to Reddit Apps")
    print_link("https://www.reddit.com/prefs/apps")
    print_note("Login to your Reddit account first")
    
    print("\n" + "-"*60)
    print_step(2, "Create a New Application")
    print("""
Click the 'Create App' or 'Create Another App' button

Fill in:
- name: "Content Factory Bot" (or any name)
- app type: Select "script"
- description: "AI Content Factory for video creation"
- about URL: (leave empty or put #)
- redirect uri: "http://localhost:8080"
    """)
    
    print("\n" + "-"*60)
    print_step(3, "Get Your Credentials")
    print("""
After creating the app, you'll see:
- CLIENT ID: (under the app name, looks like: 12abc3def456)
- CLIENT SECRET: (the long string below)

COPY THESE VALUES!
    """)
    
    # Get credentials from user
    print("\n" + "-"*60)
    print_step(4, "Enter Your Credentials")
    
    client_id = input("Enter Reddit CLIENT ID: ").strip()
    client_secret = input("Enter Reddit CLIENT SECRET: ").strip()
    
    if client_id and client_secret:
        print_success("Reddit API credentials saved!")
        
        # Save to config
        config = load_config()
        config["reddit"] = {
            "client_id": client_id,
            "client_secret": client_secret,
            "user_agent": "ContentFactoryBot/1.0"
        }
        save_config(config)
        
        return True
    else:
        print_error("Invalid credentials!")
        return False

# ============================================
# YOUTUBE API SETUP
# ============================================

def setup_youtube_api():
    """Guide user through YouTube API setup"""
    
    print_header("📺 YOUTUBE API SETUP")
    
    print("""
To upload videos automatically to YouTube, you need Google Cloud API credentials.

Follow these steps:
    """)
    
    print_step(1, "Go to Google Cloud Console")
    print_link("https://console.cloud.google.com/")
    print_note("Login with your Google account (@sinname2015)")
    
    print("\n" + "-"*60)
    print_step(2, "Create a New Project")
    print("""
Click "Select a project" at the top
Click "New Project"
Name it: "Content Factory"
Click "Create"
    """)
    
    print("\n" + "-"*60)
    print_step(3, "Enable YouTube Data API v3")
    print("""
In the sidebar, go to "APIs & Services" > "Library"
Search for "YouTube Data API v3"
Click on it
Click "Enable"
    """)
    
    print("\n" + "-"*60)
    print_step(4, "Create OAuth Credentials")
    print("""
Go to "APIs & Services" > "Credentials"
Click "Create Credentials" > "OAuth client ID"
Application type: "Desktop app"
Name: "Content Factory Uploader"
Click "Create"

A popup will show your:
- Client ID
- Client Secret

DOWNLOAD THE JSON FILE!
    """)
    
    print("\n" + "-"*60)
    print_step(5, "Save the Credentials")
    print("""
Download the JSON file Google gives you.
Rename it to: youtube_credentials.json
Place it in the same folder as this script

Or copy the content below and paste it:
    """)
    
    # Check if file exists
    creds_path = Path("youtube_credentials.json")
    if creds_path.exists():
        print_success("youtube_credentials.json found!")
        return True
    else:
        print_note("File not found yet. Create it after downloading from Google.")
        return False

# ============================================
# TIKTOK SETUP
# ============================================

def setup_tiktok():
    """Guide user through TikTok setup"""
    
    print_header("📱 TIKTOK SETUP")
    
    print("""
⚠️ IMPORTANT: TikTok does NOT have an official public API for posting videos.

You have these options:
    """)
    
    print_step(1, "Option A: Third-Party Services (RECOMMENDED)")
    print("""
Services that support TikTok posting:
- Buffer (buffer.com) - Free up to 3 accounts
- Later (later.com) - Free tier available
- SocialBee (socialbee.com) - 7-day free trial

These services have TikTok integration built-in!
    """)
    
    print("\n" + "-"*60)
    print_step(2, "Option B: Browser Automation")
    print("""
We can automate TikTok posting using browser automation.
This requires:
1. Login to TikTok in the browser
2. Save the session
3. System will use saved session for posting

This is what we'll use for now.
    """)
    
    print("\n" + "-"*60)
    print_step(3, "To Enable TikTok Automation")
    print("""
1. Run the main script
2. It will open TikTok in browser
3. Login manually with @casper.black07
4. The session will be saved automatically
5. Next time, no login needed!
    """)
    
    return True

# ============================================
# CONFIG MANAGEMENT
# ============================================

def load_config():
    """Load existing config or create new"""
    config_file = Path("api_config.json")
    
    if config_file.exists():
        with open(config_file) as f:
            return json.load(f)
    
    return {
        "reddit": {},
        "youtube": {},
        "tiktok": {"enabled": True, "username": "casper.black07"},
        "accounts": {
            "youtube": "@sinname2015",
            "tiktok": "@casper.black07"
        }
    }

def save_config(config):
    """Save config to file"""
    with open("api_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print_success("Configuration saved to api_config.json")

# ============================================
# TEST CREDENTIALS
# ============================================

def test_reddit():
    """Test Reddit API"""
    config = load_config()
    
    if not config.get("reddit", {}).get("client_id"):
        print_error("Reddit credentials not configured")
        return False
    
    try:
        import praw
        
        reddit = praw.Reddit(
            client_id=config["reddit"]["client_id"],
            client_secret=config["reddit"]["client_secret"],
            user_agent="ContentFactoryBot/1.0"
        )
        
        # Test by fetching subreddit info
        subreddit = reddit.subreddit("AskReddit")
        posts = list(subreddit.hot(limit=1))
        
        print_success("Reddit API working! Fetched sample post.")
        return True
        
    except Exception as e:
        print_error(f"Reddit API error: {e}")
        return False

def test_youtube():
    """Test YouTube API"""
    creds_file = Path("youtube_credentials.json")
    
    if not creds_file.exists():
        print_error("youtube_credentials.json not found")
        return False
    
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        creds = Credentials.from_authorized_user_file(
            str(creds_file),
            ['https://www.googleapis.com/auth/youtube.upload']
        )
        
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Test by getting channel info
        response = youtube.channels().list(
            part='snippet',
            mine=True
        ).execute()
        
        if response.get('items'):
            channel_name = response['items'][0]['snippet']['title']
            print_success(f"YouTube API working! Channel: {channel_name}")
            return True
        
        return False
        
    except FileNotFoundError:
        print_error("youtube_credentials.json not found")
        return False
    except Exception as e:
        print_error(f"YouTube API error: {e}")
        return False

# ============================================
# MAIN SETUP FLOW
# ============================================

def main():
    print(f"""
{Colors.HEADER}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🔑 API SETUP WIZARD                                        ║
║   Complete Guide to Get All APIs                             ║
║                                                              ║
║   Your Accounts:                                             ║
║   - YouTube: @sinname2015                                    ║
║   - TikTok: @casper.black07                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
    """)
    
    print("""
This wizard will help you set up all the APIs needed for:
✅ Fetching Reddit stories automatically
✅ Uploading videos to YouTube
✅ Posting to TikTok

Let's get started!
    """)
    
    input("Press ENTER to begin...")
    
    # Reddit Setup
    print("\n" + "="*60)
    reddit_ok = setup_reddit_api()
    
    # Test Reddit
    if reddit_ok:
        print("\nTesting Reddit connection...")
        test_reddit()
    
    input("\nPress ENTER to continue to YouTube setup...")
    
    # YouTube Setup
    print("\n" + "="*60)
    setup_youtube_api()
    
    # Test YouTube
    print("\nTesting YouTube connection...")
    test_youtube()
    
    input("\nPress ENTER to continue to TikTok setup...")
    
    # TikTok Setup
    print("\n" + "="*60)
    setup_tiktok()
    
    # Final summary
    print_header("📋 SETUP COMPLETE!")
    
    config = load_config()
    
    print(f"""
{Colors.CYAN}Reddit API:{Colors.END}
  - Client ID: {'✅ Configured' if config['reddit'].get('client_id') else '❌ Not set'}

{Colors.CYAN}YouTube API:{Colors.END}
  - Credentials: {'✅ Found' if Path('youtube_credentials.json').exists() else '❌ Not found'}

{Colors.CYAN}TikTok:{Colors.END}
  - Browser automation: ✅ Enabled
  - Username: @casper.black07

{Colors.GREEN}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS:

1. If YouTube credentials missing:
   - Go to Google Cloud Console
   - Download OAuth JSON
   - Save as youtube_credentials.json

2. Run the content factory:
   python ai_content_factory.py

3. For TikTok:
   - First run will prompt browser login
   - Session will be saved automatically

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{Colors.END}
    """)

if __name__ == "__main__":
    main()
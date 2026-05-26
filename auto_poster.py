#!/usr/bin/env python3
"""
TikTok & YouTube Auto Poster
Posts videos automatically from the Reddit Video Maker Bot output folder

⚠️ IMPORTANT NOTES:
- This script automates posting to TikTok and YouTube
- You need API credentials for each platform
- Respect platform terms of service and rate limits
- Ensure you have rights to all content you post
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_post.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    "videos_folder": "./video_output",  # Where RedditVideoMakerBot saves videos
    "posted_folder": "./posted_videos",   # Move posted videos here
    "drafts_folder": "./drafts",          # Drafts for review before posting
    
    # TikTok API Configuration (via third-party services)
    "tiktok": {
        "enabled": False,
        "session_cookies": "",  # TikTok session cookies
        "schedule": "09:00"     # Post at 9 AM daily
    },
    
    # YouTube API Configuration
    "youtube": {
        "enabled": False,
        "client_secrets_file": "client_secrets.json",
        "channel_id": "",       # Your YouTube channel ID
        "schedule": "12:00"     # Post at 12 PM daily
    },
    
    # Posting schedule
    "daily_limit": 5,           # Max videos per day
    "min_interval_hours": 2,    # Minimum hours between posts
}

def setup_folders():
    """Create necessary folders"""
    folders = [
        CONFIG["videos_folder"],
        CONFIG["posted_folder"],
        CONFIG["drafts_folder"]
    ]
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured folder exists: {folder}")

def get_pending_videos():
    """Get list of videos ready to be posted"""
    videos = []
    folder = Path(CONFIG["videos_folder"])
    
    if folder.exists():
        for video_file in folder.glob("*.mp4"):
            videos.append({
                "path": str(video_file),
                "name": video_file.stem,
                "size": video_file.stat().st_size,
                "created": datetime.fromtimestamp(video_file.stat().st_ctime)
            })
    
    # Sort by creation time (oldest first)
    videos.sort(key=lambda x: x["created"])
    
    logger.info(f"Found {len(videos)} pending videos")
    return videos

def select_best_video(videos):
    """
    Select the best video based on engagement potential:
    - Prefer videos with engaging titles (drama, mystery, etc.)
    - Shorter videos (30-60 seconds) for better retention
    """
    # Keywords that indicate high-engagement content
    engagement_keywords = ["update", "story", "confession", "revenge", "surprise", 
                          "wrong", "crazy", "insane", "omg", "wait", "finally"]
    
    for video in videos:
        title_lower = video["name"].lower()
        for keyword in engagement_keywords:
            if keyword in title_lower:
                logger.info(f"Selected high-engagement video: {video['name']}")
                return video
    
    # Return first video if no high-engagement found
    return videos[0] if videos else None

# ==========================================
# TIKTOK POSTING (using unofficial methods)
# ==========================================

def post_to_tiktok(video_path, title, tags):
    """
    Post video to TikTok
    
    ⚠️ WARNING: TikTok doesn't have an official public API for posting
    You can use:
    1. Third-party services (like SocialBee, Later, etc.)
    2. Browser automation (requires session cookies)
    
    This is a template - actual implementation requires additional setup
    """
    if not CONFIG["tiktok"]["enabled"]:
        logger.info("TikTok posting is disabled")
        return False
    
    logger.info(f"Would post to TikTok: {video_path}")
    logger.info(f"Title: {title}")
    logger.info(f"Tags: {tags}")
    
    # TODO: Implement TikTok posting logic
    # Options:
    # 1. Use TikTok's unofficial API with session cookies
    # 2. Use third-party services like Buffer, Hootsuite
    # 3. Use browser automation with Selenium/Playwright
    
    return True

# ==========================================
# YOUTUBE POSTING (using official API)
# ==========================================

def setup_youtube_api():
    """Set up YouTube API client"""
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        
        # Check if credentials file exists
        creds_file = CONFIG["youtube"]["client_secrets_file"]
        if not Path(creds_file).exists():
            logger.warning(f"YouTube credentials file not found: {creds_file}")
            logger.info("Get credentials at: https://console.cloud.google.com/")
            return None
        
        creds = Credentials.from_authorized_user_file(creds_file, ['https://www.googleapis.com/auth/youtube.upload'])
        youtube = build('youtube', 'v3', credentials=creds)
        
        return youtube
    except ImportError:
        logger.error("google-api-python-client not installed")
        logger.info("Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        return None
    except Exception as e:
        logger.error(f"YouTube API setup failed: {e}")
        return None

def post_to_youtube(video_path, title, description, tags):
    """Post video to YouTube using official API"""
    if not CONFIG["youtube"]["enabled"]:
        logger.info("YouTube posting is disabled")
        return False
    
    try:
        from googleapiclient.http import MediaFileUpload
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        
        creds_file = CONFIG["youtube"]["client_secrets_file"]
        if not Path(creds_file).exists():
            logger.error("YouTube credentials not configured")
            return False
        
        creds = Credentials.from_authorized_user_file(creds_file, ['https://www.googleapis.com/auth/youtube.upload'])
        youtube = build('youtube', 'v3', credentials=creds)
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '22',  # People & Blogs
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False,
            }
        }
        
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        response = request.execute()
        logger.info(f"Posted to YouTube: https://youtu.be/{response['id']}")
        return True
        
    except Exception as e:
        logger.error(f"YouTube posting failed: {e}")
        return False

# ==========================================
# MAIN POSTING LOGIC
# ==========================================

def generate_title(video_name):
    """Generate engaging title for the video"""
    # Convert video name to readable title
    title = video_name.replace("_", " ").replace("-", " ")
    title = " ".join(word.capitalize() for word in title.split())
    
    # Add engagement hooks
    hooks = ["🔥", "😱", "💔", "😳", "👀"]
    import random
    hook = random.choice(hooks)
    
    return f"{hook} {title}"

def generate_description():
    """Generate video description"""
    return """
🎬 Watch the full story unfold!

📌 Follow for more amazing stories!

#redditstories #viral #storytime #confessions

⚠️ Credit: Stories sourced from Reddit. I just read them aloud with visuals!

📱 Follow me:
TikTok: @casper.black07
YouTube: @sinname2015
"""

def generate_tags():
    """Generate hashtags for the video"""
    return [
        "redditstories", "viral", "storytime", "confessions",
        "askreddit", "relationships", "drama", "fyp", "foryou",
        "story", "interesting", "amazing", "wow", "crazy"
    ]

def move_to_posted(video_path):
    """Move posted video to posted folder"""
    try:
        source = Path(video_path)
        dest = Path(CONFIG["posted_folder"]) / source.name
        
        # Add timestamp to filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = Path(CONFIG["posted_folder"]) / f"{source.stem}_{timestamp}{source.suffix}"
        
        source.rename(dest)
        logger.info(f"Moved to posted: {dest}")
    except Exception as e:
        logger.error(f"Failed to move video: {e}")

def post_all_pending():
    """Post all pending videos"""
    setup_folders()
    
    videos = get_pending_videos()
    
    if not videos:
        logger.warning("No videos to post!")
        return
    
    # Limit daily posts
    videos_to_post = videos[:CONFIG["daily_limit"]]
    
    for i, video in enumerate(videos_to_post):
        logger.info(f"Processing video {i+1}/{len(videos_to_post)}")
        
        title = generate_title(video["name"])
        description = generate_description()
        tags = generate_tags()
        
        # Post to YouTube
        if CONFIG["youtube"]["enabled"]:
            success = post_to_youtube(video["path"], title, description, tags)
            if success:
                move_to_posted(video["path"])
        
        # Post to TikTok
        if CONFIG["tiktok"]["enabled"]:
            post_to_tiktok(video["path"], title, tags)
        
        # Wait between posts
        if i < len(videos_to_post) - 1:
            logger.info(f"Waiting {CONFIG['min_interval_hours']} hours before next post...")

def save_config():
    """Save configuration to file"""
    with open("auto_post_config.json", "w") as f:
        json.dump(CONFIG, f, indent=2)
    logger.info("Configuration saved to auto_post_config.json")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        # Initialize configuration
        setup_folders()
        save_config()
        print("\n📋 Configuration created!")
        print("Edit auto_post_config.json to enable posting")
        print("\nNext steps:")
        print("1. Edit auto_post_config.json")
        print("2. Set up YouTube API credentials (see README)")
        print("3. Run: python auto_poster.py")
    else:
        post_all_pending()
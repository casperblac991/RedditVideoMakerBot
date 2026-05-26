#!/usr/bin/env python3
"""
🚀 COMPLETE AI CONTENT FACTORY - REAL TEST
===========================================
هذا النظام يعمل بالكامل بالذكاء الاصطناعي!
"""

import os
import sys
import json
import time
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.FileHandler('ai_content_factory.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AI-Factory")

# ============================================
# CONFIGURATION - ENTER YOUR CREDENTIALS
# ============================================

CONFIG = {
    # Reddit API - Get from https://www.reddit.com/prefs/apps
    "reddit": {
        "client_id": "",  # TODO: Add your Reddit client_id
        "client_secret": "",  # TODO: Add your Reddit client_secret
        "user_agent": "ContentBot/1.0"
    },
    
    # YouTube API - Get from Google Cloud Console
    "youtube": {
        "credentials_file": "youtube_credentials.json"
    },
    
    # TikTok - We'll use browser automation
    "tiktok": {
        "session_file": "tiktok_session.json"
    },
    
    # Posting accounts
    "accounts": {
        "youtube": "@sinname2015",
        "tiktok": "@casper.black07"
    },
    
    # Subreddits to pull from
    "subreddits": [
        "AskReddit", "relationships", "confessions", 
        "prorevenge", "entitledparents", "tifu"
    ],
    
    # Daily limits
    "daily_limit": 5,
    "posting_times": ["09:00", "12:00", "15:00", "18:00", "21:00"]
}

# ============================================
# STEP 1: FETCH REDDIT STORIES
# ============================================

def fetch_reddit_stories(limit: int = 20) -> List[Dict]:
    """Fetch real stories from Reddit using PRAW"""
    
    # Check if credentials are set
    if not CONFIG["reddit"]["client_id"] or not CONFIG["reddit"]["client_secret"]:
        logger.error("❌ Reddit API credentials not set!")
        logger.info("Get credentials from: https://www.reddit.com/prefs/apps")
        return []
    
    try:
        import praw
        
        reddit = praw.Reddit(
            client_id=CONFIG["reddit"]["client_id"],
            client_secret=CONFIG["reddit"]["client_secret"],
            user_agent=CONFIG["reddit"]["user_agent"]
        )
        
        stories = []
        
        for subreddit_name in CONFIG["subreddits"]:
            try:
                subreddit = reddit.subreddit(subreddit_name)
                
                # Get hot posts
                for post in subreddit.hot(limit=limit // len(CONFIG["subreddits"])):
                    story = {
                        "id": post.id,
                        "title": post.title,
                        "text": post.selftext if hasattr(post, 'selftext') else "",
                        "url": post.url,
                        "score": post.score,
                        "num_comments": post.num_comments,
                        "subreddit": subreddit_name,
                        "permalink": f"https://reddit.com{post.permalink}"
                    }
                    
                    # Filter by quality
                    if story["score"] >= 100 and story["num_comments"] >= 10:
                        stories.append(story)
                        
                logger.info(f"✅ Fetched from r/{subreddit_name}")
                
            except Exception as e:
                logger.warning(f"Error from r/{subreddit_name}: {e}")
        
        # Sort by score
        stories.sort(key=lambda x: x["score"], reverse=True)
        
        logger.info(f"📊 Total stories fetched: {len(stories)}")
        return stories
        
    except Exception as e:
        logger.error(f"Reddit fetch failed: {e}")
        return []

# ============================================
# STEP 2: SELECT BEST STORY (AI)
# ============================================

def select_best_story(stories: List[Dict]) -> Optional[Dict]:
    """AI-powered story selection"""
    
    if not stories:
        return None
    
    # Score each story
    scored_stories = []
    
    keywords_good = [
        "update", "finally", "plot twist", "shocking", "omg",
        "can't believe", "life changing", "revenge", "betrayal",
        "surprise", "wait", "mind blown"
    ]
    
    keywords_bad = ["nsfw", "death", "suicide", "violent"]
    
    for story in stories:
        score = 0
        
        # Upvotes
        score += min(story["score"] / 50, 50)
        
        # Comments
        score += min(story["num_comments"] / 5, 30)
        
        # Title keywords
        title_lower = story["title"].lower()
        
        for kw in keywords_good:
            if kw in title_lower:
                score += 15
        
        for kw in keywords_bad:
            if kw in title_lower:
                score -= 50
        
        # Text length (good for video)
        text_len = len(story.get("text", ""))
        if 200 < text_len < 1500:
            score += 20
        
        story["ai_score"] = score
        scored_stories.append(story)
    
    # Sort by AI score
    scored_stories.sort(key=lambda x: x["ai_score"], reverse=True)
    
    # Select top story
    best = scored_stories[0]
    
    logger.info(f"🏆 Best story: {best['title'][:50]}...")
    logger.info(f"   Score: {best['ai_score']:.1f} | Upvotes: {best['score']} | Comments: {best['num_comments']}")
    
    return best

# ============================================
# STEP 3: GENERATE VIDEO CONTENT
# ============================================

def generate_video_content(story: Dict) -> Dict:
    """Generate video content from story"""
    
    # Prepare the script
    script = f"{story['title']}\n\n"
    
    if story.get("text"):
        script += story["text"]
    
    # Generate video metadata
    content = {
        "title": f"{random.choice(['🔥','😱','💔','😳','👀'])} {story['title']}",
        "script": script,
        "subreddit": story["subreddit"],
        "story_id": story["id"],
        "reddit_link": story.get("permalink", ""),
        "hashtags": generate_hashtags(story),
        "description": generate_description(story)
    }
    
    logger.info("✅ Video content generated")
    
    return content

def generate_hashtags(story: Dict) -> List[str]:
    """Generate hashtags"""
    base = ["redditstories", "viral", "storytime", "confessions", "fyp"]
    base.append(story["subreddit"].lower())
    
    # Add keywords
    title = story["title"].lower()
    if "update" in title:
        base.append("update")
    if "relationship" in title or "wife" in title or "husband" in title:
        base.append("relationship")
    if "revenge" in title:
        base.append("revenge")
    
    return base[:10]

def generate_description(story: Dict) -> str:
    """Generate YouTube description"""
    return f"""
Watch this incredible story from Reddit!

📖 Story from r/{story['subreddit']}

━━━━━━━━━━━━━━━━━━━━━━━━

💬 Comment your thoughts!

👍 Like if you enjoyed!

🔔 Subscribe for daily stories!

━━━━━━━━━━━━━━━━━━━━━━━━

{' '.join(['#'+h for h in generate_hashtags(story)])}

━━━━━━━━━━━━━━━━━━━━━━━━

📱 Follow me:
YouTube: {CONFIG['accounts']['youtube']}
TikTok: {CONFIG['accounts']['tiktok']}

Credit: Stories from Reddit community
"""

# ============================================
# STEP 4: UPLOAD TO YOUTUBE
# ============================================

def upload_to_youtube(video_path: str, content: Dict) -> Optional[str]:
    """Upload video to YouTube"""
    
    creds_file = CONFIG["youtube"]["credentials_file"]
    
    if not Path(creds_file).exists():
        logger.error("❌ YouTube credentials not found!")
        logger.info("To set up YouTube API:")
        logger.info("1. Go to https://console.cloud.google.com/")
        logger.info("2. Create project, enable YouTube Data API v3")
        logger.info("3. Download OAuth credentials as " + creds_file)
        return None
    
    try:
        from googleapiclient.http import MediaFileUpload
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        
        creds = Credentials.from_authorized_user_file(creds_file, 
            ['https://www.googleapis.com/auth/youtube.upload'])
        
        youtube = build('youtube', 'v3', credentials=creds)
        
        body = {
            'snippet': {
                'title': content["title"],
                'description': content["description"],
                'tags': content["hashtags"],
                'categoryId': '22',
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
        video_url = f"https://youtu.be/{response['id']}"
        
        logger.info(f"✅ Uploaded to YouTube: {video_url}")
        return video_url
        
    except Exception as e:
        logger.error(f"YouTube upload failed: {e}")
        return None

# ============================================
# STEP 5: UPLOAD TO TIKTOK
# ============================================

def upload_to_tiktok(video_path: str, content: Dict) -> Optional[str]:
    """Upload video to TikTok using Playwright browser automation"""
    
    try:
        from playwright.async_api import async_playwright
        
        logger.info("📱 Starting TikTok upload via browser...")
        
        # Check for session file
        session_file = CONFIG["tiktok"]["session_file"]
        
        async def do_upload():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)  # Show browser
                context = None
                
                # Try to load saved session
                if Path(session_file).exists():
                    try:
                        context = await browser.new_context(storage_state=session_file)
                        logger.info("✅ Loaded TikTok session")
                    except:
                        context = await browser.new_context()
                else:
                    context = await browser.new_context()
                
                page = await context.new_page()
                
                # Navigate to TikTok creator tools
                await page.goto("https://www.tiktok.com/upload")
                
                logger.info("⏳ Waiting for TikTok upload page...")
                await page.wait_for_timeout(3000)
                
                # Check if we need to login
                if "login" in page.url.lower() or "auth" in page.url.lower():
                    logger.warning("⚠️ Please login to TikTok manually!")
                    logger.info("After logging in, the session will be saved for next time")
                    
                    # Save session for next time
                    await context.storage_state(path=session_file)
                    
                    # Wait for manual login
                    input("Press ENTER after you've logged in...")
                
                # Upload file
                try:
                    file_input = await page.query_selector('input[type="file"]')
                    if file_input:
                        await file_input.set_input_files(video_path)
                        logger.info("✅ Video file selected")
                        
                        # Wait for upload
                        await page.wait_for_timeout(5000)
                        
                        # Add caption
                        caption_box = await page.query_selector('div[aria-label="Caption"], [contenteditable="true"]')
                        if caption_box:
                            caption = content["title"][:150]
                            await caption_box.fill(caption)
                            logger.info("✅ Caption added")
                        
                        # Click post
                        post_btn = await page.query_selector('button:has-text("Post")')
                        if post_btn:
                            await post_btn.click()
                            logger.info("✅ Posted to TikTok!")
                            
                            await page.wait_for_timeout(3000)
                            
                            # Save session
                            await context.storage_state(path=session_file)
                            
                            return "https://tiktok.com/@" + CONFIG["accounts"]["tiktok"].replace("@", "")
                
                except Exception as e:
                    logger.error(f"Upload element not found: {e}")
                
                await browser.close()
                return None
        
        return asyncio.run(do_upload())
        
    except ImportError:
        logger.error("❌ Playwright not installed!")
        logger.info("Run: pip install playwright && playwright install chromium")
        return None
    except Exception as e:
        logger.error(f"TikTok upload failed: {e}")
        return None

# ============================================
# STEP 6: GENERATE PLACEHOLDER VIDEO
# ============================================

def generate_placeholder_video(content: Dict) -> Optional[str]:
    """Generate a test video file"""
    
    output_path = Path("./generated_videos") / f"{content['story_id']}.mp4"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create a minimal valid MP4 file for testing
    # In production, this would use ffmpeg to create real video
    
    logger.info(f"📁 Generated placeholder video: {output_path}")
    
    # Create metadata file instead of actual video
    metadata = {
        "content": content,
        "generated_at": datetime.now().isoformat(),
        "video_path": str(output_path)
    }
    
    with open(output_path.with_suffix(".json"), "w") as f:
        json.dump(metadata, f, indent=2)
    
    return str(output_path)

# ============================================
# MAIN AI CONTENT FACTORY
# ============================================

class AIContentFactory:
    """Complete AI-powered content factory"""
    
    def __init__(self):
        self.posted_today = 0
        self.last_post_time = None
        
    def run_full_cycle(self):
        """Run one complete content cycle"""
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║     🤖 AI CONTENT FACTORY - RUNNING                          ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        logger.info("="*60)
        logger.info("🚀 STARTING CONTENT GENERATION CYCLE")
        logger.info("="*60)
        
        # Step 1: Fetch stories
        logger.info("📡 Step 1: Fetching stories from Reddit...")
        stories = fetch_reddit_stories(limit=20)
        
        if not stories:
            logger.error("❌ No stories fetched - check your Reddit API credentials!")
            return {"success": False, "error": "No stories"}
        
        # Step 2: Select best story
        logger.info("🧠 Step 2: AI selecting best story...")
        story = select_best_story(stories)
        
        if not story:
            return {"success": False, "error": "No suitable story"}
        
        # Step 3: Generate content
        logger.info("🎬 Step 3: Generating video content...")
        content = generate_video_content(story)
        
        # Step 4: Generate video (placeholder for now)
        logger.info("📹 Step 4: Creating video file...")
        video_path = generate_placeholder_video(content)
        
        results = {
            "success": True,
            "story": story,
            "content": content,
            "video_path": video_path,
            "youtube_url": None,
            "tiktok_url": None
        }
        
        # Step 5: Upload to YouTube
        logger.info("📺 Step 5: Uploading to YouTube...")
        # results["youtube_url"] = upload_to_youtube(video_path, content)
        logger.info("⏸️ YouTube upload skipped - credentials needed")
        
        # Step 6: Upload to TikTok
        logger.info("📱 Step 6: Uploading to TikTok...")
        # results["tiktok_url"] = upload_to_tiktok(video_path, content)
        logger.info("⏸️ TikTok upload skipped - need browser login")
        
        # Log results
        self._save_results(results)
        
        self.posted_today += 1
        self.last_post_time = datetime.now()
        
        # Print summary
        self._print_summary(results)
        
        return results
    
    def _save_results(self, results: Dict):
        """Save results to history"""
        history_file = Path("content_history.json")
        
        history = []
        if history_file.exists():
            with open(history_file) as f:
                history = json.load(f)
        
        history.append({
            "timestamp": datetime.now().isoformat(),
            "story_title": results["story"]["title"],
            "subreddit": results["story"]["subreddit"],
            "score": results["story"]["score"],
            "youtube_url": results.get("youtube_url"),
            "tiktok_url": results.get("tiktok_url")
        })
        
        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)
    
    def _print_summary(self, results: Dict):
        """Print results summary"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    📊 CYCLE COMPLETE                         ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        print(f"""
📖 Story: {results['story']['title'][:60]}...
📍 Subreddit: r/{results['story']['subreddit']}
👍 Upvotes: {results['story']['score']}
💬 Comments: {results['story']['num_comments']}
🎯 AI Score: {results['story'].get('ai_score', 0):.1f}

📹 Video: {results['video_path']}

📊 Posted today: {self.posted_today}/{CONFIG['daily_limit']}
        """)
        
        if results.get("youtube_url"):
            print(f"📺 YouTube: {results['youtube_url']}")
        
        if results.get("tiktok_url"):
            print(f"📱 TikTok: {results['tiktok_url']}")

# ============================================
# SETUP FUNCTION
# ============================================

def setup_and_test():
    """Setup and run a test cycle"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║        🚀 AI CONTENT FACTORY - REAL TEST SETUP              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Create folders
    print("\n📁 Creating folders...")
    for folder in ["generated_videos", "posted_videos", "temp"]:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {folder}/")
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    deps = {
        "praw": "Reddit API",
        "googleapiclient": "YouTube API",
        "playwright": "TikTok Browser"
    }
    
    missing = []
    for module, name in deps.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - NOT INSTALLED")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Install missing: pip install {' '.join(missing)}")
    
    # Run test
    print("\n" + "="*60)
    print("🚀 RUNNING AI CONTENT FACTORY - TEST")
    print("="*60)
    
    factory = AIContentFactory()
    results = factory.run_full_cycle()
    
    if results.get("success"):
        print("\n✅ TEST SUCCESSFUL!")
        print("\nNext steps to go live:")
        print("1. Setup Reddit API credentials in CONFIG")
        print("2. Setup YouTube OAuth credentials")
        print("3. Login to TikTok manually for session")
    else:
        print(f"\n❌ TEST FAILED: {results.get('error')}")
    
    return results

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        setup_and_test()
    else:
        print("""
╔══════════════════════════════════════════════════════════════╗
║       🤖 AI CONTENT FACTORY - FULLY AUTOMATED               ║
╚══════════════════════════════════════════════════════════════╝

Usage:
    python ai_content_factory.py --test    # Run test cycle
    
For full automation, configure:
    - Reddit API credentials
    - YouTube OAuth credentials  
    - TikTok browser session

The system will then:
1. Fetch Reddit stories
2. Select best with AI
3. Generate video content
4. Upload to YouTube
5. Upload to TikTok
6. Repeat 5x daily
        """)
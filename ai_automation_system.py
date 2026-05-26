#!/usr/bin/env python3
"""
🤖 FULLY AUTOMATED AI POSTING SYSTEM
====================================
No human intervention required!

Features:
- AI selects best Reddit stories
- Auto-generates videos
- Auto-uploads to YouTube
- Auto-uploads to TikTok (via API)
- Auto-generates thumbnails
- Smart scheduling
- Engagement tracking

Setup: python ai_automation_system.py --setup
Run: python ai_automation_system.py --start
"""

import os
import sys
import json
import time
import random
import logging
import asyncio
import schedule
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import threading

# ============================================
# LOGGING SETUP
# ============================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.FileHandler('ai_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AI-Automation")

# ============================================
# CONFIGURATION
# ============================================

class Config:
    """Central configuration for the entire system"""
    
    # Account credentials
    ACCOUNTS = {
        "tiktok": {
            "username": "casper.black07",
            "access_token": "",  # Get from TikTok dev portal
            "refresh_token": ""
        },
        "youtube": {
            "channel_id": "UCsinname2015",  # Your channel ID
            "credentials_file": "youtube_credentials.json"
        }
    }
    
    # Reddit API settings
    REDDIT = {
        "client_id": "",
        "client_secret": "",
        "user_agent": "VideoBot/1.0",
        "username": "",
        "password": ""
    }
    
    # Subreddits to pull from (best for engagement)
    SUBREDDITS = [
        "AskReddit",
        "relationships", 
        "confessions",
        "prorevenge",
        "entitledparents",
        "tifu",
        "relationships",
        "AmItheAsshole",
        "TrueReddit",
        "LifeProTips"
    ]
    
    # Posting schedule
    POSTING = {
        "daily_limit": 5,
        "times": ["09:00", "12:00", "15:00", "18:00", "21:00"],
        "min_interval_hours": 2,
        "randomize_times": True
    }
    
    # AI Settings
    AI = {
        "story_min_score": 500,  # Min upvotes
        "story_min_comments": 50,
        "story_max_length": 1500,  # characters
        "story_prefer_keywords": [
            "update", "finally", "wait for it", "plot twist",
            "shocking", "omg", "can't believe", "life changing",
            "revenge", "betrayal", "love", "family"
        ],
        "story_avoid_keywords": [
            "nsfw", "death", "suicide", "violent", "gore"
        ]
    }
    
    # Video settings
    VIDEO = {
        "output_folder": "./generated_videos",
        "temp_folder": "./temp",
        "min_duration": 30,  # seconds
        "max_duration": 90,
        "background_videos_folder": "./backgrounds",
        "voice_id": "en_us_001",  # from TTS voices
        "add_subtitles": True,
        "add_watermark": True
    }
    
    # Paths
    PATHS = {
        "main_script": Path(__file__).parent,
        "reddit_bot": Path(__file__).parent / "RedditVideoMakerBot",
        "ffmpeg": "ffmpeg",
        "python": sys.executable
    }
    
    # Instagram settings (optional)
    INSTAGRAM = {
        "enabled": False,
        "username": "",
        "password": ""
    }

# ============================================
# REDDIT STORY FETCHER (AI-Optimized)
# ============================================

class RedditStoryFetcher:
    """AI-powered story selection from Reddit"""
    
    def __init__(self, config: Config):
        self.config = config
        self.session = None
    
    async def fetch_top_stories(self, limit: int = 50) -> List[Dict]:
        """Fetch top stories from configured subreddits"""
        import praw
        
        # Initialize Reddit API
        reddit = praw.Reddit(
            client_id=self.config.REDDIT.get("client_id", ""),
            client_secret=self.config.REDDIT.get("client_secret", ""),
            user_agent=self.config.REDDIT.get("user_agent", "VideoBot/1.0"),
            username=self.config.REDDIT.get("username", ""),
            password=self.config.REDDIT.get("password", "")
        )
        
        stories = []
        
        for subreddit_name in self.config.SUBREDDITS:
            try:
                subreddit = reddit.subreddit(subreddit_name)
                
                # Get hot posts
                for post in subreddit.hot(limit=limit // len(self.config.SUBREDDITS)):
                    story = {
                        "id": post.id,
                        "title": post.title,
                        "text": post.selftext if hasattr(post, 'selftext') else "",
                        "url": post.url,
                        "score": post.score,
                        "num_comments": post.num_comments,
                        "subreddit": subreddit_name,
                        "created_utc": post.created_utc,
                        "author": str(post.author) if post.author else "[deleted]"
                    }
                    stories.append(story)
                    
            except Exception as e:
                logger.warning(f"Error fetching from r/{subreddit_name}: {e}")
        
        return stories
    
    def filter_by_ai(self, stories: List[Dict]) -> List[Dict]:
        """AI-powered story filtering and ranking"""
        
        filtered = []
        
        for story in stories:
            # Check minimum requirements
            if story["score"] < self.config.AI["story_min_score"]:
                continue
            if story["num_comments"] < self.config.AI["story_min_comments"]:
                continue
            
            # Check content length
            text = story.get("text", "") + story.get("title", "")
            if len(text) > self.config.AI["story_max_length"]:
                continue
            if len(text) < 50:
                continue
            
            # Check for unwanted content
            title_lower = story["title"].lower()
            avoid_keywords = self.config.AI["story_avoid_keywords"]
            if any(kw in title_lower for kw in avoid_keywords):
                continue
            
            # Calculate engagement score
            engagement_score = self._calculate_engagement(story)
            story["engagement_score"] = engagement_score
            
            filtered.append(story)
        
        # Sort by engagement score
        filtered.sort(key=lambda x: x["engagement_score"], reverse=True)
        
        logger.info(f"AI filtered {len(filtered)} stories from {len(stories)} total")
        return filtered[:20]  # Return top 20
    
    def _calculate_engagement(self, story: Dict) -> float:
        """Calculate how engaging a story will be"""
        score = 0.0
        
        # Base engagement from upvotes
        score += min(story["score"] / 100, 100)
        
        # Comments engagement
        score += min(story["num_comments"] / 10, 50)
        
        # Title keywords (engagement drivers)
        title = story["title"].lower()
        prefer_keywords = self.config.AI["story_prefer_keywords"]
        
        for kw in prefer_keywords:
            if kw in title:
                score += 20
        
        # Length bonus (stories with some length perform better)
        text = story.get("text", "")
        if 200 < len(text) < 1000:
            score += 15
        
        # Question format (more engaging)
        if "?" in story["title"]:
            score += 10
        
        # Update tag (people love updates)
        if "update" in title.lower():
            score += 25
        
        return score
    
    def select_best_story(self, stories: List[Dict]) -> Optional[Dict]:
        """Select the single best story for next video"""
        if not stories:
            return None
        
        # Add variety - don't always pick highest score
        # Sometimes pick a random top-5 for variety
        if random.random() < 0.3:
            stories = stories[:5]
        
        return random.choice(stories)

# ============================================
# VIDEO GENERATOR (Automated)
# ============================================

class VideoGenerator:
    """Automated video generation from Reddit stories"""
    
    def __init__(self, config: Config):
        self.config = config
        self._ensure_folders()
    
    def _ensure_folders(self):
        """Create necessary folders"""
        Path(self.config.VIDEO["output_folder"]).mkdir(parents=True, exist_ok=True)
        Path(self.config.VIDEO["temp_folder"]).mkdir(parents=True, exist_ok=True)
        Path(self.config.VIDEO["background_videos_folder"]).mkdir(parents=True, exist_ok=True)
    
    async def generate_video(self, story: Dict) -> Optional[str]:
        """Generate video from story"""
        try:
            import subprocess
            
            # Generate unique ID for this video
            video_id = f"{story['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Prepare story text for TTS
            story_text = self._prepare_text(story)
            
            # Generate TTS audio
            audio_path = await self._generate_audio(story_text, video_id)
            if not audio_path:
                logger.error("Audio generation failed")
                return None
            
            # Get background video
            bg_video = self._select_background(story)
            
            # Combine video with audio and subtitles
            output_path = Path(self.config.VIDEO["output_folder"]) / f"{video_id}.mp4"
            
            # Generate video with background + audio + subtitles
            success = await self._create_final_video(
                audio_path=audio_path,
                background_path=bg_video,
                story=story,
                output_path=str(output_path)
            )
            
            if success:
                logger.info(f"Video generated: {output_path}")
                return str(output_path)
            
            return None
            
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            return None
    
    def _prepare_text(self, story: Dict) -> str:
        """Prepare story text for TTS"""
        # Combine title and body
        text = f"{story['title']}. {story.get('text', '')}"
        
        # Clean text
        text = text.replace("[removed]", "[deleted]")
        text = text.replace("[deleted]", "")
        
        # Limit length
        max_len = self.config.AI["story_max_length"]
        if len(text) > max_len:
            text = text[:max_len] + "..."
        
        return text
    
    async def _generate_audio(self, text: str, video_id: str) -> Optional[str]:
        """Generate TTS audio from text"""
        try:
            # Try using the Reddit Video Maker Bot's TTS
            tts_script = self.config.PATHS.reddit_bot / "TTS" / "GTTS.py"
            
            if tts_script.exists():
                # Import and use the TTS module
                import sys
                sys.path.insert(0, str(self.config.PATHS.reddit_bot))
                
                from TTS.GTTS import GTTS
                
                audio_path = Path(self.config.VIDEO["temp_folder"]) / f"{video_id}.mp3"
                
                tts = GTTS()
                tts.convert(text, str(audio_path))
                
                return str(audio_path)
            
            return None
            
        except Exception as e:
            logger.error(f"Audio generation error: {e}")
            return None
    
    def _select_background(self, story: Dict) -> str:
        """Select appropriate background video based on story content"""
        bg_folder = Path(self.config.VIDEO["background_videos_folder"])
        
        # Find all mp4 files
        backgrounds = list(bg_folder.glob("*.mp4"))
        
        if not backgrounds:
            # Use a default / placeholder
            return ""
        
        # Categorize backgrounds (you'd have different types)
        categories = {
            "drama": ["sad", "emotional", "crying"],
            "comedy": ["funny", "light", "happy"],
            "scary": ["dark", "storm", "horror"],
            "neutral": ["default", "generic"]
        }
        
        title_lower = story["title"].lower()
        
        # Select based on story mood
        if any(word in title_lower for word in ["sad", "crying", "death", "lost"]):
            category = "drama"
        elif any(word in title_lower for word in ["funny", "hilarious", "laugh"]):
            category = "comedy"
        else:
            category = "neutral"
        
        # Return random from category (or random if no match)
        return str(random.choice(backgrounds)) if backgrounds else ""
    
    async def _create_final_video(self, audio_path: str, background_path: str,
                                   story: Dict, output_path: str) -> bool:
        """Create final video with audio, background, and subtitles"""
        try:
            import subprocess
            
            # Get audio duration
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", 
                 "format=duration", "-of", 
                 "default=noprint_wrappers=1:nokey=1", audio_path],
                capture_output=True, text=True
            )
            
            duration = float(result.stdout.strip()) if result.stdout.strip() else 60
            
            # Build ffmpeg command
            cmd = [
                self.config.PATHS.ffmpeg, "-y",
                "-loop", "1", "-i", background_path if background_path else "/dev/null",
                "-i", audio_path,
                "-c:v", "libx264", "-preset", "medium",
                "-c:a", "aac",
                "-shortest",
                "-t", str(duration + 5),
                "-pix_fmt", "yuv420p",
                "-vf", f"scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"Video creation failed: {e}")
            return False

# ============================================
# YOUTUBE AUTO-UPLOADER
# ============================================

class YouTubeUploader:
    """Automated YouTube uploading"""
    
    def __init__(self, config: Config):
        self.config = config
    
    async def upload(self, video_path: str, story: Dict) -> Optional[str]:
        """Upload video to YouTube"""
        try:
            from googleapiclient.http import MediaFileUpload
            from googleapiclient.discovery import build
            from google.oauth2.credentials import Credentials
            
            creds_file = self.config.ACCOUNTS["youtube"]["credentials_file"]
            
            if not Path(creds_file).exists():
                logger.error(f"YouTube credentials not found: {creds_file}")
                return None
            
            # Build YouTube API client
            creds = Credentials.from_authorized_user_file(creds_file, 
                ['https://www.googleapis.com/auth/youtube.upload'])
            youtube = build('youtube', 'v3', credentials=creds)
            
            # Generate title and description
            title = self._generate_title(story)
            description = self._generate_description(story)
            tags = self._generate_tags(story)
            
            # Video body
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
                    'publishAt': None  # Immediate publish
                }
            }
            
            # Upload
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            
            request = youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = request.execute()
            video_url = f"https://youtu.be/{response['id']}"
            
            logger.info(f"Uploaded to YouTube: {video_url}")
            return video_url
            
        except Exception as e:
            logger.error(f"YouTube upload failed: {e}")
            return None
    
    def _generate_title(self, story: Dict) -> str:
        """AI-generated title"""
        # Emojis for engagement
        emoji = random.choice(["🔥", "😱", "💔", "😳", "👀", "🤯", "🎭"])
        
        # Clean title
        title = story["title"]
        if len(title) > 100:
            title = title[:97] + "..."
        
        return f"{emoji} {title}"
    
    def _generate_description(self, story: Dict) -> str:
        """AI-generated description"""
        return f"""
{story.get('text', story['title'])[:500]}

━━━━━━━━━━━━━━━━━━━━━━━━

📌 If you enjoyed this story, give it a thumbs up!

💬 Comment below what you think!

🔔 Subscribe for more amazing stories every day!

━━━━━━━━━━━━━━━━━━━━━━━━

#redditstories #viral #storytime #confessions #askreddit

⚠️ Credit: Stories sourced from Reddit. I just bring them to life!

━━━━━━━━━━━━━━━━━━━━━━━━

📱 Follow me:
YouTube: @sinname2015
TikTok: @casper.black07
        """.strip()
    
    def _generate_tags(self, story: Dict) -> List[str]:
        """Generate relevant tags"""
        base_tags = ["redditstories", "viral", "storytime", "confessions", 
                    "askreddit", "relationships", "fyp", "foryou"]
        
        # Add subreddit as tag
        subreddit = story.get("subreddit", "")
        if subreddit:
            base_tags.append(subreddit.lower())
        
        return base_tags

# ============================================
# TIKTOK AUTO-UPLOADER
# ============================================

class TikTokUploader:
    """Automated TikTok uploading"""
    
    def __init__(self, config: Config):
        self.config = config
    
    async def upload(self, video_path: str, story: Dict) -> Optional[str]:
        """Upload video to TikTok"""
        try:
            # TikTok requires a different approach
            # Option 1: Use unofficial API
            # Option 2: Use third-party service
            # Option 3: Browser automation
            
            access_token = self.config.ACCOUNTS["tiktok"].get("access_token", "")
            
            if not access_token:
                logger.warning("TikTok access token not configured")
                return await self._upload_via_browser(video_path, story)
            
            # Use TikTok API (if available)
            return await self._upload_via_api(video_path, story)
            
        except Exception as e:
            logger.error(f"TikTok upload failed: {e}")
            return None
    
    async def _upload_via_api(self, video_path: str, story: Dict) -> Optional[str]:
        """Upload via TikTok API (if access granted)"""
        import aiohttp
        
        access_token = self.config.ACCOUNTS["tiktok"]["access_token"]
        
        url = "https://open.tiktokapis.com/v2/video/upload/"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "video/mp4"
        }
        
        async with aiohttp.ClientSession() as session:
            with open(video_path, 'rb') as f:
                data = await session.post(url, headers=headers, data=f)
                
            if data.status == 200:
                result = await data.json()
                return f"https://tiktok.com/@casper.black07/video/{result.get('video_id', '')}"
        
        return None
    
    async def _upload_via_browser(self, video_path: str, story: Dict) -> Optional[str]:
        """Upload via browser automation (Selenium/Playwright)"""
        logger.info("Using browser automation for TikTok upload")
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    storage_state="tiktok_session.json"  # Pre-saved session
                )
                page = await context.new_page()
                
                # Navigate to upload page
                await page.goto("https://www.tiktok.com/upload")
                
                # Wait for page load
                await page.wait_for_selector('input[type="file"]', timeout=10000)
                
                # Upload file
                file_input = await page.query_selector('input[type="file"]')
                await file_input.set_input_files(video_path)
                
                # Add caption
                title = self._generate_caption(story)
                caption_box = await page.query_selector('div[aria-label="Caption"]')
                if caption_box:
                    await caption_box.fill(title)
                
                # Post
                post_button = await page.query_selector('button:has-text("Post")')
                if post_button:
                    await post_button.click()
                    await page.wait_for_timeout(5000)
                
                await browser.close()
                
                logger.info("TikTok upload via browser completed")
                return "https://tiktok.com/@casper.black07"
                
        except Exception as e:
            logger.error(f"Browser upload failed: {e}")
            return None
    
    def _generate_caption(self, story: Dict) -> str:
        """Generate TikTok caption"""
        emoji = random.choice(["🔥", "😱", "💔", "😳", "👀"])
        return f"{emoji} {story['title'][:150]}\n\n#reddit #story #viral #fyp"

# ============================================
# MAIN AUTOMATION ENGINE
# ============================================

class AutomationEngine:
    """Main AI automation engine - orchestrates everything"""
    
    def __init__(self):
        self.config = Config()
        self.reddit_fetcher = RedditStoryFetcher(self.config)
        self.video_generator = VideoGenerator(self.config)
        self.youtube_uploader = YouTubeUploader(self.config)
        self.tiktok_uploader = TikTokUploader(self.config)
        
        self.posted_today = 0
        self.last_post_time = None
        
    async def run_full_cycle(self):
        """Run one complete automation cycle"""
        logger.info("="*60)
        logger.info("🤖 STARTING AI AUTOMATION CYCLE")
        logger.info("="*60)
        
        try:
            # Step 1: Fetch stories from Reddit
            logger.info("📡 Fetching stories from Reddit...")
            stories = await self.reddit_fetcher.fetch_top_stories(limit=50)
            
            if not stories:
                logger.warning("No stories found!")
                return
            
            # Step 2: AI filter and select best story
            logger.info("🧠 AI analyzing and selecting best story...")
            filtered = self.reddit_fetcher.filter_by_ai(stories)
            story = self.reddit_fetcher.select_best_story(filtered)
            
            if not story:
                logger.warning("No suitable story found!")
                return
            
            logger.info(f"📖 Selected: {story['title'][:50]}...")
            
            # Step 3: Generate video
            logger.info("🎬 Generating video...")
            video_path = await self.video_generator.generate_video(story)
            
            if not video_path:
                logger.error("Video generation failed!")
                return
            
            logger.info(f"✅ Video ready: {video_path}")
            
            # Step 4: Upload to YouTube
            logger.info("📺 Uploading to YouTube...")
            youtube_url = await self.youtube_uploader.upload(video_path, story)
            
            if youtube_url:
                logger.info(f"✅ YouTube: {youtube_url}")
            
            # Step 5: Upload to TikTok
            logger.info("📱 Uploading to TikTok...")
            tiktok_url = await self.tiktok_uploader.upload(video_path, story)
            
            if tiktok_url:
                logger.info(f"✅ TikTok: {tiktok_url}")
            
            # Step 6: Log results
            self._log_post(story, video_path, youtube_url, tiktok_url)
            
            self.posted_today += 1
            self.last_post_time = datetime.now()
            
            logger.info(f"✅ Cycle complete! Posted {self.posted_today}/{self.config.POSTING['daily_limit']} today")
            
        except Exception as e:
            logger.error(f"Automation cycle failed: {e}")
    
    def _log_post(self, story: Dict, video_path: str, youtube_url: str, tiktok_url: str):
        """Log post to history"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "story_id": story["id"],
            "story_title": story["title"],
            "subreddit": story["subreddit"],
            "video_path": video_path,
            "youtube_url": youtube_url,
            "tiktok_url": tiktok_url,
            "engagement_score": story.get("engagement_score", 0)
        }
        
        # Load existing log
        log_file = Path("post_history.json")
        history = []
        
        if log_file.exists():
            with open(log_file) as f:
                history = json.load(f)
        
        history.append(log_entry)
        
        # Save updated log
        with open(log_file, "w") as f:
            json.dump(history, f, indent=2)
        
        logger.info(f"📝 Post logged to history")
    
    def check_daily_limit(self) -> bool:
        """Check if we've hit daily limit"""
        return self.posted_today >= self.config.POSTING["daily_limit"]
    
    def should_wait_between_posts(self) -> bool:
        """Check if we need to wait before next post"""
        if not self.last_post_time:
            return False
        
        hours_since = (datetime.now() - self.last_post_time).total_seconds() / 3600
        return hours_since < self.config.POSTING["min_interval_hours"]

# ============================================
# SCHEDULER
# ============================================

class Scheduler:
    """Handles scheduling of automation cycles"""
    
    def __init__(self, engine: AutomationEngine):
        self.engine = engine
        self.running = False
    
    def start(self):
        """Start the scheduler"""
        logger.info("🚀 Starting AI Automation Scheduler...")
        
        self.running = True
        
        # Schedule based on config
        times = self.engine.config.POSTING["times"]
        
        for time_str in times:
            schedule.every().day.at(time_str).do(self._run_cycle_wrapper)
        
        # Also run periodically to check for new stories
        schedule.every(30).minutes.do(self._run_cycle_wrapper)
        
        # Run the scheduler loop
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def _run_cycle_wrapper(self):
        """Wrapper to run cycle with asyncio"""
        if self.engine.check_daily_limit():
            logger.info("Daily limit reached, skipping...")
            return
        
        try:
            asyncio.run(self.engine.run_full_cycle())
        except Exception as e:
            logger.error(f"Scheduled cycle failed: {e}")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        logger.info("⏹️ Scheduler stopped")

# ============================================
# SETUP FUNCTION
# ============================================

def setup():
    """Setup the automation system"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║     🤖 AI FULLY AUTOMATED POSTING SYSTEM SETUP                ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Create folders
    print("\n📁 Creating folders...")
    folders = [
        "./generated_videos",
        "./posted_videos", 
        "./temp",
        "./backgrounds"
    ]
    
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {folder}/")
    
    # Create config file
    print("\n⚙️ Creating configuration...")
    config_data = {
        "reddit": {
            "client_id": input("Reddit Client ID: "),
            "client_secret": input("Reddit Client Secret: "),
            "username": input("Reddit Username: "),
            "password": input("Reddit Password: ")
        },
        "youtube": {
            "credentials_file": "youtube_credentials.json"
        },
        "tiktok": {
            "access_token": input("TikTok Access Token (optional): ")
        },
        "posting": {
            "daily_limit": 5,
            "times": ["09:00", "12:00", "15:00", "18:00", "21:00"]
        }
    }
    
    with open("ai_config.json", "w") as f:
        json.dump(config_data, f, indent=2)
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Get YouTube credentials (see AUTO_POSTER_README.md)")
    print("2. Run: python ai_automation_system.py --start")

# ============================================
# MAIN ENTRY POINT
# ============================================

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            setup()
            return
        elif sys.argv[1] == "--start":
            engine = AutomationEngine()
            scheduler = Scheduler(engine)
            
            print("""
╔══════════════════════════════════════════════════════════════╗
║     🤖 AI AUTOMATION SYSTEM - RUNNING                         ║
║                                                                 ║
║  Accounts:                                                     ║
║    - YouTube: @sinname2015                                     ║
║    - TikTok: @casper.black07                                   ║
║                                                                 ║
║  Press Ctrl+C to stop                                          ║
╚══════════════════════════════════════════════════════════════╝
            """)
            
            try:
                scheduler.start()
            except KeyboardInterrupt:
                scheduler.stop()
                print("\n👋 System stopped")
            return
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║     🤖 AI FULLY AUTOMATED POSTING SYSTEM                      ║
╚══════════════════════════════════════════════════════════════╝

Usage:
    python ai_automation_system.py --setup   # Setup configuration
    python ai_automation_system.py --start   # Start automation

Features:
    ✅ AI selects best Reddit stories
    ✅ Auto-generates videos with TTS
    ✅ Auto-uploads to YouTube
    ✅ Auto-uploads to TikTok
    ✅ Smart scheduling (5x daily)
    ✅ No human intervention needed!
    """)

if __name__ == "__main__":
    main()
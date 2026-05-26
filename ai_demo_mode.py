#!/usr/bin/env python3
"""
🚀 AI CONTENT FACTORY - DEMO MODE
=================================
This runs with demo data to show full functionality
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
import random

# ============================================
# DEMO STORIES (Simulating Reddit)
# ============================================

DEMO_STORIES = [
    {
        "id": "demo001",
        "title": "My wife spent our entire savings on a dog, then things got crazy",
        "text": """Three months ago I found out my wife had spent $47,000 of our savings on a dog. Yes, you read that right. A dog.

We had been saving for 5 years for a house down payment. $85,000 in our joint account. Gone in a single transaction to some breeder in another state.

When I confronted her, she said the dog was "her dream" and that I "didn't understand". She showed me pictures of this golden doodle and I will admit, it was cute. But $47,000 cute??

I was furious. We argued for weeks. I even considered divorce. But then something unexpected happened...

The dog, which we named Max, saved my daughter's life. My 6-year-old has diabetes and Max can detect when her blood sugar drops BEFORE the sensors can. He saved her twice in one week.

Now I can't imagine life without Max. And my wife? She's pregnant with our second child.

Sometimes the universe has plans we don't understand.""",
        "score": 45000,
        "num_comments": 8900,
        "subreddit": "relationships",
        "permalink": "https://reddit.com/r/relationships/comments/demo1"
    },
    {
        "id": "demo002", 
        "title": "UPDATE: I caught my best friend stealing from me - what happened next shocked everyone",
        "text": """Original post: I (28M) discovered my best friend of 15 years had been stealing from my business for 2 years. Over $120,000 gone.

Well, I hired a forensic accountant. I gathered evidence. And then I confronted him.

But here's where it got crazy. He didn't deny it. Instead, he broke down crying and told me his wife had cancer and the medical bills were destroying them.

I was torn. Angry? Yes. Sympathetic? Also yes.

I decided not to press charges on one condition: he would pay me back every penny. He agreed.

But wait... it gets better. A month later, his wife recovered. And here's the twist: she's a partner at a major law firm. She heard what happened and insisted on paying me back TWICE what he stole, plus an extra $50,000 as an "investment" in my business.

Sometimes karma works in mysterious ways.""",
        "score": 32000,
        "num_comments": 5600,
        "subreddit": "prorevenge",
        "permalink": "https://reddit.com/r/prorevenge/comments/demo2"
    },
    {
        "id": "demo003",
        "title": "I accidentally sent a love letter to my boss instead of my girlfriend",
        "text": """So this happened today and I'm still processing it.

I wrote a heartfelt love letter to my girlfriend of 3 years. It was our anniversary tomorrow and I wanted to do something special.

I drafted it on my phone, read it back to make sure it was perfect, and hit send.

Except... I hit the wrong contact.

My boss, Karen, 52, female, received my love letter.

The letter talked about how I "couldn't stop thinking about her", how "every moment apart felt like eternity", and how I "wanted to spend forever together".

In my defense, I had started writing it at work during a boring meeting.

Karen texted me back: "Interesting. Let's discuss over drinks Friday. But for the record, I'm flattered."

I'm either getting promoted or fired. I genuinely can't tell.

UPDATE: Just got home. My girlfriend loved the letter so much she cried. Then she asked why I was acting weird about Friday drinks. FML.""",
        "score": 67000,
        "num_comments": 12000,
        "subreddit": "tifu",
        "permalink": "https://reddit.com/r/tifu/comments/demo3"
    },
    {
        "id": "demo004",
        "title": "My entitled mother-in-law tried to take my house, then karma struck",
        "text": """My mother-in-law has always been... challenging. When my husband and I bought our first home, she was furious we didn't ask her for help (we didn't need it).

She constantly made comments about "her grandson deserving a bigger room" and "this house should be in the family name".

Then she did something unforgivable. She forged my signature on a quitclaim deed and tried to transfer my house to herself.

I caught it when the title company called me about a signature verification issue.

I pressed charges. She went to court. And here's where it gets beautiful:

The judge ordered her to sign a full apology to me, pay $25,000 in legal fees, AND she lost all visitation rights to our son for 6 months (long story, she made threats).

The best part? While she was dealing with legal issues, her own house went into foreclosure. Because apparently she was using her money for lawyers instead of her mortgage.

Now she lives in a tiny apartment and calls every week asking to see our son.

Karma is real.""",
        "score": 89000,
        "num_comments": 15000,
        "subreddit": "entitledparents",
        "permalink": "https://reddit.com/r/entitledparents/comments/demo4"
    },
    {
        "id": "demo005",
        "title": "I found out my dad isn't my biological father on my wedding day",
        "text": """This is going to be long, and I'm still shaking as I write this.

I (29F) got married last Saturday. It was supposed to be the happiest day of my life.

During the reception, my mom's best friend pulled me aside. She looked nervous and said there was something I needed to know.

She handed me an old photo. It was my mom, clearly pregnant, with another man.

The man was my biological father. My "dad" - the man who raised me, taught me to ride a bike, walked me down the aisle - wasn't my real father.

I confronted my mom. She didn't deny it. She said my biological father was a one-night-stand from before she met my dad. He wanted nothing to do with me. My dad, the man I call Dad, chose to stay and raise me as his own.

He never told me because he wanted to protect me. He said I was "his daughter in every way that matters".

I'm having complicated feelings. I love my dad more than ever. But I'm also angry that they kept this from me for 29 years.

My new husband has been amazing through all of this. He's suggesting therapy for us as a couple.

I don't know what to do. Do I reach out to my biological father? Do I confront my mom further? Do I pretend this didn't happen?

Any advice appreciated.""",
        "score": 95000,
        "num_comments": 18000,
        "subreddit": "confessions",
        "permalink": "https://reddit.com/r/confessions/comments/demo5"
    }
]

# ============================================
# GLOBAL STATE FOR VARIETY
# ============================================

_used_story_ids = set()
_story_index = 0

# ============================================
# AI STORY SELECTOR
# ============================================

def select_best_story(stories):
    """AI-powered story selection with variety"""
    global _story_index
    
    # Reset if we've used all stories
    if len(_used_story_ids) >= len(stories):
        _used_story_ids.clear()
        _story_index = 0
    
    # Score each story
    keywords_good = ["update", "finally", "plot twist", "shocking", "omg", "reveal", "karma", "surprise"]
    
    for story in stories:
        score = story["score"] / 100  # Base score from upvotes
        
        # Boost for engagement keywords
        for kw in keywords_good:
            if kw.lower() in story["title"].lower():
                score += 50
        
        # Boost for longer stories (more content)
        if len(story.get("text", "")) > 500:
            score += 30
        
        story["ai_score"] = score
    
    # Sort by AI score
    stories.sort(key=lambda x: x["ai_score"], reverse=True)
    
    # Pick story that's not been used
    for story in stories:
        if story["id"] not in _used_story_ids:
            _used_story_ids.add(story["id"])
            _story_index += 1
            return story
    
    # Fallback - cycle through
    selected = stories[_story_index % len(stories)]
    _story_index += 1
    return selected

# ============================================
# CONTENT GENERATOR
# ============================================

def generate_content(story):
    """Generate video content from story"""
    
    emojis = ["🔥", "😱", "💔", "😳", "👀", "🤯", "🎭", "💯"]
    
    content = {
        "title": f"{random.choice(emojis)} {story['title']}",
        "script": f"{story['title']}\n\n{story['text']}",
        "subreddit": story["subreddit"],
        "story_id": story["id"],
        "reddit_link": story["permalink"],
        "hashtags": generate_hashtags(story),
        "description": generate_description(story)
    }
    
    return content

def generate_hashtags(story):
    """Generate hashtags based on story content"""
    base = ["redditstories", "viral", "storytime", "confessions", "fyp"]
    
    # Add subreddit
    base.append(story["subreddit"].lower())
    
    # Add content-specific
    title = story["title"].lower()
    if "update" in title:
        base.append("update")
    if "karma" in title:
        base.append("karma")
    if "shock" in title or "shocked" in title:
        base.append("shocking")
    
    return base[:10]

def generate_description(story):
    """Generate YouTube description"""
    return f"""
Watch this incredible Reddit story unfold!

📖 Story from r/{story['subreddit']}
⬆️ Upvotes: {story['score']:,}

━━━━━━━━━━━━━━━━━━━━━━━━

💬 Comment your thoughts below!

👍 Like if you enjoyed!

🔔 Subscribe for daily stories!

━━━━━━━━━━━━━━━━━━━━━━━━

{' '.join(['#'+h for h in generate_hashtags(story)])}

━━━━━━━━━━━━━━━━━━━━━━━━

📱 Follow me:
YouTube: @sinname2015
TikTok: @casper.black07

Credit: Stories from Reddit community
"""

# ============================================
# VIDEO GENERATOR
# ============================================

def create_video_metadata(content):
    """Create video metadata (in real system, would generate actual video)"""
    
    video_id = content["story_id"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    video_data = {
        "video_id": f"{video_id}_{timestamp}",
        "content": content,
        "generated_at": datetime.now().isoformat(),
        "status": "ready"
    }
    
    # Save metadata
    output_dir = Path("./generated_videos")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / f"{video_id}_metadata.json", "w") as f:
        json.dump(video_data, f, indent=2)
    
    return str(output_dir / f"{video_id}.mp4")

# ============================================
# YOUTUBE UPLOADER (Simulated)
# ============================================

def upload_to_youtube(video_path, content):
    """Simulate YouTube upload"""
    
    # Generate fake video URL
    video_id = f"d_{content['story_id'][:8]}"
    url = f"https://youtu.be/{video_id}"
    
    return url

# ============================================
# TIKTOK UPLOADER (Simulated)
# ============================================

def upload_to_tiktok(video_path, content):
    """Simulate TikTok upload"""
    
    username = "casper.black07"
    video_id = content["story_id"][:8]
    
    return f"https://tiktok.com/@{username}/video/{video_id}"

# ============================================
# MAIN FACTORY
# ============================================

class AIContentFactory:
    """Complete AI-powered content factory - DEMO MODE"""
    
    def __init__(self):
        self.posted_today = 0
        self.max_posts = 5
        
    def run_cycle(self, story_index=None):
        """Run one content generation cycle"""
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║     🤖 AI CONTENT FACTORY - RUNNING                         ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        print("="*60)
        print("🚀 STARTING CONTENT GENERATION")
        print("="*60 + "\n")
        
        # Step 1: Select story
        print("📡 Step 1: Fetching and analyzing stories from Reddit...")
        story = select_best_story(DEMO_STORIES.copy())
        print(f"   ✅ Selected: {story['title'][:50]}...")
        print(f"   📊 AI Score: {story['ai_score']:.1f} | Upvotes: {story['score']:,} | Comments: {story['num_comments']:,}")
        print()
        
        # Step 2: Generate content
        print("🎨 Step 2: AI generating video content...")
        content = generate_content(story)
        print(f"   ✅ Title: {content['title'][:50]}...")
        print(f"   📝 Script length: {len(content['script'])} characters")
        print(f"   #️⃣  Hashtags: {', '.join(content['hashtags'][:5])}...")
        print()
        
        # Step 3: Create video
        print("🎬 Step 3: Generating video file...")
        video_path = create_video_metadata(content)
        print(f"   ✅ Video created: {video_path}")
        print()
        
        # Step 4: Upload to YouTube
        print("📺 Step 4: Uploading to YouTube...")
        youtube_url = upload_to_youtube(video_path, content)
        print(f"   ✅ Uploaded: {youtube_url}")
        print()
        
        # Step 5: Upload to TikTok
        print("📱 Step 5: Uploading to TikTok...")
        tiktok_url = upload_to_tiktok(video_path, content)
        print(f"   ✅ Posted: {tiktok_url}")
        print()
        
        # Save to history
        self._save_history(story, content, youtube_url, tiktok_url)
        
        self.posted_today += 1
        
        # Print summary
        print("="*60)
        print("✅ CYCLE COMPLETE!")
        print("="*60)
        print(f"""
📊 POST #{self.posted_today}/{self.max_posts}

📖 Story: {story['title'][:60]}...
📍 Source: r/{story['subreddit']}
⬆️ Upvotes: {story['score']:,}
💬 Comments: {story['num_comments']:,}

📺 YouTube: {youtube_url}
📱 TikTok: {tiktok_url}

━━━━━━━━━━━━━━━━━━━━━━━━

🎯 CONTENT READY FOR DISTRIBUTION!

The AI has:
   ✅ Selected the best story
   ✅ Generated engaging title
   ✅ Created video content
   ✅ Uploaded to YouTube
   ✅ Posted to TikTok
        """)
        
        return {
            "success": True,
            "story": story,
            "content": content,
            "youtube_url": youtube_url,
            "tiktok_url": tiktok_url
        }
    
    def _save_history(self, story, content, youtube_url, tiktok_url):
        """Save to content history"""
        
        history_file = Path("content_history.json")
        history = []
        
        if history_file.exists():
            try:
                with open(history_file) as f:
                    history = json.load(f)
            except:
                pass
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "story_title": story["title"],
            "subreddit": story["subreddit"],
            "score": story["score"],
            "ai_score": story.get("ai_score", 0),
            "youtube_url": youtube_url,
            "tiktok_url": tiktok_url
        }
        
        history.append(entry)
        
        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)
        
        print(f"\n📝 History saved to {history_file}")

# ============================================
# RUN DEMO
# ============================================

def run_demo():
    """Run the AI content factory demo"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   🚀 AI CONTENT FACTORY - FULL DEMONSTRATION                 ║
║                                                                ║
║   This will show the complete workflow of:                    ║
║   1. Fetching stories (simulated)                              ║
║   2. AI selecting best content                                 ║
║   3. Generating video metadata                                 ║
║   4. Uploading to YouTube                                      ║
║   5. Posting to TikTok                                         ║
║                                                                ║
║   Accounts:                                                   ║
║   - YouTube: @sinname2015                                     ║
║   - TikTok: @casper.black07                                   ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    input("\nPress ENTER to start the demo...\n")
    
    factory = AIContentFactory()
    
    # Run 3 demo cycles
    for i in range(3):
        print(f"\n{'#'*60}")
        print(f"# CONTENT CYCLE #{i+1}")
        print(f"{'#'*60}\n")
        
        results = factory.run_cycle()
        
        if i < 2:
            input("\nPress ENTER for next cycle...\n")
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ✅ DEMO COMPLETE!                                           ║
║                                                                ║
║   The AI Content Factory is fully operational!                ║
║                                                                ║
║   To go LIVE with real content:                               ║
║   1. Add Reddit API credentials                               ║
║   2. Add YouTube OAuth credentials                             ║
║   3. Login to TikTok in browser                               ║
║                                                                ║
║   Then run: python ai_content_factory.py --start              ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    import sys
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║   🚀 AI CONTENT FACTORY - FULL DEMONSTRATION                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    factory = AIContentFactory()
    
    # Run 3 demo cycles automatically
    for i in range(3):
        print(f"\n{'#'*60}")
        print(f"# CONTENT CYCLE #{i+1}")
        print(f"{'#'*60}\n")
        
        results = factory.run_cycle()
        time.sleep(1)  # Brief pause between cycles
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║   ✅ DEMO COMPLETE!                                          ║
╚══════════════════════════════════════════════════════════════╝
    """)
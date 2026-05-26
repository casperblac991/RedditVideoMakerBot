#!/usr/bin/env python3
"""
🎬 NO-API VIDEO POSTING SYSTEM
===============================
Simple system to post videos without needing APIs!
Works with just browser automation.

No API keys needed! ✅
"""

import os
import json
import time
import shutil
import webbrowser
from pathlib import Path
from datetime import datetime
import random

# ============================================
# ACCOUNT INFO
# ============================================

ACCOUNTS = {
    "youtube": {
        "name": "@sinname2015",
        "upload_url": "https://www.youtube.com/upload"
    },
    "tiktok": {
        "name": "@casper.black07",
        "upload_url": "https://www.tiktok.com/upload"
    }
}

# ============================================
# DEMO STORIES (Simulated Reddit)
# ============================================

STORIES = [
    {
        "id": "story001",
        "title": "My wife spent $47,000 on a dog - what happened next shocked me",
        "text": """Three months ago I discovered my wife spent our entire house savings on a dog. $47,000 on a golden doodle.

We had been saving for 5 years. $85,000 total. Gone in one transaction.

When I found out, I was ready to divorce her. But then something incredible happened...

The dog, Max, saved my daughter's life. My 6-year-old has diabetes and Max can detect blood sugar drops before any machine can.

Now I can't imagine life without Max. And my wife is pregnant with our second child.

Sometimes the universe has plans we don't understand.""",
        "subreddit": "relationships",
        "score": 45000
    },
    {
        "id": "story002",
        "title": "UPDATE: I caught my best friend stealing - what happened next will blow your mind",
        "text": """Original post: My best friend of 15 years stole $120,000 from my business.

I hired a forensic accountant. I gathered evidence. I confronted him.

He broke down crying. His wife had cancer and the medical bills were destroying them.

I decided not to press charges. He would pay me back every penny.

Then something unexpected happened. His wife recovered. She's a partner at a major law firm.

She insisted on paying me back TWICE what he stole, plus $50,000 as an investment in my business.

Karma works in mysterious ways.""",
        "subreddit": "prorevenge",
        "score": 32000
    },
    {
        "id": "story003",
        "title": "I accidentally sent a love letter to my boss instead of my girlfriend",
        "text": """So this happened today and I'm still processing it.

I wrote a heartfelt love letter to my girlfriend. It was our anniversary.

I drafted it on my phone during a boring meeting, hit send...

Except I hit the wrong contact.

My boss, Karen, 52, received my love letter about how I "couldn't stop thinking about her" and "wanted to spend forever together".

She texted back: "Interesting. Let's discuss over drinks Friday. But I'm flattered."

I'm either getting promoted or fired.

UPDATE: My girlfriend loved the letter so much she cried. She asked why I was acting weird about Friday drinks. FML.""",
        "subreddit": "tifu",
        "score": 67000
    }
]

# ============================================
# VIDEO GENERATOR (No API needed!)
# ============================================

def generate_video_package(story):
    """Generate a video package ready for upload"""
    
    print(f"\n🎬 Generating video for: {story['title'][:50]}...")
    
    # Create output folder
    output_dir = Path("./ready_to_upload")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create story folder
    story_folder = output_dir / f"{story['id']}_{datetime.now().strftime('%Y%m%d')}"
    story_folder.mkdir(exist_ok=True)
    
    # Generate content files
    content = {
        "title": f"{random.choice(['🔥','😱','💔','😳','👀'])} {story['title']}",
        "description": generate_description(story),
        "hashtags": generate_hashtags(story),
        "script": story["text"],
        "subreddit": story["subreddit"],
        "reddit_link": f"https://reddit.com/r/{story['subreddit']}",
        "reddit_upvotes": story["score"],
        "created_at": datetime.now().isoformat()
    }
    
    # Save content as JSON
    with open(story_folder / "content.json", "w") as f:
        json.dump(content, f, indent=2)
    
    # Save script as text file (for TTS)
    with open(story_folder / "script.txt", "w") as f:
        f.write(f"TITLE: {content['title']}\n\n")
        f.write(f"SOURCE: r/{story['subreddit']}\n")
        f.write(f"UPVOTES: {story['score']:,}\n\n")
        f.write("="*50 + "\n\n")
        f.write(content["script"])
    
    # Save title/description files
    with open(story_folder / "title.txt", "w") as f:
        f.write(content["title"])
    
    with open(story_folder / "description.txt", "w") as f:
        f.write(content["description"])
    
    with open(story_folder / "hashtags.txt", "w") as f:
        f.write(" ".join(["#"+h for h in content["hashtags"]]))
    
    # Create placeholder video info
    video_info = {
        "video_name": f"{story['id']}.mp4",
        "status": "generate_video",
        "folder_path": str(story_folder),
        "content": content
    }
    
    with open(story_folder / "video_info.json", "w") as f:
        json.dump(video_info, f, indent=2)
    
    # Create upload instructions
    instructions = f"""
╔══════════════════════════════════════════════════════════════╗
║                  📤 UPLOAD INSTRUCTIONS                       ║
╚══════════════════════════════════════════════════════════════╝

STORY: {content['title']}
SOURCE: r/{story['subreddit']} ({story['score']:,} upvotes)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 TIKTOK UPLOAD:
1. Go to: https://www.tiktok.com/upload
2. Login as @{ACCOUNTS['tiktok']['name']}
3. Upload video: {story['id']}.mp4 (or any video you create)
4. Caption: Copy from title.txt and hashtags.txt

📺 YOUTUBE UPLOAD:
1. Go to: https://www.youtube.com/upload
2. Login as @{ACCOUNTS['youtube']['name']}
3. Upload video: {story['id']}.mp4 (or any video you create)
4. Title: Copy from title.txt
5. Description: Copy from description.txt
6. Tags: Copy from hashtags.txt

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 TIP: Use the Reddit Video Maker Bot to generate actual video!
   python main.py
   Then move the output .mp4 to this folder as {story['id']}.mp4

    """
    
    with open(story_folder / "UPLOAD_INSTRUCTIONS.txt", "w") as f:
        f.write(instructions)
    
    print(f"✅ Video package created: {story_folder}")
    print(f"   📁 Files: content.json, script.txt, title.txt, description.txt")
    print(f"   📋 Instructions: UPLOAD_INSTRUCTIONS.txt")
    
    return story_folder

def generate_description(story):
    """Generate YouTube description"""
    return f"""
Watch this incredible Reddit story!

📖 Story from r/{story['subreddit']}
⬆️ Upvotes: {story['score']:,}
🔗 Original: https://reddit.com/r/{story['subreddit']}

━━━━━━━━━━━━━━━━━━━━━━━━

💬 Comment your thoughts!

👍 Like if you enjoyed!

🔔 Subscribe for daily stories!

━━━━━━━━━━━━━━━━━━━━━━━━

#redditstories #viral #storytime #confessions #{story['subreddit'].lower()} #fyp #foryou

━━━━━━━━━━━━━━━━━━━━━━━━

📱 Follow me:
YouTube: {ACCOUNTS['youtube']['name']}
TikTok: {ACCOUNTS['tiktok']['name']}

Credit: Stories from Reddit community
"""

def generate_hashtags(story):
    """Generate hashtags"""
    base = ["redditstories", "viral", "storytime", "confessions", "fyp", "foryou"]
    base.append(story["subreddit"].lower())
    
    title = story["title"].lower()
    if "update" in title:
        base.append("update")
    if "wife" in title or "husband" in title:
        base.append("relationship")
    if "boss" in title:
        base.append("funny")
    
    return base[:15]

# ============================================
# BROWSER AUTO-OPEN (No API needed!)
# ============================================

def open_upload_pages():
    """Open upload pages in browser"""
    
    print("\n🌐 Opening upload pages in browser...")
    
    # YouTube
    print(f"📺 Opening YouTube upload: {ACCOUNTS['youtube']['upload_url']}")
    webbrowser.open(ACCOUNTS['youtube']['upload_url'])
    time.sleep(2)
    
    # TikTok
    print(f"📱 Opening TikTok upload: {ACCOUNTS['tiktok']['upload_url']}")
    webbrowser.open(ACCOUNTS['tiktok']['upload_url'])
    
    print("\n✅ Upload pages opened!")
    print("   Login and upload your videos.")

# ============================================
# MAIN SYSTEM
# ============================================

def create_video_packages(count=5):
    """Create specified number of video packages"""
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║           🎬 NO-API VIDEO CONTENT FACTORY                    ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    print(f"Creating {count} video packages...\n")
    
    packages = []
    
    for i in range(count):
        print(f"\n{'='*60}")
        print(f"📦 PACKAGE #{i+1}/{count}")
        print(f"{'='*60}")
        
        # Pick a story
        story = STORIES[i % len(STORIES)]
        
        # Generate package
        folder = generate_video_package(story)
        packages.append(folder)
    
    print(f"""

╔══════════════════════════════════════════════════════════════╗
║                    ✅ COMPLETE!                              ║
╚══════════════════════════════════════════════════════════════╝

📁 {count} video packages created in: ./ready_to_upload/

Each package contains:
  📄 content.json      - All video metadata
  📝 script.txt        - Story script for TTS
  📌 title.txt         - Ready-to-copy title
  📋 description.txt   - Ready-to-copy description
  🏷️ hashtags.txt      - Ready-to-copy hashtags
  📖 UPLOAD_INSTRUCTIONS.txt - How to upload

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 NEXT STEPS:

Option 1: Quick Upload (Open pages manually)
   → Run: python no_api_poster.py
   → Opens YouTube/TikTok upload pages
   → Copy titles from ready_to_upload/ folder

Option 2: Use Reddit Video Maker Bot (Full Automation)
   → Run: python main.py
   → Generates actual video
   → Move to ready_to_upload/
   → Upload manually

Option 3: Hire a video editor
   → Give them ready_to_upload/ folder
   → They create videos
   → You upload

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Your Accounts:
   YouTube: {ACCOUNTS['youtube']['name']}
   TikTok: {ACCOUNTS['tiktok']['name']}

Good luck! 🚀
    """)
    
    return packages

def quick_upload():
    """Open upload pages and show packages"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                  🚀 QUICK UPLOAD MODE                        ║
╚══════════════════════════════════════════════════════════════╝

Opening upload pages and listing ready packages...
    """)
    
    # Open upload pages
    open_upload_pages()
    
    # List packages
    ready_folder = Path("./ready_to_upload")
    
    if ready_folder.exists():
        packages = list(ready_folder.iterdir())
        
        if packages:
            print(f"\n📦 Found {len(packages)} ready packages:\n")
            
            for i, package in enumerate(packages):
                if package.is_dir():
                    title_file = package / "title.txt"
                    if title_file.exists():
                        with open(title_file) as f:
                            title = f.read().strip()
                        print(f"   {i+1}. {title[:60]}...")
                        print(f"      📁 {package.name}/")
                    print()
    
    print("\n✅ Open the browser tabs and start uploading!")
    print("   Copy titles/descriptions from the ready_to_upload folder.")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--create":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            create_video_packages(count)
        elif sys.argv[1] == "--upload":
            quick_upload()
        elif sys.argv[1] == "--all":
            packages = create_video_packages(5)
            response = input("\nOpen upload pages? (y/n): ")
            if response.lower() == 'y':
                open_upload_pages()
    else:
        print("""
╔══════════════════════════════════════════════════════════════╗
║          🎬 NO-API VIDEO POSTING SYSTEM                      ║
╚══════════════════════════════════════════════════════════════╝

Usage:
    python no_api_poster.py --create [count]   Create video packages
    python no_api_poster.py --upload           Open upload pages
    python no_api_poster.py --all              Create + open pages

Examples:
    python no_api_poster.py --create 5         Create 5 video packages
    python no_api_poster.py --upload            Open upload pages
    python no_api_poster.py --all               Do everything
        """)
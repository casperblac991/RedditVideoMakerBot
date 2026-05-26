# 🎬 Auto Poster - TikTok & YouTube Automated Posting

## 📋 Overview

This auto-poster automatically uploads videos from the Reddit Video Maker Bot to your TikTok and YouTube accounts.

**Your Accounts:**
- 📱 TikTok: @casper.black07
- 🎥 YouTube: @sinname2015

---

## 🚀 Quick Setup

### 1. YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Search and enable "YouTube Data API v3"
4. Go to "APIs & Services" → "Credentials"
5. Create "OAuth client ID" (Desktop app)
6. Download the JSON file
7. Rename to `client_secrets.json` and place in this folder

### 2. Run Setup

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

python setup_auto_poster.py
```

### 3. Start Posting

```bash
python auto_poster.py
```

---

## 📁 Folder Structure

```
RedditVideoMakerBot/
├── video_output/        ← Videos from RedditVideoMakerBot go here
├── posted_videos/       ← Already posted videos
├── drafts/              ← Videos pending review
├── auto_poster.py       ← Main posting script
├── setup_auto_poster.py ← Setup wizard
└── client_secrets.json  ← YouTube API credentials (create this)
```

---

## ⚙️ Configuration

Edit `auto_post_config.json`:

```json
{
    "videos_folder": "./video_output",
    "daily_limit": 5,
    "youtube": {
        "enabled": true
    },
    "tiktok": {
        "enabled": false
    }
}
```

---

## ⏰ Scheduling (Linux/Mac)

Add to crontab:
```bash
crontab -e
```

Add line:
```
0 9,12 * * * cd /path/to/RedditVideoMakerBot && python3 auto_poster.py
```

This posts at 9 AM and 12 PM daily.

---

## ⏰ Scheduling (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 9:00 AM
4. Action: Start a program
5. Program: `python`
6. Arguments: `auto_poster.py`

---

## ⚠️ Important Notes

1. **Quality Content**: Only post engaging stories (drama, surprises, confessions)
2. **Don't Spam**: Limit to 5 videos per day per platform
3. **Engage**: Respond to comments to grow your channel
4. **Copyright**: Only post content you have rights to
5. **TikTok API**: No official API exists; use third-party services like Buffer or Later

---

## 🔧 Troubleshooting

### YouTube: "Access Denied"
- Delete `client_secrets.json` and re-authenticate
- Make sure OAuth consent screen is configured

### No videos found
- Check `videos_folder` path in config
- Make sure RedditVideoMakerBot has produced videos

### TikTok not working
- TikTok doesn't have public API
- Use Buffer, Later, or SocialBee for TikTok posting

---

## 💡 Tips for Success

1. **Best Subreddits for stories**:
   - r/AskReddit
   - r/relationships
   - r/confessions
   - r/entitledparents
   - r/prorevenge

2. **Video timing**:
   - Post when your audience is active
   - Morning (7-9 AM) and evening (6-9 PM) work best

3. **Titles that work**:
   - Use emojis: 🔥😱💔😳
   - Create curiosity: "Wait for the ending..."
   - Simple and clear

4. **Consistency**: Post every day for best results

---

## 📞 Support

For issues, check the logs in `auto_post.log`

Good luck with your content! 🚀
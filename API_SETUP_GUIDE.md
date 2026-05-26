# 🔑 COMPLETE API SETUP GUIDE
## For AI Content Factory - @sinname2015 & @casper.black07

---

## 📱 REDDIT API SETUP

### Step 1: Go to Reddit Apps
**URL:** https://www.reddit.com/prefs/apps

1. Login to your Reddit account
2. Scroll down to "Developed Applications"
3. Click "Create App" or "Create Another App"

### Step 2: Fill in App Details

```
Name: ContentFactoryBot
App Type: script
Description: AI-powered content factory for video creation
Redirect URI: http://localhost:8080
```

### Step 3: Get Your Credentials

After creating, you'll see:
- **CLIENT ID** - Located under your app name (looks like: `abc123DEF456`)
- **CLIENT SECRET** - The long password string

### Step 4: Add to Configuration

Open `api_config.json` and add:
```json
{
  "reddit": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "user_agent": "ContentFactoryBot/1.0"
  }
}
```

---

## 📺 YOUTUBE API SETUP

### Step 1: Go to Google Cloud Console
**URL:** https://console.cloud.google.com/

1. Login with your Google account
2. Click "Select a project" at the top
3. Click "New Project"

### Step 2: Create Project

```
Project Name: ContentFactory
Location: No organization
```

Click "Create"

### Step 3: Enable YouTube Data API v3

1. In the sidebar, go to "APIs & Services" → "Library"
2. Search: "YouTube Data API v3"
3. Click on it
4. Click "Enable"

### Step 4: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: "Desktop app"
4. Name: "Content Factory Uploader"
5. Click "Create"

### Step 5: Download Credentials

1. A popup will appear with your Client ID and Client Secret
2. Click "Download JSON"
3. **RENAME** the file to: `youtube_credentials.json`
4. **PLACE** it in the project folder (same folder as this script)

### Step 6: First Authentication

The first time you run the script, it will:
1. Open a browser window
2. Ask you to login to your Google account
3. Ask permission to "Manage your YouTube account"
4. Give you a code to paste back

This creates the `youtube_credentials.json` file needed for future runs.

---

## 📱 TIKTOK API SETUP

### ⚠️ Important Notice

**TikTok does NOT have an official public API for posting videos.**

We use **Browser Automation** instead:

### Setup Process:

1. **First Run:** The script will open TikTok in your browser
2. **Login:** Manually login with `@casper.black07`
3. **Save Session:** The browser session is automatically saved
4. **Future Runs:** No login needed - session is reused

### How to Enable:

1. Make sure Chrome/Chromium is installed
2. Install Playwright: `pip install playwright`
3. Install browsers: `playwright install chromium`

---

## 📋 QUICK SETUP CHECKLIST

```
[ ] Reddit App Created at reddit.com/prefs/apps
[ ] Reddit Client ID: _______________
[ ] Reddit Client Secret: _______________
[ ] Google Cloud Project Created
[ ] YouTube Data API v3 Enabled
[ ] OAuth Credentials Downloaded
[ ] youtube_credentials.json in project folder
[ ] Chrome/Chromium installed for TikTok
```

---

## 🧪 TEST YOUR SETUP

Run the setup wizard:
```bash
python setup_api_guide.py
```

Or test individually:
```bash
# Test Reddit
python -c "import praw; print('✅ PRAW installed')"

# Test YouTube
python -c "from googleapiclient.discovery import build; print('✅ YouTube API ready')"

# Test Playwright
python -m playwright install chromium
```

---

## 📁 EXPECTED FILE STRUCTURE

After setup, your folder should have:

```
RedditVideoMakerBot/
├── api_config.json           ← Reddit credentials
├── youtube_credentials.json  ← YouTube OAuth
├── tiktok_session.json      ← TikTok session (after first login)
├── ai_content_factory.py    ← Main script
├── ai_demo_mode.py          ← Demo script
├── setup_api_guide.py       ← Setup wizard
└── ... (other files)
```

---

## 🚀 START THE CONTENT FACTORY

Once all APIs are configured:

```bash
# Demo mode (works without API keys)
python ai_demo_mode.py

# Full automation mode
python ai_content_factory.py

# Setup wizard
python setup_api_guide.py
```

---

## 📊 EXPECTED OUTPUT

When everything is working:

```
🤖 AI CONTENT FACTORY - RUNNING

📡 Step 1: Fetching stories from Reddit...
   ✅ Fetched 20 stories from r/AskReddit, r/relationships, etc.

🧠 Step 2: AI selecting best story...
   ✅ Selected: "My wife spent our savings on a dog..." (95k upvotes)

🎨 Step 3: Generating video content...
   ✅ Title: 🔥 My wife spent our entire savings on a dog...

🎬 Step 4: Generating video file...
   ✅ Video created: generated_videos/story_123.mp4

📺 Step 5: Uploading to YouTube...
   ✅ Uploaded: https://youtu.be/abc123

📱 Step 6: Posting to TikTok...
   ✅ Posted: https://tiktok.com/@casper.black07/video/123

✅ CYCLE COMPLETE!
```

---

## ⚠️ TROUBLESHOOTING

### Reddit: "Invalid client_id"
- Check that you copied the correct client ID
- Make sure the app is set to "script" type
- Try creating a new app

### YouTube: "access_denied"
- Delete `youtube_credentials.json`
- Run the script again and re-authenticate
- Make sure you're logged into the correct Google account

### TikTok: "Login required"
- Delete `tiktok_session.json`
- Run the script - it will prompt for browser login
- Login manually and the session will be saved

---

## 🔐 SECURITY NOTES

- Never share your API credentials
- Never commit `api_config.json` or `youtube_credentials.json` to git
- The `.gitignore` file should exclude these files
- If credentials are compromised, delete the app and create new ones

---

## 📞 SUPPORT

If you need help:
1. Check the logs in `ai_content_factory.log`
2. Run setup wizard: `python setup_api_guide.py`
3. Verify each API independently

Good luck! 🚀
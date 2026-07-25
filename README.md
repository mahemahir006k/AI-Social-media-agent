# 🤖 AI Social Media Manager

An AI-powered social media automation system built with **Flowise**, **Groq LLM**, **Pollinations AI**, **Meta Graph API**, **PowerShell**, and **Windows Task Scheduler**.

This project automatically generates high-quality Facebook posts, creates AI-generated images, and publishes them to a Facebook Page every day without manual intervention.

---

# 🚀 Features

- ✅ AI-generated Facebook captions
- ✅ AI-generated image prompts
- ✅ Automatic image generation using Pollinations AI
- ✅ Automatic Facebook publishing
- ✅ Daily scheduling using Windows Task Scheduler
- ✅ Flowise AgentFlow orchestration
- ✅ Groq LLM integration
- ✅ PowerShell automation
- ✅ Logging for every execution
- ✅ Easy deployment

---

# 🏗 Architecture

```text
                    +-----------------------+
                    | Windows Task Scheduler|
                    +-----------+-----------+
                                |
                                v
                 daily-facebook-post.ps1
                                |
                                v
                 Flowise Prediction API
                                |
         +----------------------+----------------------+
         |                      |                      |
         v                      v                      v
 Caption Writer      Image Prompt Writer      Image Generator
         |                      |                      |
         +----------------------+----------------------+
                                |
                                v
                    Facebook Publisher Tool
                                |
                                v
                     Meta Graph API
                                |
                                v
                        Facebook Page
```

---

# 📂 Project Structure

```text
AI-Social-Media-Manager
│
├── automation
│   ├── daily-facebook-post.ps1
│   ├── Daily-Facebook-AI-Post.xml
│   └── start-flowise.cmd
│
├── flowise
│   └── ai-social-media-manager.json
│
├── docs
│
├── screenshots
│
├── logs
│
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙ Technologies Used

- Flowise
- Groq LLM
- Meta Graph API
- Pollinations AI
- PowerShell
- Windows Task Scheduler
- JavaScript Tool Nodes
- REST APIs

---

# 🔄 Workflow

```
Start
      │
      ▼
Facebook Caption Writer
      │
      ▼
Image Prompt Writer
      │
      ▼
Generate AI Image
      │
      ▼
Publish to Facebook
      │
      ▼
End
```

---

# 📅 Automatic Posting

The project uses **Windows Task Scheduler** to automatically execute the PowerShell automation script.

Schedule:

```
Every Day
10:00 AM
```

The scheduler performs:

1. Checks Flowise availability
2. Calls the Flowise Prediction API
3. Generates today's topic
4. Creates the Facebook caption
5. Generates the AI image
6. Publishes the post to Facebook
7. Stores execution logs

---

# 🖥 Flowise AgentFlow

The workflow consists of four AI agents:

### 1. Facebook Caption Writer

Generates:

- Professional Facebook caption
- Call-to-action
- Exactly 5 hashtags

---

### 2. Facebook Image Prompt Writer

Creates a premium image-generation prompt including:

- Subject
- Composition
- Lighting
- Color palette
- Social media optimized design

---

### 3. Image Generator

Uses:

- Pollinations AI

Returns:

- Public image URL

---

### 4. Facebook Publisher

Uses:

- Meta Graph API

Publishes:

- Caption
- Generated image

Returns:

```json
{
  "id": "photo_id",
  "post_id": "facebook_post_id"
}
```

---

# 📸 Example Output

### AI Generated Caption

```
🚀 Unlock the future of business automation with Generative AI!

Discover how AI can streamline workflows, increase productivity, and transform your business.

Ready to innovate?

Follow us for more AI insights.

#AI
#GenerativeAI
#Automation
#Business
#Technology
```

---

# 🛠 Requirements

- Windows 10 / Windows 11
- Node.js
- Flowise
- Groq API Key
- Facebook Page
- Long-lived Facebook Page Access Token
- Internet Connection

---

# 🔑 Environment Variables

Create a local `.env` file using:

```
FLOWISE_BASE_URL=
FLOWISE_FLOW_ID=
FLOWISE_API_KEY=

FB_PAGE_ID=
FB_PAGE_ACCESS_TOKEN=

GROQ_API_KEY=
```

**Do not commit real credentials to GitHub.**

---

# ▶ Running Manually

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\automation\daily-facebook-post.ps1"
```

---

# ⏰ Scheduled Execution

Import:

```
automation/Daily-Facebook-AI-Post.xml
```

using

```
Task Scheduler
→ Import Task
```

---

# 📊 Logging

Execution logs are stored in:

```
logs/
```

Example:

```
facebook-post-2026-07-25.log
```

---

# 📈 Future Enhancements

- LinkedIn publishing
- Instagram publishing
- Twitter/X publishing
- AI hashtag optimization
- Multiple post scheduling
- AI analytics dashboard
- Trending topic detection
- Multi-language content generation

---

# 🔒 Security

Never upload:

- Facebook Access Tokens
- Groq API Keys
- Flowise API Keys
- `.env`
- Database files
- Log files

Use `.env.example` for configuration templates.

---

# 🤝 Contributing

Pull requests and suggestions are welcome.

If you'd like to improve this project, feel free to fork the repository and submit a PR.

---

# ⭐ If you like this project

Please consider giving it a ⭐ on GitHub.

---

# 👩‍💻 Author

**Rohini Thulasiraman**

Technical Architect | AI Enthusiast | Java | Spring Boot | Azure | Flowise | Generative AI

---

## 📄 License

This project is licensed under the MIT License.

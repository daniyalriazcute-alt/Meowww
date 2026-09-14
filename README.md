# 🛡️ AI Offensive Security — Streamlit Website

A black-and-pink neon "cyberpunk" themed research & blog site about AI
offensive security (prompt injection, jailbreaking, indirect prompt
injection, and evasion techniques), with MongoDB-backed user registration
and login. Built entirely in Python with Streamlit.

## ✨ Features

- **Home** — animated neon hero, feature highlights, latest research preview
- **Blog** — filterable/searchable articles on:
  - Prompt Injection 101
  - Jailbreaking (roleplay, obfuscation, persona attacks)
  - Indirect Prompt Injection (RAG / agent attacks)
  - Evasion Techniques (bypassing safety filters)
  - OWASP LLM Top 10 mapping
- **Contact** — `daniyalriazcute@gmail.com`, with a mailto contact form
- **Register / Login** — name, email, password; passwords hashed with
  PBKDF2-HMAC-SHA256 (200,000 iterations, stdlib only, no plaintext storage)
- **MongoDB Atlas (free tier)** for persisting user accounts, with a
  local in-memory fallback so the app still runs without a DB configured

> ⚠️ **Content note:** all offensive-security articles are written at a
> conceptual / defensive level for research and awareness. They explain how
> attack classes work and how to defend against them — they do not publish
> ready-to-use exploit payloads.

## 📁 Project structure

```
aioffsec/
├── Home.py                      # Main entry point (Home page)
├── pages/
│   ├── 1_📝_Blog.py
│   ├── 2_📧_Contact.py
│   ├── 3_🔐_Login.py
│   └── 4_✍️_Register.py
├── utils/
│   ├── style.py                 # Shared black/pink neon CSS theme
│   ├── db.py                    # MongoDB connection + auth helpers
│   └── content.py                # Blog post content
├── assets/
│   └── background.jpg           # Cyborg background image (your upload)
├── .streamlit/
│   ├── config.toml              # Theme config
│   └── secrets.toml.example     # Template for MongoDB URI
├── requirements.txt
└── README.md
```

## 🚀 Run locally

```bash
cd aioffsec
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run Home.py
```

The app works immediately in **local demo mode** (no database needed) —
registered accounts just won't survive a restart. To persist users, set up
free MongoDB Atlas (next section).

## 🍃 Free MongoDB Atlas setup (takes ~5 minutes)

1. Go to <https://www.mongodb.com/cloud/atlas/register> and create a free
   account (no credit card required).
2. Create a new **free "M0" cluster** (pick any region close to you).
3. Under **Database Access**, create a database user with a username and
   password (save these — you'll need them for the connection string).
4. Under **Network Access**, add `0.0.0.0/0` (allow access from anywhere)
   so Streamlit Cloud can connect — or restrict it to Streamlit Cloud's IPs
   if you prefer tighter security.
5. Click **Connect → Drivers**, choose **Python**, and copy the connection
   string. It looks like:
   ```
   mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority
   ```
6. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and
   paste your connection string in as `MONGO_URI`:
   ```toml
   MONGO_URI = "mongodb+srv://myuser:mypassword@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
   ```
7. Restart the app — the "local demo mode" warning should disappear once
   it connects successfully.

The app automatically creates an `ai_offensive_security` database and a
`users` collection the first time someone registers — no manual schema
setup required.

## ☁️ Deploy to Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Go to <https://share.streamlit.io> and click **New app**.
3. Point it at your repo, branch, and set the main file path to `Home.py`.
4. In the app's **Settings → Secrets**, paste the contents of your
   `secrets.toml` (the `MONGO_URI` line from above).
5. Click **Deploy**. Streamlit Cloud installs `requirements.txt`
   automatically.

## 🔒 Security notes

- Passwords are hashed with PBKDF2-HMAC-SHA256 + a random 16-byte salt per
  user, using only the Python standard library (`hashlib`, `hmac`) — no
  extra native dependency required.
- Never commit a real `secrets.toml` to version control — only the
  `.example` template is included here.
- The contact form does not send email server-side; it opens the visitor's
  own email client via a `mailto:` link addressed to
  `daniyalriazcute@gmail.com`, so no SMTP credentials are needed.

## 🎨 Customizing the theme

All neon glow / black-pink styling lives in `utils/style.py`
(`inject_global_css()`). Tweak the CSS variables at the top of that file —
`--neon-pink`, `--neon-magenta`, `--bg-black` — to adjust the palette
site-wide.

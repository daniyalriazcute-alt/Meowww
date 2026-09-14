"""
Shared visual theme for the AI Offensive Security website.
Black + neon pink glow aesthetic, with the cyborg background image
applied as a fixed, darkened backdrop on every page.
"""

import base64
from pathlib import Path

import streamlit as st

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
BG_IMAGE_PATH = ASSETS_DIR / "background.jpg"


@st.cache_data(show_spinner=False)
def _get_base64(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def inject_global_css():
    """Injects the full black/pink neon theme + background image."""
    bg_b64 = _get_base64(BG_IMAGE_PATH) if BG_IMAGE_PATH.exists() else ""

    bg_css = (
        f"""
        background-image:
            linear-gradient(180deg, rgba(0,0,0,0.88) 0%, rgba(5,0,8,0.93) 45%, rgba(0,0,0,0.97) 100%),
            url("data:image/jpg;base64,{bg_b64}");
        """
        if bg_b64
        else "background-color:#05010a;"
    )

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

        :root {{
            --neon-pink: #ff2fb0;
            --neon-pink-soft: #ff6fd8;
            --neon-magenta: #d600ff;
            --bg-black: #050007;
            --panel-black: rgba(15, 4, 18, 0.72);
            --text-light: #f3e9f7;
            --text-dim: #c9a9d6;
        }}

        html, body, [class*="css"] {{
            font-family: 'Rajdhani', sans-serif;
        }}

        .stApp {{
            {bg_css}
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
            color: var(--text-light);
        }}

        /* Hide default streamlit chrome for a custom feel */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{background: transparent !important;}}

        h1, h2, h3, h4 {{
            font-family: 'Orbitron', sans-serif;
            color: #ffffff;
            text-shadow: 0 0 8px var(--neon-pink), 0 0 22px rgba(255,47,176,0.55);
            letter-spacing: 1px;
        }}

        p, li, label, span, div {{
            color: var(--text-light);
        }}

        a {{
            color: var(--neon-pink-soft);
        }}

        /* ---------- Glass / glow panel ---------- */
        .glow-panel {{
            background: var(--panel-black);
            border: 1px solid rgba(255, 47, 176, 0.35);
            border-radius: 18px;
            padding: 28px 32px;
            margin-bottom: 22px;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 18px rgba(255, 47, 176, 0.18), inset 0 0 40px rgba(214, 0, 255, 0.05);
            transition: all 0.25s ease-in-out;
        }}
        .glow-panel:hover {{
            box-shadow: 0 0 30px rgba(255, 47, 176, 0.45), inset 0 0 50px rgba(214, 0, 255, 0.08);
            border-color: rgba(255, 111, 216, 0.7);
        }}

        /* ---------- Hero title ---------- */
        .hero-title {{
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            font-size: 3.2rem;
            text-align: center;
            background: linear-gradient(90deg, #ffffff 0%, #ff6fd8 45%, #ff2fb0 70%, #d600ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 35px rgba(255, 47, 176, 0.6);
            margin-bottom: 0;
        }}
        .hero-sub {{
            text-align: center;
            color: var(--text-dim);
            font-size: 1.15rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 4px;
        }}

        .neon-divider {{
            height: 2px;
            border: none;
            margin: 26px 0;
            background: linear-gradient(90deg, transparent, var(--neon-pink), var(--neon-magenta), transparent);
            box-shadow: 0 0 12px var(--neon-pink);
        }}

        /* ---------- Badges / tags ---------- */
        .tag {{
            display: inline-block;
            padding: 4px 14px;
            margin: 3px 6px 3px 0;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            color: #fff;
            background: rgba(255, 47, 176, 0.15);
            border: 1px solid var(--neon-pink);
            box-shadow: 0 0 8px rgba(255, 47, 176, 0.35);
        }}

        .severity-high {{ border-color:#ff2f6a; box-shadow:0 0 8px rgba(255,47,106,.5); }}
        .severity-med  {{ border-color:#ff9d2f; box-shadow:0 0 8px rgba(255,157,47,.5); }}
        .severity-low  {{ border-color:#2fe4ff; box-shadow:0 0 8px rgba(47,228,255,.5); }}

        /* ---------- Buttons ---------- */
        .stButton>button, .stFormSubmitButton>button {{
            background: linear-gradient(90deg, #ff2fb0, #d600ff);
            color: #fff;
            border: none;
            border-radius: 10px;
            padding: 10px 26px;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            letter-spacing: 1px;
            box-shadow: 0 0 14px rgba(255, 47, 176, 0.55);
            transition: all 0.2s ease-in-out;
            width: 100%;
        }}
        .stButton>button:hover, .stFormSubmitButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 0 26px rgba(255, 47, 176, 0.9);
            color: #fff;
        }}

        /* ---------- Inputs ---------- */
        .stTextInput>div>div>input, .stTextArea textarea {{
            background: rgba(20, 4, 24, 0.75) !important;
            color: #fff !important;
            border: 1px solid rgba(255, 47, 176, 0.4) !important;
            border-radius: 8px !important;
        }}
        .stTextInput>div>div>input:focus, .stTextArea textarea:focus {{
            border: 1px solid var(--neon-pink) !important;
            box-shadow: 0 0 10px rgba(255, 47, 176, 0.6) !important;
        }}

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0a0210 0%, #05000a 100%);
            border-right: 1px solid rgba(255, 47, 176, 0.25);
        }}
        section[data-testid="stSidebar"] * {{
            color: var(--text-light) !important;
        }}

        /* ---------- Center avatar / logo image ---------- */
        .avatar-glow img {{
            border-radius: 50%;
            border: 2px solid var(--neon-pink);
            box-shadow: 0 0 25px rgba(255, 47, 176, 0.7), 0 0 60px rgba(214, 0, 255, 0.35);
        }}

        .footer-note {{
            text-align:center;
            color: var(--text-dim);
            font-size: 0.85rem;
            margin-top: 40px;
            opacity: 0.8;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str = ""):
    st.markdown(f'<div class="hero-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="hero-sub">{subtitle}</div>', unsafe_allow_html=True)


def divider():
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)


def panel_start():
    st.markdown('<div class="glow-panel">', unsafe_allow_html=True)


def panel_end():
    st.markdown('</div>', unsafe_allow_html=True)


def footer():
    st.markdown(
        '<div class="footer-note">© 2026 AI Offensive Security &nbsp;|&nbsp; '
        'Research &amp; education for defenders, not a how-to for attackers.</div>',
        unsafe_allow_html=True,
    )

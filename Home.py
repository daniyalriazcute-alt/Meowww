import base64
from pathlib import Path

import streamlit as st

from utils.style import inject_global_css, hero, divider, panel_start, panel_end, footer, BG_IMAGE_PATH
from utils.db import is_authenticated
from utils.content import get_all_posts

st.set_page_config(
    page_title="AI Offensive Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

# --- TEMPORARY DEBUG BLOCK ---
try:
    _keys = list(st.secrets.keys())
    st.warning(f"DEBUG: keys = {_keys}")
    if "MONGO_URI" in st.secrets:
        st.success("DEBUG: MONGO_URI found")
    else:
        st.error("DEBUG: MONGO_URI MISSING")
except Exception as e:
    st.error(f"DEBUG: error reading secrets — {e}")
# --- END DEBUG BLOCK ---

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    if BG_IMAGE_PATH.exists():
        st.markdown('<div class="avatar-glow">', unsafe_allow_html=True)
        st.image(str(BG_IMAGE_PATH), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("### 🛡️ AI Offensive Security")
    if is_authenticated():
        st.success(f"Signed in as **{st.session_state.get('user_name')}**")
    else:
        st.info("You're browsing as a guest. Log in for the full experience.")
    st.caption("Navigate using the pages menu above ☝️")

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
hero("AI OFFENSIVE SECURITY", "Red-teaming the machines before someone else does")

st.markdown(
    """
    <p style='text-align:center; max-width:780px; margin:18px auto 0 auto; color:#e7d4ee; font-size:1.05rem;'>
    A research &amp; education hub covering how large language models get attacked —
    prompt injection, jailbreaking, indirect injection, and evasion — so defenders
    can build AI systems that hold up under real adversarial pressure.
    </p>
    """,
    unsafe_allow_html=True,
)

divider()

# ---------------------------------------------------------------------------
# Feature cards
# ---------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    panel_start()
    st.markdown("#### 🧬 Attack Taxonomy")
    st.write(
        "Deep-dive write-ups on prompt injection, jailbreaking, indirect "
        "injection, and filter-evasion technique families — explained at a "
        "conceptual level for red teams and defenders."
    )
    panel_end()

with col2:
    panel_start()
    st.markdown("#### 🧪 Defense Playbooks")
    st.write(
        "Every post pairs the offense with concrete mitigations: least-privilege "
        "tool access, output handling, context segmentation, and monitoring "
        "strategies you can apply today."
    )
    panel_end()

with col3:
    panel_start()
    st.markdown("#### 🔐 Member Access")
    st.write(
        "Create a free account to bookmark research, track your reading, and "
        "get notified as new technique write-ups are published."
    )
    if not is_authenticated():
        st.page_link("pages/4_✍️_Register.py", label="Create your account →")
    panel_end()

divider()

# ---------------------------------------------------------------------------
# Latest posts preview
# ---------------------------------------------------------------------------
st.markdown("### 📰 Latest Research")

posts = get_all_posts()
cols = st.columns(3)
for i, post in enumerate(posts[:3]):
    with cols[i % 3]:
        panel_start()
        sev_class = f"severity-{post['severity']}"
        st.markdown(
            f'<span class="tag {sev_class}">{post["severity"].upper()} SEVERITY</span>',
            unsafe_allow_html=True,
        )
        st.markdown(f"##### {post['title']}")
        st.caption(f"⏱️ {post['read_time']} &nbsp;|&nbsp; " + " • ".join(post["tags"]))
        st.write(post["summary"])
        panel_end()

st.markdown("")
left, mid, right = st.columns([1, 1, 1])
with mid:
    st.page_link("pages/1_📝_Blog.py", label="Browse the full blog →", icon="📝")

divider()
footer()

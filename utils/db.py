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

# ============================================================
# TEMPORARY MONGODB DIAGNOSTIC
# ============================================================
st.markdown("## 🔧 MongoDB Diagnostic")

try:
    _keys = list(st.secrets.keys())
    st.write(f"**1. Secrets keys:** `{_keys}`")

    if "MONGO_URI" not in st.secrets:
        st.error("❌ MONGO_URI is MISSING from Streamlit Cloud secrets.")
    else:
        _uri = st.secrets["MONGO_URI"]
        st.write(f"**2. MONGO_URI length:** `{len(_uri)}` characters")
        st.write(f"**3. MONGO_URI prefix:** `{_uri[:55]}`")

        try:
            from pymongo import MongoClient
            st.write("**4. Pinging MongoDB...**")
            _c = MongoClient(_uri, serverSelectionTimeoutMS=8000)
            _result = _c.admin.command("ping")
            st.success(f"✅ PING SUCCESS — {_result}")
        except Exception as _e:
            st.error(f"❌ PING FAILED — **{type(_e).__name__}**")
            st.code(str(_e))
except Exception as _outer:
    st.error(f"❌ Error reading secrets — {type(_outer).__name__}")
    st.code(str(_outer))

st.markdown("---")
# ============================================================

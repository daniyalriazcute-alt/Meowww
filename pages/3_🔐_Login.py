import streamlit as st

from utils.style import inject_global_css, hero, divider, panel_start, panel_end, footer, BG_IMAGE_PATH
from utils.db import authenticate_user, is_authenticated, logout, db_is_connected

st.set_page_config(page_title="Login | AI Offensive Security", page_icon="🔐", layout="wide")
inject_global_css()

hero("MEMBER LOGIN", "Access your AI Offensive Security account")
divider()

if not db_is_connected():
    st.warning(
        "⚠️ No MongoDB connection configured — running in **local demo mode**. "
        "Accounts created this session will work for login but won't persist "
        "after a restart. See the README to connect a free MongoDB Atlas cluster.",
        icon="⚠️",
    )

if is_authenticated():
    img_col, info_col = st.columns([1, 2])
    with img_col:
        if BG_IMAGE_PATH.exists():
            st.markdown('<div class="avatar-glow">', unsafe_allow_html=True)
            st.image(str(BG_IMAGE_PATH), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    with info_col:
        panel_start()
        st.markdown(f"### 👋 Welcome back, {st.session_state.get('user_name')}")
        st.write(f"**Email:** {st.session_state.get('user_email')}")
        st.write(
            "You're logged in. Head over to the Blog to keep reading the latest "
            "offensive-security research, or log out below."
        )
        if st.button("Log out"):
            logout()
            st.rerun()
        panel_end()
else:
    img_col, form_col = st.columns([1, 1.3])

    with img_col:
        if BG_IMAGE_PATH.exists():
            st.markdown('<div class="avatar-glow">', unsafe_allow_html=True)
            st.image(str(BG_IMAGE_PATH), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align:center; color:#c9a9d6;'>Access granted only to authenticated operators.</p>",
            unsafe_allow_html=True,
        )

    with form_col:
        panel_start()
        with st.form("login_form"):
            st.markdown("#### 🔐 Sign In")
            email = st.text_input("Email address", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Log In")

            if submitted:
                if not email or not password:
                    st.error("Please enter both email and password.")
                else:
                    ok, msg = authenticate_user(email, password)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

        st.markdown("Don't have an account?")
        st.page_link("pages/4_✍️_Register.py", label="Create one here →", icon="✍️")
        panel_end()

divider()
footer()

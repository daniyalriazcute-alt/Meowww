import streamlit as st

from utils.style import inject_global_css, hero, divider, panel_start, panel_end, footer, BG_IMAGE_PATH
from utils.db import register_user, is_authenticated, db_is_connected

st.set_page_config(page_title="Register | AI Offensive Security", page_icon="✍️", layout="wide")
inject_global_css()

hero("CREATE ACCOUNT", "Join the AI Offensive Security research community")
divider()

if not db_is_connected():
    st.warning(
        "⚠️ No MongoDB connection configured — running in **local demo mode**. "
        "Accounts created this session will work for login but won't persist "
        "after a restart. See the README to connect a free MongoDB Atlas cluster.",
        icon="⚠️",
    )

if is_authenticated():
    st.success(f"You're already signed in as **{st.session_state.get('user_name')}**.")
    st.page_link("pages/3_🔐_Login.py", label="Go to your account →", icon="🔐")
else:
    img_col, form_col = st.columns([1, 1.3])

    with img_col:
        if BG_IMAGE_PATH.exists():
            st.markdown('<div class="avatar-glow">', unsafe_allow_html=True)
            st.image(str(BG_IMAGE_PATH), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align:center; color:#c9a9d6;'>Passwords are hashed with "
            "PBKDF2-HMAC-SHA256 and never stored in plain text.</p>",
            unsafe_allow_html=True,
        )

    with form_col:
        panel_start()
        with st.form("register_form"):
            st.markdown("#### ✍️ Sign Up")
            name = st.text_input("Full name", placeholder="Jane Doe")
            email = st.text_input("Email address", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="At least 8 characters")
            confirm = st.text_input("Confirm password", type="password", placeholder="Re-enter your password")
            st.caption("Password must include an uppercase letter, a lowercase letter, and a number.")
            submitted = st.form_submit_button("Create Account")

            if submitted:
                if password != confirm:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = register_user(name, email, password)
                    if ok:
                        st.success(msg)
                        st.balloons()
                    else:
                        st.error(msg)

        st.markdown("Already have an account?")
        st.page_link("pages/3_🔐_Login.py", label="Log in here →", icon="🔐")
        panel_end()

divider()
footer()

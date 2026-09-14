import streamlit as st

from utils.style import inject_global_css, hero, divider, panel_start, panel_end, footer

st.set_page_config(page_title="Contact | AI Offensive Security", page_icon="📧", layout="wide")
inject_global_css()

hero("GET IN TOUCH", "Questions, collaborations, or responsible disclosure")
divider()

CONTACT_EMAIL = "daniyalriazcute@gmail.com"

left, right = st.columns([1, 1.2])

with left:
    panel_start()
    st.markdown("#### 📮 Contact Details")
    st.markdown(
        f"""
        **Email:** [{CONTACT_EMAIL}](mailto:{CONTACT_EMAIL})

        Whether you want to talk research collaboration, report a
        responsible-disclosure finding, or just say hi — this inbox is
        monitored regularly.
        """
    )
    st.markdown('<span class="tag">Research</span> <span class="tag">Collaboration</span> '
                '<span class="tag">Disclosure</span>', unsafe_allow_html=True)
    panel_end()

    panel_start()
    st.markdown("#### 🔒 Responsible Disclosure")
    st.write(
        "If you've found a genuine safety or security issue in an AI system, "
        "please report it through the vendor's official disclosure program "
        "first. Feel free to loop us in for research-sharing purposes once "
        "it's been responsibly reported."
    )
    panel_end()

with right:
    panel_start()
    st.markdown("#### ✉️ Send a Message")
    st.caption("This form composes an email locally — no data is stored server-side.")

    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Your name")
        email = st.text_input("Your email")
        subject = st.text_input("Subject")
        message = st.text_area("Message", height=160)
        submitted = st.form_submit_button("Send Message")

        if submitted:
            if not name or not email or not message:
                st.error("Please fill in your name, email, and a message.")
            else:
                st.success("Thanks! Please use the button below to open your email client and send this along.")
                import urllib.parse
                body = urllib.parse.quote(f"From: {name} ({email})\n\n{message}")
                subj = urllib.parse.quote(subject or "Message from AI Offensive Security site")
                mailto = f"mailto:{CONTACT_EMAIL}?subject={subj}&body={body}"
                st.markdown(f"[📤 Open in email client]({mailto})")
    panel_end()

divider()
footer()

import streamlit as st

from utils.style import inject_global_css, hero, divider, panel_start, panel_end, footer
from utils.content import get_all_posts, get_post, get_all_tags

st.set_page_config(page_title="Blog | AI Offensive Security", page_icon="📝", layout="wide")
inject_global_css()

hero("RESEARCH & BLOG", "Prompt Injection • Jailbreaking • Indirect Injection • Evasion")
divider()

query_slug = st.query_params.get("post")

# ---------------------------------------------------------------------------
# Single article view
# ---------------------------------------------------------------------------
if query_slug:
    post = get_post(query_slug)
    if post is None:
        st.error("That article couldn't be found.")
        if st.button("← Back to all posts"):
            st.query_params.clear()
            st.rerun()
    else:
        if st.button("← Back to all posts"):
            st.query_params.clear()
            st.rerun()

        panel_start()
        sev_class = f"severity-{post['severity']}"
        st.markdown(
            f'<span class="tag {sev_class}">{post["severity"].upper()} SEVERITY</span> '
            + " ".join(f'<span class="tag">{t}</span>' for t in post["tags"]),
            unsafe_allow_html=True,
        )
        st.markdown(f"## {post['title']}")
        st.caption(f"⏱️ {post['read_time']} read")
        st.markdown(post["content"])
        panel_end()

        st.info(
            "🛡️ **Educational purpose only.** This article explains concepts and "
            "defenses for security research and awareness. It does not provide "
            "step-by-step exploit instructions."
        )

# ---------------------------------------------------------------------------
# Listing view
# ---------------------------------------------------------------------------
else:
    posts = get_all_posts()
    tags = ["All"] + get_all_tags()

    filter_col, search_col = st.columns([1, 2])
    with filter_col:
        selected_tag = st.selectbox("Filter by topic", tags)
    with search_col:
        search_term = st.text_input("Search articles", placeholder="e.g. jailbreak, RAG, evasion...")

    filtered = posts
    if selected_tag != "All":
        filtered = [p for p in filtered if selected_tag in p["tags"]]
    if search_term:
        s = search_term.lower()
        filtered = [
            p for p in filtered
            if s in p["title"].lower() or s in p["summary"].lower() or any(s in t.lower() for t in p["tags"])
        ]

    st.markdown(f"**{len(filtered)}** article(s) found")
    st.markdown("")

    if not filtered:
        st.warning("No articles match your filters yet.")

    cols = st.columns(2)
    for i, post in enumerate(filtered):
        with cols[i % 2]:
            panel_start()
            sev_class = f"severity-{post['severity']}"
            st.markdown(
                f'<span class="tag {sev_class}">{post["severity"].upper()}</span> '
                + " ".join(f'<span class="tag">{t}</span>' for t in post["tags"]),
                unsafe_allow_html=True,
            )
            st.markdown(f"### {post['title']}")
            st.caption(f"⏱️ {post['read_time']} read")
            st.write(post["summary"])
            if st.button("Read article →", key=f"read_{post['slug']}"):
                st.query_params["post"] = post["slug"]
                st.rerun()
            panel_end()

divider()
footer()

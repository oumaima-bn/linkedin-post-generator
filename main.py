import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded",
)

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Français"]

# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .main .block-container { padding-top: 2.5rem; max-width: 760px; }
        h1, h2, h3 { letter-spacing: -0.02em; }
        .subtitle { color: #6b7280; font-size: 1.02rem; margin-top: -0.6rem; margin-bottom: 1.6rem; }
        .post-card {
            background: #f8f9fb;
            color: #1f2937;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            margin-top: 0.6rem;
            white-space: pre-wrap;
            line-height: 1.55;
            font-size: 1rem;
        }
        .post-card * { color: #1f2937 !important; }
        div.stButton > button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.55rem 1.4rem;
        }
        .stCaption, .st-emotion-cache-1629p8f { color: #9ca3af; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def load_few_shot_posts():
    return FewShotPosts()


# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.title("📝 LinkedIn Post Generator")
st.markdown(
    '<div class="subtitle">Generate on-brand LinkedIn posts, styled after your own past writing.</div>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.header("ℹ️ About")
    st.write(
        "This tool learns the topics, tone and format of past LinkedIn posts, "
        "then uses that as few-shot examples to generate new posts that match "
        "the same writing style."
    )
    st.divider()
 
    st.caption("Powered by Groq & LangChain")

# ----------------------------------------------------------------------------
# Load data (with a friendly error if the file is missing)
# ----------------------------------------------------------------------------
try:
    fs = load_few_shot_posts()
    tags = fs.get_tags()
except FileNotFoundError:
    st.error(
        "Couldn't find `data/processed_posts.json`. Run `preprocess.py` first, "
        "or make sure the `data/` folder is next to `main.py`."
    )
    st.stop()

if not tags:
    st.warning("No tags found in your processed posts yet.")
    st.stop()

# ----------------------------------------------------------------------------
# Controls
# ----------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    selected_tag = st.selectbox("Topic", options=tags)

with col2:
    selected_length = st.selectbox("Length", options=length_options, index=1)

with col3:
    selected_language = st.selectbox("Language", options=language_options)

generate_clicked = st.button("✨ Generate", type="primary", use_container_width=True)

# ----------------------------------------------------------------------------
# Generation
# ----------------------------------------------------------------------------
if generate_clicked:
    with st.spinner("Writing your post..."):
        try:
            st.session_state["generated_post"] = generate_post(
                selected_length, selected_language, selected_tag
            )
            st.session_state["generated_meta"] = (selected_tag, selected_length, selected_language)
        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Something went wrong while generating the post: {e}")

# ----------------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------------
if st.session_state.get("generated_post"):
    tag, length, language = st.session_state["generated_meta"]
    st.markdown(f"**Topic:** {tag} &nbsp;·&nbsp; **Length:** {length} &nbsp;·&nbsp; **Language:** {language}")
    st.markdown(f'<div class="post-card">{st.session_state["generated_post"]}</div>', unsafe_allow_html=True)

    dl_col, _ = st.columns([1, 3])
    with dl_col:
        st.download_button(
            "⬇️ Download as .txt",
            data=st.session_state["generated_post"],
            file_name="linkedin_post.txt",
            mime="text/plain",
            use_container_width=True,
        )

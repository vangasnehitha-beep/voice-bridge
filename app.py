import io
import html
import streamlit as st
from gtts import gTTS

st.set_page_config(
    page_title="Voice Bridge",
    page_icon="🤝",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
}

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    margin-top: 10px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #64748b;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    background: rgba(255,255,255,0.95);
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #e2e8f0;
    box-shadow: 0 5px 20px rgba(0,0,0,0.06);
    margin-bottom: 18px;
}

.card-icon {
    font-size: 32px;
    margin-bottom: 8px;
}

.card-title {
    font-size: 19px;
    font-weight: 700;
}

.card-text {
    color: #64748b;
    font-size: 14px;
}

.section-title {
    font-size: 24px;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 12px;
}

.sentence-box {
    background: white;
    border-radius: 18px;
    padding: 25px;
    min-height: 80px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    text-align: center;
}

.sentence-text {
    font-size: 27px;
    font-weight: 700;
    color: #1e293b;
}

.footer {
    text-align: center;
    color: #64748b;
    margin-top: 30px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🤝 Voice Bridge</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Sign → AI Recognition → Sentence → 🔊 Automatic Voice</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🖐️</div>
        <div class="card-title">Sign Recognition</div>
        <div class="card-text">Capture sign gestures</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📝</div>
        <div class="card-title">Sentence</div>
        <div class="card-text">Build communication</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🔊</div>
        <div class="card-title">Voice Output</div>
        <div class="card-text">Speak the sentence</div>
    </div>
    """, unsafe_allow_html=True)

if "sentence" not in st.session_state:
    st.session_state.sentence = ""

if "audio" not in st.session_state:
    st.session_state.audio = None

st.markdown(
    '<div class="section-title">📷 Sign Input</div>',
    unsafe_allow_html=True
)

camera = st.camera_input("Show your sign and capture an image")

if camera is not None:
    st.image(
        camera,
        caption="Captured Sign",
        use_container_width=True
    )

    st.success("Sign image captured successfully.")

st.markdown(
    '<div class="section-title">📝 Sentence Builder</div>',
    unsafe_allow_html=True
)

word = st.text_input(
    "Recognized word",
    placeholder="Example: Hello"
)

col1, col2 = st.columns(2)

with col1:
    add_word = st.button(
        "➕ Add Word",
        use_container_width=True
    )

with col2:
    clear_sentence = st.button(
        "🗑️ Clear",
        use_container_width=True
    )

if add_word:
    if word.strip():
        new_word = word.strip()

        if st.session_state.sentence:
            st.session_state.sentence += " " + new_word
        else:
            st.session_state.sentence = new_word

        st.session_state.audio = None
        st.rerun()
    else:
        st.warning("Please enter a word.")

if clear_sentence:
    st.session_state.sentence = ""
    st.session_state.audio = None
    st.rerun()

st.markdown(
    '<div class="section-title">💬 Generated Sentence</div>',
    unsafe_allow_html=True
)

if st.session_state.sentence:
    safe_sentence = html.escape(st.session_state.sentence)

    st.markdown(
        f'<div class="sentence-box"><div class="sentence-text">{safe_sentence}</div></div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="sentence-box"><div class="card-text">Your sentence will appear here</div></div>',
        unsafe_allow_html=True
    )

st.markdown(
    '<div class="section-title">🔊 Automatic Voice</div>',
    unsafe_allow_html=True
)

language = st.selectbox(
    "Select voice language",
    ["English", "Hindi", "Telugu"]
)

language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te"
}

if st.button(
    "🔊 Generate Voice",
    use_container_width=True
):
    if st.session_state.sentence.strip():
        try:
            audio = io.BytesIO()

            speech = gTTS(
                text=st.session_state.sentence,
                lang=language_codes[language],
                slow=False
            )

            speech.write_to_fp(audio)
            audio.seek(0)

            st.session_state.audio = audio.getvalue()

            st.success("Voice generated successfully.")

        except Exception as error:
            st.error(f"Voice generation failed: {error}")
    else:
        st.warning("Please create a sentence first.")

if st.session_state.audio:
    st.audio(
        st.session_state.audio,
        format="audio/mp3"
    )

st.markdown(
    '<div class="footer">Voice Bridge | AI Accessibility Communication Project</div>',
    unsafe_allow_html=True
)
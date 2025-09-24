import uuid
import shutil
import streamlit as st
from pathlib import Path
from text_speech import TextSpeech

st.set_page_config(page_title="TTS Studio", page_icon="🔊", layout="centered")

# Custom CSS for dark theme with gradients
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Dark theme base */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main title gradient */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #fda085 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        padding: 1rem 0;
        animation: gradient-shift 8s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #a0a0b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background: rgba(20, 20, 40, 0.8) !important;
        border: 2px solid rgba(102, 126, 234, 0.5) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #764ba2 !important;
        box-shadow: 0 0 20px rgba(118, 75, 162, 0.3) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Download button special styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 20px rgba(245, 87, 108, 0.5);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(20, 20, 40, 0.8) !important;
        border: 2px solid rgba(102, 126, 234, 0.5) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f23 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Sidebar headers */
    .sidebar-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* History container styling */
    div[data-testid="stVerticalBlock"] > div:has(> div > div > button) {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }
    
    /* Audio player styling */
    audio {
        border-radius: 10px;
        background: rgba(30, 30, 50, 0.5);
    }
    
    /* Success/Warning/Error messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
        border: 1px solid #10b981;
        border-radius: 10px;
        color: #10b981;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.2) 0%, rgba(251, 191, 36, 0.1) 100%);
        border: 1px solid #fbbf24;
        border-radius: 10px;
        color: #fbbf24;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
        border: 1px solid #ef4444;
        border-radius: 10px;
        color: #ef4444;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1) !important;
        border-radius: 8px !important;
        color: #a0a0b8 !important;
    }
    
    /* Divider styling */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
        margin: 2rem 0;
    }
    
    /* Info box styling */
    .stInfo {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        color: #a0a0b8;
    }
    
    /* Latest output section */
    .output-section {
        background: rgba(118, 75, 162, 0.1);
        border: 2px solid rgba(118, 75, 162, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ---- Load user's module safely ----
tts = TextSpeech()

# Create cache directory if it doesn't exist
Path("cache_audio").mkdir(exist_ok=True)

# ---- Sidebar controls ----
st.sidebar.title("⚙️ Settings")

SPEAKER = {
    "🎭 Man": "twi_speaker_5",
    "👩 Woman": "twi_speaker_9"
}

LANGUAGE = {
    "🇬🇧 English": "en",
    "🇬🇭 Twi": "tw"
}

# Speaker select (optional; passed only if supported by your method)
speaker = st.sidebar.selectbox("Speaker", SPEAKER.keys())
spk_code = SPEAKER[speaker]

# Language select
lang = st.sidebar.selectbox("Language", LANGUAGE.keys())
lang_code = LANGUAGE[lang]

# Main title with gradient
st.markdown('<h1 class="main-title">🔊 TTS Studio</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Type text, pick language & speaker, then synthesize. Outputs appear below with history.</p>', unsafe_allow_html=True)

# ---- Main input ----
text = st.text_area("✨ Text to synthesize", height=120, 
            placeholder="Type or paste your text here...", max_chars=1000)

synth_btn = st.button("🎵 Synthesize", type="primary")

# session history
if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.divider()
    st.subheader("📜 History")
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history):
            with st.container(border=True):
                st.markdown(f"**#{len(st.session_state.history)-i}** — {item['lang']} · {item['speaker']}")
                st.audio(item["path"])
                st.download_button("💾 Download", data=Path(item["path"]).read_bytes(), file_name=Path(item["path"]).name, key=f"dl_{i}")
                with st.expander("Text"):
                    st.write(item["text"])
    else:
        st.caption("Your past syntheses will appear here.")


def call_tts(text_val: str):
    
    tts.text = text_val.strip()

    if lang_code not in ["en", "tw"]:
        st.info(f"Language '{lang_code}' not supported yet.")
        raise ValueError("Unsupported language code.")
    
    tts.text_to_speech(code=lang_code, speaker_code=spk_code)
    
    # get the temp file path
    path = tts.filename

    # Copy to a unique file in the Streamlit working dir to preserve history
    unique_name = f"tts_{uuid.uuid4().hex}.wav"
    dest = f"cache_audio/{unique_name}"
    shutil.copyfile(path, dest)
    return dest

# ---- Action ----
if synth_btn:
    if not text.strip():
        st.warning("⚠️ Please enter some text first.")
    else:
        with st.spinner("🎨 Synthesizing..."):
            try:
                audio_file = call_tts(text)
                st.session_state.history.insert(0, {
                    "text": text.strip(),
                    "lang": lang,
                    "speaker": speaker,
                    "path": str(audio_file),
                })
                st.success("✅ Done! See the newest item below.")
            except Exception as e:
                st.error(str(e))

# ---- Output & History ----
st.subheader("🎧 Latest Output")
if st.session_state.history:
    latest = st.session_state.history[0]
    st.audio(latest["path"])
    st.download_button("📥 Download audio", data=Path(latest["path"]).read_bytes(), file_name=Path(latest["path"]).name)
    with st.expander("Details"):
        st.json({"language": latest["lang"], "speaker": latest["speaker"], "text": latest["text"]})
else:
    st.info("🎤 No audio yet. Enter text and click **Synthesize**.")
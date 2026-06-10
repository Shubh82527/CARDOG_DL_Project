import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pawprint · Image Classifier",
    page_icon="🐾",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap');

/* ──────────────────────────────────────────────────────────────
   ANIMATED BACKGROUND
   A soft pearl-white base with a slow-drifting radial mesh of
   navy → teal orbs. Feels alive without being distracting.
────────────────────────────────────────────────────────────── */
@keyframes drift1 {
  0%   { transform: translate(0px,   0px)   scale(1);   }
  50%  { transform: translate(40px, -30px)  scale(1.08);}
  100% { transform: translate(0px,   0px)   scale(1);   }
}
@keyframes drift2 {
  0%   { transform: translate(0px,  0px)  scale(1);   }
  50%  { transform: translate(-50px, 25px) scale(0.94);}
  100% { transform: translate(0px,  0px)  scale(1);   }
}
@keyframes drift3 {
  0%   { transform: translate(0px, 0px) scale(1);    }
  50%  { transform: translate(30px, 40px) scale(1.05);}
  100% { transform: translate(0px, 0px) scale(1);    }
}
@keyframes subtlePulse {
  0%, 100% { opacity: 0.55; }
  50%       { opacity: 0.80; }
}

/* Fixed full-screen canvas behind everything */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  z-index: -2;
  background-color: #EEF2F7;
  /* Fine diagonal linen texture */
  background-image:
    repeating-linear-gradient(
      135deg,
      rgba(15,45,74,0.028) 0px,
      rgba(15,45,74,0.028) 1px,
      transparent 1px,
      transparent 18px
    ),
    repeating-linear-gradient(
      45deg,
      rgba(42,125,107,0.022) 0px,
      rgba(42,125,107,0.022) 1px,
      transparent 1px,
      transparent 18px
    );
}

/* Orb 1 — large navy, top-left */
body::after {
  content: '';
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background:
    radial-gradient(ellipse 640px 520px at 8% 12%,
      rgba(15,45,74,0.13) 0%, transparent 70%),
    radial-gradient(ellipse 500px 400px at 92% 80%,
      rgba(42,125,107,0.12) 0%, transparent 70%),
    radial-gradient(ellipse 380px 340px at 55% 50%,
      rgba(100,160,210,0.07) 0%, transparent 60%),
    radial-gradient(ellipse 280px 260px at 78% 18%,
      rgba(42,125,107,0.09) 0%, transparent 65%),
    radial-gradient(ellipse 320px 280px at 22% 85%,
      rgba(15,45,74,0.07) 0%, transparent 65%);
  animation: drift1 18s ease-in-out infinite;
}

/* Floating geometric accent shapes */
.bg-shape {
  position: fixed;
  pointer-events: none;
  z-index: -1;
  border-radius: 50%;
  filter: blur(0px);
}
.bg-shape-1 {
  width: 220px; height: 220px;
  top: 6%; right: 8%;
  border: 1.5px solid rgba(42,125,107,0.18);
  animation: drift2 22s ease-in-out infinite;
}
.bg-shape-2 {
  width: 120px; height: 120px;
  top: 6%; right: 12.5%;
  border: 1px solid rgba(42,125,107,0.12);
  animation: drift2 22s ease-in-out infinite 1s;
}
.bg-shape-3 {
  width: 340px; height: 340px;
  bottom: 8%; left: 4%;
  border: 1.5px solid rgba(15,45,74,0.10);
  animation: drift3 26s ease-in-out infinite;
}
.bg-shape-4 {
  width: 180px; height: 180px;
  bottom: 14%; left: 8%;
  border: 1px solid rgba(15,45,74,0.08);
  animation: drift3 26s ease-in-out infinite 2s;
}
/* Corner accent — top-left dot grid */
.bg-dots {
  position: fixed;
  top: 18px; left: 20px;
  width: 160px; height: 140px;
  background-image: radial-gradient(circle, rgba(15,45,74,0.18) 1.4px, transparent 1.4px);
  background-size: 16px 16px;
  z-index: -1;
  animation: subtlePulse 8s ease-in-out infinite;
}
.bg-dots-br {
  position: fixed;
  bottom: 20px; right: 18px;
  width: 130px; height: 110px;
  background-image: radial-gradient(circle, rgba(42,125,107,0.20) 1.4px, transparent 1.4px);
  background-size: 16px 16px;
  z-index: -1;
  animation: subtlePulse 10s ease-in-out infinite 3s;
}

/* ── Override Streamlit backgrounds to transparent ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
[data-testid="stMain"],
.main,
section.main > div {
    background: transparent !important;
    color: #1C2333 !important;
}
[data-testid="stSidebar"] { display: none !important; }

/* ── Typography ── */
html { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'DM Serif Display', serif !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Content card — frosted glass ── */
.block-container {
    max-width: 800px !important;
    padding: 0 1.4rem 3rem !important;
    margin-top: 0 !important;
}

/* Hero banner at top — full-width tinted strip */
.hero-banner {
    background: linear-gradient(100deg, #0F2D4A 0%, #174060 55%, #1a5247 100%);
    border-radius: 0 0 24px 24px;
    padding: 2.6rem 2.6rem 2.2rem;
    margin: 0 -1.4rem 2.2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(15,45,74,0.22);
}
.hero-banner::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 300px 200px at 90% 50%, rgba(42,125,107,0.25) 0%, transparent 70%),
        radial-gradient(ellipse 200px 180px at 10% 80%, rgba(100,160,210,0.15) 0%, transparent 60%);
    pointer-events: none;
}
/* Subtle grid lines inside banner */
.hero-banner::after {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
}

.wordmark {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 6px;
    position: relative;
    z-index: 1;
}
.wordmark-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.9rem;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    line-height: 1;
    text-shadow: 0 2px 12px rgba(0,0,0,0.18);
}
.wordmark-badge {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #7FDFC8;
    border: 1.5px solid rgba(127,223,200,0.55);
    border-radius: 4px;
    padding: 2px 8px;
    position: relative;
    top: -3px;
    background: rgba(42,125,107,0.20);
}
.hero-sub {
    font-size: 0.96rem;
    color: rgba(220,232,245,0.85);
    margin-bottom: 0;
    font-weight: 400;
    position: relative;
    z-index: 1;
    max-width: 480px;
}
.hero-sub strong { color: #7FDFC8; font-weight: 600; }

/* Paw print decoration in banner */
.hero-paw {
    position: absolute;
    right: 2.4rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5.5rem;
    opacity: 0.10;
    z-index: 0;
    line-height: 1;
    user-select: none;
}

/* ── Main content area ── */
.content-card {
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 18px;
    padding: 2rem 2.2rem 2rem;
    box-shadow:
        0 2px 0px rgba(255,255,255,0.9) inset,
        0 8px 32px rgba(15,45,74,0.09),
        0 1px 0 rgba(255,255,255,0.6);
    border: 1px solid rgba(255,255,255,0.72);
    margin-bottom: 1.4rem;
}

/* Section label inside card */
.section-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #2A7D6B;
    margin-bottom: 0.7rem;
}

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    border: 1.5px dashed #AABCD4 !important;
    border-radius: 12px !important;
    background: rgba(255,255,255,0.6) !important;
    padding: 1rem !important;
    transition: border-color 0.2s, background 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #2A7D6B !important;
    background: rgba(42,125,107,0.04) !important;
}
[data-testid="stFileUploadDropzone"] p {
    color: #5A6479 !important;
    font-size: 0.9rem !important;
}

/* ── Predict button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #0F2D4A 0%, #174F72 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    padding: 0.7rem 2.4rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 3px 12px rgba(15,45,74,0.28), 0 1px 0 rgba(255,255,255,0.1) inset !important;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #2A7D6B 0%, #1f9e87 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(42,125,107,0.35) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── Result card ── */
.result-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #F0F6FF 100%);
    border-radius: 16px;
    padding: 1.8rem 2rem 1.6rem;
    margin-top: 1.6rem;
    box-shadow:
        0 4px 28px rgba(15,45,74,0.10),
        0 1px 0 rgba(255,255,255,0.9) inset;
    border: 1px solid #D8E4F0;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 5px; height: 100%;
    border-radius: 16px 0 0 16px;
}
.result-card.cat::before { background: linear-gradient(180deg, #2A7D6B, #1f9e87); }
.result-card.dog::before { background: linear-gradient(180deg, #0F2D4A, #174F72); }

.result-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    color: #8E99AD;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    margin-bottom: 4px;
}
.result-value {
    font-family: 'DM Serif Display', serif;
    font-size: 3.2rem;
    line-height: 1.1;
    margin-bottom: 0.1rem;
}
.result-value.dog { color: #0F2D4A; }
.result-value.cat { color: #2A7D6B; }

/* Confidence meter */
.confidence-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 1.2rem;
}
.conf-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #6B7A94;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    white-space: nowrap;
    min-width: 86px;
}
.conf-bar-bg {
    flex: 1;
    height: 8px;
    background: #E0E8F4;
    border-radius: 99px;
    overflow: hidden;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.7s cubic-bezier(0.4,0,0.2,1);
}
.conf-pct {
    font-size: 0.9rem;
    font-weight: 700;
    color: #1C2333;
    min-width: 44px;
    text-align: right;
}

/* ── Image display ── */
[data-testid="stImage"] img {
    border-radius: 12px !important;
    box-shadow: 0 4px 20px rgba(15,45,74,0.13) !important;
    border: 1px solid rgba(255,255,255,0.8) !important;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 2.2rem 0 1rem;
    color: #9AA3B2;
    font-size: 0.9rem;
}
.empty-state .empty-icon {
    font-size: 2.6rem;
    display: block;
    margin-bottom: 0.6rem;
    opacity: 0.45;
}

/* ── Footer ── */
.info-note {
    font-size: 0.78rem;
    color: #8E99AD;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(200,215,230,0.6);
    text-align: center;
}

/* ── Spinner override ── */
[data-testid="stSpinner"] { color: #2A7D6B !important; }

</style>

<!-- Fixed background decorations injected into DOM -->
<div class="bg-shape bg-shape-1"></div>
<div class="bg-shape bg-shape-2"></div>
<div class="bg-shape bg-shape-3"></div>
<div class="bg-shape bg-shape-4"></div>
<div class="bg-dots"></div>
<div class="bg-dots-br"></div>
""", unsafe_allow_html=True)


# ── Model loader (cached) ──────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    return tf.keras.models.load_model("cat_dog_model.keras")


def predict_image(image: Image.Image):
    img = image.resize((256, 256))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array, verbose=0)
    label = "Dog" if prediction[0][0] > 0.5 else "Cat"
    raw_score = float(prediction[0][0])
    confidence = raw_score if label == "Dog" else 1 - raw_score
    return label, confidence


# ── Load model ────────────────────────────────────────────────────────────────
with st.spinner("Loading model…"):
    model = load_model()


# ── Hero banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-paw">🐾</div>
    <div class="wordmark">
        <span class="wordmark-title">Pawprint</span>
        <span class="wordmark-badge">Cat · Dog</span>
    </div>
    <p class="hero-sub">
        Upload any photo — the model will tell you whether it shows
        a <strong>cat</strong> or a <strong>dog</strong>, with a confidence score.
    </p>
</div>
""", unsafe_allow_html=True)


# ── Upload card ───────────────────────────────────────────────────────────────
st.markdown('<div class="content-card"><div class="section-eyebrow">Step 1 — Select image</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drop an image here, or click to browse",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="visible",
)

st.markdown('</div>', unsafe_allow_html=True)


# ── Preview + predict ─────────────────────────────────────────────────────────
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    st.markdown('<div class="content-card"><div class="section-eyebrow">Step 2 — Preview &amp; classify</div>', unsafe_allow_html=True)

    col_img, col_btn = st.columns([1.2, 0.8])
    with col_img:
        st.image(image, caption=uploaded_file.name, use_container_width=True)
    with col_btn:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:0.82rem;color:#6B7A94;margin-bottom:0.3rem;'><strong style='color:#1C2333;'>{uploaded_file.name}</strong></p>", unsafe_allow_html=True)
        w, h = image.size
        st.markdown(f"<p style='font-size:0.78rem;color:#9AA3B2;margin-bottom:1.2rem;'>{w} × {h} px</p>", unsafe_allow_html=True)
        predict_clicked = st.button("🔍 &nbsp;Classify Image", use_container_width=True)

    if predict_clicked:
        with st.spinner("Analysing image…"):
            label, confidence = predict_image(image)

        conf_pct = round(confidence * 100, 1)
        bar_color = "linear-gradient(90deg,#2A7D6B,#1f9e87)" if label == "Cat" else "linear-gradient(90deg,#0F2D4A,#174F72)"
        label_class = label.lower()
        emoji = "🐱" if label == "Cat" else "🐶"

        st.markdown(f"""
        <div class="result-card {label_class}">
            <div class="result-label">Classification Result</div>
            <div class="result-value {label_class}">{emoji}&nbsp;{label}</div>
            <div class="confidence-row">
                <span class="conf-label">Confidence</span>
                <div class="conf-bar-bg">
                    <div class="conf-bar-fill"
                         style="width:{conf_pct}%; background:{bar_color};">
                    </div>
                </div>
                <span class="conf-pct">{conf_pct}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="content-card">
        <div class="empty-state">
            <span class="empty-icon">🐾</span>
            No image selected yet — upload one above to get started.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<p class="info-note">
    Model input: 256 × 256 · Normalised [0, 1] · Binary cross-entropy classifier
</p>
""", unsafe_allow_html=True)
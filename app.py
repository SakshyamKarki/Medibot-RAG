import streamlit as st
from datetime import datetime
from agent import run_agent

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediBot — AI Medical Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS injection ─────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 2rem 2.5rem 5rem 2.5rem;
    max-width: 860px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d1117;
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
[data-testid="stSidebar"] h1 { color: #58a6ff !important; }
[data-testid="stSidebar"] .sidebar-section {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
}
[data-testid="stSidebar"] .sidebar-tag {
    display: inline-block;
    background: #1f3a5f;
    color: #79c0ff !important;
    font-size: 0.72rem;
    font-weight: 500;
    padding: 2px 10px;
    border-radius: 20px;
    margin: 3px 3px 3px 0;
    cursor: pointer;
    border: 1px solid #388bfd44;
}
[data-testid="stSidebar"] .stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0;
    border-bottom: 1px solid #21262d;
    font-size: 0.82rem;
}
[data-testid="stSidebar"] .stat-row:last-child { border-bottom: none; }
[data-testid="stSidebar"] .stat-val {
    color: #58a6ff !important;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
}

/* ── Header ── */
.app-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 0.5rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid #21262d;
}
.app-header .icon-wrap {
    width: 46px; height: 46px;
    background: linear-gradient(135deg, #1a5e4a, #0d9370);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    flex-shrink: 0;
}
.app-header h1 {
    font-size: 1.45rem;
    font-weight: 600;
    color: #e6edf3;
    margin: 0;
    line-height: 1.2;
}
.app-header p {
    font-size: 0.78rem;
    color: #8b949e;
    margin: 2px 0 0;
}
.status-dot {
    width: 8px; height: 8px;
    background: #3fb950;
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
    box-shadow: 0 0 6px #3fb950aa;
}

/* ── Chat messages ── */
.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 14px;
    margin: 1.2rem 0;
}
.msg-row {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    animation: fadeUp 0.25s ease;
}
.msg-row.user { flex-direction: row-reverse; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

.avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
    margin-top: 2px;
}
.avatar.bot  { background: #1a5e4a; border: 1.5px solid #0d9370; }
.avatar.user { background: #1f3a5f; border: 1.5px solid #388bfd; }

.bubble {
    max-width: 78%;
    padding: 11px 16px;
    border-radius: 14px;
    font-size: 0.9rem;
    line-height: 1.65;
    position: relative;
}
.bubble.bot {
    background: #161b22;
    border: 1px solid #21262d;
    color: #c9d1d9;
    border-top-left-radius: 4px;
}
.bubble.user {
    background: #1f3a5f;
    border: 1px solid #388bfd44;
    color: #cae8ff;
    border-top-right-radius: 4px;
    text-align: right;
}
.bubble .ts {
    font-size: 0.68rem;
    color: #484f58;
    margin-top: 6px;
    font-family: 'DM Mono', monospace;
}
.bubble.user .ts { color: #4a82b8; }

.bubble .tool-badge {
    display: inline-block;
    background: #1a3a2a;
    color: #3fb950;
    font-size: 0.68rem;
    font-family: 'DM Mono', monospace;
    padding: 1px 8px;
    border-radius: 20px;
    border: 1px solid #2ea04344;
    margin-bottom: 7px;
}

/* ── Disclaimer banner ── */
.disclaimer {
    background: #1c1a12;
    border: 1px solid #d29922aa;
    border-left: 3px solid #d29922;
    border-radius: 8px;
    padding: 9px 14px;
    font-size: 0.78rem;
    color: #b3831e;
    margin-bottom: 1.2rem;
}

/* ── Input row ── */
.stTextInput > div > div > input {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
    color: #e6edf3 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 0.65rem 1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #388bfd !important;
    box-shadow: 0 0 0 3px #388bfd22 !important;
}
.stTextInput > div > div > input::placeholder { color: #484f58 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0d9370, #1a5e4a) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px #0d937055 !important;
}

.stButton[data-testid="clear-btn"] > button {
    background: transparent !important;
    border: 1px solid #30363d !important;
    color: #8b949e !important;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #484f58;
}
.empty-state .big-icon { font-size: 2.8rem; margin-bottom: 0.7rem; }
.empty-state h3 { color: #8b949e; font-weight: 400; font-size: 1rem; }

/* ── Spinner override ── */
[data-testid="stSpinner"] { color: #0d9370 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #21262d; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "chat" not in st.session_state:
    st.session_state.chat = []
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🩺 MediBot")
    st.markdown("---")

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**⚡ System Status**")
    st.markdown(f"""
    <div class="stat-row"><span>Model</span><span class="stat-val">llama-3.3-70b</span></div>
    <div class="stat-row"><span>RAG Index</span><span class="stat-val">FAISS</span></div>
    <div class="stat-row"><span>Embeddings</span><span class="stat-val">all-mpnet-base-v2</span></div>
    <div class="stat-row"><span>Messages</span><span class="stat-val">{st.session_state.msg_count}</span></div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**💡 Try asking**")
    example_questions = [
        "What is diabetes?",
        "Symptoms of hypertension?",
        "I have a fever and cough",
        "How is pneumonia treated?",
        "What causes anaemia?",
        "Signs of a heart attack",
    ]
    cols = st.columns(2)
    for i, q in enumerate(example_questions):
        st.markdown(f'<span class="sidebar-tag">{q}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**🛠 Tools**")
    st.markdown("""
    <div class="stat-row"><span>📚 Medical Knowledge Base</span><span class="stat-val">RAG</span></div>
    <div class="stat-row"><span>🔍 Symptom Checker</span><span class="stat-val">Rule</span></div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.72rem; color:#484f58; margin-top:1rem; line-height:1.6;">
    ⚠️ For educational purposes only.<br>
    Always consult a qualified doctor.
    </div>
    """, unsafe_allow_html=True)

# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div class="icon-wrap">🩺</div>
  <div>
    <h1>Medical AI Assistant</h1>
    <p><span class="status-dot"></span>RAG · Memory · Llama 3.3 70B via Groq</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
  ⚠️ &nbsp;This assistant provides general medical information only — not diagnosis or treatment advice. Always consult a qualified healthcare professional.
</div>
""", unsafe_allow_html=True)

# ── Chat display ──────────────────────────────────────────────────────────────
chat_container = st.container()

with chat_container:
    if not st.session_state.chat:
        st.markdown("""
        <div class="empty-state">
          <div class="big-icon">💬</div>
          <h3>Ask a medical question to get started</h3>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
        for role, msg, ts in st.session_state.chat:
            if role == "User":
                st.markdown(f"""
                <div class="msg-row user">
                  <div class="avatar user">👤</div>
                  <div class="bubble user">
                    {msg}
                    <div class="ts">{ts}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # detect if symptom tool was used
                badge = '<span class="tool-badge">🔍 symptom checker</span><br>' if "Symptom check:" in msg else '<span class="tool-badge">📚 knowledge base</span><br>'
                st.markdown(f"""
                <div class="msg-row bot">
                  <div class="avatar bot">🩺</div>
                  <div class="bubble bot">
                    {badge}
                    {msg}
                    <div class="ts">{ts}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── Input row ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([7, 1.3, 1.3])

with col1:
    query = st.text_input(
        label="query",
        placeholder="Ask a medical question…",
        label_visibility="collapsed",
        key="user_input",
    )
with col2:
    send = st.button("Send →", use_container_width=True)
with col3:
    clear = st.button("Clear", use_container_width=True)

# ── Logic ─────────────────────────────────────────────────────────────────────
if send and query.strip():
    ts = datetime.now().strftime("%H:%M")
    st.session_state.chat.append(("User", query.strip(), ts))
    st.session_state.msg_count += 1

    with st.spinner("Thinking…"):
        try:
            response = run_agent(query.strip())
        except Exception as e:
            response = f"⚠️ Error: {e}"

    st.session_state.chat.append(("Bot", response, datetime.now().strftime("%H:%M")))
    st.rerun()

if clear:
    st.session_state.chat = []
    st.session_state.msg_count = 0
    st.rerun()
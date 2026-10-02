import streamlit as st
import streamlit.components.v1 as components
from main import ask_gemini

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Welcome to AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# ============================================================
# CUSTOM CSS — Premium Dark Theme
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root Variables ───────────────────────────────────────── */
:root {
    --bg-dark:       #0a0a0f;
    --bg-card:       rgba(255,255,255,0.04);
    --bg-card-hover: rgba(255,255,255,0.07);
    --border:        rgba(255,255,255,0.08);
    --border-glow:   rgba(124,58,237,0.4);
    --accent-1:      #7c3aed;
    --accent-2:      #06b6d4;
    --accent-3:      #f59e0b;
    --text-primary:  #f1f5f9;
    --text-secondary:#94a3b8;
    --text-muted:    #475569;
    --user-bubble:   linear-gradient(135deg, #7c3aed, #4f46e5);
    --ai-bubble:     rgba(255,255,255,0.05);
    --shadow:        0 8px 32px rgba(0,0,0,0.4);
}

/* ── Global Reset ─────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-dark) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Animated gradient background */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 0%, rgba(124,58,237,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 100%, rgba(6,182,212,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 40% 40% at 50% 50%, rgba(245,158,11,0.03) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* ── Hide Streamlit chrome without hiding sidebar controls ── */
#MainMenu, footer { visibility: hidden !important; display: none !important; }
[data-testid="stDeployButton"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }

/* Keep header non-blocking and visible so toggle controls can be accessed */
header[data-testid="stHeader"] {
    background: transparent !important;
    visibility: visible !important;
    display: block !important;
    z-index: 1000 !important;
    pointer-events: none !important;
}

header[data-testid="stHeader"] button,
header[data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
header[data-testid="stHeader"] [data-testid="stSidebarCollapsedControl"] {
    pointer-events: auto !important;
    visibility: visible !important;
}

/* ── Sidebar ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: rgba(10,10,20,0.95) !important;
    border-right: 1px solid var(--border) !important;
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── Sidebar collapsed-state re-open button (>> Right Arrow) ── */
[data-testid="stExpandSidebarButton"],
button[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapsedControl"] button {
    display: inline-flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    z-index: 999999 !important;
    background: linear-gradient(135deg, rgba(124,58,237,0.4), rgba(6,182,212,0.3)) !important;
    border: 1px solid rgba(124,58,237,0.7) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    min-width: 44px !important;
    height: 44px !important;
    padding: 0 10px !important;
    cursor: pointer !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.45) !important;
    backdrop-filter: blur(12px) !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.25s ease !important;
    pointer-events: auto !important;
}

[data-testid="stExpandSidebarButton"]:hover,
button[data-testid="stExpandSidebarButton"]:hover,
[data-testid="stSidebarCollapsedControl"]:hover,
[data-testid="stSidebarCollapsedControl"] button:hover {
    background: linear-gradient(135deg, rgba(124,58,237,0.7), rgba(6,182,212,0.5)) !important;
    border-color: rgba(124,58,237,0.95) !important;
    transform: scale(1.08) translateX(2px) !important;
    box-shadow: 0 6px 26px rgba(124,58,237,0.6) !important;
    color: #ffffff !important;
}

[data-testid="stExpandSidebarButton"] svg,
button[data-testid="stExpandSidebarButton"] svg,
[data-testid="stSidebarCollapsedControl"] svg {
    fill: #f1f5f9 !important;
    color: #f1f5f9 !important;
    width: 24px !important;
    height: 24px !important;
}

[data-testid="stExpandSidebarButton"] span,
button[data-testid="stExpandSidebarButton"] span {
    color: #f1f5f9 !important;
    font-size: 1.4rem !important;
}

/* ── Custom Floating >> button ─────────────────────────────── */
#custom-sidebar-toggle-btn {
    position: fixed;
    top: 14px;
    left: 14px;
    z-index: 999999;
    display: none;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 10px;
    background: linear-gradient(135deg, rgba(124,58,237,0.4), rgba(6,182,212,0.3));
    border: 1px solid rgba(124,58,237,0.7);
    color: #f1f5f9;
    font-size: 20px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(124,58,237,0.45);
    backdrop-filter: blur(12px);
    transition: all 0.25s ease;
    user-select: none;
}
#custom-sidebar-toggle-btn:hover {
    background: linear-gradient(135deg, rgba(124,58,237,0.7), rgba(6,182,212,0.5));
    border-color: rgba(124,58,237,0.95);
    transform: scale(1.08) translateX(2px);
    box-shadow: 0 6px 26px rgba(124,58,237,0.6);
}

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0 20px;
}
.sidebar-logo-icon {
    font-size: 2rem;
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sidebar-logo-text {
    font-size: 1.1rem;
    font-weight: 700;
    background: linear-gradient(135deg, #e2d9f3, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.sidebar-section-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    margin: 20px 0 10px;
}

.tool-chip {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    margin-bottom: 6px;
    font-size: 0.85rem;
    color: var(--text-secondary) !important;
    transition: all 0.2s;
}
.tool-chip:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-glow);
}
.tool-chip-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    flex-shrink: 0;
}

.capability-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 0;
    font-size: 0.85rem;
    color: var(--text-secondary) !important;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

.sidebar-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 18px 0;
}

/* Sidebar clear button */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: rgba(239,68,68,0.12) !important;
    border: 1px solid rgba(239,68,68,0.25) !important;
    color: #fca5a5 !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 10px !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(239,68,68,0.22) !important;
    border-color: rgba(239,68,68,0.5) !important;
    transform: translateY(-1px);
}

/* ── Main Content Area ────────────────────────────────────── */
.main .block-container {
    padding: 2rem 3rem 2rem !important;
    max-width: 900px !important;
    margin: 0 auto !important;
}

/* Force Streamlit's inner layout columns to stay centered */
[data-testid="stAppViewContainer"] > .main {
    display: flex;
    justify-content: center;
}
[data-testid="column"] {
    margin: 0 auto !important;
}

/* ── Hero Header ──────────────────────────────────────────── */
.hero-container {
    text-align: center !important;
    padding: 48px 24px 36px;
    position: relative;
    margin: 0 auto !important;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #c4b5fd;
    letter-spacing: 0.05em;
    margin-bottom: 20px;
}
.hero-badge-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #7c3aed;
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(1.4); }
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #f1f5f9 0%, #c4b5fd 40%, #67e8f9 80%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 16px;
    text-align: center;
}
.hero-subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    max-width: 520px;
    margin: 0 auto 28px !important;
    line-height: 1.7;
    text-align: center !important;
}
.hero-pills {
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
}
.hero-pill {
    padding: 5px 13px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 999px;
    font-size: 0.78rem;
    color: var(--text-secondary);
}

/* ── Example Cards ────────────────────────────────────────── */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 32px 0;
}
.example-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.example-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(124,58,237,0.06), rgba(6,182,212,0.04));
    opacity: 0;
    transition: opacity 0.25s;
}
.example-card:hover {
    border-color: var(--border-glow);
    transform: translateY(-3px);
    box-shadow: var(--shadow), 0 0 20px rgba(124,58,237,0.1);
}
.example-card:hover::before { opacity: 1; }
.card-icon {
    font-size: 1.6rem;
    margin-bottom: 10px;
    display: block;
}
.card-category {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent-1);
    margin-bottom: 6px;
}
.card-text {
    font-size: 0.88rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

/* ── Chat Messages — WhatsApp style ──────────────────────── */
/* Hide Streamlit's native chat component entirely */
[data-testid="stChatMessage"] { display: none !important; }

/* ── Custom bubble wrapper ────────────────────────────────── */
.chat-row {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    margin: 10px 0;
    animation: bubbleIn 0.25s ease;
}
@keyframes bubbleIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── AI bubble (LEFT) ─────────────────────────────────────── */
.chat-row.ai {
    flex-direction: row;
    justify-content: flex-start;
}
.chat-row.ai .avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    box-shadow: 0 2px 10px rgba(124,58,237,0.3);
}
.chat-row.ai .bubble {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px;
    max-width: 70%;
    color: var(--text-primary);
    font-size: 0.92rem;
    line-height: 1.7;
    backdrop-filter: blur(10px);
    word-break: break-word;
    white-space: pre-wrap;
}

/* ── User bubble (RIGHT) ──────────────────────────────────── */
.chat-row.user {
    flex-direction: row-reverse;
    justify-content: flex-start;
}
.chat-row.user .avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    box-shadow: 0 2px 10px rgba(79,70,229,0.35);
}
.chat-row.user .bubble {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    border: none;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    max-width: 70%;
    color: #fff;
    font-size: 0.92rem;
    line-height: 1.7;
    word-break: break-word;
    white-space: pre-wrap;
    box-shadow: 0 4px 15px rgba(124,58,237,0.35);
}

/* Timestamp */
.bubble-time {
    font-size: 0.68rem;
    opacity: 0.5;
    margin-top: 5px;
    text-align: right;
    display: block;
}

/* ── Chat Input ───────────────────────────────────────────── */
[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(124,58,237,0.5) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
}

/* ── Stat Chips ───────────────────────────────────────────── */
.stats-row {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin: 0 0 32px;
    flex-wrap: wrap;
}
.stat-chip {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    font-size: 0.8rem;
    color: var(--text-secondary);
}
.stat-chip-icon { font-size: 1rem; }
.stat-chip-label { font-weight: 500; }

/* ── Spinner / loading ────────────────────────────────────── */
[data-testid="stSpinner"] > div {
    color: var(--accent-2) !important;
}

/* ── Info / Error boxes ───────────────────────────────────── */
[data-testid="stAlert"] {
    background: rgba(124,58,237,0.08) !important;
    border: 1px solid rgba(124,58,237,0.2) !important;
    border-radius: 12px !important;
    color: var(--text-secondary) !important;
}

/* ── Scrollbar ────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(124,58,237,0.3);
    border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(124,58,237,0.6); }

/* ── Chat divider ─────────────────────────────────────────── */
.chat-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 28px 0 16px;
    color: var(--text-muted);
    font-size: 0.75rem;
}
.chat-divider::before, .chat-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Message count badge */
.msg-count {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 4px 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 99px;
    font-size: 0.72rem;
    color: var(--text-muted);
    white-space: nowrap;
}

/* ── Chat History Items ───────────────────────────────────── */
.history-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 9px 12px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    margin-bottom: 5px;
    font-size: 0.82rem;
    color: var(--text-secondary) !important;
    cursor: pointer;
    transition: all 0.2s;
    overflow: hidden;
}
.history-item:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-glow);
}
.history-item.active {
    background: rgba(124,58,237,0.15);
    border-color: rgba(124,58,237,0.4);
    color: #c4b5fd !important;
}
.history-item-icon { flex-shrink: 0; font-size: 0.9rem; }
.history-item-label {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
}
.history-item-count {
    font-size: 0.7rem;
    opacity: 0.5;
    flex-shrink: 0;
}

/* ── What I Can Do cards ──────────────────────────────────── */
.can-do-item {
    display: flex;
    gap: 10px;
    padding: 10px 12px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    margin-bottom: 6px;
    transition: all 0.2s;
}
.can-do-item:hover { background: var(--bg-card-hover); }
.can-do-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }
.can-do-text {}
.can-do-title {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-primary) !important;
    margin-bottom: 2px;
}
.can-do-desc {
    font-size: 0.75rem;
    color: var(--text-muted) !important;
    line-height: 1.4;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar Toggle Helper (Guarantees ">>" button appears when sidebar is closed) ──
components.html("""
<script>
(function() {
    function initSidebarToggle() {
        try {
            const parentDoc = window.parent.document;
            if (!parentDoc) return;

            let btn = parentDoc.getElementById('custom-sidebar-toggle-btn');
            if (!btn) {
                btn = parentDoc.createElement('button');
                btn.id = 'custom-sidebar-toggle-btn';
                btn.innerHTML = '&#187;'; // » symbol
                btn.title = 'Show Sidebar';
                btn.setAttribute('aria-label', 'Show Sidebar');
                parentDoc.body.appendChild(btn);

                btn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    const target = parentDoc.querySelector('[data-testid="stExpandSidebarButton"]')
                                || parentDoc.querySelector('button[data-testid="stExpandSidebarButton"]')
                                || parentDoc.querySelector('[data-testid="stSidebarCollapsedControl"] button')
                                || parentDoc.querySelector('[data-testid="stSidebarCollapsedControl"]')
                                || parentDoc.querySelector('button[aria-label="Expand sidebar"]');
                    if (target) {
                        target.click();
                    } else {
                        const sb = parentDoc.querySelector('[data-testid="stSidebar"]');
                        if (sb) {
                            sb.setAttribute('aria-expanded', 'true');
                        }
                    }
                });
            }

            function checkSidebar() {
                const sb = parentDoc.querySelector('[data-testid="stSidebar"]');
                const nativeBtn = parentDoc.querySelector('[data-testid="stExpandSidebarButton"]')
                               || parentDoc.querySelector('button[data-testid="stExpandSidebarButton"]')
                               || parentDoc.querySelector('[data-testid="stSidebarCollapsedControl"]');
                
                let isCollapsed = false;
                if (sb) {
                    const rect = sb.getBoundingClientRect();
                    const style = window.parent.getComputedStyle(sb);
                    isCollapsed = (
                        sb.getAttribute('aria-expanded') === 'false' ||
                        rect.width <= 10 ||
                        rect.right <= 0 ||
                        style.display === 'none' ||
                        style.visibility === 'hidden'
                    );
                }

                if (isCollapsed) {
                    const nativeRect = nativeBtn ? nativeBtn.getBoundingClientRect() : null;
                    const nativeIsVisible = nativeRect && nativeRect.width > 0 && nativeRect.height > 0;
                    if (!nativeIsVisible) {
                        btn.style.display = 'flex';
                    } else {
                        btn.style.display = 'none';
                    }
                } else {
                    btn.style.display = 'none';
                }
            }

            setInterval(checkSidebar, 300);
            checkSidebar();
        } catch (err) {
            console.error('Sidebar toggle error:', err);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSidebarToggle);
    } else {
        initSidebarToggle();
    }
})();
</script>
""", height=0, width=0)

# ============================================================
# INITIALIZE SESSION STATE
# ============================================================

import datetime, uuid

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []   # list of {id, title, messages, timestamp}
if "active_session_id" not in st.session_state:
    st.session_state.active_session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def _save_current_to_history():
    """Persist current messages into the active session slot."""
    sid = st.session_state.active_session_id
    if sid is None or not st.session_state.messages:
        return
    for s in st.session_state.chat_sessions:
        if s["id"] == sid:
            s["messages"] = list(st.session_state.messages)
            return

def _new_chat():
    """Archive current chat and start a fresh one."""
    _save_current_to_history()
    if st.session_state.messages:
        # Only create a new archive entry if there are messages
        first_user = next((m["content"] for m in st.session_state.messages if m["role"] == "user"), "New Chat")
        title = first_user[:38] + "…" if len(first_user) > 38 else first_user
        already_exists = any(s["id"] == st.session_state.active_session_id for s in st.session_state.chat_sessions)
        if not already_exists:
            st.session_state.chat_sessions.insert(0, {
                "id": st.session_state.active_session_id or str(uuid.uuid4()),
                "title": title,
                "messages": list(st.session_state.messages),
                "timestamp": datetime.datetime.now().strftime("%d %b, %H:%M"),
            })
        else:
            for s in st.session_state.chat_sessions:
                if s["id"] == st.session_state.active_session_id:
                    s["title"] = title
                    s["messages"] = list(st.session_state.messages)
    st.session_state.messages = []
    st.session_state.active_session_id = str(uuid.uuid4())

def _load_session(sid):
    """Load a past session as the active one."""
    _save_current_to_history()
    for s in st.session_state.chat_sessions:
        if s["id"] == sid:
            st.session_state.messages = list(s["messages"])
            st.session_state.active_session_id = sid
            return

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="sidebar-logo-icon">✦</span>
        <span class="sidebar-logo-text">Harshan's AI Chatbot</span>
    </div>
    """, unsafe_allow_html=True)

    # ── New Chat & Clear Chat controls ───────────────────────
    if st.button("✦  New Chat", use_container_width=True, key="new_chat_btn"):
        _new_chat()
        st.rerun()

    msg_count = len(st.session_state.messages)
    st.markdown(f"""
    <div style="text-align:center; margin: 10px 0 8px 0;">
        <span class="msg-count">💬 {msg_count} message{'s' if msg_count != 1 else ''} in this chat</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Current Chat", use_container_width=True, key="clear_btn"):
        st.session_state.messages = []
        st.session_state.active_session_id = str(uuid.uuid4())
        st.rerun()

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # ── Chat History ─────────────────────────────────────────
    st.markdown('<p class="sidebar-section-title">💬 Chat History</p>', unsafe_allow_html=True)

    if not st.session_state.chat_sessions:
        st.markdown('<p style="font-size:0.78rem;color:var(--text-muted);padding:4px 0;">No past chats yet.</p>', unsafe_allow_html=True)
    else:
        for s in st.session_state.chat_sessions:
            is_active = s["id"] == st.session_state.active_session_id
            active_cls = "active" if is_active else ""
            msg_n = len(s["messages"])
            st.markdown(f"""
            <div class="history-item {active_cls}">
                <span class="history-item-icon">{'🟣' if is_active else '💬'}</span>
                <span class="history-item-label">{s['title']}</span>
                <span class="history-item-count">{msg_n}</span>
            </div>
            """, unsafe_allow_html=True)
            if not is_active:
                if st.button(f"Load", key=f"load_{s['id']}", use_container_width=True):
                    _load_session(s["id"])
                    st.rerun()

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # ── What This Chatbot Can Do ────────────────────────────────
    st.markdown('<p class="sidebar-section-title">🚀 What I Can Do</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="can-do-item">
        <span class="can-do-icon">🌐</span>
        <div class="can-do-text">
            <div class="can-do-title">Live Web Search</div>
            <div class="can-do-desc">Searches DuckDuckGo in real-time for up-to-date info</div>
        </div>
    </div>
    <div class="can-do-item">
        <span class="can-do-icon">📚</span>
        <div class="can-do-text">
            <div class="can-do-title">Wikipedia Lookup</div>
            <div class="can-do-desc">Fetches detailed articles on any topic instantly</div>
        </div>
    </div>
    <div class="can-do-item">
        <span class="can-do-icon">🧠</span>
        <div class="can-do-text">
            <div class="can-do-title">Multi-step Reasoning</div>
            <div class="can-do-desc">Chains multiple tools together to answer complex questions</div>
        </div>
    </div>
    <div class="can-do-item">
        <span class="can-do-icon">💬</span>
        <div class="can-do-text">
            <div class="can-do-title">Context-Aware Chat</div>
            <div class="can-do-desc">Remembers your conversation to give coherent responses</div>
        </div>
    </div>
    <div class="can-do-item">
        <span class="can-do-icon">⚡</span>
        <div class="can-do-text">
            <div class="can-do-title">Gemini-Powered</div>
            <div class="can-do-desc">Backed by Google Gemini for fast, accurate answers</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN PAGE — Hero Header
# ============================================================

if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">
            <span class="hero-badge-dot"></span>
            AI CHATBOT ONLINE
        </div>
        <h1 class="hero-title">Welcome to AI Chatbot</h1>
        <p class="hero-subtitle">
            Ask anything — I search the web, look up Wikipedia,
            and reason through complex questions in real time.
        </p>
        <div class="hero-pills">
            <span class="hero-pill">⚡ Gemini-Powered</span>
            <span class="hero-pill">🌐 Web Search</span>
            <span class="hero-pill">📚 Wikipedia</span>
            <span class="hero-pill">🧠 Context-Aware</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cards-grid">
        <div class="example-card">
            <span class="card-icon">📚</span>
            <div class="card-category">Knowledge</div>
            <div class="card-text">Who invented the telephone and how does it work?</div>
        </div>
        <div class="example-card">
            <span class="card-icon">🌍</span>
            <div class="card-category">Web Search</div>
            <div class="card-text">What are the latest breakthroughs in AI research?</div>
        </div>
        <div class="example-card">
            <span class="card-icon">💻</span>
            <div class="card-category">Programming</div>
            <div class="card-text">Explain how Java HashMaps work internally.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# CHAT HISTORY DIVIDER (when messages exist)
# ============================================================

if len(st.session_state.messages) > 0:
    st.markdown(f"""
    <div class="chat-divider">
        <span class="msg-count">
            {len(st.session_state.messages)} messages
        </span>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# DISPLAY PREVIOUS MESSAGES — custom WhatsApp-style bubbles
# ============================================================

import html as html_lib

for message in st.session_state.messages:
    role = message["role"]
    safe_content = html_lib.escape(message["content"])
    if role == "user":
        st.markdown(f"""
        <div class="chat-row user">
            <div class="avatar">👤</div>
            <div class="bubble">{safe_content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-row ai">
            <div class="avatar">✦</div>
            <div class="bubble">{safe_content}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input("Ask me anything — I can search the web for you...")

# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if user_input:

    # Assign a session id if this is the first message
    if st.session_state.active_session_id is None:
        st.session_state.active_session_id = str(uuid.uuid4())

    # Save and show user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    safe_user = html_lib.escape(user_input)
    st.markdown(f"""
    <div class="chat-row user">
        <div class="avatar">👤</div>
        <div class="bubble">{safe_user}</div>
    </div>
    """, unsafe_allow_html=True)

    # Build conversation history
    conversation = ""
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        if role == "user":
            conversation += f"User: {content}\n"
        elif role == "assistant":
            conversation += f"Assistant: {content}\n"

    # Get AI response and render as left bubble
    with st.spinner("✦ Thinking..."):
        try:
            answer = ask_gemini(conversation)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            safe_answer = html_lib.escape(answer)
            st.markdown(f"""
            <div class="chat-row ai">
                <div class="avatar">✦</div>
                <div class="bubble">{safe_answer}</div>
            </div>
            """, unsafe_allow_html=True)
            # Persist the updated session to history
            _save_current_to_history()
            # Auto-archive: update title based on first user message
            first_user = next((m["content"] for m in st.session_state.messages if m["role"] == "user"), "New Chat")
            title = first_user[:38] + "…" if len(first_user) > 38 else first_user
            already = any(s["id"] == st.session_state.active_session_id for s in st.session_state.chat_sessions)
            if not already:
                st.session_state.chat_sessions.insert(0, {
                    "id": st.session_state.active_session_id,
                    "title": title,
                    "messages": list(st.session_state.messages),
                    "timestamp": datetime.datetime.now().strftime("%d %b, %H:%M"),
                })
        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")
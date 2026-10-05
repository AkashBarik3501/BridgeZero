import streamlit as st
from google import genai
import os

# Page setup
st.set_page_config(
    page_title="BridgeZero - From Ground Zero to Any Life Goal",
    page_icon="🧭",
    layout="wide"
)

# Custom Styling for modern clean card aesthetics
st.markdown("""
<style>
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #4b5563;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        background: #e0e7ff;
        color: #3730a3;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="badge">AI-First Goal Execution Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">🧭 BridgeZero</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Bridge the gap between where you stand right now and where you want to be. '
    'A brutal reality check, zero-fluff roadmap, anti-goals (what NOT to do), and an emotional control engine.</div>', 
    unsafe_allow_html=True
)

# API Key handling: checks Streamlit Secrets first, falls back to sidebar input
default_key = st.secrets.get("GEMINI_API_KEY", "")

with st.sidebar:
    st.header("⚙️ Configuration")
    if default_key:
        api_key = default_key
        st.success("✅ Gemini API Key connected via Secrets")
    else:
        api_key = st.text_input(
            "Gemini API Key", 
            type="password", 
            placeholder="AIzaSy...",
            help="Enter your Gemini API key here or add it to Streamlit Secrets."
        )
        if not api_key:
            st.caption("Need a key? Get a free key at [Google AI Studio](https://aistudio.google.com/).")
            
    st.markdown("---")
    st.markdown("### 💡 Why BridgeZero?")
    st.info(
        "Most guides only tell you syllabus or theory. BridgeZero acts like an honest mentor: "
        "giving you exact degree/skills needed, fastest execution timeline, costly mistakes to avoid, "
        "and how to survive self-doubt."
    )

# 1-Click Samples for Reviewer testing
samples = {
    "Select a quick sample...": "",
    "🏛️ Become an IAS Officer from Scratch": "I want to become an IAS officer starting from zero. What degree do I need, how to clear UPSC in the fastest realistic timeframe, and how to avoid burnout?",
    "💻 Remote AI Engineer (No CS Degree)": "I want to become a high-earning remote AI/ML Engineer in 8 months starting with basic Python knowledge. No fancy degree.",
    "🚀 Launch a Profitable Micro-SaaS": "I want to build and launch a profitable solo B2B Micro-SaaS from zero with minimal budget while working full-time."
}

# Main Input Section
col_input, col_preset = st.columns([2, 1], gap="medium")

with col_preset:
    selected_sample = st.selectbox("⚡ Quick 1-Click Test (Reviewer Preset):", list(samples.keys()))

with col_input:
    default_prompt = samples[selected_sample] if selected_sample != "Select a quick sample..." else ""
    user_goal = st.text_area(
        "🎯 What is your target goal from Zero?",
        value=default_prompt,
        placeholder="E.g., How to become an IAS officer / How to become a Remote AI Engineer in 6 months...",
        height=100
    )

col_curr, col_speed = st.columns(2)
with col_curr:
    current_status = st.selectbox(
        "Your Current Level:",
        ["College Student / Complete Beginner", "Working Professional (Limited Time)", "Self-Taught / Switching Careers"]
    )
with col_speed:
    timeline_preference = st.selectbox(
        "Pace & Urgency:",
        ["Fast-Track & Intense (Maximum Focus)", "Balanced & Sustainable (1-2 Years)", "Part-time (2-3 Hours Daily)"]
    )

run_button = st.button("🚀 Build Zero-to-One Blueprint", type="primary", use_container_width=True)

# Execution Logic with Dynamic Active Model Detection
if run_button:
    if not api_key:
        st.error("⚠️ Please enter your Gemini API Key in the sidebar or configure GEMINI_API_KEY in secrets.")
    elif not user_goal.strip():
        st.warning("⚠️ Please define your goal or choose one of the quick presets above.")
    else:
        with st.spinner("Analyzing real-world execution path, anti-goals, and psychology..."):
            system_instruction = f"""
You are BridgeZero: an elite, empathetic, and brutally honest mentor who helps ambitious people reach massive life goals from absolute ground zero.
Your tone is like a high-performing elder brother or trusted friend: zero corporate jargon, realistic, practical, encouraging, and razor-sharp.

The User's Goal: {user_goal}
Current Status: {current_status}
Pace: {timeline_preference}

Generate a master blueprint structured EXACTLY with these 4 sections using GitHub Markdown:

### 1. 🔍 The Reality Check & Prerequisites
- Minimum degree/qualification legally or practically required (truth, no myths).
- Realistic timeline (fastest possible vs average).
- Hard truths: what this journey actually costs in time, energy, and sacrifices.

### 2. 🗺️ The Sprint Execution Roadmap
Break it down into 3-4 distinct chronological phases (e.g. Month 0-2: Foundation, Month 3-5: Mastery & Projects, etc.).
For each phase:
- **Core Focus:** The 1 single thing that matters.
- **Top 2 High-ROI Actions:** Specific resources or actionable routines.
- **Milestone Check:** How do they know this phase is complete?

### 3. 🚫 The Anti-Roadmap ("Kya KABHI Mat Karna")
The fatal mistakes where 90% of beginners waste months or quit:
- Avoidable time-traps (e.g., buying too many books, fake productivity, tutorial hell).
- Illusions to drop immediately.

### 4. 🧠 Emotional Control & The Mental Game
- What to do when self-doubt, fear of failure, or relative pressure kicks in.
- The 24-hour reset rule when you feel like quitting.
- A direct, high-energy closing note from you as a friend.
"""
            try:
                client = genai.Client(api_key=api_key)
                
                # Active supported models list in priority order
                preferred_models = [
                    "gemini-2.5-flash",
                    "gemini-3.8-flash",
                    "gemini-3.1-flash-lite",
                    "gemini-2.5-pro"
                ]
                
                response = None
                last_error = None
                
                for target_model in preferred_models:
                    try:
                        response = client.models.generate_content(
                            model=target_model,
                            contents=system_instruction
                        )
                        if response and response.text:
                            break
                    except Exception as e:
                        last_error = e
                        continue

                if response and response.text:
                    st.success("✅ Your Blueprint is Ready!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                    st.download_button(
                        label="📥 Download Blueprint (.md)",
                        data=response.text,
                        file_name="BridgeZero_Blueprint.md",
                        mime="text/markdown"
                    )
                else:
                    st.error(f"Execution Error: {str(last_error)}")

            except Exception as e:
                st.error(f"Initialization Error: {str(e)}")
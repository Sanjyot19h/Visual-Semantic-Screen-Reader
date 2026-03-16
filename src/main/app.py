import streamlit as st
import os
import time
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="Visionary AI Console",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# # 2. Custom CSS for Dark Mode/Pro Look
# st.markdown("""
#     <style>
#     .main { background-color: #0e1117; }
#     .stTextArea textarea { color: #00FF00 !important; font-family: 'Courier New', Courier, monospace !important; background-color: #161b22 !important; }
#     .status-box { padding: 10px; border-radius: 5px; border: 1px solid #30363d; background-color: #21262d; margin-bottom: 20px; }
#     </style>
#     """, unsafe_allow_value=True)
# 2. Custom CSS for Dark Mode/Pro Look

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { color: #00FF00 !important; font-family: 'Courier New', Courier, monospace !important; background-color: #161b22 !important; }
    .status-box { padding: 10px; border-radius: 5px; border: 1px solid #30363d; background-color: #21262d; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True) # <--- Changed this line

# 3. Header Section
st.title("👁️ Visionary: Visual-Semantic Monitor")
st.write("Real-time desktop analysis for the visually impaired.")

# 4. Layout Columns
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("🖼️ Live Vision Feed")
    placeholder_img = st.empty() # This allows us to update the image without refreshing the whole page

with col_right:
    st.subheader("📜 Neural Narrative Log")
    placeholder_text = st.empty()

# 5. The "Manual" Refresh Loop
# This is the "Engine" that makes the UI live without shortcuts
while True:
    # --- UPDATE IMAGE ---
    if os.path.exists("latest_capture.png"):
        try:
            img = Image.open("latest_capture.png")
            placeholder_img.image(img, use_container_width=True, caption="Current AI Perspective")
        except:
            pass # Handles file-access conflicts if the AI is currently writing the file

    # --- UPDATE LOGS ---
    if os.path.exists("narrative_log.txt"):
        with open("narrative_log.txt", "r") as f:
            lines = f.readlines()
            # Show the last 20 lines so the most recent is always visible
            recent_logs = "".join(lines[-20:])
            placeholder_text.text_area(label="Recent Thinking", value=recent_logs, height=450, key=str(time.time()))

    time.sleep(1) # Wait 1 second before checking for new data


 
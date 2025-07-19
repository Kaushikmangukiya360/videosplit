import os
import shutil
import zipfile
import subprocess
from datetime import datetime
import streamlit as st

# --- CONFIG ---
MAX_FILE_SIZE_MB = 2024
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
LOG_DIR = "logs"
HISTORY_FILE = os.path.join(LOG_DIR, "history.csv")
ZIP_NAME = "split_clips.zip"
PASSWORD = "nexvision" 

# --- SETUP ---
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

st.set_page_config(page_title="🔒 NexVision Video Splitter", layout="centered")
st.title("🔒 NexVision Secure Video Splitter")
st.caption("✨ Made by Kaushik Mangukiya")

# --- LOGIN ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if password == PASSWORD:
            st.session_state.authenticated = True
            st.success("✅ Logged in!")
        else:
            st.error("❌ Incorrect password")
    st.stop()

# --- UPLOAD VIDEO ---
uploaded_file = st.file_uploader("📤 Upload your video file (Max 100MB)", type=["mp4", "mkv", "mov"])

if uploaded_file:
    if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.error("🚫 File too large. Please upload a file under 100MB.")
    else:
        filename = uploaded_file.name
        input_path = os.path.join(UPLOAD_DIR, filename)
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        split_duration = st.number_input("⏱️ Clip duration in seconds", min_value=10, max_value=300, value=60, step=10)

        if st.button("🚀 Split & Download"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_id = f"{timestamp}_{filename}"
            output_subdir = os.path.join(OUTPUT_DIR, session_id)
            os.makedirs(output_subdir, exist_ok=True)

            output_pattern = os.path.join(output_subdir, "part_%03d.mkv")

            command = [
                "ffmpeg",
                "-i", input_path,
                "-c", "copy",
                "-map", "0",
                "-f", "segment",
                "-segment_time", str(split_duration),
                "-reset_timestamps", "1",
                output_pattern
            ]

            with st.spinner("🔧 Splitting video, please wait..."):
                process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if process.returncode == 0:
                zip_path = os.path.join(output_subdir, ZIP_NAME)
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for file in os.listdir(output_subdir):
                        if file.endswith(".mkv"):
                            zipf.write(os.path.join(output_subdir, file), arcname=file)

                # Save to history
                with open(HISTORY_FILE, "a") as log:
                    log.write(f"{timestamp},{filename},{split_duration},{session_id}\n")

                st.success("✅ Video successfully split and zipped.")
                with open(zip_path, "rb") as f:
                    st.download_button("⬇️ Download ZIP of Clips", f, file_name=ZIP_NAME)
            else:
                st.error("❌ FFmpeg failed")
                st.code(process.stderr)

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "🔒 Powered by NexVision | Developed by Kaushik Mangukiya"
    "</div>",
    unsafe_allow_html=True
)

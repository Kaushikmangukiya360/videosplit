import streamlit as st
import subprocess
import os
import uuid
import glob
import shutil

# Page config
st.set_page_config(page_title="Secure Video Splitter", layout="centered")
st.title("🎬 Secure Video Splitter (macOS/Web)")

# Upload input
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mkv", "avi", "mov"])
duration = st.number_input("Split duration (in seconds)", min_value=10, value=60)

if uploaded_file and duration:
    if st.button("🔪 Split Video"):
        # Unique session ID
        session_id = str(uuid.uuid4())[:8]
        input_dir = f"uploads/{session_id}"
        output_dir = f"outputs/{session_id}"
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        input_path = os.path.join(input_dir, uploaded_file.name)
        output_pattern = os.path.join(output_dir, "part_%03d.mkv")

        # Save uploaded video
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # FFmpeg command
        cmd = [
            "ffmpeg", "-i", input_path,
            "-c", "copy", "-map", "0",
            "-segment_time", str(duration),
            "-f", "segment",
            "-reset_timestamps", "1",
            output_pattern
        ]

        # Run FFmpeg
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            st.success("✅ Video split successfully!")
            st.info("Download your video clips below:")

            part_files = sorted(glob.glob(os.path.join(output_dir, "*.mkv")))
            for part in part_files:
                with open(part, "rb") as f:
                    st.download_button(
                        label=f"⬇️ {os.path.basename(part)}",
                        data=f.read(),
                        file_name=os.path.basename(part),
                        mime="video/x-matroska"
                    )

            # Optional cleanup after success
            shutil.rmtree(input_dir)

        else:
            st.error("❌ FFmpeg failed! Please check your input video.")
            st.code(result.stderr.decode("utf-8"))

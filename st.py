import streamlit as st
import subprocess
import os

st.title("🎬 Video Splitter")

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mkv", "avi", "mov"])
duration = st.number_input("Split duration (in seconds)", min_value=10, step=10)

if uploaded_file and duration:
    if st.button("Split Video"):
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        output_dir = "output_parts"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "part_%03d.mkv")

        cmd = [
            "ffmpeg", "-i", uploaded_file.name,
            "-c", "copy", "-map", "0",
            "-segment_time", str(duration),
            "-f", "segment", "-reset_timestamps", "1",
            output_path
        ]
        subprocess.run(cmd)
        st.success(f"✅ Video split successfully. Check the '{output_dir}' folder.")

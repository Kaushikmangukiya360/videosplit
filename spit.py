import subprocess
import os

def split_video(input_file, output_dir, duration):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_pattern = os.path.join(output_dir, "part_%03d.mkv")

    command = [
        "ffmpeg",
        "-i", input_file,        
        "-c", "copy",
        "-map", "0",
        "-segment_time", str(duration),
        "-f", "segment",
        "-reset_timestamps", "1",
        output_pattern
    ]

    subprocess.run(command)

    print(f"✅ Video splitting completed. Parts saved in: {output_dir}")

input_video = "1.mkv"
output_folder = "output_parts"
split_duration = 50

split_video(input_video, output_folder, split_duration)
#!/bin/bash

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Input video file (hardcoded or ask client to replace 1.mkv)
INPUT_VIDEO="$DIR/1.mkv"
OUTPUT_FOLDER="$DIR/output_parts"

# Create output folder
mkdir -p "$OUTPUT_FOLDER"

# Run ffmpeg split
"$DIR/ffmpeg" -i "$INPUT_VIDEO" -c copy -map 0 -segment_time 50 -f segment -reset_timestamps 1 "$OUTPUT_FOLDER/part_%03d.mkv"

echo "✅ Video split complete. Check $OUTPUT_FOLDER"
read -p "Press [Enter] to exit"
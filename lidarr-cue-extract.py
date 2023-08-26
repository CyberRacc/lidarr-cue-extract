import os
import subprocess
import re
import sys

def split_flac_with_cue(album_dir):
    print(f"Processing directory: {album_dir}")

    # Check for .flac and .cue files in the album directory
    flac_files = [f for f in os.listdir(album_dir) if f.endswith('.flac')]
    cue_files = [f for f in os.listdir(album_dir) if f.endswith('.cue')]

    # If there's more than one .flac file or no .cue file, exit
    if len(flac_files) != 1 or len(cue_files) == 0:
        print(f"Skipping directory. Found {len(flac_files)} FLAC files and {len(cue_files)} CUE files.")
        return

    flac_file = os.path.join(album_dir, flac_files[0])
    cue_file = os.path.join(album_dir, cue_files[0])
    
    with open(cue_file, 'r') as f:
        cue_content = f.read()

    # Extract album information
    matches = re.findall(r'TITLE "(.*?)"', cue_content)
    album_title = matches[0] if matches else "Unknown Album"
    print(f"Album Title: {album_title}")
    
    # Extract track information
    tracks = re.findall(r'TRACK (\d+) AUDIO.*?TITLE "(.*?)".*?INDEX 01 (\d+:\d+:\d+)', cue_content, re.DOTALL)
    
    for track in tracks:
        track_num, track_title, start_time = track
        
        # Convert start time to seconds
        mins, secs, frames = map(int, start_time.split(':'))
        start_seconds = mins * 60 + secs + frames / 75.0
        
        # Set output file name
        output_file = os.path.join(album_dir, f"{track_num} - {track_title}.flac")
        
        # Use ffmpeg to split flac
        print(f"Extracting track {track_num}: {track_title} to {output_file}")
        cmd = [
            'ffmpeg',
            '-i', flac_file,
            '-ss', str(start_seconds),
            '-t', '30',  # Assuming a max track length of 30 mins. Adjust if needed.
            '-c', 'copy',
            output_file
        ]
        subprocess.run(cmd, capture_output=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the album directory.")
        sys.exit(1)
    split_flac_with_cue(sys.argv[1])

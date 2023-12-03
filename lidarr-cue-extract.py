import os
import subprocess
import re
import sys

def split_flac_with_cue(album_dir):
    print(f"Processing directory: {album_dir}")

    flac_files = [f for f in os.listdir(album_dir) if f.endswith('.flac')]
    cue_files = [f for f in os.listdir(album_dir) if f.endswith('.cue')]

    if len(flac_files) != 1 or len(cue_files) == 0:
        print(f"Skipping directory. Found {len(flac_files)} FLAC files and {len(cue_files)} CUE files.")
        return

    flac_file = os.path.join(album_dir, flac_files[0])
    cue_file = os.path.join(album_dir, cue_files[0])
    
    with open(cue_file, 'r') as f:
        cue_content = f.read()

    tracks = re.findall(r'TRACK (\d+) AUDIO.*?TITLE "(.*?)".*?INDEX 01 (\d+:\d+:\d+)', cue_content, re.DOTALL)

    for index, (track_num, track_title, start_time) in enumerate(tracks):
        track_num = track_num.zfill(2)
        
        mins, secs, frames = map(int, start_time.split(':'))
        start_seconds = mins * 60 + secs + frames / 75.0

        if index + 1 < len(tracks):
            next_mins, next_secs, next_frames = map(int, tracks[index + 1][2].split(':'))
            next_start_seconds = next_mins * 60 + next_secs + next_frames / 75.0
            duration = next_start_seconds - start_seconds
            duration_option = ['-t', str(duration)]
        else:
            duration_option = []

        output_file = os.path.join(album_dir, f"{track_num} - {track_title}.flac")

        cmd = [
            'ffmpeg',
            '-i', flac_file,
            '-ss', str(start_seconds),
            *duration_option,
            '-c', 'copy',
            '-map_metadata', '0',
            output_file
        ]
        subprocess.run(cmd, capture_output=True, text=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the album directory.")
        sys.exit(1)
    split_flac_with_cue(sys.argv[1])

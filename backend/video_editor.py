import os
import subprocess

def create_summary(video_path: str, cuts: list, output_dir: str = "output") -> str:
    """
    Cuts the video segments and stitches them together.
    Retruns path to the output video.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    filename = os.path.basename(video_path)
    name, _ = os.path.splitext(filename)
    # Force .mp4 for output stability
    ext = ".mp4"
    output_path = os.path.abspath(os.path.join(output_dir, f"{name}_highlight{ext}"))
    
    temp_clips_dir = os.path.join(output_dir, "temp_clips")
    if os.path.exists(temp_clips_dir):
        import shutil
        shutil.rmtree(temp_clips_dir)
    os.makedirs(temp_clips_dir)
    
    clip_files = []
    
    for i, (start, end) in enumerate(cuts):
        clip_name = f"clip_{i:03d}{ext}"
        clip_path = os.path.join(temp_clips_dir, clip_name)
        
        duration = end - start
        
        # Strict compatibility settings
        # -r 30: Force 30 fps
        # scale: Ensure divisible by 2 for yuv420p
        # profile:v main: widely supported
        cmd = [
            'ffmpeg', '-y',
            '-ss', str(start),
            '-t', str(duration),
            '-i', video_path,
            '-vf', "scale=ceil(iw/2)*2:ceil(ih/2)*2,format=yuv420p", 
            '-c:v', 'libx264', '-profile:v', 'main', '-preset', 'medium',
            '-r', '30',
            '-c:a', 'aac',
            clip_path
        ]
        
        try:
             subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
             print(f"Error cutting clip {i}: {e.stderr.decode()}")
             raise e

        clip_files.append(clip_name) # Store relative filename
        
    # 2. Concat clips
    list_file_path = os.path.join(temp_clips_dir, "list.txt")
    with open(list_file_path, "w") as f:
        for clip in clip_files:
            f.write(f"file '{clip}'\n")
            
    # RE-ENCODE CONCAT to fix timestamps and container issues
    cmd_concat = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', "list.txt",
        '-c:v', 'libx264', '-preset', 'ultrafast', 
        '-c:a', 'aac',
        '-movflags', '+faststart',
        output_path
    ]
    
    try:
        # Run inside temp_clips_dir so relative paths work
        subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, cwd=temp_clips_dir)
    except subprocess.CalledProcessError as e:
        print(f"Error merging: {e.stderr.decode()}")
        raise e
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_clips_dir)
    
    return output_path

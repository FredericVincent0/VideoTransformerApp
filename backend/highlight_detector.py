import librosa
import numpy as np
import os
import subprocess

def extract_audio(video_path: str, audio_path: str):
    """Extracts audio from video file to WAV format for analysis."""
    command = [
        'ffmpeg', '-y', '-i', video_path, 
        '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '1', 
        audio_path
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def analyze_highlights(video_path: str, target_duration: int = 60):
    """
    Analyzes the audio of the video to find the most energetic moments.
    Returns a list of (start, end) tuples in seconds.
    """
    temp_audio = video_path + ".wav"
    try:
        extract_audio(video_path, temp_audio)
        
        # Load audio
        y, sr = librosa.load(temp_audio, sr=None)
        
        # Calculate RMS energy
        hop_length = 512
        frame_length = 2048
        rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        
        # Convert frames to time
        times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)
        
        # Find high energy segments
        # 1. Thresholding: top 20% of energy
        threshold = np.percentile(rms, 80)
        
        high_energy_frames = rms > threshold
        
        # Group frames into segments
        # We want segments of at least 2 seconds
        min_segment_frames = int(2.0 * sr / hop_length) 
        
        segments = []
        current_start = None
        
        for i, is_high in enumerate(high_energy_frames):
            if is_high:
                if current_start is None:
                    current_start = i
            else:
                if current_start is not None:
                    # Segment ended
                    if i - current_start >= min_segment_frames:
                        start_time = times[current_start]
                        end_time = times[i]
                        segments.append((start_time, end_time))
                    current_start = None
                    
        # If we have too many segments, pick the loudest ones to fit target_duration
        # Calculate average energy for each segment
        scored_segments = []
        for start, end in segments:
            # Convert time back to frames roughly for slicing rms (approx)
            start_frame = int(start * sr / hop_length)
            end_frame = int(end * sr / hop_length)
            segment_energy = np.mean(rms[start_frame:end_frame])
            scored_segments.append({
                "start": start,
                "end": end,
                "duration": end - start,
                "score": segment_energy
            })
            
        # Sort by score descending
        scored_segments.sort(key=lambda x: x["score"], reverse=True)
        
        final_cuts = []
        current_total_duration = 0
        
        # Add a buffer to each cut (e.g. 1 sec before and after) to capture context
        buffer = 1.0 
        
        for seg in scored_segments:
            if current_total_duration >= target_duration:
                break
                
            # Add context
            seg_start = max(0, seg["start"] - buffer)
            # We don't know total video length here easily without probing, but ffmpeg handles over-read usually.
            # Let's just hold the end.
            seg_end = seg["end"] + buffer
            
            final_cuts.append((seg_start, seg_end))
            current_total_duration += (seg_end - seg_start)
            
        # Sort cuts by time so they appear in order
        final_cuts.sort(key=lambda x: x[0])
        
        # Merge overlapping cuts
        if not final_cuts:
            return []
            
        merged = []
        curr_start, curr_end = final_cuts[0]
        
        for i in range(1, len(final_cuts)):
            next_start, next_end = final_cuts[i]
            if next_start < curr_end: # Overlap or touch
                curr_end = max(curr_end, next_end)
            else:
                merged.append((curr_start, curr_end))
                curr_start, curr_end = next_start, next_end
        merged.append((curr_start, curr_end))
        
        return merged

    finally:
        if os.path.exists(temp_audio):
            os.remove(temp_audio)

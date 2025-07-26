#!/usr/bin/env python3
"""
Video Recording Utility for CrowdFlow AI
Records video from webcam and saves to specified path
"""

import cv2
import sys
import os
from pathlib import Path

def record_video(output_path, duration=10, fps=25):
    """
    Record video from webcam
    
    Args:
        output_path (str): Path to save the recorded video
        duration (int): Recording duration in seconds
        fps (int): Frames per second
    """
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open webcam")
        return False
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    print(f"🎥 Recording video for {duration} seconds...")
    print("Press 'q' to stop recording early")
    
    frame_count = 0
    max_frames = duration * fps
    
    try:
        while frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Could not read frame")
                break
            
            # Write frame to video
            out.write(frame)
            
            # Display frame
            cv2.imshow('Recording... Press Q to stop', frame)
            
            # Check for 'q' key to stop early
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("⏹️  Recording stopped by user")
                break
            
            frame_count += 1
            
            # Show progress
            if frame_count % fps == 0:
                seconds_recorded = frame_count // fps
                print(f"📹 Recorded {seconds_recorded}/{duration} seconds")
    
    except KeyboardInterrupt:
        print("\n⏹️  Recording interrupted")
    
    finally:
        # Clean up
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        if frame_count > 0:
            print(f"✅ Video saved to: {output_path}")
            print(f"📊 Frames recorded: {frame_count}")
            return True
        else:
            print("❌ No frames were recorded")
            return False

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python record_video.py <output_path> [duration] [fps]")
        print("Example: python record_video.py data/videos/recorded.mp4 10 25")
        sys.exit(1)
    
    output_path = sys.argv[1]
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    fps = int(sys.argv[3]) if len(sys.argv) > 3 else 25
    
    success = record_video(output_path, duration, fps)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 
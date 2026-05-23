import os
import subprocess

video_path = r'media\videos\Scene5_3\1920p15\Scene5_3_3D.mp4'

# Use ffmpeg to extract frames
for name, time in [('start', '00:00:00'), ('middle', '00:00:01'), ('end', '00:00:01.9')]:
    output = f'debug_{name}.png'
    cmd = ['ffmpeg', '-ss', time, '-i', video_path, '-vf', 'scale=960:540', '-vframes', '1', '-y', output]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        print(f'✓ Extracted {output}')
    else:
        print(f'✗ Failed to extract {output}')

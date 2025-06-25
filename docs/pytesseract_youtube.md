### Using pytesseract to extract text from YouTube

This example demonstrates how to apply the [pytesseract](https://pypi.org/project/pytesseract/) wrapper to frames from a YouTube video. Ensure the Tesseract OCR engine is installed and available from the command line.

#### Install dependencies

```bash
pip install pytesseract pytube opencv-python Pillow
```

#### Example

```python linenums="1"
from pytube import YouTube
import pytesseract
import cv2
from PIL import Image
import tempfile
import os

url = "https://www.youtube.com/watch?v=VIDEO_ID"
yt = YouTube(url)
stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
tmp_dir = tempfile.mkdtemp()
video_path = stream.download(output_path=tmp_dir)

cap = cv2.VideoCapture(video_path)
frame_idx = 0
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
    if frame_idx % 30 == 0:  # roughly every second for 30 FPS video
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        text = pytesseract.image_to_string(img)
        print(f"Frame {frame_idx}: {text.strip()}")
    frame_idx += 1

cap.release()
os.remove(video_path)
os.rmdir(tmp_dir)
```

The script downloads the video, processes every 30th frame, and prints the recognized text.

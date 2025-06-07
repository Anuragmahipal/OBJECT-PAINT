# 🎨 Object Paint Using Real-Time Color Tracking with OpenCV

Bring your creativity to life — **draw in the air** using just a colored object and your webcam! This simple yet powerful paint app tracks the color of any object you choose (like a  pen cap, or marker) and lets you create beautiful digital art in real time.

---

## ✨ Features

- 🎯 **Easy Color Calibration:** Sample your object's color inside a convenient on-screen box  
- 🔍 **Robust Color Tracking:** Uses HSV color space for accurate real-time detection  
- 🖌️ **Smooth Drawing:** Draw freehand lines that follow your object’s movement seamlessly  
- 🌈 **Multiple Brush Colors:** Switch between vibrant colors with just a key press (`x`)  
- 🎚️ **Adjustable Brush Size:** Make your strokes thicker or thinner using `d` and `a` keys  
- 🧹 **Clear Your Canvas:** Press `c` to wipe the slate clean and start fresh  
- 🚪 **Exit Anytime:** Press `q` to quit the app gracefully  

---

## 🚀 How It Works

1. **Place your colored object inside the green sampling box** on the webcam feed — this helps the app learn your object’s unique color profile.  
2. **Hit the `s` key to calibrate** the color detection based on the sample.  
3. The app **isolates your object by filtering colors** and tracks its position in each video frame.  
4. As you move the object, it **draws smooth lines on a virtual canvas** following the object’s centroid.  
5. Use keyboard shortcuts to change colors, adjust brush thickness, or clear the canvas — all without touching your mouse !  

---

## 🛠️ Installation

Make sure Python is installed, then grab the required packages with:

```
pip install opencv-python numpy
```


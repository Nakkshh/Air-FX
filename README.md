
---

# ✋ Air-FX

Air-FX is a hand gesture-controlled computer vision project built with OpenCV and MediaPipe. Use your hand gestures to control zoom and apply visual effects in real-time — no touch required!

---

## 🚀 Features

- 🖐️ Detects hand gestures using webcam
- 🔍 Zoom in and out with finger distance
- 🎨 Apply effects like **Grayscale**, **Sepia**, and **Blur**
- 🔄 Reset effects with open hand
- ✨ Smooth, real-time gesture control

---

## 📦 Setup

### 1. Clone the repository

```bash
git clone https://github.com/Nakkshh/Air-FX.git
cd Air-FX
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv .venv
.\.venv\Scripts\activate     # On Windows
# or
source .venv/bin/activate    # On Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, install manually:

```bash
pip install opencv-python mediapipe numpy
```

### 4. Run the app

```bash
python air_fx.py
```

---

## 🎮 Controls

| 👆 Fingers | 🧠 Functionality        |
|-----------|------------------------|
| 0         | Reset to Normal View   |
| 1         | Zoom to **2x**         |
| 2         | Apply **Sepia**        |
| 3         | Apply **Blur**         |
| 4         | Apply **Grayscale**    |
| 5         | Reset Effects & Zoom   |

Zoom will auto-adjust based on the distance between index fingertip and PIP joint.

---

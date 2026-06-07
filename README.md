# Smart Face Recognition Attendance System

A real-time face recognition attendance system built with Python and OpenCV — automatically detects and logs employee/student attendance using webcam feed, stores records in SQLite, and visualises data through interactive charts.

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| Face Detection | OpenCV — Haar Cascade Classifier |
| Face Recognition | LBPH (Local Binary Patterns Histograms) |
| GUI | Tkinter |
| Database | SQLite |
| Data Analysis | Pandas, NumPy |
| Visualisation | Matplotlib |
| Export | OpenPyXL (Excel) |
| Concurrency | Python Threading |

---

## Features

- **Real-time face detection** — Haar cascade detects faces in live webcam frames
- **Face recognition** — LBPH algorithm matches faces with confidence threshold of 60
- **Automatic attendance logging** — name, date, and time recorded on successful recognition
- **New user registration** — captures 30 face samples per user for training
- **Model training** — trains LBPH recognizer on registered face dataset
- **Data visualisation** — bar chart and pie chart of attendance per person
- **Excel export** — auto-exports attendance to `.xlsx` on every recognition event
- **Threading** — face recognition runs on a separate thread to keep GUI responsive

---

## Project Structure

```
smart-face-attendance/
├── src/
│   └── face_attendance_gui.py      ← main application — GUI + recognition + training
├── database/
│   └── create_db.py                ← run once to initialise SQLite database
├── docs/
│   └── project_report.pdf          ← full project synopsis and module description
├── requirements.txt                ← Python dependencies
├── .gitignore
└── README.md
```

**Runtime files (auto-generated, not committed):**
```
dataset/          ← captured face images per user
trainer.yml       ← trained LBPH model
label_map.txt     ← maps numeric labels to user names
attendance.db     ← SQLite attendance database
attendance_export.xlsx  ← auto-exported attendance data
```

---

## How It Works

### 1. Registration
- User enters ID and name
- Webcam captures 30 grayscale face samples
- Saved to `dataset/User.<id>.<count>.jpg`
- Label mapping written to `label_map.txt`

### 2. Training
- LBPH recognizer trained on all images in the dataset directory
- Trained model saved to `trainer.yml`

### 3. Recognition
- Live webcam feed processed frame by frame
- Haar cascade detects face regions
- LBPH predicts label + confidence score
- If confidence < 60 → recognised → attendance marked in SQLite + exported to Excel
- If confidence ≥ 60 → marked as "Unknown"

### 4. Visualisation
- Bar chart — attendance count per person
- Pie chart — attendance distribution percentage

---

## Setup Instructions

**1. Clone the repository**
```bash
git clone https://github.com/nidhib08/smart-face-attendance.git
cd smart-face-attendance
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Initialise the database**
```bash
python database/create_db.py
```

**4. Run the application**
```bash
python src/face_attendance_gui.py
```

**5. First time setup**
- Click **Register New User** → enter ID and name → captures 30 face samples
- Click **Train Model** → trains the LBPH recognizer
- Click **Start Face Scan** → begins real-time attendance marking

---

## ML Pipeline

```
Webcam Input
    ↓
Grayscale Conversion
    ↓
Haar Cascade Face Detection
    ↓
LBPH Face Recognition (confidence threshold: 60)
    ↓
Attendance Logged → SQLite + Excel Export
    ↓
Matplotlib Visualisation
```

---

## SDLC Mapping

| Phase | Implementation |
|---|---|
| Requirements | Problem statement — replace manual attendance with automated CV system |
| Design | Module-wise architecture — GUI, recognition, DB, visualisation |
| Development | Python, OpenCV LBPH, SQLite, Tkinter, threading |
| Testing | Confidence threshold tuning, edge case handling for unknown faces |
| Deployment | Standalone desktop application |

---

## Achievement

This project received a **Special Mention** at the Web Protoplot Competition — Innovation 2025, Cummins College of Engineering for Women, Pune.

---

## Author

Nidhi Borkar — Computer Engineering, Cummins College of Engineering for Women, Pune

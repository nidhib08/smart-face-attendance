# This code is a simple GUI application for a face recognition attendance system using OpenCV and Tkinter.
# It allows users to register new faces, start face scanning, visualize attendance data, and train the model.
# The attendance data is stored in a SQLite database and can be exported to an Excel file.
# The code also includes functions to display attendance data in bar and pie charts using Matplotlib.

import tkinter as tk
from tkinter import messagebox
import cv2
import sqlite3
from datetime import datetime
import threading
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime
filename = f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"




# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# Load label map
label_map = {}
with open("label_map.txt", "r") as f:
    for line in f:
        label, name = line.strip().split(":")
        label_map[int(label)] = name

def mark_attendance(name):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, time))
    conn.commit()
    conn.close()
    export_latest_data() 


def start_recognition():
    def run_recognition():
        cap = cv2.VideoCapture(0)  # Change to 1 if 0 doesn't work
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                label, confidence = recognizer.predict(face)
                if confidence < 60:  # Threshold: lower means more confident
                    name = label_map[label]
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    mark_attendance(name)
                    messagebox.showinfo("Attendance", f"{name}'s Attendance Marked!")
                    cap.release()
                    cv2.destroyAllWindows()
                    return
                else:
                    cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Face Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    threading.Thread(target=run_recognition).start()

def fetch_data():
    conn = sqlite3.connect("attendance.db")
    df = pd.read_sql_query("SELECT * FROM attendance", conn)
    conn.close()
    return df

def show_bar_chart(df):
    count = df['name'].value_counts()
    count.plot(kind='bar', title='Attendance Count per Person', color='mediumpurple')
    plt.xlabel('Name')
    plt.ylabel('Days Present')
    plt.tight_layout()
    plt.show()

def show_pie_chart(df):
    count = df['name'].value_counts()
    count.plot(kind='pie', title='Attendance Distribution', autopct='%1.1f%%', startangle=90)
    plt.ylabel('')
    plt.tight_layout()
    plt.show()


def export_latest_data(filename="attendance_export.xlsx"):
    conn = sqlite3.connect("attendance.db")
    df = pd.read_sql_query("SELECT * FROM attendance", conn)
    conn.close()
    df.to_excel(filename, index=False)
    print(f"[INFO] Auto-exported attendance to {filename}")



def register_user():
    def capture_images():
        user_id = entry_id.get()
        name = entry_name.get().strip()

        if not user_id or not name:
            messagebox.showwarning("Input Error", "Please enter both ID and Name.")
            return

        if not os.path.exists("dataset"):
            os.makedirs("dataset")

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        cap = cv2.VideoCapture(0)
        count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                count += 1
                cv2.imwrite(f"dataset/User.{user_id}.{count}.jpg", gray[y:y+h, x:x+w])
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow("Registering Face", frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or count >= 30:
                break

        cap.release()
        cv2.destroyAllWindows()

        with open("label_map.txt", "a") as f:
            f.write(f"{user_id}:{name}\n")

        messagebox.showinfo("Success", "Images captured successfully!")

    top = tk.Toplevel(app)
    top.title("Register New User")
    tk.Label(top, text="User ID").pack()
    entry_id = tk.Entry(top)
    entry_id.pack()
    tk.Label(top, text="Name").pack()
    entry_name = tk.Entry(top)
    entry_name.pack()
    tk.Button(top, text="Capture Faces", command=capture_images).pack(pady=10)


def train_model():
    dataset_path = "D:\\College work\\projectt\\face_data"
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    labels = []
    label_map = {}
    current_label = 0

    for person_name in os.listdir(dataset_path):
        person_dir = os.path.join(dataset_path, person_name)
        if not os.path.isdir(person_dir):
            continue

        label_map[current_label] = person_name

        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            faces.append(img)
            labels.append(current_label)

        current_label += 1

    recognizer.train(faces, np.array(labels))
    recognizer.save("trainer.yml")

    with open("label_map.txt", "w") as f:
        for label, name in label_map.items():
            f.write(f"{label}:{name}\n")

    messagebox.showinfo("Training Complete", "Model training completed successfully!")



def visualize_attendance():
    df = fetch_data()
    if df.empty:
        messagebox.showwarning("No Data", "No attendance data found.")
        return

    show_bar_chart(df)
    show_pie_chart(df)
    show_trend_graph(df)

# Create main GUI window
app = tk.Tk()
app.title("Face Attendance System")
app.geometry("400x300")
app.configure(bg="#8A2BE2")  # Purple background color

# Title Label
tk.Label(app, text="Face Recognition Attendance System", font=("Arial", 16), bg="#8A2BE2", fg="white").pack(pady=20)

# Start Face Scan Button
tk.Button(app, text="Start Face Scan", command=start_recognition, width=20, height=2, bg="white", fg="purple", font=("Arial", 12)).pack(pady=10)

# Visualize Attendance Button
tk.Button(app, text="Visualize Attendance", command=visualize_attendance, width=20, height=2, bg="white", fg="purple", font=("Arial", 12)).pack(pady=10)

# Exit Button
tk.Button(app, text="Exit", command=app.quit, width=20, height=2, bg="white", fg="purple", font=("Arial", 12)).pack(pady=10)

# Register User Button
tk.Button(app, text="Register New User", command=register_user, width=20, height=2, bg="white", fg="purple", font=("Arial", 12)).pack(pady=10)

# Train Model Button
tk.Button(app, text="Train Model", command=train_model, width=20, height=2, bg="white", fg="purple", font=("Arial", 12)).pack(pady=10)

# Run the GUI
app.mainloop()


#This is the attendance dashboard code for a face recognition attendance system.
#It allows users to view attendance data, export it to Excel, and visualize it using bar and pie charts.

"""import sqlite3
import pandas as pd
from tabulate import tabulate

def fetch_data():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    data = cursor.fetchall()
    conn.close()
    return data

def export_excel(data, filename="attendance_export.xlsx"):
    df = pd.DataFrame(data, columns=["ID", "Name", "Date", "Time"])
    df.to_excel(filename, index=False)
    print(f"[INFO] Exported to {filename}")

def dashboard():
    while True:
        print("\n1. View All\n2. Export to Excel\n3. Exit")
        choice = input("Choice: ")

        if choice == '1':
            data = fetch_data()
            print(tabulate(data, headers=["ID", "Name", "Date", "Time"], tablefmt="pretty"))
        elif choice == '2':
            data = fetch_data()
            export_excel(data)
        elif choice == '3':
            break
        else:
            print("Invalid.")

if __name__ == "__main__":
    dashboard()"""

#This create tables code is for creating a SQLite database and an attendance table.
#It checks if the table already exists before creating it, and prints a success message.

"""
import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print("[INFO] Table created successfully.")


"""

#This is Train Model code for a face recognition attendance system.
#It trains a face recognizer using images from a dataset directory and saves the trained model and label mapping to files.

"""import os
import cv2
import numpy as np

dataset_path = "D:\\College work\\projectt\\face_data"
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
label_map = {}
current_label = 0

for person_name in os.listdir(dataset_path):
    person_dir = os.path.join(dataset_path, person_name)
    if not os.path.isdir(person_dir):
        continue

    label_map[current_label] = person_name

    for image_name in os.listdir(person_dir):
        image_path = os.path.join(person_dir, image_name)
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        faces.append(img)
        labels.append(current_label)

    current_label += 1

recognizer.train(faces, np.array(labels))
recognizer.save("trainer.yml")

# Save the label mapping
with open("label_map.txt", "w") as f:
    for label, name in label_map.items():
        f.write(f"{label}:{name}\n")

print("[INFO] Training complete.")"""
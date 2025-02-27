import tkinter as tk
from tkinter import ttk, messagebox
import speech_recognition as sr
import pyttsx3
import pandas as pd
from datetime import datetime
import os
import threading

class VoiceAttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice-Based Attendance System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Initialize speech recognition and text-to-speech
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Create attendance directory if not exists
        self.attendance_dir = "attendance_records"
        if not os.path.exists(self.attendance_dir):
            os.makedirs(self.attendance_dir)

        self.setup_gui()

    def setup_gui(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg="#2c3e50")
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame,
            text="Voice-Based Attendance System",
            font=("Helvetica", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)

        # Main Content Frame
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Status Display
        self.status_var = tk.StringVar()
        self.status_var.set("System Ready")
        status_label = tk.Label(
            content_frame,
            textvariable=self.status_var,
            font=("Helvetica", 12),
            bg="#f0f0f0"
        )
        status_label.pack(pady=10)

        # Buttons Frame
        button_frame = tk.Frame(content_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)

        # Start Recording Button
        self.record_button = ttk.Button(
            button_frame,
            text="Start Recording",
            command=self.start_recording,
            style="Custom.TButton"
        )
        self.record_button.pack(pady=10)

        # View Records Button
        view_button = ttk.Button(
            button_frame,
            text="View Records",
            command=self.view_records,
            style="Custom.TButton"
        )
        view_button.pack(pady=10)

        # Records Display
        self.records_text = tk.Text(
            content_frame,
            height=15,
            width=60,
            font=("Courier", 10),
            bg="white"
        )
        self.records_text.pack(pady=20)

        # Custom Style
        style = ttk.Style()
        style.configure(
            "Custom.TButton",
            padding=10,
            font=("Helvetica", 12)
        )

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def start_recording(self):
        self.status_var.set("Listening... Speak the names clearly")
        self.record_button.configure(state="disabled")
        
        # Start recording in a separate thread
        threading.Thread(target=self.record_attendance, daemon=True).start()

    def record_attendance(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5)
                
            text = self.recognizer.recognize_google(audio)
            names = [name.strip() for name in text.split("and")]
            
            # Record attendance
            timestamp = datetime.now()
            date_str = timestamp.strftime("%Y-%m-%d")
            time_str = timestamp.strftime("%H:%M:%S")
            
            # Create or append to CSV file
            filename = os.path.join(self.attendance_dir, f"attendance_{date_str}.csv")
            
            data = {
                'Name': names,
                'Time': [time_str] * len(names),
                'Date': [date_str] * len(names)
            }
            
            df = pd.DataFrame(data)
            if os.path.exists(filename):
                df.to_csv(filename, mode='a', header=False, index=False)
            else:
                df.to_csv(filename, index=False)
            
            self.status_var.set(f"Attendance recorded for {', '.join(names)}")
            self.speak("Attendance recorded successfully")
            self.view_records()  # Refresh the display
            
        except sr.UnknownValueError:
            self.status_var.set("Could not understand audio. Please try again.")
            self.speak("Could not understand audio. Please try again.")
        except sr.RequestError:
            self.status_var.set("Could not connect to the speech recognition service")
            self.speak("Service error. Please check your internet connection.")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.speak("An error occurred. Please try again.")
        
        finally:
            self.root.after(0, lambda: self.record_button.configure(state="normal"))

    def view_records(self):
        self.records_text.delete(1.0, tk.END)
        try:
            # Get today's date
            today = datetime.now().strftime("%Y-%m-%d")
            filename = os.path.join(self.attendance_dir, f"attendance_{today}.csv")
            
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                self.records_text.insert(tk.END, "Today's Attendance Records:\n")
                self.records_text.insert(tk.END, "=" * 50 + "\n")
                self.records_text.insert(tk.END, df.to_string())
            else:
                self.records_text.insert(tk.END, "No records found for today.")
        except Exception as e:
            self.records_text.insert(tk.END, f"Error reading records: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAttendanceSystem(root)
    root.mainloop()

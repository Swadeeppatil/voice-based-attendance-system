# Voice-Based Attendance System

A Python-based attendance system that uses voice recognition to record attendance with a modern Tkinter GUI interface.

## Features

- **Voice-Based Recognition**: Uses Google Speech Recognition API to take attendance via voice
- **Local Storage**: Saves attendance records as CSV files in a dedicated folder
- **Time and Date Stamp**: Automatically records the time and date of attendance
- **User-Friendly Interface**: Modern Tkinter GUI with intuitive controls
- **Audio Feedback**: Text-to-speech confirmations for better user experience
- **Daily Records View**: View and track attendance records for the current day

## Requirements

- Python 3.x
- Required packages are listed in `requirements.txt`

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python voice_attendance.py
```

## Usage

1. Click the "Start Recording" button to begin recording attendance
2. Speak the names clearly (use "and" to separate multiple names)
3. The system will automatically record the attendance with timestamp
4. View today's records using the "View Records" button

## Data Storage

Attendance records are stored in CSV format in the `attendance_records` folder, organized by date.

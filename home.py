import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, parent):
        self.parent = parent
        self.video_path = "Login.mp4"  # Update with your actual video path

        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Failed to open video file!")
            return

        self.video_label = tk.Label(parent)
        self.video_label.pack(fill="both", expand=True)

        self.running = True
        self.update_frame()

    def update_frame(self):
        if not self.running:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to read video frame!")
                self.cap.release()
                return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        self.video_label.after(20, self.update_frame)

    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

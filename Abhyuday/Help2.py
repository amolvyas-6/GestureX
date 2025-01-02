
import customtkinter as ctk
import tkinter as tk
from tkVideoPlayer import TkinterVideo
from tkinter import filedialog

# File locations (same structure as before)
VIDEOS = {
    "gesture": {
        "gesture1": r".\Abhyuday\Help\Gestures\1.mp4",
        "gesture2": r".\Abhyuday\Help\Gestures\2.mp4",
        "gesture3": r".\Abhyuday\Help\Gestures\3.mp4",
        "gesture4": r".\Abhyuday\Help\Gestures\4.mp4",
        "gesture5": r".\Abhyuday\Help\Gestures\5.mp4",
    },
    "brightness": r".\Abhyuday\Help\Brightness\1.mp4",
    "volume": r".\Abhyuday\Help\Audio\1.mp4",
    "cursor": r".\Abhyuday\Help\Cursor\1.mp4"
}

class VideoPlayer(ctk.CTkFrame):
    """Reusable Video Player Component"""

    def __init__(self, parent, video_file=None, width=800, height=450):
        super().__init__(parent)

        # Variables
        self.video_file = video_file
        self.vid_player = TkinterVideo(self, scaled=True, bg="black", width=width, height=height)

        # UI Components
        self.create_widgets()

        # If video file is provided, load it
        if self.video_file:
            self.load_video(self.video_file)

    def create_widgets(self):
        """Create video player controls"""
        self.vid_player.pack(expand=True, fill="both", pady=10)

        # Progress Slider
        self.progress_slider = ctk.CTkSlider(self, from_=-1, to=1, command=self.seek)
        self.progress_slider.pack(fill="x", padx=10, pady=10)

        # Play/Pause Button
        self.play_pause_button = ctk.CTkButton(self, text="Play ►", command=self.play_pause)
        self.play_pause_button.pack(pady=10)

        # Bind events
        self.vid_player.bind("<<Duration>>", self.update_duration)
        self.vid_player.bind("<<SecondChanged>>", self.update_progress)
        self.vid_player.bind("<<Ended>>", self.video_ended)

    def load_video(self, video_file):
        """Load video into the player"""
        try:
            self.video_file = video_file
            self.vid_player.load(video_file)
            self.play()
        except Exception as e:
            print(f"Error loading video: {e}")

    def play_pause(self):
        """Toggle play/pause state"""
        if self.vid_player.is_paused():
            self.play()
        else:
            self.pause()

    def play(self):
        """Play the video"""
        self.vid_player.play()
        self.play_pause_button.configure(text="Pause ||")

    def pause(self):
        """Pause the video"""
        self.vid_player.pause()
        self.play_pause_button.configure(text="Play ►")

    def seek(self, value):
        """Seek to a specific time"""
        if self.video_file:
            self.vid_player.seek(int(value))

    def update_duration(self, event):
        """Update the slider's duration"""
        try:
            duration = int(self.vid_player.video_info()["duration"])
            self.progress_slider.configure(from_=0, to=duration)
        except Exception as e:
            print(f"Error updating duration: {e}")

    def update_progress(self, event):
        """Update the slider's current position"""
        try:
            self.progress_slider.set(int(self.vid_player.current_duration()))
        except Exception as e:
            print(f"Error updating progress: {e}")

    def video_ended(self, event):
        """Reset play/pause button on video end"""
        self.play_pause_button.configure(text="Play ►")
        self.progress_slider.set(0)

class HelpWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Help")
        self.geometry("1200x800")

        self.seg_button = ctk.CTkSegmentedButton(
            self,
            values=["Gesture", "Brightness", "Volume", "Cursor"],
            command=self.segment_callback
        )
        self.seg_button.pack(pady=20)

        self.frames = {
            "Gesture": self.create_gesture_frame(),
            "Brightness": self.create_video_frame(VIDEOS["brightness"]),
            "Volume": self.create_video_frame(VIDEOS["volume"]),
            "Cursor": self.create_video_frame(VIDEOS["cursor"]),
        }

        # Initially display the "Gesture" frame
        self.segment_callback("Gesture")

    def create_gesture_frame(self):
        """Create the gesture frame with multiple videos"""
        container = ctk.CTkFrame(self)

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(container, bg="white")
        scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)

        # Configure the canvas
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add videos to the scrollable frame
        for i, (key, video_file) in enumerate(VIDEOS["gesture"].items()):
            video_player = VideoPlayer(scrollable_frame, video_file, width=800, height=450)
            video_player.pack(padx=10, pady=10, fill="x")

        container.pack(fill="both", expand=True, padx=10, pady=10)
        return container

    def create_video_frame(self, video_file):
        """Create a frame with a single video"""
        frame = VideoPlayer(self, video_file, width=800, height=450)
        return frame

    def segment_callback(self, value):
        """Switch between frames"""
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[value].pack(fill="both", expand=True, padx=20, pady=20)

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        help_button = ctk.CTkButton(self, text="HELP", command=self.open_help)
        help_button.pack(pady=20)

    def open_help(self):
        """Open the Help window"""
        HelpWindow()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

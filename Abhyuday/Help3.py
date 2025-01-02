import customtkinter as ctk
import tkinter as tk
from tkVideoPlayer import TkinterVideo
from tkinter import filedialog


# File locations (same structure as before)
VIDEOS = {
    "gesture": {
        "gesture1": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\1.mp4",
        "gesture2": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\2.mp4",
        "gesture3": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\3.mp4",
        "gesture4": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\4.mp4",
        "gesture5": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\5.mp4",
    },
    "brightness": r"D:\VS Code\GestureX\Abhyuday\Help\Brightness\1.mp4",
    "volume": r"D:\VS Code\GestureX\Abhyuday\Help\Audio\1.mp4",
    "cursor": r"D:\VS Code\GestureX\Abhyuday\Help\Cursor\1.mp4"
}


class VideoPlayer(ctk.CTkFrame):
    """Reusable Video Player Component"""

    def __init__(self, parent, video_file=None):
        super().__init__(parent)

        # Variables
        self.video_file = video_file
        self.vid_player = TkinterVideo(self, scaled=True, bg="black", width=800, height=600)  # Set desired size here

        # UI Components
        self.create_widgets()

        # If video file is provided, load it
        if self.video_file:
            self.load_video(self.video_file)

    def create_widgets(self):
        """Create video player controls"""
        self.vid_player.pack(expand=True, fill="both", pady=10)

        # Open Video Button
        self.open_button = ctk.CTkButton(self, text="Open Video", command=self.open_video)
        self.open_button.pack(pady=10)

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

    def open_video(self):
        """Open video file dialog and load video"""
        video_file = filedialog.askopenfilename(filetypes=[
            ('Video Files', ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.gif']),
            ('All Files', '*.*')
        ])
        if video_file:
            self.load_video(video_file)

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
        frame = ctk.CTkFrame(self)
        
        for i, (key, video_file) in enumerate(VIDEOS["gesture"].items()):
            video_player = VideoPlayer(frame, video_file)
            video_player.grid(row=i // 2, column=i % 2, padx=10, pady=10)
        
        return frame

    def create_video_frame(self, video_file):
        """Create a frame with a single video"""
        
        frame = VideoPlayer(self, video_file)
        
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

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
from PIL import Image, ImageTk

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
    "cursor": r"D:\VS Code\GestureX\Abhyuday\Help\Cursor\1.mp4",
}

# Generate all 26 letters for ASL
SIGN_LANGUAGE_IMAGES = [
    {"path": fr"D:\VS Code\GestureX\Abhyuday\Help\ASL\{chr(65+i)}.jpg", "label": f"Sign {chr(65+i)}"}
    for i in range(26)
]

# Mode images with their labels
MODE_IMAGES = [
    {"path": r"D:\VS Code\GestureX\Abhyuday\Help\Modes\1.jpg", "label": "Gesture"},
    {"path": r"D:\VS Code\GestureX\Abhyuday\Help\Modes\2.jpg", "label": "Brightness"},
    {"path": r"D:\VS Code\GestureX\Abhyuday\Help\Modes\3.jpg", "label": "Volume"},
    {"path": r"D:\VS Code\GestureX\Abhyuday\Help\Modes\4.jpg", "label": "Cursor"},
    {"path": r"D:\VS Code\GestureX\Abhyuday\Help\Modes\5.jpg", "label": "Sign Language"},
]

class VideoPlayer(ctk.CTkFrame):
    def __init__(self, parent, video_file=None):
        super().__init__(parent)
        
        self.video_file = video_file
        if self.video_file:
            try:
                self.vid_player = TkinterVideo(self, scaled=True)
                self.vid_player.load(video_file)
                self.vid_player.pack(expand=True, fill="both", pady=10)
                
                controls_frame = ctk.CTkFrame(self)
                controls_frame.pack(fill="x", padx=10)
                
                self.play_pause_button = ctk.CTkButton(
                    controls_frame, 
                    text="Play", 
                    command=self.play_pause,
                    width=80
                )
                self.play_pause_button.pack(pady=5)
                
                self.vid_player.play()
                
            except Exception as e:
                error_label = ctk.CTkLabel(self, text=f"Error loading video:\n{str(e)}")
                error_label.pack(pady=10)
                print(f"Error loading video {video_file}: {e}")

    def play_pause(self):
        if self.vid_player.is_paused():
            self.vid_player.play()
            self.play_pause_button.configure(text="Pause")
        else:
            self.vid_player.pause()
            self.play_pause_button.configure(text="Play")

class HelpWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Help")
        self.geometry("1200x800")
        
        # Create main container with two columns
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left column for Modes
        self.left_column = ctk.CTkFrame(self.main_container)
        self.left_column.pack(side="left", fill="y", padx=(0, 10))
        
        # Right column for content
        self.right_column = ctk.CTkFrame(self.main_container)
        self.right_column.pack(side="left", fill="both", expand=True)
        
        # Modes section
        modes_label = ctk.CTkLabel(self.left_column, text="Modes:", font=("Arial", 16, "bold"))
        modes_label.pack(pady=(0, 10))
        
        # Create scrollable frame for modes
        self.modes_frame = ctk.CTkScrollableFrame(self.left_column, width=200)
        self.modes_frame.pack(fill="both", expand=True)
        
        # Add mode images with labels
        for img_data in MODE_IMAGES:
            try:
                img = Image.open(img_data["path"])
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                container = ctk.CTkFrame(self.modes_frame)
                container.pack(pady=10, padx=5)
                
                img_label = ctk.CTkLabel(container, image=photo, text="")
                img_label.image = photo
                img_label.pack()
                
                text_label = ctk.CTkLabel(container, text=img_data["label"])
                text_label.pack(pady=5)
                
            except Exception as e:
                print(f"Error loading mode image {img_data['path']}: {e}")
        
        # Content section in right column
        self.seg_button = ctk.CTkSegmentedButton(
            self.right_column,
            values=["Gesture", "Brightness", "Volume", "Cursor", "Sign Language"],
            command=self.segment_callback
        )
        self.seg_button.pack(pady=10)
        
        # Frame to hold the changing content
        self.changing_frame = ctk.CTkFrame(self.right_column)
        self.changing_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialize frames
        self.frames = {}
        self.create_frames()
        
        # Show initial frame
        self.segment_callback("Gesture")

    def create_frames(self):
        # Gesture frame
        gesture_frame = ctk.CTkFrame(self.changing_frame)
        for i, (key, video_file) in enumerate(VIDEOS["gesture"].items()):
            video_player = VideoPlayer(gesture_frame, video_file)
            video_player.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
        self.frames["Gesture"] = gesture_frame
        
        # Other video frames
        self.frames["Brightness"] = VideoPlayer(self.changing_frame, VIDEOS["brightness"])
        self.frames["Volume"] = VideoPlayer(self.changing_frame, VIDEOS["volume"])
        self.frames["Cursor"] = VideoPlayer(self.changing_frame, VIDEOS["cursor"])
        
        # Sign Language frame
        sign_frame = ctk.CTkScrollableFrame(self.changing_frame)
        for i, img_data in enumerate(SIGN_LANGUAGE_IMAGES):
            try:
                img = Image.open(img_data["path"])
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Container frame for each sign
                sign_container = ctk.CTkFrame(sign_frame)
                sign_container.grid(row=i//4, column=i%4, padx=10, pady=10, sticky="ew")
                
                label_img = ctk.CTkLabel(sign_container, image=photo, text="")
                label_img.image = photo
                label_img.grid(row=0, column=0, padx=10, pady=10)
                
                label_text = ctk.CTkLabel(sign_container, text=img_data["label"])
                label_text.grid(row=1, column=0, padx=10, pady=(0, 10))
                
            except Exception as e:
                print(f"Error loading image {img_data['path']}: {e}")
                
        self.frames["Sign Language"] = sign_frame

    def segment_callback(self, value):
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()
        
        # Show selected frame
        if value in self.frames:
            self.frames[value].pack(fill="both", expand=True)

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        self.geometry("200x100")
        
        help_button = ctk.CTkButton(self, text="HELP", command=self.open_help)
        help_button.pack(expand=True, pady=20)

    def open_help(self):
        help_window = HelpWindow()
        help_window.focus_force()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
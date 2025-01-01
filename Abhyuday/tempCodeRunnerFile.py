import customtkinter as ctk
import tkinter as tk
from tkVideoPlayer import TkinterVideo
from PIL import Image
from tkinter import filedialog

# File locations (same as before)
VIDEOS = {
    "gesture": {
        "gesture1": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\1.mp4",
        "gesture2": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\2.mp4",
        "gesture3": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\3.mp4",
        "gesture4": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\4.mp4",
        "gesture5": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\5.mp4",
        "gesture6": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\6.mp4",
        "gesture7": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\7.mp4",
        "gesture8": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\8.mp4",
        "gesture9": r"D:\VS Code\GestureX\Abhyuday\Help\Gestures\9.mp4"
    },
    "brightness": r"D:\VS Code\GestureX\Abhyuday\Help\Brightness\1.mp4",
    "volume": r"D:\VS Code\GestureX\Abhyuday\Help\Audio\1.mp4",
    "cursor": r"D:\VS Code\GestureX\Abhyuday\Help\Cursor\1.mp4"
}

IMAGES = {
    "sign_language": [
        r"D:\VS Code\GestureX\Abhyuday\Help\ASL\A.jpg",
        r"D:\VS Code\GestureX\Abhyuday\Help\ASL\B.jpg",
        r"D:\VS Code\GestureX\Abhyuday\Help\ASL\C.jpg",
        r"D:\VS Code\GestureX\Abhyuday\Help\ASL\D.jpg",
        r"D:\VS Code\GestureX\Abhyuday\Help\ASL\E.jpg",
        r"D:\VS Code\GestureX\Abhyuday\Help\ASL\F.jpg",
        r"D:\VS Code\GestureX\Abhyuday\Help\ASL\G.jpg",
        r"D:\VS Code\GestureX\Abhyuday\Help\ASL\H.jpg",
        r"D:\VS Code\GestureX\Abhyuday\Help\ASL\I.jpg",
        r"D:\VS Code\GestureX\Abhyuday\Help\ASL\J.jpg"
    ],
    "modes": [
        r"D:\VS Code\GestureX\Abhyuday\Help\Modes\1.jpg",
        r"D:\VS Code\GestureX\Abhyuday\Help\Modes\2.jpg",
        r"D:\VS Code\GestureX\Abhyuday\Help\Modes\3.jpg",
        r"D:\VS Code\GestureX\Abhyuday\Help\Modes\4.jpg",
        r"D:\VS Code\GestureX\Abhyuday\Help\Modes\5.jpg"
    ]
}

TEXTS = {
    "gesture": [f"Gesture {i+1} Description" for i in range(9)],
    "brightness": "Brightness Control Instructions",
    "volume": "Volume Control Instructions",
    "cursor": "Cursor Control Instructions",
    "modes": [f"Mode {i+1} Description" for i in range(5)]
}


class HelpWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Help")
        self.geometry("1200x800")

        self.seg_button = ctk.CTkSegmentedButton(
            self,
            values=["Gesture", "Brightness", "Volume", "Cursor", "Sign Language", "Modes", "Custom Video"],
            command=self.segment_callback
        )
        self.seg_button.pack(pady=20)

        self.frames = {
            "Gesture": self.create_gesture_frame(),
            "Brightness": self.create_single_video_frame("brightness"),
            "Volume": self.create_single_video_frame("volume"),
            "Cursor": self.create_single_video_frame("cursor"),
            "Sign Language": self.create_sign_language_frame(),
            "Modes": self.create_modes_frame(),
            "Custom Video": self.create_custom_video_frame()
        }

        # Initially display the "Gesture" frame
        self.segment_callback("Gesture")

    def create_gesture_frame(self):
        frame = ctk.CTkFrame(self)
        for i in range(3):
            for j in range(3):
                idx = i * 3 + j
                if idx >= len(VIDEOS["gesture"]):
                    break

                cell_frame = ctk.CTkFrame(frame)
                cell_frame.grid(row=i, column=j, padx=10, pady=10)

                try:
                    video_player = TkinterVideo(master=cell_frame, scaled=True)
                    video_player.load(VIDEOS["gesture"][f"gesture{idx+1}"])
                    video_player.pack(expand=True)
                    video_player.play()

                    label = ctk.CTkLabel(cell_frame, text=TEXTS["gesture"][idx])
                    label.pack()
                except FileNotFoundError:
                    label = ctk.CTkLabel(cell_frame, text=f"Gesture {idx+1} (Video Missing)")
                    label.pack()
        return frame

    def create_single_video_frame(self, section):
        frame = ctk.CTkFrame(self)
        try:
            video_player = TkinterVideo(master=frame, scaled=True)
            video_player.load(VIDEOS[section])
            video_player.pack(expand=True, pady=20)
            video_player.play()

            label = ctk.CTkLabel(frame, text=TEXTS[section])
            label.pack(pady=10)
        except FileNotFoundError:
            label = ctk.CTkLabel(frame, text=f"{section.capitalize()} Video Missing")
            label.pack(pady=20)
        return frame

    def create_sign_language_frame(self):
        frame = ctk.CTkFrame(self)
        for i, img_path in enumerate(IMAGES["sign_language"]):
            try:
                img = ctk.CTkImage(light_image=Image.open(img_path), size=(300, 300))
                label = ctk.CTkLabel(frame, image=img, text="")
                label.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            except FileNotFoundError:
                label = ctk.CTkLabel(frame, text=f"Sign Language {chr(65 + i)} Missing")
                label.grid(row=i // 2, column=i % 2, padx=10, pady=10)
        return frame

    def create_modes_frame(self):
        frame = ctk.CTkFrame(self)
        canvas = tk.Canvas(frame)
        scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
        content_frame = ctk.CTkFrame(canvas)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        for i, img_path in enumerate(IMAGES["modes"]):
            try:
                img = ctk.CTkImage(light_image=Image.open(img_path), size=(200, 200))
                label = ctk.CTkLabel(content_frame, image=img, text=TEXTS["modes"][i])
                label.pack(pady=10)
            except FileNotFoundError:
                label = ctk.CTkLabel(content_frame, text=f"Mode {i+1} Image Missing")
                label.pack(pady=10)
        return frame

    def create_custom_video_frame(self):
        frame = ctk.CTkFrame(self)
        vid_player = TkinterVideo(master=frame, scaled=True, bg="black")
        vid_player.pack(expand=True, fill="both", pady=10)
        vid_player.bind("<<Ended>>", lambda e: play_pause_btn.configure(text="Play ►"))

        def open_video():
            video_file = filedialog.askopenfilename(filetypes=[
                ('Video Files', ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.gif']),
                ('All Files', '*.*')
            ])
            if video_file:
                vid_player.load(video_file)
                vid_player.play()

        def play_pause():
            if vid_player.is_paused():
                vid_player.play()
            else:
                vid_player.pause()

        open_button = ctk.CTkButton(frame, text="Open Video", command=open_video)
        open_button.pack(pady=10)
        play_pause_btn = ctk.CTkButton(frame, text="Play ►", command=play_pause)
        play_pause_btn.pack(pady=10)

        return frame

    def segment_callback(self, value):
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
        help_window = HelpWindow()
        help_window.focus()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

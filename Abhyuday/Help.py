import customtkinter as ctk
import tkinter as tk
from tkVideoPlayer import TkinterVideo
from PIL import Image

class HelpWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Help")
        self.geometry("1200x800")
        
        self.seg_button = ctk.CTkSegmentedButton(
            self,
            values=["Gesture", "Brightness", "Volume", "Cursor", "Sign Language", "Modes"],
            command=self.segment_callback
        )
        self.seg_button.pack(pady=20)
        
        self.frames = {
            "Gesture": self.create_gesture_frame(),
            "Brightness": self.create_single_video_frame("brightness"),
            "Volume": self.create_single_video_frame("volume"),
            "Cursor": self.create_single_video_frame("cursor"),
            "Sign Language": self.create_sign_language_frame(),
            "Modes": self.create_modes_frame()
        }

    def create_gesture_frame(self):
        frame = ctk.CTkFrame(self)
        gesture_videos = [f"path/to/gesture{i+1}.mp4" for i in range(9)]
        gesture_texts = [f"Gesture {i+1} Description" for i in range(9)]
        
        for i in range(3):
            for j in range(3):
                idx = i*3 + j
                cell_frame = ctk.CTkFrame(frame)
                cell_frame.grid(row=i, column=j, padx=10, pady=10)
                
                video_player = TkinterVideo(master=cell_frame, scaled=True)
                video_player.load(gesture_videos[idx])
                video_player.pack(expand=True)
                video_player.play()
                
                label = ctk.CTkLabel(cell_frame, text=gesture_texts[idx])
                label.pack()
        
        return frame

    def create_single_video_frame(self, section):
        frame = ctk.CTkFrame(self)
        
        video_player = TkinterVideo(master=frame, scaled=True)
        video_player.load(f"path/to/{section}_video.mp4")
        video_player.pack(expand=True, pady=20)
        video_player.play()
        
        label = ctk.CTkLabel(frame, text=f"{section.title()} Instructions")
        label.pack(pady=10)
        
        return frame

    def create_sign_language_frame(self):
        main_frame = ctk.CTkFrame(self)
        canvas = tk.Canvas(main_frame)
        scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
        content_frame = ctk.CTkFrame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_frame = canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        sign_images = [f"path/to/sign{i+1}.png" for i in range(10)]
        
        for i, img_path in enumerate(sign_images):
            try:
                img = ctk.CTkImage(light_image=Image.open(img_path), size=(300, 300))
                label = ctk.CTkLabel(content_frame, image=img, text="")
                label.grid(row=i//2, column=i%2, padx=10, pady=10)
            except FileNotFoundError:
                pass
        
        return main_frame

    def create_modes_frame(self):
        frame = ctk.CTkFrame(self)
        mode_images = [f"path/to/mode{i+1}.png" for i in range(5)]
        mode_texts = [f"Mode {i+1} Description" for i in range(5)]
        
        for i in range(5):
            try:
                img = ctk.CTkImage(light_image=Image.open(mode_images[i]), size=(200, 200))
                image_label = ctk.CTkLabel(frame, image=img, text="")
                image_label.pack(pady=10)
                
                text_label = ctk.CTkLabel(frame, text=mode_texts[i])
                text_label.pack(pady=(0, 20))
            except FileNotFoundError:
                pass
        
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
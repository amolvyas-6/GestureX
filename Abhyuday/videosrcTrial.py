import tkinter
import customtkinter
from tkVideoPlayer import TkinterVideo

def create_video_grid(video_files):
    # Create a new window to display the video grid
    new_window = customtkinter.CTkToplevel(app)
    new_window.geometry("800x600")
    new_window.title("Videos Grid")

    # Create a grid layout with 2 columns and 1 row for 2 videos
    for i, video_file in enumerate(video_files):
        row = i // 2
        column = i % 2

        section_frame = customtkinter.CTkFrame(new_window, corner_radius=10)
        section_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        label = customtkinter.CTkLabel(section_frame, text=f"Label {i+1}", anchor="w")
        label.pack(side="left", padx=10)

        # Create a video player for each video file
        video_player = TkinterVideo(master=section_frame, scaled=True, keep_aspect=True, consistant_frame_rate=True, bg="black")
        video_player.set_resampling_method(1)
        video_player.load(video_file)
        video_player.pack(side="right", expand=True, fill="both")

        # Play/Pause button for each video
        play_pause_btn = customtkinter.CTkButton(section_frame, text="Play ►", command=lambda vp=video_player: toggle_play_pause(vp))
        play_pause_btn.pack(side="bottom", pady=5)

    new_window.mainloop()

def toggle_play_pause(video_player):
    # Toggle play/pause state for each video
    if video_player.is_paused():
        video_player.play()
    else:
        video_player.pause()

# Set appearance mode
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Main window setup
app = customtkinter.CTk()
app.geometry("600x500")
app.title("CustomTkinter x TkVideoPlayer.py")

# Define the video file paths (2 videos as an example)
video_files = [
    '"D:\VS Code\In meeting · Meeting · Webex - Google Chrome 2024-12-11 19-10-19.mp4',  # Replace with the actual path to your first video
    ':\VS Code\WhatsApp Video 2024-12-24 at 16.49.33_7da3175a.mp4',  # Replace with the actual path to your second video
]

# Create video grid when the application starts
create_video_grid(video_files)

# Run the main loop
app.mainloop()

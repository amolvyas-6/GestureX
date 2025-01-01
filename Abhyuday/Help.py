import customtkinter as ctk

class HelpWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Help")
        self.geometry("800x600")
        
        # Create segmented button
        self.seg_button = ctk.CTkSegmentedButton(
            self,
            values=["Gesture", "Brightness", "Volume", "Cursor", "Sign Language"],
            command=self.segment_callback
        )
        self.seg_button.pack(pady=20)
        
        # Create frames for each section
        self.frames = {
            "Gesture": ctk.CTkFrame(self),
            "Brightness": ctk.CTkFrame(self),
            "Volume": ctk.CTkFrame(self),
            "Cursor": ctk.CTkFrame(self),
            "Sign Language": ctk.CTkFrame(self)
        }
        
    def segment_callback(self, value):
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()
        
        # Show selected frame
        self.frames[value].pack(fill="both", expand=True, padx=20, pady=20)

# Main window with help button
class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        
        help_button = ctk.CTkButton(
            self, 
            text="HELP",
            command=self.open_help
        )
        help_button.pack(pady=20)
        
    def open_help(self):
        help_window = HelpWindow()
        help_window.focus()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
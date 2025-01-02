from tkinter import *
import customtkinter
from Help2 import HelpWindow

#CTK windows formatting

#colour theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

#to create app instance
root = customtkinter.CTk()

root.title("Hand Recognition System for the future")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", root)

window_width = 1000
window_height = 700# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position to center the window
x_pos = int((screen_width - window_width) / 1.5)
y_pos = int((screen_height - window_height) / 2)

# Set window size and position (centered)
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

#end of CTK window formatting

def open_help():
    HelpWindow()

#creating help button
help_but = customtkinter.CTkButton(root, text='Help',
                         fg_color='grey', text_color='black', height=35,
                         width=100, font=('Segoe UI', 20),
                         hover_color='light blue', corner_radius=10000, border_width=1, command=open_help)
help_but.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)  # Move to top-right corner

#end of help button


#making of ASl help button

# Asl_help = customtkinter.CTkButton(root, text="ASL Help",
#                                    fg_color='grey', text_color='black', height=36,
#                          width=100, font=('Segoe UI', 20),
#                          hover_color='light blue', corner_radius=10000, border_width=1)
# Asl_help.place(relx=0.0, rely=0.0, anchor="nw", x=20, y=20) 

#making Intro page
greeting = ""
def clear_all():
    global greeting
    my_entry.delete(0, END)
    submit_button.pack_forget()
    my_entry.pack_forget()
    my_label = customtkinter.CTkLabel(root, text = f"Hello, {greeting},Welcome to the future of input peripherals!\n Please Map your Action with your choice of gestures.\n Hint: Don't assign them same gestures :) ", font = ("helevetice", 18, 'italic'))
    my_label.pack(pady = 20)
    my_progressbar.set(my_progressbar.get() + 0.125)
    progress_label.configure(text = f'Progress: {my_progressbar.get()*100}%')

def show_submit_button(event = None):
    global greeting
    if my_entry.get():
        greeting = my_entry.get()
        submit_button.pack(pady = 20)
    else:
        submit_button.pack_forget()


my_entry = customtkinter.CTkEntry(root, placeholder_text= "Enter your name",
height= 50, width= 200,
font = ("Helvetica", 18),
text_color= 'dark green',
corner_radius= 500,
fg_color=('dark blue', 'light blue'))
my_entry.pack(pady = 20)
my_entry.bind("<KeyRelease>", show_submit_button)

submit_button = customtkinter.CTkButton(root, text = 'Continue', command = clear_all, 
corner_radius= 5000)

#end of intro page

#list keeping current options taken
lst = []

def listing(menu, labeling):
    selected = menu.get()
    if(selected in lst):
        labeling.configure(text = "Same gestures not allowed for multiple actions")
    else:
        lst.append(selected)
        labeling.configure(text = 'Allowed')
        my_progressbar.set(my_progressbar.get()+0.125)
        progress_label.configure(text = f'Progress: {my_progressbar.get()*100}%')
    if(len(lst) == 7):
        Submit.place(relx=0.5, rely=0.9, anchor="center")

#main page
#gestures to select from
gestures = ['Three Finger Swipe Up',
'Two Finger Swipe Down',
'Three Finger Swipe Left',
'Three Finger Swipe Right',
'Make Fist',
'Hand Swipe',
'One Finger Down']

scrollable_frame = customtkinter.CTkScrollableFrame(root, width=500, height= 350)
scrollable_frame.pack(pady=20, padx=20)  # Use pack to make it scrollable


# Use grid to place them side by side within the frame
option1_label = customtkinter.CTkLabel(scrollable_frame, text="Choose: ")
options1 = customtkinter.CTkOptionMenu(scrollable_frame, values=gestures, command=lambda value: listing(options1, option1_label))
option1_status_label = customtkinter.CTkLabel(scrollable_frame, text = "To Display all apps")
options1.set("Please Select your gesture!")
option1_label.grid(row=0, column=0, padx=(10, 5), pady=10)
options1.grid(row=0, column=1, padx=(5, 10), pady=10)
option1_status_label.grid(row=0, column=2, padx=(5, 10), pady=10)

# Option 2
option2_label = customtkinter.CTkLabel(scrollable_frame, text="Choose: ")
options2 = customtkinter.CTkOptionMenu(scrollable_frame, values=gestures, command=lambda value: listing(options2, option2_label))
option2_status_label = customtkinter.CTkLabel(scrollable_frame, text = "To minimise all apps")
options2.set("Please Select your gesture!")
option2_label.grid(row=1, column=0, padx=(10, 5), pady=10)
options2.grid(row=1, column=1, padx=(5, 10), pady=10)
option2_status_label.grid(row=1, column=2, padx=(5, 10), pady=10)


# Option 3
option3_label = customtkinter.CTkLabel(scrollable_frame, text="Choose: ")
options3 = customtkinter.CTkOptionMenu(scrollable_frame, values=gestures, command=lambda value: listing(options3, option3_label))
option3_status_label = customtkinter.CTkLabel(scrollable_frame, text = "Left Arrow Key")
options3.set("Please Select your gesture!")
option3_label.grid(row=2, column=0, padx=(10, 5), pady=10)
options3.grid(row=2, column=1, padx=(5, 10), pady=10)
option3_status_label.grid(row=2, column=2, padx=(5, 10), pady=10)

# Option 4
option4_label = customtkinter.CTkLabel(scrollable_frame, text="Choose: ")
options4 = customtkinter.CTkOptionMenu(scrollable_frame, values=gestures, command=lambda value: listing(options4, option4_label))
option4_status_label = customtkinter.CTkLabel(scrollable_frame, text = "Right Arrow Key")
options4.set("Please Select your gesture!")
option4_label.grid(row=3, column=0, padx=(10, 5), pady=10)
options4.grid(row=3, column=1, padx=(5, 10), pady=10)
option4_status_label.grid(row=3, column=2, padx=(5, 10), pady=10)

# Option 5
option5_label = customtkinter.CTkLabel(scrollable_frame, text="Choose: ")
options5 = customtkinter.CTkOptionMenu(scrollable_frame, values=gestures, command=lambda value: listing(options5, option5_label))
option5_status_label = customtkinter.CTkLabel(scrollable_frame, text = "Play/Pause")
options5.set("Please Select your gesture!")
option5_label.grid(row=4, column=0, padx=(10, 5), pady=10)
options5.grid(row=4, column=1, padx=(5, 10), pady=10)
option5_status_label.grid(row=4, column=2, padx=(5, 10), pady=10)

# Option 6
option6_label = customtkinter.CTkLabel(scrollable_frame, text="Choose: ")
options6 = customtkinter.CTkOptionMenu(scrollable_frame, values=gestures, command=lambda value: listing(options6, option6_label))
option6_status_label = customtkinter.CTkLabel(scrollable_frame, text = "Switch App")
options6.set("Please Select your gesture!")
option6_label.grid(row=5, column=0, padx=(10, 5), pady=10)
options6.grid(row=5, column=1, padx=(5, 10), pady=10)
option6_status_label.grid(row=5, column=2, padx=(5, 10), pady=10)

option7_label = customtkinter.CTkLabel(scrollable_frame, text="Choose: ")
options7 = customtkinter.CTkOptionMenu(scrollable_frame, values=gestures, command=lambda value: listing(options7, option7_label))
option7_status_label = customtkinter.CTkLabel(scrollable_frame, text = "Press enter key")
options7.set("Please Select your gesture!")
option7_label.grid(row=6, column=0, padx=(10, 5), pady=10)
options7.grid(row=6, column=1, padx=(5, 10), pady=10)
option7_status_label.grid(row=6, column=2, padx=(5, 10), pady=10)



#starting the progress bar

frame = customtkinter.CTkFrame(root)
frame.pack(pady = 5, padx = 20, fill = 'x')
my_progressbar = customtkinter.CTkProgressBar(frame,
    corner_radius= 3,
    width = 500,
    height= 10,
    fg_color= 'grey', 
    progress_color = 'cyan',
    )
my_progressbar.grid(row=0, column=0, padx=(10, 5))
my_progressbar.set(0)
progress_label = customtkinter.CTkLabel(frame, text="Progress: 0%")
progress_label.grid(row=0, column=1, padx=(5, 10))

mode = 'dark'
#theme change
def theme():
    global mode
    if mode == 'dark':
        customtkinter.set_appearance_mode("light")
        mode = 'light'
    else:
        customtkinter.set_appearance_mode("dark")
        mode = 'dark'

theme_change = customtkinter.CTkButton(root, text = "Light/Dark Mode", command = theme)
theme_change.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20) 


#Submit button that actually maps keys to ML
dict = {}
def submit():
    dict[options1.get()] = 'Display All Apps'
    dict[options2.get()] = 'Minimize All Apps'
    dict[options3.get()] = 'Left Arrow Key'
    dict[options4.get()] = 'Right Arrow Key'
    dict[options5.get()] = 'Play/Pause' 
    dict[options6.get()] = 'Switch App'
    dict[options7.get()] = 'Press enter key'
    root.destroy()
    #import mainProg

Submit = customtkinter.CTkButton(root, text = "Submit", command = submit)
Submit.place(relx=0.5, rely=0.9, anchor="center")
Submit.place_forget()

def Default():
    global lst
    lst = []
    my_progressbar.set(1)
    progress_label.configure(text = f'Progress: {my_progressbar.get()*100}%')
    Submit.place_forget()
    options1.set('Three Finger Swipe Up')
    options2.set('Two Finger Swipe Down')
    options3.set('Three Finger Swipe Left')
    options4.set('Three Finger Swipe Right')
    options5.set('Make Fist')  
    options6.set('Hand Swipe')
    options7.set('One Finger Down')
    option1_label.configure(text = "Default")
    option2_label.configure(text = "Default")
    option3_label.configure(text = "Default")
    option4_label.configure(text = "Default")
    option5_label.configure(text = "Default")
    option6_label.configure(text = "Default")
    option7_label.configure(text = "Default")
    Submit.place(relx=0.5, rely=0.9, anchor="center")

default = customtkinter.CTkButton(root, text = "Default", command = Default)
default.place(relx=0.0, rely=1.0, anchor="sw", x=20, y=-20)

def clear_all():
    global dict
    dict = {}
    global lst
    lst = []
    my_progressbar.set(0.125)
    progress_label.configure(text = f'Progress: {my_progressbar.get()*100}%')
    Submit.place_forget()
    options1.set('Please Select your gesture!')
    options2.set('Please Select your gesture!')
    options3.set('Please Select your gesture!')
    options4.set('Please Select your gesture!')
    options5.set('Please Select your gesture!')
    options7.set('Please Select your gesture!')
    options6.set('Please Select your gesture!')
    option1_label.configure(text = "Choose:")
    option2_label.configure(text = "Choose:")
    option3_label.configure(text = "Choose:")
    option4_label.configure(text = "Choose:")
    option5_label.configure(text = "Choose:")
    option6_label.configure(text = "Choose:")
    option7_label.configure(text = "Choose:")

Clear = customtkinter.CTkButton(root, text = "Clear", command = clear_all)
Clear.place(relx=0.0, rely=1.0, anchor="sw", x=20, y=-60)
root.mainloop()
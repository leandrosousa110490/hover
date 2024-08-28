import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Initialize the main window without the title bar and set always on top
root = ttk.Window(themename="darkly")
root.title("Hover Notepad Example")
root.geometry("300x200+50+50")  # Set initial window size and position
root.overrideredirect(True)  # Remove the window title bar
root.attributes("-topmost", True)  # Keep the window always on top

# Set a minimum window size to ensure the buttons are always visible
min_width = 300
min_height = 200

# Variables to store the last position of the mouse
last_x, last_y = None, None
resizing = False  # To track resizing
locked = True  # Window starts in a locked state

# Function to start dragging the window (only if unlocked)
def start_drag(event):
    global last_x, last_y
    if not locked:
        last_x, last_y = event.x_root, event.y_root

# Function to drag the window (only if unlocked)
def on_drag(event):
    global last_x, last_y
    if not locked and last_x is not None and last_y is not None:
        dx = event.x_root - last_x
        dy = event.y_root - last_y
        x = root.winfo_x() + dx
        y = root.winfo_y() + dy
        root.geometry(f"+{x}+{y}")
        last_x, last_y = event.x_root, event.y_root

# Function to stop dragging the window
def stop_drag(event):
    global last_x, last_y
    last_x, last_y = None, None

# Function to close the entire application (only if unlocked)
def close_application(event=None):
    if not locked:
        root.destroy()  # Close the application

# Function to start resizing the window (only if unlocked)
def start_resize(event):
    global last_x, last_y, resizing
    if not locked:
        resizing = True
        last_x, last_y = event.x_root, event.y_root

# Function to resize the window with minimum size constraints (only if unlocked)
def on_resize(event):
    global last_x, last_y, resizing
    if not locked and resizing:
        dx = event.x_root - last_x
        dy = event.y_root - last_y
        new_width = root.winfo_width() + dx
        new_height = root.winfo_height() + dy

        # Enforce minimum size
        if new_width < min_width:
            new_width = min_width
        if new_height < min_height:
            new_height = min_height

        root.geometry(f"{new_width}x{new_height}")
        last_x, last_y = event.x_root, event.y_root

# Function to stop resizing the window
def stop_resize(event):
    global resizing
    resizing = False

# Function to toggle the lock state when Ctrl+Space is pressed
def toggle_lock(event=None):
    global locked
    locked = not locked  # Toggle the locked state
    if locked:
        header.pack_forget()  # Hide header (buttons) when locked
    else:
        header.pack(side="bottom", fill=X)  # Show header (buttons) when unlocked

# Create the header frame with buttons at the bottom
header_visible = True  # Make header visible by default
header = ttk.Frame(root, bootstyle="secondary")
header.pack_forget()  # Initially, hide the buttons since it's locked

# Add buttons to the header
drag_button = ttk.Button(header, text="Drag", bootstyle="secondary")
drag_button.pack(side=LEFT, padx=5)
resize_button = ttk.Button(header, text="Resize", bootstyle="secondary")
resize_button.pack(side=LEFT, padx=5)
close_button = ttk.Button(header, text="Close", command=close_application, bootstyle="danger")
close_button.pack(side=LEFT, padx=5)

# Bind events for dragging and resizing
drag_button.bind("<ButtonPress-1>", start_drag)
drag_button.bind("<B1-Motion>", on_drag)
drag_button.bind("<ButtonRelease-1>", stop_drag)

resize_button.bind("<ButtonPress-1>", start_resize)
resize_button.bind("<B1-Motion>", on_resize)
resize_button.bind("<ButtonRelease-1>", stop_resize)

# Create a frame for the Text widget and Scrollbar
text_frame = ttk.Frame(root)
text_frame.pack(fill=BOTH, expand=True)

# Create the scrollbar
scrollbar = ttk.Scrollbar(text_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

# Create the notepad (Text widget) that is always visible, above the buttons
notepad = tk.Text(text_frame, height=10, width=30, yscrollcommand=scrollbar.set)
notepad.pack(side="left", fill=BOTH, expand=True)

# Configure the scrollbar to work with the Text widget
scrollbar.config(command=notepad.yview)

# Bind the keyboard shortcut Ctrl+Space to toggle lock/unlock state
root.bind("<Control-space>", toggle_lock)

# Set the minimum size of the window after it's fully loaded
root.update_idletasks()
root.minsize(min_width, min_height)

# Run the application
root.mainloop()

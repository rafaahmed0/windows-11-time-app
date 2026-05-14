# A basic system tray clock app for Windows

# Imports
# Creates and manages the system tray icon
import pystray

# Handles UI logic
import timeDisplay

# Allows the tray icon to run in a separate thread than the time display
import threading

# For accessing assets
from pathlib import Path

# Loads the tray icon
from PIL import Image

from pystray import Menu as menu, MenuItem as item

BASE_DIR = Path(__file__).resolve().parent.parent
ICON_PATH = BASE_DIR / "assets" / "clockIcon.ico"

# Tray menu callback functions
# Function to detect when the tray icon is left-clicked, so the checked state and clock window visibility changes
def on_clicked(icon):
    icon.checked = not icon.checked
    timeDisplay.app.toggleWindow()

# Function to switch between the 12-hr and 24-hr format
def toggle_format():
    timeDisplay.app.toggleFormat()

# Functiont to terminate the application
def quit_app(icon):
    icon.stop()
    timeDisplay.app.shutdown()

# Creates an instance of the tray icon
icon = pystray.Icon(
    "clockIcon",
    icon=Image.open(ICON_PATH),
    title="Current Time"
)

# Attaches the checked state to the icon
icon.checked = False

# Builds the context menu of the icon
icon.menu = menu(
    item(
        "Left-Click-Action",
        on_clicked,
        # Runs on left click
        default=True,
        # hides the text
        visible=False 
    ),

    item(
        "24-hr clock",
        # Changes the format of the clock
        toggle_format,
        # The '24-hr clock' menu item being checked directly corresponds to the 24-hr format being utilized
        checked=lambda item: timeDisplay.app.use24h
    ),

    item(
        "Quit",
        quit_app
    )
)

# Start the system tray icon background thread
pystrayThread = threading.Thread(target=icon.run, daemon=True)
pystrayThread.start()

# Start the main clock application
timeDisplay.app.run()
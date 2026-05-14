# Functions to create the time display window

# Imports
# Main tkinter module for GUI creation
import tkinter as tk
from tkinter import *
# Allows for retrieval and formatting of current time
from time import strftime

# Windows API access for Win11 DPI scaling detection
import ctypes

# Time application class
class TimeApp:

    # Initilalize the time application window and configurations
    def __init__(self):
        # Create a instance of the Tk class to create main window of the app
        self.root = tk.Tk() 

        # Create the label used to display current time
        self.clockLabel = tk.Label(self.root)
        self.clockLabel.pack(anchor='center')

        # Initialize the clock to 12-hr format on start-up
        self.use24h = False

        # Get screen resolution in px
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()

        # Returns a value like 100, 125, 150 representing the scale percentage
        scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        actualScale = scaleFactor / 100
        
        # Calculate width and height for the scaled Tk root (window)
        rootWidth = 200*actualScale 
        rootHeight = 35*actualScale

        xOffset = (screenWidth) - rootWidth

        # Windows 11 taskbar (small) height is 32 pixels
        CONST_TASKBAR_HEIGHT = 32
        yOffset = (screenHeight) - (rootHeight+(CONST_TASKBAR_HEIGHT*actualScale))

        # Set the dimensions and placement of the root 
        self.root.geometry('%dx%d+%d+%d' % (rootWidth, rootHeight, xOffset, yOffset))
        
        # Match background of root to Windows theme
        self.root.configure(bg='SystemMenu')

        # Mimic transparancy of Windows taskbar menus
        self.root.attributes("-alpha", 0.985)
        
        # Remove app title bar
        self.root.overrideredirect(True) 

        # Force main window to be displayed on top of all other windows
        self.root.attributes('-topmost', True)

        # Immediately hide after creation, should only be shown on icon click event
        self.root.withdraw()

        # Indicate the window is not being displayed
        self.displayed = False

        # Prevent multiple loops
        self.clockRunning = False

    # Function to continuously update the displayed time
    def updateClock(self):
        # H for 24-hr format, %I for 12-hr format
        if self.use24h:
            timeString = strftime('%H:%M:%S')
        else:
            timeString = strftime('%I:%M:%S %p')
        
        # Match Windows default fonts and themes
        CONST_CLOCK_FONT_SIZE = 21
        self.clockLabel.config(text=timeString, font=('Segoe UI Variable Small', CONST_CLOCK_FONT_SIZE), bg='SystemMenu')

        # Update the clock every 1000 ms
        self.clockLabel.after(1000, self.updateClock)
    
    # Function to toggle between 12-hr and 24-hr display formats
    def toggleFormat(self):
        self.use24h = not self.use24h
    
    # Function to show the clock window
    def showWindow(self):
        # Restore window
        self.root.deiconify()
        self.displayed = True

        # Only start the clock loop once
        if not self.clockRunning:
            self.clockRunning = True
            self.updateClock()

        return self.displayed
    
    # Function to hide the clock window
    def hideWindow(self):
        self.root.withdraw()
        self.displayed = False

    # Function to toggle window visibility based on the displayed state of the app object
    def toggleWindow(self):
        if(self.displayed):
            self.hideWindow()
        else:
            self.showWindow()
    
    # Function to run the tkinter event loop
    def run(self):
        self.root.mainloop()

    # Function to shut down the app
    def shutdown(self):
        self.root.after(0, self.root.destroy)

# global TimeApp instance
app = TimeApp()
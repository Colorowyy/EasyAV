#!/usr/bin/env python3
"""
EasyAV - Simple Antivirus Software
Main application entry point
"""

import tkinter as tk
from ui.main_window import MainWindow

def main():
    """Initialize and run the application"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

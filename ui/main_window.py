"""
Main Window Module
Tkinter GUI for the antivirus application
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path

from scanner.file_scanner import FileScanner
from scanner.threat_detector import ThreatDetector
from database.signature_db import SignatureDatabase


class MainWindow:
    """Main window for the antivirus GUI"""

    def __init__(self, root):
        """
        Initialize the main window
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("EasyAV - Antivirus Software")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Initialize components
        self.scanner = FileScanner()
        self.detector = ThreatDetector()
        self.database = SignatureDatabase()

        self.scan_thread = None
        self.scanning = False

        self._create_widgets()
        self._setup_styles()

    def _setup_styles(self):
        """Setup tkinter styles"""
        style = ttk.Style()
        style.theme_use("aqua")  # Use aqua theme on macOS

    def _create_widgets(self):
        """Create GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title = ttk.Label(
            main_frame,
            text="EasyAV - Antivirus Scanner",
            font=("Helvetica", 18, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Scan button frame
        button_frame = ttk.LabelFrame(main_frame, text="Quick Scan", padding="10")
        button_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(
            button_frame,
            text="Scan File",
            command=self._scan_file_dialog
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Scan Folder",
            command=self._scan_folder_dialog
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Stop Scan",
            command=self._stop_scan
        ).pack(side=tk.LEFT, padx=5)

        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky=tk.W)
        self.status_label = ttk.Label(status_frame, text="Ready", foreground="green")
        self.status_label.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(status_frame, text="Files Scanned:").grid(row=1, column=0, sticky=tk.W)
        self.files_label = ttk.Label(status_frame, text="0")
        self.files_label.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(status_frame, text="Threats Found:").grid(row=2, column=0, sticky=tk.W)
        self.threats_label = ttk.Label(status_frame, text="0", foreground="red")
        self.threats_label.grid(row=2, column=1, sticky=tk.W)

        # Progress bar
        self.progress = ttk.Progressbar(
            status_frame,
            mode="indeterminate"
        )
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Scan Results", padding="10")
        results_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            pady=10
        )

        # Results text area with scrollbar
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_text = tk.Text(
            results_frame,
            width=80,
            height=15,
            yscrollcommand=scrollbar.set
        )
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_text.yview)

        # Info frame at bottom
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(
            info_frame,
            text="View History",
            command=self._view_history
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            info_frame,
            text="Update Signatures",
            command=self._update_signatures
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            info_frame,
            text="About",
            command=self._show_about
        ).pack(side=tk.LEFT, padx=5)

    def _scan_file_dialog(self):
        """Open file selection dialog and scan"""
        file_path = filedialog.askopenfilename(
            title="Select file to scan",
            initialdir=str(Path.home())
        )

        if file_path:
            self._start_scan([file_path])

    def _scan_folder_dialog(self):
        """Open folder selection dialog and scan"""
        folder_path = filedialog.askdirectory(
            title="Select folder to scan",
            initialdir=str(Path.home())
        )

        if folder_path:
            self._start_scan([folder_path], recursive=True)

    def _start_scan(self, paths, recursive=False):
        """Start a scan in a separate thread"""
        if self.scanning:
            messagebox.showwarning("Warning", "A scan is already in progress")
            return

        self.scanning = True
        self.scan_thread = threading.Thread(
            target=self._run_scan,
            args=(paths, recursive),
            daemon=True
        )
        self.scan_thread.start()

    def _run_scan(self, paths, recursive):
        """Run the actual scan"""
        self._update_status("Scanning...", "blue")
        self.progress.start()
        self.results_text.delete(1.0, tk.END)

        try:
            all_results = []

            for path in paths:
                if Path(path).is_file():
                    result = self.scanner.scan_file(path)
                    result = self.detector.analyze_file(result)
                    all_results.append(result)
                else:
                    results = self.scanner.scan_directory(path, recursive)
                    for result in results:
                        if "path" in result:
                            result = self.detector.analyze_file(result)
                            all_results.append(result)

            # Display results
            self._display_results(all_results)

            # Save to history
            summary = self.scanner.get_scan_summary()
            self.database.add_scan_history(summary)

            # Update status
            threats = sum(1 for r in all_results if r.get("status") == "infected")
            if threats > 0:
                self._update_status(f"Scan Complete - {threats} threats found!", "red")
            else:
                self._update_status("Scan Complete - No threats found", "green")

        except Exception as e:
            self._update_status(f"Error: {str(e)}", "red")
            self.results_text.insert(tk.END, f"Error during scan: {str(e)}\n")

        finally:
            self.progress.stop()
            self.scanning = False

    def _display_results(self, results):
        """Display scan results in the text area"""
        self.results_text.delete(1.0, tk.END)

        self.results_text.insert(tk.END, "=" * 80 + "\n")
        self.results_text.insert(tk.END, "SCAN RESULTS\n")
        self.results_text.insert(tk.END, "=" * 80 + "\n\n")

        clean_count = 0
        infected_count = 0

        for result in results:
            if result.get("status") == "error":
                self.results_text.insert(tk.END, f"ERROR: {result.get('message', 'Unknown error')}\n\n")
                continue

            if result.get("status") == "infected":
                infected_count += 1
                self.results_text.insert(tk.END, "[INFECTED] ", "infected")
                threat = result.get("threat", {})
                self.results_text.insert(
                    tk.END,
                    f"{result['path']}\n"
                    f"  Threat: {threat.get('name', 'Unknown')}\n"
                    f"  Severity: {threat.get('severity', 'Unknown')}\n\n"
                )
            else:
                clean_count += 1

        self.results_text.insert(
            tk.END,
            "\n" + "=" * 80 + "\n"
            f"Summary: {clean_count} clean, {infected_count} infected\n"
            f"Total files scanned: {len(results)}\n"
            "=" * 80 + "\n"
        )

        # Configure tags
        self.results_text.tag_configure("infected", foreground="red", font=("Helvetica", 10, "bold"))

        # Update labels
        self.files_label.config(text=str(len(results)))
        self.threats_label.config(text=str(infected_count))

    def _stop_scan(self):
        """Stop the current scan"""
        if self.scanning:
            self.scanning = False
            self._update_status("Scan stopped by user", "orange")
            messagebox.showinfo("Info", "Scan will stop after current file")

    def _update_status(self, status, color="black"):
        """Update the status label"""
        self.status_label.config(text=status, foreground=color)
        self.root.update_idletasks()

    def _view_history(self):
        """Display scan history"""
        history = self.database.get_scan_history()
        message = "Recent Scans:\n\n"

        for i, scan in enumerate(history, 1):
            timestamp = scan.get("timestamp", "Unknown").split("T")[0]
            total = scan.get("total_files", 0)
            threats = scan.get("threats_found", 0)
            message += f"{i}. {timestamp} - {total} files scanned, {threats} threats found\n"

        messagebox.showinfo("Scan History", message if history else "No scan history available")

    def _update_signatures(self):
        """Update virus signatures"""
        messagebox.showinfo(
            "Update Signatures",
            "Signature update feature coming soon!\n\n"
            "Current signatures are up to date."
        )

    def _show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About EasyAV",
            "EasyAV v1.0\n"
            "A simple antivirus scanner built with Python and Tkinter\n\n"
            "Features:\n"
            "- File and folder scanning\n"
            "- Threat detection\n"
            "- Scan history\n"
            "- Cross-platform support"
        )

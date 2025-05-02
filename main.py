#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple FTP Client

A lightweight GUI application for FTP file operations using tkinter.
This tool allows users to connect to FTP servers and perform basic operations
such as listing, uploading, and downloading files.

Created: May 2, 2025
License: MIT
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from ftplib import FTP
import os
import sys
import logging
from typing import Optional, Callable


class FTPClientApp:
    """
    A simple FTP client with a tkinter GUI interface.
    
    This application provides a user-friendly interface for connecting to FTP servers
    and performing basic file operations.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the FTP client application.
        
        Args:
            root: The tkinter root window
        """
        self.ftp: Optional[FTP] = None
        self.root = root
        self.root.title("Simple FTP Client")
        self.root.geometry("600x400")

        # Connection frame
        conn_frame = tk.Frame(root)
        conn_frame.pack(pady=10)

        tk.Label(conn_frame, text="Host:").grid(row=0, column=0)
        self.host_entry = tk.Entry(conn_frame, width=30)
        self.host_entry.grid(row=0, column=1)

        tk.Label(conn_frame, text="User:").grid(row=1, column=0)
        self.user_entry = tk.Entry(conn_frame)
        self.user_entry.grid(row=1, column=1)

        tk.Label(conn_frame, text="Pass:").grid(row=2, column=0)
        self.pass_entry = tk.Entry(conn_frame, show="*")
        self.pass_entry.grid(row=2, column=1)

        tk.Button(conn_frame, text="Connect", command=self.connect_ftp).grid(row=3, column=0, columnspan=2, pady=5)

        # Buttons frame
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="List Files", command=self.list_files).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Upload File", command=self.upload_file).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Download File", command=self.download_file).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Disconnect", command=self.disconnect).grid(row=0, column=3, padx=5)

        # File list & log
        self.output = scrolledtext.ScrolledText(root, height=15)
        self.output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def log(self, message: str) -> None:
        """
        Display a message in the log window.
        
        Args:
            message: The message to display
        """
        self.output.insert(tk.END, message + "\n")
        self.output.see(tk.END)

    def connect_ftp(self) -> None:
        """Connect to the FTP server using the provided credentials."""
        host = self.host_entry.get().strip()
        user = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not host or not user or not password:
            messagebox.showwarning("Missing Info", "Please fill in all fields.")
            return

        try:
            self.ftp = FTP(host)
            self.ftp.login(user, password)
            self.log(f"✅ Connected to {host} as {user}")
            self.status_var.set(f"Connected to {host}")
        except Exception as e:
            self.log(f"❌ Connection failed: {e}")
            self.status_var.set("Not connected")
            messagebox.showerror("Connection Error", str(e))
    
    def disconnect(self) -> None:
        """Disconnect from the FTP server."""
        if self.ftp:
            try:
                self.ftp.quit()
                self.log("Disconnected from server")
                self.status_var.set("Disconnected")
                self.ftp = None
            except Exception as e:
                self.log(f"Error disconnecting: {e}")
        else:
            self.log("❗ Not connected.")

    def list_files(self) -> None:
        """List files in the current directory on the FTP server."""
        if self.ftp:
            self.output.delete(1.0, tk.END)
            try:
                self.ftp.retrlines('LIST', callback=self.log)
                self.status_var.set("Files listed")
            except Exception as e:
                self.log(f"Error listing files: {e}")
                self.status_var.set("Failed to list files")
        else:
            self.log("❗ Not connected.")

    def upload_file(self) -> None:
        """Select and upload a file to the FTP server."""
        if self.ftp:
            filepath = filedialog.askopenfilename()
            if filepath:
                filename = os.path.basename(filepath)
                try:
                    with open(filepath, "rb") as f:
                        self.ftp.storbinary(f"STOR {filename}", f)
                    self.log(f"📤 Uploaded: {filename}")
                    self.status_var.set(f"Uploaded {filename}")
                except Exception as e:
                    self.log(f"Upload failed: {e}")
                    self.status_var.set("Upload failed")
        else:
            self.log("❗ Not connected.")

    def download_file(self) -> None:
        """Download a file from the FTP server."""
        if self.ftp:
            filename = filedialog.askstring("Download File", "Enter the filename to download:")
            if filename:
                save_path = filedialog.asksaveasfilename(initialfile=filename)
                if save_path:
                    try:
                        with open(save_path, "wb") as f:
                            self.ftp.retrbinary(f"RETR {filename}", f.write)
                        self.log(f"📥 Downloaded: {filename}")
                        self.status_var.set(f"Downloaded {filename}")
                    except Exception as e:
                        self.log(f"Download failed: {e}")
                        self.status_var.set("Download failed")
        else:
            self.log("❗ Not connected.")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = FTPClientApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


# README
# ======
# Simple FTP Client
# ----------------
# 
# ### Installation
# 
# No installation required beyond Python 3.6+ with standard libraries.
# 
# ### Usage
# 
# Run the script with Python:
# ```
# python ftptool.py
# ```
# 
# ### Features
# 
# - Connect to FTP servers
# - List directories
# - Upload and download files
# - Simple GUI interface
# 
# ### License
# 
# This project is licensed under the MIT License - see the comments at the top of the file.

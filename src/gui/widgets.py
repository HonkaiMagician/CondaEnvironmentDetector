import tkinter as tk
from tkinter import ttk

class ErrorDialog:
    """Dialog for displaying error messages"""
    
    def __init__(self, parent, title, message):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x200")
        self.dialog.configure(bg="#f0f0f0")
        
        # Add icon and message
        frame = tk.Frame(self.dialog, bg="#ffffff", bd=1, relief=tk.SOLID)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Error title
        title_frame = tk.Frame(frame, bg="#ff5252", height=30)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text=title, font=("Microsoft YaHei UI", 12, "bold"), 
                              bg="#ff5252", fg="white")
        title_label.pack(pady=5)
        
        # Error message
        msg_frame = tk.Frame(frame, bg="#ffffff", padx=20, pady=20)
        msg_frame.pack(fill=tk.BOTH, expand=True)
        msg_label = tk.Label(msg_frame, text=message, wraplength=350, justify=tk.LEFT,
                            bg="#ffffff", fg="#333333", font=("Microsoft YaHei UI", 10))
        msg_label.pack(pady=10)
        
        # OK button
        ok_button = tk.Button(msg_frame, text="OK", command=self.dialog.destroy, width=10,
                             bg="#4a86e8", fg="white", font=("Microsoft YaHei UI", 10),
                             relief=tk.FLAT, activebackground="#3a76d8", activeforeground="white")
        ok_button.pack(pady=10)

class PackageInfoDialog:
    """Dialog for displaying package details"""
    
    def __init__(self, parent, pkg_name, env_path, package_manager):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Package Details - {pkg_name}")
        self.dialog.geometry("600x400")
        self.dialog.configure(bg="#f0f0f0")
        
        # Create main frame
        main_frame = tk.Frame(self.dialog, bg="#ffffff", bd=1, relief=tk.SOLID)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Add title bar
        title_frame = tk.Frame(main_frame, bg="#4a86e8", height=40)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text=f"Package Details - {pkg_name}",
                               font=("Microsoft YaHei UI", 12, "bold"),
                               bg="#4a86e8", fg="white")
        title_label.pack(pady=8)
        
        # Create content area
        content_frame = tk.Frame(main_frame, bg="#ffffff", padx=15, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text box with scrollbar
        text_frame = tk.Frame(content_frame, bg="#ffffff")
        scrollbar = tk.Scrollbar(text_frame)
        self.desc_text = tk.Text(text_frame, wrap=tk.WORD, height=20, width=70,
                            yscrollcommand=scrollbar.set, bg="#ffffff", fg="#333333",
                            font=("Microsoft YaHei UI", 10), bd=1, relief=tk.SOLID)
        
        # Initial display content
        self.desc_text.insert(tk.END, "Fetching detailed description from PyPI...")
        self.desc_text.config(state=tk.NORMAL)  # Keep editable for user to copy
        
        scrollbar.config(command=self.desc_text.yview)
        text_frame.pack(fill=tk.BOTH, expand=True)
        self.desc_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add status bar
        status_frame = tk.Frame(main_frame, height=25, bg="#e7e7e7")
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_label = tk.Label(status_frame, text="", anchor=tk.W, bg="#e7e7e7", fg="#666666",
                                font=("Microsoft YaHei UI", 9))
        self.status_label.pack(side=tk.LEFT, padx=10, pady=3)
        
        # Start loading package information
        package_manager.load_package_info_async(pkg_name, self.update_info)
    
    def update_info(self, summary, description):
        """Update package information in the dialog"""
        try:
            # Update description text
            self.desc_text.delete(1.0, tk.END)
            self.desc_text.insert(tk.END, description)
            
            # Update status label
            self.status_label.config(text="Information updated from PyPI")
        except Exception as e:
            print(f"Failed to update package info: {str(e)}")
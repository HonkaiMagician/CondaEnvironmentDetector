from tkinter import ttk, font as tkfont

def setup_styles(root):
    """Set up custom styles for the application
    
    Args:
        root: The root window instance
    """
    # Create custom fonts
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(family="Microsoft YaHei UI", size=10)
    root.option_add("*Font", default_font)
    
    # Create large font for environment names
    root.env_font = tkfont.Font(family="Microsoft YaHei UI", size=12, weight="bold")
    
    # Set Treeview style
    style = ttk.Style()
    style.theme_use('clam')  # Use clam theme as base
    
    # Set overall Treeview style
    style.configure("Custom.Treeview",
                    background="#ffffff",
                    foreground="#333333",
                    rowheight=30,
                    fieldbackground="#ffffff",
                    borderwidth=0,
                    font=("Microsoft YaHei UI", 10))
                    
    # Set special font for environment nodes
    root.tree_env_font = tkfont.Font(family="Microsoft YaHei UI", size=12, weight="bold")
    root.tree_pkg_font = tkfont.Font(family="Microsoft YaHei UI", size=10)
    
    # Set Treeview header style
    style.configure("Custom.Treeview.Heading",
                    background="#e7e7e7",
                    foreground="#333333",
                    relief="flat",
                    font=("Microsoft YaHei UI", 10, "bold"))
    style.map("Custom.Treeview.Heading",
             background=[("active", "#d0d0d0")])
    
    # Set selected item style
    style.map("Custom.Treeview",
             background=[("selected", "#4a86e8")],
             foreground=[("selected", "#ffffff")])
             
    # Set scrollbar style
    style.configure("Custom.Vertical.TScrollbar", 
                    background="#e0e0e0",
                    arrowcolor="#606060",
                    bordercolor="#e0e0e0",
                    troughcolor="#f0f0f0")
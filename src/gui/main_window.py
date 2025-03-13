import tkinter as tk
from tkinter import ttk, font as tkfont
from ..utils.conda_manager import CondaManager
from ..utils.package_manager import PackageManager
from .styles import setup_styles
from .widgets import ErrorDialog, PackageInfoDialog

class CondaEnvViewer(tk.Tk):
    """Main window class for Conda Environment Detector"""
    
    def __init__(self):
        super().__init__()  # Initialize parent class
        self.title("Conda Environment Detector")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")

        # Initialize managers
        self.conda_manager = CondaManager()
        self.package_manager = PackageManager()
        
        # Set custom styles
        setup_styles(self)

        # Initialize custom fonts
        self.tree_env_font = tkfont.Font(family="Microsoft YaHei UI", size=10, weight="bold")

        # Create UI components
        self._create_main_frame()
        self._create_title_bar()
        self._create_content_area()
        
        # Load environment list
        self.load_environments()

    def _create_main_frame(self):
        """Create main frame with rounded corners and shadow effect"""
        self.main_frame = tk.Frame(self, bg="#ffffff", bd=1, relief=tk.SOLID)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    def _create_title_bar(self):
        """Create title bar with application name"""
        title_frame = tk.Frame(self.main_frame, bg="#4a86e8", height=40)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="Conda Environment Detector",
                            font=("Microsoft YaHei UI", 14, "bold"),
                            bg="#4a86e8", fg="white")
        title_label.pack(pady=8)

    def _create_content_area(self):
        """Create content area with tree view"""
        content_frame = tk.Frame(self.main_frame, bg="#ffffff")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tree view widget
        self.tree = ttk.Treeview(content_frame, columns=("Version", "Summary"), style="Custom.Treeview")
        self.tree.heading("#0", text="Environment/Package")
        self.tree.heading("Version", text="Version")
        self.tree.heading("Summary", text="Summary")
        self.tree.column("#0", width=200)
        self.tree.column("Version", width=100)
        self.tree.column("Summary", width=400)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Layout
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add click event binding
        self.tree.bind("<Button-1>", self.on_item_clicked)

        # Set different fonts for different types of nodes
        self.tree.tag_configure("env", font=self.tree_env_font)

    def load_environments(self):
        """Load all Conda environments"""
        try:
            envs_data = self.conda_manager.get_environments()
            
            # Add environments to tree view
            if envs_data.get("base_prefix"):
                self._add_environment_to_tree("base", envs_data["base_prefix"])
                
            for env_path in envs_data.get("envs", []):
                env_name = self.conda_manager.get_env_name(env_path)
                self._add_environment_to_tree(env_name, env_path)

            if not envs_data.get("envs") and "base_prefix" not in envs_data:
                ErrorDialog(self, "No Conda Environments Found",
                           "No Conda environments detected. Please ensure Conda is properly installed and environment variables are set.")

        except Exception as e:
            ErrorDialog(self, "Failed to Load Environments",
                       f"Unable to load Conda environment list: {str(e)}\n\nPlease ensure Conda is properly installed and accessible from command line.")

    def _add_environment_to_tree(self, env_name, env_path):
        """Add environment node to tree view"""
        env_item = self.tree.insert("", "end", text=env_name, values=("",), iid=env_path, open=False)
        self.tree.item(env_item, tags=("env",))

    def on_item_clicked(self, event):
        """Handle tree node click event"""
        item = self.tree.identify('item', event.x, event.y)
        parent = self.tree.parent(item)

        if not parent:  # Click on environment node
            is_open = self.tree.item(item, "open")
            
            # Load package list if node hasn't been loaded
            if not self.tree.get_children(item):
                self.load_packages(item)

            # Toggle node's expand/collapse state
            self.tree.item(item, open=not is_open)
        else:  # Click on package node
            self.show_package_info(item)

    def load_packages(self, env_item):
        """Load package list for specified environment"""
        env_path = env_item
        try:
            # Get conda and pip packages
            packages = self.package_manager.get_all_packages(env_path)
            
            # Add packages to tree view
            for pkg_name, pkg_info in packages.items():
                self.tree.insert(env_item, "end", text=pkg_name,
                               values=(pkg_info["version"], "Loading..."),
                               tags=(pkg_name,))
                # Asynchronously load summary information
                self.package_manager.load_package_summary_async(pkg_name,
                    self.tree.get_children(env_item)[-1], self._update_summary_in_tree)
                    
        except Exception as e:
            print(f"Failed to load packages: {str(e)}")

    def show_package_info(self, item):
        """Show package details popup"""
        pkg_name = self.tree.item(item)["text"]
        env_path = self.tree.parent(item)
        PackageInfoDialog(self, pkg_name, env_path, self.package_manager)

    def _update_summary_in_tree(self, item_id, summary):
        """Update summary information in tree view"""
        try:
            current_values = self.tree.item(item_id, "values")
            if len(current_values) >= 1:
                self.tree.item(item_id, values=(current_values[0], summary))
        except Exception as e:
            print(f"Failed to update summary: {str(e)}")
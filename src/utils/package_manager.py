import json
import glob
import os
import subprocess
import requests
from threading import Thread
from urllib.parse import quote

class PackageManager:
    """Manager class for package operations"""
    
    def get_all_packages(self, env_path):
        """Get all packages (conda and pip) in the environment
        
        Args:
            env_path (str): Path to Conda environment
            
        Returns:
            dict: Dictionary of package information
        """
        packages = {}
        
        # Get conda packages
        conda_packages = self._get_conda_packages(env_path)
        packages.update(conda_packages)
        
        # Get pip packages
        pip_packages = self._get_pip_packages(env_path)
        for pkg_name, pkg_info in pip_packages.items():
            if pkg_name not in packages:  # Avoid duplicates
                packages[pkg_name] = pkg_info
                
        return packages
    
    def _get_conda_packages(self, env_path):
        """Get conda-installed packages
        
        Args:
            env_path (str): Path to Conda environment
            
        Returns:
            dict: Dictionary of conda package information
        """
        packages = {}
        meta_dir = os.path.join(env_path, "conda-meta")
        
        if os.path.exists(meta_dir):
            for json_file in glob.glob(os.path.join(meta_dir, "*.json")):
                try:
                    with open(json_file, "r", encoding='utf-8') as f:
                        data = json.load(f)
                        packages[data["name"]] = {
                            "version": data.get("version", "Unknown")
                        }
                except Exception as e:
                    print(f"Failed to load conda package: {str(e)}")
                    
        return packages
    
    def _get_pip_packages(self, env_path):
        """Get pip-installed packages
        
        Args:
            env_path (str): Path to Conda environment
            
        Returns:
            dict: Dictionary of pip package information
        """
        packages = {}
        
        try:
            # Get python executable path
            python_exe = os.path.join(env_path, "python.exe" if os.name == "nt" else "bin/python")
            
            if os.path.exists(python_exe):
                # Use environment's python to execute pip list command
                result = subprocess.run(
                    [python_exe, "-m", "pip", "list", "--format=json"],
                    capture_output=True, text=True, check=True
                )
                pip_packages = json.loads(result.stdout)
                
                for pkg in pip_packages:
                    packages[pkg["name"]] = {
                        "version": pkg.get("version", "Unknown")
                    }
        except Exception as e:
            print(f"Failed to load pip packages: {str(e)}")
            
        return packages
    
    def load_package_summary_async(self, pkg_name, item_id, callback):
        """Asynchronously load package summary
        
        Args:
            pkg_name (str): Package name
            item_id: ID for the tree item to update
            callback: Callback function to update UI
        """
        thread = Thread(target=self._fetch_summary_async,
                       args=(pkg_name, item_id, callback))
        thread.daemon = True
        thread.start()
    
    def _fetch_summary_async(self, pkg_name, item_id, callback):
        """Fetch package summary from PyPI
        
        Args:
            pkg_name (str): Package name
            item_id: ID for the tree item to update
            callback: Callback function to update UI
        """
        try:
            summary, _ = self._fetch_pypi_info(pkg_name)
            if len(summary) > 100:
                summary = summary[:97] + "..."
            callback(item_id, summary)
        except Exception as e:
            print(f"Failed to fetch summary: {str(e)}")
            callback(item_id, "Failed to fetch summary")
    
    def load_package_info_async(self, pkg_name, callback):
        """Asynchronously load package information
        
        Args:
            pkg_name (str): Package name
            callback: Callback function to update UI
        """
        thread = Thread(target=self._fetch_info_async,
                       args=(pkg_name, callback))
        thread.daemon = True
        thread.start()
    
    def _fetch_info_async(self, pkg_name, callback):
        """Fetch package information from PyPI
        
        Args:
            pkg_name (str): Package name
            callback: Callback function to update UI
        """
        try:
            summary, description = self._fetch_pypi_info(pkg_name)
            callback(summary, description)
        except Exception as e:
            print(f"Failed to fetch package info: {str(e)}")
            callback("Error fetching information", str(e))
    
    def _fetch_pypi_info(self, pkg_name):
        """Get package information from PyPI
        
        Args:
            pkg_name (str): Package name
            
        Returns:
            tuple: (summary, description)
        """
        try:
            url = f"https://pypi.org/pypi/{quote(pkg_name)}/json"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                info = data.get("info", {})
                
                description = info.get("description", "")
                summary = info.get("summary", "")
                
                # Build summary
                summary_text = summary if summary else "No summary provided by PyPI"
                
                # Build detailed description
                desc_parts = []
                if description:
                    desc_parts.append(description)
                
                # Add project links
                project_url = info.get("project_url") or info.get("home_page")
                if project_url:
                    desc_parts.append(f"\nProject Homepage: {project_url}")
                
                desc_text = "\n\n".join(desc_parts) if desc_parts else "No detailed description provided by PyPI"
                
                return summary_text, desc_text
            else:
                error_msg = "No description available"
                return error_msg, error_msg
        except requests.RequestException:
            error_msg = "Network error, unable to fetch information from PyPI"
            return error_msg, error_msg
        except Exception as e:
            error_msg = f"Error fetching PyPI information: {str(e)}"
            return error_msg, error_msg
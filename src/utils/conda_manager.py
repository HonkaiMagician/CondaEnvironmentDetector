import subprocess
import json
import os

class CondaManager:
    """Manager class for Conda environment operations"""
    
    def get_environments(self):
        """Get list of all Conda environments
        
        Returns:
            dict: Dictionary containing environment information
        """
        try:
            result = subprocess.run(["conda", "env", "list", "--json"],
                                  capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except Exception as e:
            raise Exception(f"Failed to get Conda environments: {str(e)}")
    
    def get_env_name(self, env_path):
        """Get environment name from path
        
        Args:
            env_path (str): Path to Conda environment
            
        Returns:
            str: Environment name
        """
        return os.path.basename(env_path) or "base"
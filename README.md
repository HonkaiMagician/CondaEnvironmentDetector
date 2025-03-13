# Conda Environment Detector

A graphical interface tool for visualizing and managing Conda environments.

## Features

- Automatically detects and displays all Conda environments
- Tree structure display of installed packages in each environment
- Shows package versions and brief descriptions
- Supports viewing detailed package information
- Displays both conda and pip installed packages
- Modern user interface design

## Requirements

- Python 3.x
- Conda installed and properly configured in environment variables
- tkinter (Python standard library, usually installed with Python)
- requests (for fetching package information)

## Installation

1. Clone or download this project to your local machine
2. Ensure Python and Conda are installed on your system
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Recommended to create a new Conda environment:
   ```bash
   conda create -n conda-detector python=3.10
   conda activate conda-detector
   pip install -r requirements.txt
   ```

## Usage

1. Navigate to the project directory
2. Run the main program:
   ```bash
   python run.py
   ```
3. In the opened graphical interface:
   - Click on environment names to expand/collapse package lists
   - Click on package names to view detailed information
   - Use the scrollbar to browse long lists

## Interface Description

- Main window displays all available Conda environments
- Each environment shows its installed packages in a tree structure
- Package information includes:
  - Name
  - Version number
  - Brief description

## Important Notes

- Initial package information loading may take some time
- Ensure Conda command works properly in command line
- If environments are not displayed, check Conda installation and environment variable configuration
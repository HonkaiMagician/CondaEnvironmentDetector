from src.gui.main_window import CondaEnvViewer

def main():
    """Main entry point of the application"""
    app = CondaEnvViewer()
    app.mainloop()

if __name__ == "__main__":
    main()
import sys
from PyQt5.QtWidgets import QApplication
from src.controllers.app_controller import AppController
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application-wide stylesheet
    style_path = os.path.join(os.path.dirname(__file__), "src", "assets", "style.qss")
    with open(style_path, "r") as f:
        app.setStyleSheet(f.read())
    
    controller = AppController()
    controller.show_start_screen()
    
    sys.exit(app.exec_())
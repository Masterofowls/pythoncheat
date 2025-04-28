from PyQt5.QtCore import Qt
import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                           QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, 
                           QComboBox, QCheckBox, QRadioButton, QMessageBox)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Demo")
        self.setGeometry(100, 100, 600, 400)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Basic widgets demonstration
        # Label
        label = QLabel("This is a label")
        layout.addWidget(label)
        
        # Button
        button = QPushButton("Click Me")
        button.clicked.connect(self.button_clicked)
        layout.addWidget(button)
        
        # Text input
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter text here")
        layout.addWidget(self.text_input)
        
        # Combo box
        combo = QComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3"])
        combo.currentTextChanged.connect(self.combo_selected)
        layout.addWidget(combo)
        
        # Checkbox
        checkbox = QCheckBox("Check me")
        checkbox.stateChanged.connect(self.checkbox_changed)
        layout.addWidget(checkbox)
        
        # Radio buttons
        radio_layout = QHBoxLayout()
        self.radio1 = QRadioButton("Radio 1")
        self.radio2 = QRadioButton("Radio 2")
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        layout.addLayout(radio_layout)
        
    def button_clicked(self):
        """Handle button click event"""
        text = self.text_input.text()
        QMessageBox.information(self, "Info", f"Button clicked! Text: {text}")
        
    def combo_selected(self, text):
        """Handle combo box selection"""
        QMessageBox.information(self, "Selection", f"Selected: {text}")
        
    def checkbox_changed(self, state):
        """Handle checkbox state change"""
        status = "checked" if state == Qt.Checked else "unchecked"
        QMessageBox.information(self, "Checkbox", f"Checkbox {status}")

def main():
    # Create the application
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
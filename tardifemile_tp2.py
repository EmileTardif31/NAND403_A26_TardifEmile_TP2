## hello world

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QCheckBox
 
class MessageBoard(QWidget):
    def __init__(self): # Constructeur
        super().__init__() # Constructeur QWidget
        self.setWindowTitle("Outliner Organiser")
        self.setFixedWidth(400)
        self.create_ui()
 
    def create_ui(self):
        layout = QVBoxLayout(self)

        label = QLabel("Enter JSON rule path")
        layout.addWidget(label)
 
        global text_box
        text_box = QLineEdit(self)
        text_box.setText("file path")
        layout.addWidget(text_box)

        global check_select
        check_select = QCheckBox(self)
        check_select.setText("Apply on selection only")
        ## pour get si ye coché : check_select.isChecked() (faudra surement mettre en global)
        layout.addWidget(check_select)

        global check_color
        check_color = QCheckBox(self)
        check_color.setText("Apply colors")
        layout.addWidget(check_color)

        global check_order
        check_order = QCheckBox(self)
        check_order.setText("Apply reorder")
        layout.addWidget(check_order)
 
        button = QPushButton(self)
        button.setText("Organise Outliner")
        layout.addWidget(button)
        button.clicked.connect(self.on_click)
   
    def on_click(self):
        print("click")
   
 
def main():
    global widget
    try:
        widget.close()
    except Exception:
        pass
    widget = MessageBoard()
    widget.show()
 
main()
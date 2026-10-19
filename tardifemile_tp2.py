## tp2 emile tardif
import json
import os
import maya.cmds as cmds

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
        cmds.undoInfo(closeChunk=True) ## on le close au debut pour si jamais on refresh le script et que le close ne sest pas fait (garantit que le ctrl-z marche)
        cmds.undoInfo(openChunk=True) ## debut du ctrl z
        print("----")

        fichier = text_box.text()

        if os.path.exists(fichier):
            print("Valid file.")

            ## selected objects
            all_obj = cmds.ls(type="transform")
            selected_obj = cmds.ls(selection=True, objectsOnly=True)
            sorted_selec = sorted(selected_obj)

            if(check_select.isChecked()):
                ## les objets sélectionnés
                for i in reversed(sorted_selec):
                    print(i)

                    if(check_order.isChecked()):
                        cmds.reorder(i, front=True)

                    if(check_color.isChecked()):
                        if cmds.attributeQuery("useOutlinerColor", node=i, exists=True): # on vérifie si l'attribut existe sinon ca crash
                            cmds.setAttr(f"{i}.useOutlinerColor", 1)
                            cmds.setAttr(f"{i}.outlinerColor", 1, 0, 0)

            else:
                ## tous les objets
                for i in reversed(all_obj):

                    if(check_order.isChecked()):
                        cmds.reorder(i, front=True)

                    if(check_color.isChecked()):
                        print(f"Coloration de : {i}")

                        cmds.setAttr(f"{i}.useOutlinerColor", 1)
                        cmds.setAttr(f"{i}.outlinerColor", 1, 0, 0)  

        else:
            print("Invalid file.")

        cmds.undoInfo(closeChunk=True) ## fin du ctrl z
 
def main():
    global widget
    try:
        widget.close()
    except Exception:
        pass
    widget = MessageBoard()
    widget.show()
 
main()
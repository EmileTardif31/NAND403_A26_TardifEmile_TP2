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

        fichier = text_box.text() # get le path entré

        # validation du fichier
        if os.path.exists(fichier):
            print("Valid file.")

            # récupération des infos du fichier
            with open(fichier, "r", encoding="utf-8") as small_fichier:
                donnees = json.load(small_fichier)

            ## selected objects            
            selected_obj = cmds.ls(selection=True, objectsOnly=True) # get tous les objets sélectionnés
            sorted_selec = sorted(selected_obj) # sort les objets sélectionnés

            # ouvre les attributs du json pour faire les changements
            for prefixe, couleur in reversed(donnees.items()):

                if(check_select.isChecked()):
                    ## les objets sélectionnés avec le préfixe
                    for i in reversed(sorted_selec):
                        if(i.startswith(prefixe)): # si l'objet a un préfixe qui est dans les rules

                            # changer l'ordre
                            if(check_order.isChecked()):
                                cmds.reorder(i, front=True)

                            # changer la couleur
                            if(check_color.isChecked()):
                                if cmds.attributeQuery("useOutlinerColor", node=i, exists=True): # on vérifie si l'attribut existe sinon ca crash
                                    cmds.setAttr(f"{i}.useOutlinerColor", 1)
                                    cmds.setAttr(f"{i}.outlinerColor", *couleur)

                else:
                    ## tous les objets avec le préfixe
                    all_obj = cmds.ls(f"{prefixe}*", type="transform") # sélectionne tous les objets avec un des préfixes dans les rules
                    sorted_all = sorted(all_obj)

                    for i in reversed(sorted_all):
                        print(i)
                        print("--")

                        # changer l'ordre
                        if(check_order.isChecked()):
                            cmds.reorder(i, front=True) # remet au top l'objet

                        # changer la couleur
                        if(check_color.isChecked()):
                            cmds.setAttr(f"{i}.useOutlinerColor", 1)
                            cmds.setAttr(f"{i}.outlinerColor", *couleur)  

        else:
            print("Invalid file.")

        cmds.undoInfo(closeChunk=True) ## fin du ctrl z

# le truc du prof pour afficher le widget
def main():
    global widget
    try:
        widget.close()
    except Exception:
        pass
    widget = MessageBoard()
    widget.show()
 
main()
import math
import os

from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QDialog, QMainWindow, QPushButton

import FreeCAD
import FreeCADGui
import Draft
import DraftVecUtils
import Part
import Sketcher

import ChassisScripts.chassisTubing as chassisTubing


ui_name = "chassis_tubing.ui"
__dir__ = os.path.dirname(__file__)
uiPath = os.path.join(os.path.dirname(__dir__), 'Gui' + os.sep + 'Panels')
iconPath = os.path.join(os.path.dirname(__dir__), 'Gui' + os.sep + 'Icons')
path_to_ui = os.path.join(uiPath, ui_name)

class TubingPanel:
    def __init__(self):
        # self will create a Qt widget from our ui file
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)

       # Load UI Components
        self.sectionsComboBox = self.form.sectionsComboBox
        self.createPB = self.form.createPB

        self.tubing = chassisTubing.ChassisTubing()
        self.setupUI()

        #connect
        self.createPB.clicked.connect(self._createTube)


    def _createTube(self):
        """ call the createTube function"""
        self.tubing.createTube(self.sectionsComboBox.currentIndex())

    def reject(self):
        FreeCAD.Console.PrintMessage("Reject Signal")
        self.quit()

    def accept(self):
        self.quit()

    def quit(self):
        FreeCADGui.Control.closeDialog()

    def setupUI(self):
        sections = self.tubing.getSections()

        if sections:
            for i, section in enumerate(sections):
                print("Section", i, " - ", section.Label)
                self.sectionsComboBox.addItem(section.Label)


class chassisTubingCommand:
    def Activated(self):
        panel = TubingPanel()

        if FreeCADGui.Control.activeDialog():
            FreeCAD.Console.PrintMessage("Dialog Panel currently open: Close it?")
        FreeCADGui.Control.showDialog(panel)

    def GetResources(self):
        return {
            'Pixmap' : os.path.join( iconPath, 'importPart.svg' ),
            'MenuText': 'Create chassis tubing',
            'ToolTip': 'Create chassis tubing'
            }     
FreeCADGui.addCommand('chassisTubing', chassisTubingCommand())

import os

import FreeCAD
import FreeCADGui

import ChassisScripts.analyse as analyse


ui_name = "analyse.ui"
__dir__ = os.path.dirname(__file__)
uiPath = os.path.join(os.path.dirname(__dir__), 'Gui' + os.sep + 'Panels')
iconPath = os.path.join(os.path.dirname(__dir__), 'Gui' + os.sep + 'Icons')
path_to_ui = os.path.join(uiPath, ui_name)


class AnalysePanel:
    def __init__(self):
        # self will create a Qt widget from our ui file
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)

        # Load UI Components
        self.systemsComboBox = self.form.systemsComboBox
        self.analysePB = self.form.analysePB

        self.setupUI()

        # connect
        self.analysePB.clicked.connect(self.runAnalysis)

    def runAnalysis(self):
        """ call the createTube function"""
        FreeCAD.Console.PrintMessage("Start Analysis\n")

        systemName = self.systemsComboBox.currentText()
        if not systemName:
            FreeCAD.Console.PrintError("No Suspension systems in chassis")
            return

        system = FreeCAD.ActiveDocument.getObject(systemName)
        ani = analyse.AnimateSuspension()
        ani.start(system)

    def reject(self):
        FreeCAD.Console.PrintMessage("Reject Signal\n")
        self.quit()

    def accept(self):
        self.quit()

    def quit(self):
        FreeCADGui.Control.closeDialog()

    def setupUI(self):

        chassis = FreeCAD.ActiveDocument.getObject('Chassis')

        if not chassis:
            FreeCAD.Console.PrintMessage("No Chassis Object\n")
            return

        for item in chassis.Group:
            if '_Suspension' in item.Label:
                self.systemsComboBox.addItem(item.Label)


class analyseCommand:
    def Activated(self):
        panel = AnalysePanel()

        if FreeCADGui.Control.activeDialog():
            FreeCAD.Console.PrintMessage("Dialog Panel currently open: Close it?")
        FreeCADGui.Control.showDialog(panel)

    def GetResources(self):
        return {
            'Pixmap': os.path.join(iconPath, 'importPart.svg'),
            'MenuText': 'Analyse chassis geometry',
            'ToolTip': 'Analyse chassis geometry'
        }


FreeCADGui.addCommand('analyse', analyseCommand())

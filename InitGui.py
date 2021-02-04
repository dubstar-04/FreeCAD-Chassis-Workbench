import FreeCAD
import FreeCADGui

from ChassisScripts import chassis  # noqa: F401
from ChassisScripts import frontSuspension  # noqa: F401
from ChassisScripts import chassisTubingGui  # noqa: F401
from ChassisScripts import analyseGui  # noqa: F401


class ChassisWorkbench (Workbench):  # noqa: F821
    MenuText = 'Chassis'

    def Initialize(self):

        commandslist = [
            'chassis',
            'frontSuspension',
            'chassisTubing',
            'analyse'
        ]

        self.appendToolbar('Chassis', commandslist)
        self.treecmdList = ['chassis', 'frontSuspension']
        self.appendMenu('Chassis', commandslist)

    def Activated(self):
        FreeCAD.Console.PrintMessage("Loading Chassis Workbench")


FreeCADGui.addWorkbench(ChassisWorkbench())

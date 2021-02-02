import os

import FreeCAD
import FreeCADGui

from ChassisScripts import chassisProject

__dir__ = os.path.dirname(__file__)
iconPath = os.path.join(os.path.dirname(__dir__), 'Gui' + os.sep + 'Icons')


class frontSuspension:
    def __init__(self, obj):
        "'''Add some custom properties to our box feature'''"
        obj.addProperty("App::PropertyVector", "LFHP", "Suspension", "Hardpoint").LFHP = (1.0, 1.0, 1.0)
        obj.addProperty("App::PropertyVector", "LRHP", "Suspension", "Hardpoint").LRHP = (1.0, 1.0, 1.0)
        obj.addProperty("App::PropertyVector", "UFHP", "Suspension", "Hardpoint").UFHP = (1.0, 1.0, 1.0)
        obj.addProperty("App::PropertyVector", "URHP", "Suspension", "Hardpoint").URHP = (1.0, 1.0, 1.0)
        obj.Proxy = self
        self.Object = obj

    def onChanged(self, fp, prop):
        "'''Do something when a property has changed'''"
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, fp):
        "'''Do something when doing a recomputation, this method is mandatory'''"
        FreeCAD.Console.PrintMessage("Recompute Chassis feature\n")

    def getIcon(self):
        return '''
            /* XPM */
            static const char * ViewProviderBox_xpm[] = {
            "16 16 6 1",
            "   c None",
            ".  c #141010",
            "+  c #615BD2",
            "@  c #C39D55",
            "#  c #000000",
            "$  c #57C355",
            "        ........",
            "   ......++..+..",
            "   .@@@@.++..++.",
            "   .@@@@.++..++.",
            "   .@@  .++++++.",
            "  ..@@  .++..++.",
            "###@@@@ .++..++.",
            "##$.@@$#.++++++.",
            "#$#$.$$$........",
            "#$$#######      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            " #$#$$$$$#      ",
            "  ##$$$$$#      ",
            "   #######      "};
            '''


class frontSuspensionCommand:
    def Activated(self):
        chassis = FreeCAD.ActiveDocument.getObject('Chassis')    

        if not chassis:
            FreeCAD.Console.PrintMessage("No Chassis Object")
            return

        obj_front = FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Front Suspension")
        frontSuspension(obj_front)
        for o in FreeCAD.ActiveDocument.Objects:
            if "Proxy" in o.PropertiesList:
                if isinstance(o.Proxy, chassisProject.ChassisProject):
                    FreeCAD.Console.PrintMessage("Add Suspension to Chassis\n")
                    o.addObject(obj_front)

    def GetResources(self):
        return {
            'Pixmap': os.path.join(iconPath, 'importPart.svg'),
            'MenuText': 'Create a front suspension',
            'ToolTip': 'Create a front suspension'
        }


FreeCADGui.addCommand('frontSuspension', frontSuspensionCommand())

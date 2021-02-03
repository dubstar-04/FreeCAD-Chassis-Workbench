import os

from PySide import QtCore, QtGui

import FreeCAD
import FreeCADGui
import Part

__dir__ = os.path.dirname(__file__)
iconPath = os.path.join(os.path.dirname(__dir__), 'Gui' + os.sep + 'Icons')


class frontSuspension:
    def __init__(self, obj):
        "'''Add some custom properties to our box feature'''"
        obj.addProperty("App::PropertyVector", "LFHP", "Suspension", "Hardpoint").LFHP = (-10.0, 100.0, 1.0)
        obj.addProperty("App::PropertyVector", "LRHP", "Suspension", "Hardpoint").LRHP = (-10.0, 100.0, 1.0)
        obj.addProperty("App::PropertyVector", "UFHP", "Suspension", "Hardpoint").UFHP = (10.0, 100.0, 1.0)
        obj.addProperty("App::PropertyVector", "URHP", "Suspension", "Hardpoint").URHP = (10.0, 100.0, 1.0)
        obj.Proxy = self
        self.Object = obj

    def onChanged(self, fp, prop):
        "'''Do something when a property has changed'''"
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, fp):
        "'''Do something when doing a recomputation, this method is mandatory'''"
        FreeCAD.Console.PrintMessage("Recompute Front suspension feature\n")

        chassis = FreeCAD.ActiveDocument.getObject('Chassis')

        if not chassis:
            FreeCAD.Console.PrintMessage("No Chassis Object\n")
            return

        geom = []

        FreeCAD.Console.PrintMessage("CHASSIS FRONT TRACK: {}".format(chassis.Wheelbase))

        frontLeftWheel = FreeCAD.Vector(-chassis.FrontTrack / 2, chassis.Wheelbase, 0)
        frontRightWheel = FreeCAD.Vector(chassis.FrontTrack / 2, chassis.Wheelbase, 0)
        geom.append(Part.Edge(Part.LineSegment(frontLeftWheel, frontRightWheel)))

        fp.Shape = Part.Wire(geom)

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


class ViewProviderFrontSuspension:
    def __init__(self, obj):
        """
        Set this object to the proxy object of the actual view provider
        """
        obj.Proxy = self

    def attach(self, obj):
        """
        Setup the scene sub-graph of the view provider, this method is mandatory
        """
        return

    def setEdit(self, vobj, mode=0):
        # pylint: disable=unused-argument
        # panel = PathHelperFaceGui.PathHelperPanel(vobj.Object)
        # FreeCADGui.Control.showDialog(panel)
        FreeCAD.Console.PrintMessage("Front Suspension: View Object - SetEdit")
        return False

    def unsetEdit(self, vobj, mode=0):
        # pylint: disable=unused-argument
        return False

    def getIcon(self):
        return os.path.join(iconPath, 'importPart.svg')

    def setupContextMenu(self, vobj, menu):
        action_edit = QtGui.QAction(QtGui.QIcon(os.path.join(iconPath, 'importPart.svg')), "Edit Front Suspension", menu)
        QtCore.QObject.connect(action_edit, QtCore.SIGNAL("triggered()"), print("Edit Front Suspension Triggered"))
        menu.addAction(action_edit)


class frontSuspensionCommand:
    def Activated(self):
        chassis = FreeCAD.ActiveDocument.getObject('Chassis')

        if not chassis:
            FreeCAD.Console.PrintMessage("No Chassis Object")
            return

        obj_front = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Front Suspension")
        frontSuspension(obj_front)
        ViewProviderFrontSuspension(obj_front.ViewObject)
        chassis.addObject(obj_front)
        FreeCAD.ActiveDocument.recompute()
        return obj_front

    def GetResources(self):
        return {
            'Pixmap': os.path.join(iconPath, 'importPart.svg'),
            'MenuText': 'Create a front suspension',
            'ToolTip': 'Create a front suspension'
        }


FreeCADGui.addCommand('frontSuspension', frontSuspensionCommand())

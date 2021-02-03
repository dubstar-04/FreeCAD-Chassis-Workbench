import os

from PySide import QtCore, QtGui

import FreeCAD
import FreeCADGui
import Part

__dir__ = os.path.dirname(__file__)
iconPath = os.path.join(os.path.dirname(__dir__), 'Gui' + os.sep + 'Icons')


class frontSuspension:
    def __init__(self, obj):
        """
        Keys:
        U = UPPER
        L = LOWER
        F = FRONT
        R = REAR
        HP = HARD POINT
        Ur = Upright

        UFHP = UPPER FRONT HARD POINT
        """

        chassis = FreeCAD.ActiveDocument.getObject('Chassis')

        if not chassis:
            FreeCAD.Console.PrintMessage("No Chassis Object\n")
            return

        # chassis hardpoints
        obj.addProperty("App::PropertyVector", "LFHP", "Suspension", "Hardpoint").LFHP = (300, 1775, 100)
        obj.addProperty("App::PropertyVector", "LRHP", "Suspension", "Hardpoint").LRHP = (300, 1525, 100)
        obj.addProperty("App::PropertyVector", "UFHP", "Suspension", "Hardpoint").UFHP = (300, 1750, 400)
        obj.addProperty("App::PropertyVector", "URHP", "Suspension", "Hardpoint").URHP = (300, 1550, 400)
        # upright hardpoints
        obj.addProperty("App::PropertyVector", "UrLHP", "Suspension", "Hardpoint").UrLHP = (600, 1650, 100)
        obj.addProperty("App::PropertyVector", "UrUHP", "Suspension", "Hardpoint").UrUHP = (600, 1650, 400)

        # roll centre
        obj.addProperty("App::PropertyVector", "RollCentre", "Suspension", "Hardpoint")
        obj.RollCentre = (0.0, 0.0, 0.0)
        obj.setEditorMode("RollCentre", 1)  # Read only

        obj.Proxy = self
        self.Object = obj

    def onChanged(self, fp, prop):
        "'''Do something when a property has changed'''"
        return

    def execute(self, fp):
        "'''Do something when doing a recomputation, this method is mandatory'''"
        FreeCAD.Console.PrintMessage("Recompute Front suspension feature\n")
        self.draw(fp)

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def draw(self, fp):

        geom = []

        # frontLeftWheel = FreeCAD.Vector(-chassis.FrontTrack / 2, chassis.Wheelbase, 0)
        # frontRightWheel = FreeCAD.Vector(chassis.FrontTrack / 2, chassis.Wheelbase, 0)
        # geom.append(Part.Edge(Part.LineSegment(frontLeftWheel, frontRightWheel)))

        # upper wishbones
        # right
        geom.append(Part.Edge(Part.LineSegment(fp.UFHP, fp.UrUHP)))
        geom.append(Part.Edge(Part.LineSegment(fp.URHP, fp.UrUHP)))
        # left
        LeftUFHP = FreeCAD.Vector(-fp.UFHP.x, fp.UFHP.y, fp.UFHP.z)
        LeftURHP = FreeCAD.Vector(-fp.URHP.x, fp.URHP.y, fp.URHP.z)
        LeftUrUHP = FreeCAD.Vector(-fp.UrUHP.x, fp.UrUHP.y, fp.UrUHP.z)
        geom.append(Part.Edge(Part.LineSegment(LeftUFHP, LeftUrUHP)))
        geom.append(Part.Edge(Part.LineSegment(LeftURHP, LeftUrUHP)))

        # lower wishbone
        # right
        geom.append(Part.Edge(Part.LineSegment(fp.LFHP, fp.UrLHP)))
        geom.append(Part.Edge(Part.LineSegment(fp.LRHP, fp.UrLHP)))
        # left
        LeftLFHP = FreeCAD.Vector(-fp.LFHP.x, fp.LFHP.y, fp.LFHP.z)
        LeftLRHP = FreeCAD.Vector(-fp.LRHP.x, fp.LRHP.y, fp.LRHP.z)
        LeftUrLHP = FreeCAD.Vector(-fp.UrLHP.x, fp.UrLHP.y, fp.UrLHP.z)
        geom.append(Part.Edge(Part.LineSegment(LeftLFHP, LeftUrLHP)))
        geom.append(Part.Edge(Part.LineSegment(LeftLRHP, LeftUrLHP)))

        # uprights
        geom.append(Part.Edge(Part.LineSegment(fp.UrLHP, fp.UrUHP)))
        geom.append(Part.Edge(Part.LineSegment(LeftUrLHP, LeftUrUHP)))

        resPart = Part.Compound(geom)
        fp.Shape = resPart


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

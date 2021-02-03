import os

from PySide import QtCore, QtGui

import FreeCAD
import FreeCADGui

__dir__ = os.path.dirname(__file__)
iconPath = os.path.join(os.path.dirname(__dir__), 'Gui' + os.sep + 'Icons')


class Chassis:
    def __init__(self, obj):
        '''Add some custom properties to our box feature'''
        obj.addProperty("App::PropertyLength", "Wheelbase", "Chassis", "Wheelbase of the vehicle").Wheelbase = 1650.0
        obj.addProperty("App::PropertyLength", "FrontTrack", "Chassis", "Front Track of the vehicle").FrontTrack = 1200.0
        obj.addProperty("App::PropertyLength", "RearTrack", "Chassis", "Rear Track of the vehicle").RearTrack = 1400.0
        obj.addProperty("App::PropertyVector", "COG", "Chassis", "Center of Gravity").COG = (1.0, 1.0, 1.0)
        obj.setEditorMode("COG", 1)  # Read only
        obj.Proxy = self
        self.Object = obj

    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("Chassis Change property: " + str(prop) + "\n")
        for item in fp.Group:
            item.recompute()

    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute Chassis feature\n")
        # fp.Shape = Part.makeSphere(10, fp.COG)

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    '''
    def addObject(self, child):
        if hasattr(self, "Object"):
            g = self.Object.Group
            if child not in g:
                g.append(child)
                self.Object.Group = g

    def removeObject(self, child):
        if hasattr(self, "Object"):
            g = self.Object.Group
            if child in g:
                g.remove(child)
                self.Object.Group = g
    '''

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


class ViewProviderChassis:
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
        FreeCAD.Console.PrintMessage("Chassis: View Object - SetEdit")
        return False

    def unsetEdit(self, vobj, mode=0):
        # pylint: disable=unused-argument
        return False

    def getIcon(self):
        return os.path.join(iconPath, 'importPart.svg')

    def setupContextMenu(self, vobj, menu):
        action_edit = QtGui.QAction(QtGui.QIcon(os.path.join(iconPath, 'importPart.svg')), "Edit Chassis", menu)
        QtCore.QObject.connect(action_edit, QtCore.SIGNAL("triggered()"), print("Edit Chassis Triggered"))
        menu.addAction(action_edit)


class chassisCommand:
    def Activated(self):
        doc = FreeCAD.activeDocument()

        if not doc:
            FreeCAD.Console.PrintMessage("No active document")
            return

        obj_chassis = doc.addObject('App::DocumentObjectGroupPython', 'Chassis')
        Chassis(obj_chassis)
        ViewProviderChassis(obj_chassis.ViewObject)
        FreeCAD.ActiveDocument.recompute()
        return obj_chassis

    def GetResources(self):
        return {
            'Pixmap': os.path.join(iconPath, 'importPart.svg'),
            'MenuText': 'Create a new chassis',
            'ToolTip': 'Create a new chassis'
        }


FreeCADGui.addCommand('chassis', chassisCommand())

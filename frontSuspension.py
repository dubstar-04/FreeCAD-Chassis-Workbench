'''
Creates a new front suspension
'''

from PySide import QtGui
import FreeCADGui, FreeCAD
import Part
import os
import chassisProject

__dir__ = os.path.dirname(__file__)


class frontSuspension:
    def __init__(self, obj):
        "'''Add some custom properties to our box feature'''"
        obj.addProperty("App::PropertyVector","LFHP","Suspension","Hardpoint").LFHP=(1.0, 1.0, 1.0)
        obj.addProperty("App::PropertyVector","LRHP","Suspension","Hardpoint").LRHP=(1.0, 1.0, 1.0)
        obj.addProperty("App::PropertyVector","UFHP","Suspension","Hardpoint").UFHP=(1.0, 1.0, 1.0)
        obj.addProperty("App::PropertyVector","URHP","Suspension","Hardpoint").URHP=(1.0, 1.0, 1.0)
        obj.Proxy = self
        self.Object = obj        


    def onChanged(self, fp, prop):
        "'''Do something when a property has changed'''"
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
 
    def execute(self, fp):
        "'''Do something when doing a recomputation, this method is mandatory'''"
        FreeCAD.Console.PrintMessage("Recompute Chassis feature\n")    
             
    def getIcon(self):
        #"'''Return the icon in XPM format which will appear in the tree view. This method is\'''
        #        '''optional and if not defined a default icon is shown.'''"
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
        doc = FreeCAD.activeDocument()
        obj_front = doc.addObject("App::FeaturePython","Front Suspension")   
        frontSuspension(obj_front)
        for o in FreeCAD.ActiveDocument.Objects:
             if "Proxy" in o.PropertiesList:
                if isinstance(o.Proxy, chassisProject.ChassisProject):
                    FreeCAD.Console.PrintMessage("Add Suspension to Chassis\n")
                    o.addObject(obj_front)
                    
    def GetResources(self): 
        return {
            'Pixmap' : os.path.join( __dir__ , 'importPart.svg' ) , 
            'MenuText': 'Create a front suspension', 
            'ToolTip': 'Create a front suspension'
            }    
            
FreeCADGui.addCommand('frontSuspension', frontSuspensionCommand())


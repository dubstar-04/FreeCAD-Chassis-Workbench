'''
Creates a new chassis
'''

from PySide import QtGui
import FreeCADGui, FreeCAD
import Part
import os
import chassisProject

__dir__ = os.path.dirname(__file__)


    
class Chassis:
    def __init__(self, obj):
        "'''Add some custom properties to our box feature'''"
        obj.addProperty("App::PropertyLength","Wheelbase","Chassis","Wheelbase of the vehicle").Wheelbase=1.0
        obj.addProperty("App::PropertyLength","FrontTrack","Chassis","Front Track of the vehicle").FrontTrack=1.0
        obj.addProperty("App::PropertyLength","RearTrack","Chassis", "Rear Track of the vehicle").RearTrack=1.0
        obj.addProperty("App::PropertyVector","COG","Chassis","Center of Gravity").COG=(1.0, 1.0, 1.0)
        obj.Proxy = self
        self.Object = obj        

    def onChanged(self, fp, prop):
        "'''Do something when a property has changed'''"
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
 
    def execute(self, fp):
        "'''Do something when doing a recomputation, this method is mandatory'''"
        FreeCAD.Console.PrintMessage("Recompute Chassis feature\n")
        fp.Shape = Part.makeSphere(10,fp.COG)
        
    def addObject(self,child):
        if hasattr(self,"Object"):
            g = self.Object.Group
            if not child in g:
                g.append(child)
                self.Object.Group = g

    def removeObject(self,child):
        if hasattr(self,"Object"):
            g = self.Object.Group
            if child in g:
                g.remove(child)
                self.Object.Group = g
        
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

class chassisCommand:
    def Activated(self):
        doc = FreeCAD.activeDocument()
        obj_chassis = doc.addObject("Part::FeaturePython","Chassis")     
        Chassis(obj_chassis)
        obj_chassis.ViewObject.Proxy=0
        
        for o in FreeCAD.ActiveDocument.Objects:
            if "Proxy" in o.PropertiesList:
                if isinstance(o.Proxy, chassisProject.ChassisProject):
                    FreeCAD.Console.PrintMessage("Add Suspension to Chassis\n")
                    o.addObject(obj_chassis)
        
        FreeCAD.ActiveDocument.recompute()

        
    def GetResources(self): 
        return {
            'Pixmap' : os.path.join( __dir__ , 'importPart.svg' ) , 
            'MenuText': 'Create a new chassis', 
            'ToolTip': 'Create a new chassis'
            }    
            
FreeCADGui.addCommand('chassis', chassisCommand())


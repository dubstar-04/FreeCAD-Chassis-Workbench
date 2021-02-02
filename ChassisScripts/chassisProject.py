'''
Creates a new chassis
'''

from PySide import QtGui
import FreeCADGui, FreeCAD
import Part
import os

__dir__ = os.path.dirname(__file__)
iconPath = os.path.join(os.path.dirname(__dir__), 'Gui' + os.sep + 'Icons')
  
class ChassisProject:
    def __init__(self, obj):
        "'''Add some custom properties to our box feature'''"
        obj.Proxy = self
        self.Object = obj        

    def onChanged(self, fp, prop):
        "'''Do something when a property has changed'''"
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
 
    def execute(self, fp):
        "'''Do something when doing a recomputation, this method is mandatory'''"
        
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

class NewChassisCommand:
    def Activated(self):
        doc = FreeCAD.activeDocument()
        obj_chassis_project = doc.addObject("App::DocumentObjectGroupPython","Chassis Project")
        ChassisProject(obj_chassis_project)
        
    def GetResources(self): 
        return {
            'Pixmap' : os.path.join( iconPath , 'importPart.svg' ) , 
            'MenuText': 'Create a new chassis project', 
            'ToolTip': 'Create a new chassis project'
            }    
            
FreeCADGui.addCommand('chassisProject', NewChassisCommand())


# -*- coding: utf-8 -*-

import FreeCAD
import FreeCADGui
import Draft
import DraftVecUtils
import Part
import Sketcher

from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QDialog, QMainWindow, QPushButton

import math
import os

ui_name = "chassis_tubing.ui"
__dir__ = os.path.dirname(__file__)
uiPath = os.path.join(os.path.dirname(__dir__), 'Gui' + os.sep + 'Panels')
iconPath = os.path.join(os.path.dirname(__dir__), 'Gui' + os.sep + 'Icons')
path_to_ui = os.path.join(uiPath, ui_name)

def getSections():
        """ check there is a section Group """
        documentGroupList = FreeCAD.ActiveDocument.findObjects('App::DocumentObjectGroup')

        if not any(group.Label == "Sections" for group in documentGroupList):
            FreeCAD.Console.PrintWarning("Tubing_Macro: Sections not found, Creating them now\n")      
            createSectionGroup()

        group = FreeCAD.ActiveDocument.getObject('Sections')
        sections = group.Group

        if not len(sections):
            FreeCAD.Console.PrintError("Tubing_Macro: No sections found, Sections group is empty\n")
            return []

        return sections

def create_circular_tube(group, size):
    # add an example circular section
    section_name = "Circular-Section-{0}mm".format(size)
    radius = size / 2
    circular_sketch = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObject', section_name)
    circular_sketch.addGeometry(Part.Circle(FreeCAD.Vector(0.000000,0.000000,0),FreeCAD.Vector(0,0,1),radius),False)
    circular_sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
    circular_sketch.addConstraint(Sketcher.Constraint('Radius',0,radius)) 
    circular_sketch.setDatum(1,FreeCAD.Units.Quantity("{0}mm".format(radius)))
    group.addObject(circular_sketch)

def create_square_tube(group, size):
    # add an example square section
    section_name = "Square-Section-{0}mm".format(size)
    half_size = size / 2	
    square_section = FreeCAD.ActiveDocument.addObject('Sketcher::SketchObject', section_name)
    geoList = []
    geoList.append(Part.LineSegment(FreeCAD.Vector(-half_size,half_size,0),FreeCAD.Vector(half_size,half_size,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(half_size,half_size,0),FreeCAD.Vector(half_size,-half_size,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(half_size,-half_size,0),FreeCAD.Vector(-half_size,-half_size,0)))
    geoList.append(Part.LineSegment(FreeCAD.Vector(-half_size,-half_size,0),FreeCAD.Vector(-half_size,half_size,0)))
    square_section.addGeometry(geoList,False)
    conList = []
    conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
    conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
    conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
    conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
    conList.append(Sketcher.Constraint('Horizontal',0))
    conList.append(Sketcher.Constraint('Horizontal',2))
    conList.append(Sketcher.Constraint('Vertical',1))
    conList.append(Sketcher.Constraint('Vertical',3))
    square_section.addConstraint(conList)
    square_section.addConstraint(Sketcher.Constraint('Symmetric',0,1,1,2,-1,1)) 
    square_section.addConstraint(Sketcher.Constraint('Equal',0,1)) 
    square_section.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,size)) 
    square_section.setDatum(10,FreeCAD.Units.Quantity("{0}mm".format(size)))
    group.addObject(square_section)


def createSectionGroup():
    """ Create a sections group """
    group = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Sections")
    sizes = [20, 30, 40, 50]
    for size in sizes:
        create_circular_tube(group, size)
        create_square_tube(group, size)
	
    # hide the group so the sections don't show in the 3d view 
    group.Visibility = False
    FreeCAD.ActiveDocument.recompute()


def createTube(section_idx):
    """ create a tube using the selected section and path """

    # get the selected elements
    sel = FreeCADGui.Selection.getSelectionEx()
    if not len(sel):
        FreeCAD.Console.PrintWarning("Tubing_Macro: Nothing selected\n")
        return

    selpath = sel[0]    
    # make a copy of the selected path
    path = selpath.Object
    # get a list of edges to convert to tube
    edges = selpath.SubElementNames
    print("Selected:", path.Label, " with edges ", edges)
    
    #get the startpoint of the edge
    edge = selpath.SubObjects[0]
    vertex = edge.Vertexes[0]
    #get normal of segment
    if isinstance(edge.Curve,Part.Circle):
        n = edge.tangentAt(edge.FirstParameter) # .negative()
    else:
        n = (edge.Vertexes[1].Point - edge.Vertexes[0].Point).normalize()

    parents = path.InListRecursive
    for parent in parents:
        if isinstance(parent, FreeCAD.Part):
            chassis = parent

    # get list of available sections
    sections = getSections()
    
    # make a copy of the section
    section = FreeCAD.ActiveDocument.copyObject(sections[section_idx])

    try:
        chassis.addObject(section)
    except NameError:
        FreeCAD.ActiveDocument.removeObject(section.Name)
        FreeCAD.Console.PrintError("Tubing_Macro: Tube must to be created inside a Part Element\n")
        return
    
    # get sketch normal
    vector = FreeCAD.Vector(0,0,1)
    # get the rotation axis
    r = vector.cross(n)
    # calculate the rotation angle in degrees
    a = DraftVecUtils.angle(n, vector, r) * 180 / math.pi
    Draft.rotate(section, 0-a, axis=r)
    # move the section to the start of the tube
    section.Placement.Base = vertex.Point
    # create new tube
    tube =chassis.newObject('PartDesign::AdditivePipe','Tube')
    tube.Profile = section
    tube.Spine = (path, edges)
    tube.Transition = 'Transformed'
    tube.Mode = 'Frenet'
    FreeCAD.ActiveDocument.recompute()

class TubingPanel:
    def __init__(self):
        # self will create a Qt widget from our ui file
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)
        
       #Load UI Components
        self.sectionsComboBox = self.form.sectionsComboBox
        self.createPB = self.form.createPB

        self.setupUI()

        #connect
        self.createPB.clicked.connect(self._createTube)

    
    def _createTube(self):
        """ call the createTube function"""
        createTube(self.sectionsComboBox.currentIndex())

    def reject(self):
        FreeCAD.Console.PrintMessage("Reject Signal")
        self.quit()

    def accept(self):
        self.quit()
        
    def quit(self):
        FreeCADGui.Control.closeDialog()
    
    def setupUI(self):
        sections = getSections()

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
            'Pixmap' : os.path.join( iconPath , 'importPart.svg' ) , 
            'MenuText': 'Create chassis tubing', 
            'ToolTip': 'Create chassis tubing'
            }    
            
FreeCADGui.addCommand('chassisTubing', chassisTubingCommand())



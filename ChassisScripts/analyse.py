import os
import math

from PySide import QtCore
import FreeCAD
import DraftVecUtils

__dir__ = os.path.dirname(__file__)
iconPath = os.path.join(os.path.dirname(__dir__), 'Gui' + os.sep + 'Icons')


class AnimateSuspension():
    def __init__(self):
        self.timer = QtCore.QTimer()
        self.iterations = 0
        self.angle = 0
        self.increment = 0.1
        self.upperlimit = 5
        self.lowerLimit = -2
        self.hp = {}

        self.timer.timeout.connect(self.animate)
        self.timer.setInterval(100)

    def start(self, system):
        print("starting animation using system:", system.Label)
        self.hp = system.Proxy.getHardpoints(system)
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def animate(self):

        self.angle += self.increment

        print("angle:", self.angle)

        FreeCAD.Console.PrintMessage("Timer is running\n")

        # self.timer.stop()

        print("rotated vector:", self.rotateVector(self.hp["UrUHP"], self.hp["UFHP"], self.hp["URHP"], self.angle))

        if self.angle > self.upperlimit or self.angle < self.lowerLimit:
            self.increment = 0 - self.increment
            self.iterations += 1

        if self.iterations > 4:
            self.timer.stop()

    def rotateVector(self, vec, axisVecStart, axisVecEnd, angle):
        """
        rotate vector: vec
        about axis defined by: axisVecStart and axisVecEnd
        by angle in degrees: angle
        """

        if angle == 0:
            return vec

        u = vec.sub(axisVecStart)
        angle = math.radians(5)
        axis = axisVecEnd.sub(axisVecStart)
        v = DraftVecUtils.rotate(u, angle, axis).add(axisVecStart)

        return v

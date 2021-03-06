#coding=utf-8

from Value import Value
from Utils import Utils
from NBestList import NBestList
from Gesture import Gesture
from lxml import etree as ET
from datetime import datetime
from PointR import PointR
import string

#GeometricRecognizer class definition
##Videos to identify gestures

class GeometricRecognizer:

    def __init__(self):
        self.__gestures = []
        
    def Recognize(self, points, acceptedGesturesNames=None):
        p = Utils.Resample(points, Value.NumResamplePoints)

        radians = Utils.AngleInRadians(Utils.Centroid(p), p[0], False)
        p = Utils.RotateByRadians(p, -radians)

        p = Utils.ScaleTo(p, Value.ResampleScale)
        p = Utils.TranslateCentroidTo(p, Value.ResampleOrigin)

        # # Uncomment these lines to add new gestures (and change Name !)
        # print '<?xml version="1.0" encoding="utf-8" standalone="yes"?>'
        # print '<Gesture Name="name" NumPts="%d" Millseconds="%d" AppName="WUW01" AppVer="1.0.0.0" Date="Wenesday, January 08, 2016" TimeOfDay="14:56:51 PM">' % (len(p), points[-1].T - points[0].T);
        # for k in p:
        #     print '  <Point X="%d" Y="%d" T="%d" />' % (k.X, k.Y, k.T)
        # print '</Gesture>'

        nBest = NBestList()
        for pp in self.__gestures:
            if acceptedGesturesNames is None or pp.Name in acceptedGesturesNames or pp.Name == "close":
                best = self.GoldenSectionSearch(p, pp.Points, Utils.DegToRad(-45.0), Utils.DegToRad(+45.0), Utils.DegToRad(2.0))
                score = 1.0 - best[0] / Value.HalfDiagonal
                nBest.AddResult(pp.Name, score, best[0], best[1])
        nBest.AddResult("Try Again", Value.tolerance, 0.0, 0.0)
        nBest.SortDescending()
        return nBest

    #Golden Search
    def GoldenSectionSearch(self, pts1, pts2, a, b, threshold):
        x1 = Value.Phi * a + (1 - Value.Phi) * b
        newPoints = Utils.RotateByRadians(pts1, x1)
        fx1 = Utils.PathDistance(newPoints, pts2)

        x2 = (1 - Value.Phi) * a + Value.Phi * b
        newPoints = Utils.RotateByRadians(pts1, x2)
        fx2 = Utils.PathDistance(newPoints, pts2)

        i = 2.0
        while abs(b - a) > threshold:
            if fx1 < fx2:
                b = x2
                x2 = x1
                fx2 = fx1
                x1 = Value.Phi * a + (1 - Value.Phi) * b
                newPoints = Utils.RotateByRadians(pts1, x1)
                fx1 = Utils.PathDistance(newPoints, pts2)
            else:
                a = x1
                x1 = x2
                fx1 = fx2
                x2 = (1 - Value.Phi) * a + Value.Phi * b
                newPoints = Utils.RotateByRadians(pts1, x2)
                fx2 = Utils.PathDistance(newPoints, pts2)
            i += 1
        return [min(fx1, fx2), Utils.RadToDeg((b+a)/2.0), i]

    #Hill climbing search
    def HillClimbSearch(self, pts1, pts2, D, step):
        i = 0.0
        theta = 0.0
        d = D
        while d <= D:
            D = d
            theta += step
            newPoints = Utils.RotateByDegrees(pts1, theta)
            d = Utils.Distance(newPoints, pts2)
            i += 1
        return [D, theta - step, i]

    #Full search
    def FullSearch(self, pts1, pts2):
        bestA = 0.0
        bestD = Utils.PathDistance(pts1, pts2)

        for i in range(-180, 180+1):
            newPoints = Utils.RotateByDegrees(pts1, i)
            d = Utils.PathDistance(newPoints, pts2)
            if d < bestD:
                bestD = d
                bestA = i
        return [bestD, bestA, 360.0]

    @property
    def NumGestures(self):
        return len(self.__gestures)

    @property
    def Gestures(self):
        l = []
        for g in self.__gestures:
            l.append(g[:])
        l.sort(cmp = Gesture.CompareTo)
        return l

    def ClearGestures(self):
        counts = len(self.__gestures)
        for i in range(counts):
            self.__gestures.pop()

    def SaveGesture(self, filename, points):
        name = Gesture.ParseName(filename)
        counts = self.NumGestures
        for i in range(counts):
            if self.__gestures[i].Name == name:
                del self.__gestures[i]
                break
        newPrototype = Gesture(name, points)
        self.__gestures.append(newPrototype)

        p0 = points[0]
        pn = points[len(points) -1]

        success = True
        try:
            ges = ET.Element("Gesture")
            ges.attrib["Name"] = name
            ges.attrib["NumPts"] = "%d" % len(points)
            ges.attrib["Millseconds"] = "%d" % (pn.T - p0.T)
            ges.attrib["AppName"] = "WUW01"
            ges.attrib["AppVer"] = "1.0.0.0"
            ges.attrib["Date"] = datetime.now().strftime("%A, %B %d, %Y")
            ges.attrib["TimeOfDay"] = datetime.now().strftime("%I:%M:%S %p")
            
            for p in points:
                q = ET.SubElement(ges, "Point")
                q.attrib["X"] = "%f" % p.X
                q.attrib["Y"] = "%f" % p.Y
                q.attrib["T"] = "%f" % p.T

            tree = ET.ElementTree(ges)
            tree.write(filename, pretty_print = True, xml_declaration = True, encoding = "UTF-8")
        except Exception:
            success = false
        return success
    

    def ReadGesture(self, root):
        if root.tag != "Gesture":
            return None
        name = root.get("Name")

        points = []
        plist = root.findall("Point")
        for p in plist:
            qx = string.atof(p.get("X"))
            qy = string.atof(p.get("Y"))
            qt = string.atoi(p.get("T"))
            q = PointR(qx,qy,qt)
            points.append(q)

        return Gesture(name, points)

    def LoadGesture(self, filename):
        success = True
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            p = self.ReadGesture(root)
            
            counts = self.NumGestures
            # for i in range(counts):
            #     if self.__gestures[i].Name == p.Name:
            #         del self.__gesture[i]
            #         break
            self.__gestures.append(p)
        except Exception as e:
            print(e)
            success = False
        return success
    

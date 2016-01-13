#coding=utf-8

import math
from random import random
from random import randint
from RectangleR import RectangleR
from PointR import PointR
from SizeR import SizeR
class Utils:

    ##Lengths and Rects
    
    #Returns the smallest rectangle that can envelope points dot column
    @staticmethod
    def FindBox(points):
        minX = float("inf")
        maxX = float("-inf")
        minY = float("inf")
        maxY = float("-inf")

        for p in points:
            if p.X < minX:
                minX = p.X
            if p.X > maxX:
                maxX = p.X
            if p.Y < minY:
                minY = p.Y
            if p.Y > maxY:
                maxY = p.Y
                
        return RectangleR(minX,minY,maxX-minX,maxY-minY)

    #Returns the distance between two points
    @staticmethod
    def Distance(p1, p2):
        dx = p2.X - p1.X
        dy = p2.Y - p1.Y
        return math.sqrt(dx * dx + dy * dy)

    #Returns the center point of the column
    @staticmethod
    def Centroid(points):
        xsum = 0.0
        ysum = 0.0
        for p in points:
            xsum += p.X
            ysum += p.Y
        return PointR(xsum / len(points), ysum / len(points))

    #Column represents the return point of the path length
    @staticmethod
    def PathLength(points):
        length = 0
        i = 1
        counts = len(points)
        while i < counts:
            length += Utils.Distance(points[i-1], points[i])
            i += 1
        return length
    

    ##Angles and Rotations

    #Radians to degrees
    @staticmethod
    def RadToDeg(rad):
        return rad * 180.0 / math.pi

    #Degrees to radians
    @staticmethod
    def DegToRad(deg):
        return deg * math.pi / 180.0

    #Returns the end point to start at the origin, the horizontal x- axis positive right down to the positive y -axis of the arc
    @staticmethod
    def AngleInRadians(start, end, positiveOnly):
        radians = 0.0
        if start.X != end.X:
            radians = math.atan2(end.Y-start.Y, end.X-start.X)
        else:
            if end.Y < start.Y:
                radians = -math.pi / 2.0
            elif end.Y > start.Y:
                radians = math.pi / 2.0
        if positiveOnly and radians < 0.0:
            radians += math.pi * 2.0
        return radians

    #Returns the end point to start at the origin, the horizontal x- axis positive right down to the y -axis of the forward angle
    @staticmethod
    def AngleInDegrees(start, end, positiveOnly):
        radians = Utils.AngleInRadians(start, end, positiveOnly)
        return Utils.RadToDeg(radians)

    #Radians clockwise rotation around the center
    @staticmethod
    def RotateByRadians(points, radians):
        newPoints = []
        c = Utils.Centroid(points)

        cos = math.cos(radians)
        sin = math.sin(radians)

        cx = c.X
        cy = c.Y

        counts = len(points)
        for i in range(counts):
            p = points[i]
            dx = p.X - cx
            dy = p.Y - cy
            q = PointR()
            q.X = dx * cos - dy * sin + cx
            q.Y = dx * sin + dy * cos + cy
            newPoints.append(q)
        return newPoints

    #Degrees clockwise rotation around the center angle
    @staticmethod
    def RotateByDegrees(points, degrees):
        radians = Utils.DegToRad(degrees)
        return RotateByRadians(points, radians)

    #Return p point clockwise rotation around the c point radians radians results
    @staticmethod
    def RotatePoint(p, c, radians):
        q = PointR()
        q.X = (p.X - c.X) * math.cos(radians) - (p.Y - c.Y) * math.sin(radians) + c.X
        q.Y = (p.X - c.X) * math.sin(radians) + (p.Y - c.Y) * math.cos(radians) + c.Y
        return q

    ##Translations

    #Converting coordinates for the upper left corner to toPt
    @staticmethod
    def TranslateBBoxTo(points, toPt):
        newPoints = []
        r = Utils.FindBox(points)
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            p.X += toPt.X - r.X
            p.Y += toPt.Y - r.Y
            newPoints.append(p)
        return newPoints

    #Converting coordinates for the center to toPt
    @staticmethod
    def TranslateCentroidTo(points, toPt):
        newPoints = []
        centroid = Utils.Centroid(points)
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            p.X += toPt.X - centroid.X
            p.Y += toPt.Y - centroid.Y
            newPoints.append(p)
        return newPoints

    #Translation
    @staticmethod
    def TranslateBy(points, sz):
        newPoints = []
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            p.X += sz.Width
            p.Y += sz.Height
            newPoints.append(p)
        return newPoints

    ##Scaling

    #Zooming along the origin , the rectangle becomes sz size
    @staticmethod
    def ScaleTo(points, sz):
        newPoints = []
        r = Utils.FindBox(points)
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            if r.Width != 0.0:
                p.X *= (sz.Width / r.Width)
            if r.Height != 0.0:
                p.Y *= (sz.Height / r.Height)
            newPoints.append(p)
        return newPoints

    #Zooming along the origin , the rectangle enlarge sz times
    @staticmethod
    def ScaleBy(points, sz):
        newPoints = []
        r = Utils.FindBox(points)
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            p.X *= sz.Width
            p.Y *= sz.Height
            newPoints.append(p)
        return newPoints

    @staticmethod
    def ScaleToMax(points, box):
        newPoints = []
        r = Utils.FindBox(points)
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            p.X *= (box.MaxSide / r.MaxSide)
            p.Y *= (box.MaxSide / r.MaxSide)
            newPoints.append(p)
        return newPoints

    @staticmethod
    def ScaleToMin(points, box):
        newPoints = []
        r = Utils.FindBox(points)
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            p.X *= (box.MinSide / r.MinSide)
            p.Y *= (box.MinSide / r.MinSide)
            newPoints.append(p)
        return newPoints

    ##Path Sampling and Distance

    #From the point of the column was elected average of n
    @staticmethod
    def Resample(points, n):
        I = 1.0 * Utils.PathLength(points) / (n-1)
        D = 0.0
        srcPts = []
        for p in points:
            srcPts.append(p[:])
        dstPts = []
        dstPts.append(srcPts[0][:])
        counts = len(srcPts)
        i = 1
        while i < counts:
            pt1 = srcPts[i-1]
            pt2 = srcPts[i]

            d = Utils.Distance(pt1, pt2)
            if (D+d) >= I:
                qx = pt1.X + ((I - D) / d) * (pt2.X - pt1.X)
                qy = pt1.Y + ((I - D) / d) * (pt2.Y - pt1.Y)
                q = PointR(qx, qy)
                dstPts.append(q)
                srcPts.insert(i, q[:])
                counts += 1
                D = 0.0
            else:
                D += d
            i += 1
        if len(dstPts) == n-1:
            dstPts.append(srcPts[len(srcPts) -1][:])
        return dstPts

    #The average distance calculation of the two paths
    @staticmethod
    def PathDistance(path1, path2):
        distance = 0
        counts = len(path1)
        for i in range(counts):
            distance += Utils.Distance(path1[i], path2[i])
        return distance / counts

    ##Random Numbers

    #Produce num will not repeat between the low-high random number 
    @staticmethod
    def Random(low, high, num):
        array = []
        n = high - low + 1
        if num > n:
            return array
        if n * 1.0 / num < 1.0 / 3.0:
            for i in range(num):
                array.append(i)
            i = 0
            while i < num:
                array[i] = randint(low, high)
                for j in range(i):
                    if array[i] == array[j]:
                        i -= 1
                        break
            return array
        tmp = []
        for i in range(n):
            tmp.append(i + low)
        for i in range(num):
            t = randint(0, n-i-1)
            array.append(tmp[t])
            tmp[t] = tmp[n-i-1]
        return array
    
    

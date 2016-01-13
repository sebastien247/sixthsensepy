#coding=utf-8

"""
** WUW Python
** Chendaxixi
** SixthSense Group
** Date: 2015/02/10
"""

#WUW应用
##包括窗口建立和响应函数

import wx
import threading
import thread
import time
import os
import math
import TouchlessLib
import ystockquote
import wx.lib.plot as plot
import  pywapi
import string
from classes.Value import Value
from classes.PointR import PointR
from classes.GeometricRecognizer import GeometricRecognizer
from classes.NBestList import NBestList

from Apps.AppBase import AppBase

from Apps.AppClock import AppClock
from Apps.AppPhoto import AppPhoto
from Apps.AppStock import AppStock
from Apps.AppBook import AppBook
<<<<<<< HEAD
from Apps.AppWeather import AppWeather
=======
from Apps.AppLearn import AppLearn
>>>>>>> Add App Learn

DEBUG = False
AUTO_LOAD_DEFAULT = True


class WuwPanel(wx.Panel):
    Width = Value.WuwWidth
    Height = Value.WuwHeight
    def __init__(self, parent):
        self.Grid = self.Width / 100
        wx.Panel.__init__(self, parent)

        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.SetForegroundColour(wx.Colour(255, 255, 255))

        ###构建界面
        #构建TabPage构件组
        self.btnShowHide=wx.Button(self,pos=(self.Width-self.Grid*5,self.Grid),
                                 size=(3*self.Grid,3*self.Grid))
        self.btnExit=wx.Button(self,label="Exit",pos=(self.Width-self.Grid*9,self.Grid),
                             size=(3*self.Grid,3*self.Grid))
        self.tabSettings=wx.Notebook(self,pos=(self.Width-self.Grid*62,self.Grid*3),
                                   size=(60*self.Grid,20*self.Grid))
        self.pictureBoxDisplay=wx.StaticBox(self,pos=(self.Width-self.Grid*66,self.Grid*23),
                                             size=(64*self.Grid,48*self.Grid))
        #self.tabSettings.SetTabSize((self.Grid,1.5*self.Grid))
        self.tabPageCamera=wx.Panel(self.tabSettings)
        self.tabPageTokens=wx.Panel(self.tabSettings)
        self.tabPageApps=wx.Panel(self.tabSettings)
        self.tabSettings.AddPage(self.tabPageCamera, "Camera")
        self.tabSettings.AddPage(self.tabPageTokens, "Tokens")
        self.tabSettings.AddPage(self.tabPageApps, "Apps")
        ##构建TabPageCamera
        self.comboBoxCameras=wx.ComboBox(self.tabPageCamera,value="Select A Camera",
                                       pos=(0,0), size=(25*self.Grid,2*self.Grid))
        self.lblCameraInfo=wx.StaticText(self.tabPageCamera,label="No Camera Selected",
                                       pos=(0,3*self.Grid),size=(25*self.Grid,2*self.Grid))
        self.buttonCameraProperties=wx.Button(self.tabPageCamera,label="Adjust Camera Properties",
                                            pos=(0,5*self.Grid),size=(23*self.Grid,2*self.Grid))
        self.labelCameraFPS=wx.StaticText(self.tabPageCamera,label="Current FPS:",
                                        pos=(0,7*self.Grid),size=(8*self.Grid,2*self.Grid))
        self.labelCameraFPSValue=wx.StaticText(self.tabPageCamera,label="0.00",
                                             pos=(8*self.Grid,7*self.Grid),
                                             size=(6*self.Grid,2*self.Grid))
        self.checkBoxCameraFPSLimit=wx.CheckBox(self.tabPageCamera,label="Limit Frames Per Second",
                                              pos=(0,9*self.Grid),
                                              size=(16*self.Grid,2*self.Grid))
        self.CameraFPSLimit=wx.TextCtrl(self.tabPageCamera,value="30",
                                      pos=(17*self.Grid,9*self.Grid),
                                      size=(6*self.Grid,2*self.Grid))
        self.lblRecord=wx.StaticText(self.tabPageCamera,label="[Recording]",
                                   pos=(41*self.Grid,1*self.Grid),
                                   size=(8*self.Grid,2*self.Grid))
        self.btnRecord=wx.Button(self.tabPageCamera,label="RECORD",
                               pos=(42*self.Grid,3*self.Grid),
                               size=(6*self.Grid,2*self.Grid))
        self.btnLoad=wx.Button(self.tabPageCamera,label="LOAD",
                             pos=(42*self.Grid,5*self.Grid),
                             size=(6*self.Grid,2*self.Grid))
        self.btnView=wx.Button(self.tabPageCamera,label="VIEW",
                             pos=(42*self.Grid,7*self.Grid),
                             size=(6*self.Grid,2*self.Grid))
        self.btnClear=wx.Button(self.tabPageCamera,label="CLEAR",
                              pos=(42*self.Grid,9*self.Grid),
                              size=(6*self.Grid,2*self.Grid))
        ##构建TabPageTokens
        self.buttonMarkerAdd=wx.Button(self.tabPageTokens,label="New Marker",
                                     pos=(0,0),size=(10*self.Grid,2*self.Grid))
        self.comboBoxMarkers=wx.ComboBox(self.tabPageTokens,value="Edit Existing Marker",
                                       pos=(11*self.Grid,0),
                                       size=(14*self.Grid,2*self.Grid))
        self.lblTotalMarker=wx.StaticText(self.tabPageTokens,label="Number of markers:",
                                        pos=(26*self.Grid,0),
                                        size=(13*self.Grid,2*self.Grid))
        self.lblMarkerCount=wx.StaticText(self.tabPageTokens,label="0",
                                        pos=(40*self.Grid,0),
                                        size=(4*self.Grid,2*self.Grid))
        self.buttonMarkerSave=wx.Button(self.tabPageTokens,label="Save M",
                                      pos=(45*self.Grid,0),
                                      size=(6*self.Grid,2*self.Grid))
        self.buttonMarkerLoad=wx.Button(self.tabPageTokens,label="Load M",
                                      pos=(52*self.Grid,0),
                                      size=(6*self.Grid,2*self.Grid))
        self.buttonMarkerLoadDefault=wx.Button(self.tabPageTokens,label="Load Default\n     Markers",
                                      pos=(45*self.Grid,25),
                                      size=(6*self.Grid*2.17,4*self.Grid))
        self.lblMarkerControl=wx.StaticText(self.tabPageTokens,label="No Marker Selected",
                                          pos=(0,3*self.Grid),
                                          size=(58*self.Grid,2*self.Grid))
        self.buttonMarkerRemove=wx.Button(self.tabPageTokens,label="Remove This Marker",
                                        pos=(0,5*self.Grid),
                                        size=(20*self.Grid,2*self.Grid))
        self.checkBoxMarkerHighlight=wx.CheckBox(self.tabPageTokens,label="Highlight Marker",
                                               pos=(0,7*self.Grid),
                                               size=(16*self.Grid,2*self.Grid))
        self.checkBoxMarkerSmoothing=wx.CheckBox(self.tabPageTokens,label="Smooth Marker Data",
                                               pos=(0,9*self.Grid),
                                               size=(16*self.Grid,2*self.Grid))
        self.labelMarkerThresh=wx.StaticText(self.tabPageTokens,label="Marker Threshold:",
                                           pos=(0,11*self.Grid),
                                            size=(15*self.Grid,2*self.Grid))
        self.MarkerThresh=wx.TextCtrl(self.tabPageTokens,value="0",
                                    pos=(15*self.Grid,11*self.Grid),
                                    size=(5*self.Grid,2*self.Grid))
        self.labelMarkerData=wx.TextCtrl(self.tabPageTokens,pos=(21*self.Grid,5*self.Grid),
                                       size=(37*self.Grid,8*self.Grid))
        self.labelMarkerData.SetEditable(False)
        ##构建TabPageApps
        self.labelDemoInstructions=wx.TextCtrl(self.tabPageApps,pos=(44*self.Grid,0),
                                             size=(16*self.Grid,16*self.Grid))
        self.labelDemoInstructions.SetEditable(False)
        
        self.buttonWeatherDemo=wx.Button(self.tabPageApps,label="Weather",pos=(1*self.Grid,7*self.Grid),
                                         size=(8*self.Grid,2*self.Grid))

        #构建Label组
        self.labelM=wx.StaticText(self, label=" M", pos=(4*self.Grid,self.Grid),
                                size=(2*self.Grid,2*self.Grid))
        self.labelN=wx.StaticText(self, label=" N", pos=(4*self.Grid,4*self.Grid),
                                size=(2*self.Grid,2*self.Grid))
        self.labelO=wx.StaticText(self, label=" O", pos=(1*self.Grid,self.Grid),
                                size=(2*self.Grid,2*self.Grid))
        self.labelP=wx.StaticText(self, label=" P", pos=(1*self.Grid,4*self.Grid),
                                size=(2*self.Grid,2*self.Grid))
        self.labelM.SetBackgroundColour("ORANGE RED")
        self.labelO.SetBackgroundColour("ORANGE RED")
        self.labelN.SetBackgroundColour("RED")
        self.labelP.SetBackgroundColour("RED")
        self.labelDemoName=wx.StaticText(self, label="WUW", pos=(7*self.Grid,self.Grid),
                                       size=(4*self.Grid,2*self.Grid))
        self.lblResult=wx.StaticText(self, label="Test", pos=(12*self.Grid,self.Grid),
                                    size=(12*self.Grid,2*self.Grid))

        #构建DemoBox
        #self.BoxPhoto=wx.StaticBox(self,pos=(18*self.Grid,16*self.Grid),
        #                            size=(64*self.Grid,48*self.Grid))
        # self.BoxLearn=wx.StaticBox(self,pos=(0*self.Grid,0*self.Grid),
        #                             size=(100*self.Grid,100*self.Grid))


        ###Global Variables
        self.__touchlessMgr = None
        self.__fAddingMarker = False
        self.__inBoxArea = False
        self.m = None
        self.n = None
        self.o = None
        self.p = None
        self.__isDown = False
        self.__recording = False
        self.__rec = GeometricRecognizer()
        self.__points = []
        self.__show_settings = False
        self.__markerCenter = None
        self.__markerRadius = 0
        self.__drawSelectionAdornment = False
        self.__addedMarkerCount = 0
        self.__latestFrame = None
        self.__latestFrameTime = time.time()
        self.__latestFrameTimeSegment = False
        self.__ratioScreenCameraHeight = 0
        self.__ratioScreenCameraWidth = 0
        self.trying = []
        self.__drawingGesture = False
        self.__drawingStart = None
        self.__drawingPoints = []


        self.apps = []

        ###Load
        self.__touchlessMgr = TouchlessLib.TouchlessMgr()
        self.__touchlessMgr.RefreshCameraList()
        #self.__touchlessMgr.CurrentCamera.ImageCaptured()
        #self.__touchlessMgr.CurrentCamera.GetCurrentImage().show()
        self.threadCapture = self.ThreadCapture("Capture", 0.03, self.pictureBoxDisplay, self.__touchlessMgr.CurrentCamera, self)
        self.threadCapture.setDaemon(True)
        self.threadCapture.start()
        self.threadMarker = self.ThreadMarker("Marker", 0.08, self.__touchlessMgr, self)
        self.threadMarker.setDaemon(True)
        self.threadMarker.start()
        self.gestureLoad()
        time.clock()
        

        self.ResetEnvironment()

        ###事件响应
        self.Bind(wx.EVT_WINDOW_DESTROY, self.WUW_Destroy)
        self.Bind(wx.EVT_PAINT, self.WUW_Paint)

        #self.Bind(wx.EVT_PAINT, self.drawLatestImage)
        #self.Bind(wx.EVT_PAINT, self.drawLatestImage, self)
        #self.pictureBoxDisplay.Bind(wx.EVT_PAINT, self.drawLatestImage)

        self.buttonMarkerAdd.Bind(wx.EVT_BUTTON, self.buttonMarkerAdd_Click)
        self.comboBoxMarkers.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.comboBoxMarkers_DropDown)
        self.comboBoxMarkers.Bind(wx.EVT_COMBOBOX,self.comboBoxMarkers_SelectedIndexChanged)
        self.checkBoxMarkerHighlight.Bind(wx.EVT_CHECKBOX,self.checkBoxMarkerHighlight_CheckedChanged)
        self.checkBoxMarkerSmoothing.Bind(wx.EVT_CHECKBOX,self.checkBoxMarkerSmoothing_CheckedChanged)
        self.MarkerThresh.Bind(wx.EVT_TEXT,self.MarkerThresh_ValueChanged)
        self.buttonMarkerRemove.Bind(wx.EVT_BUTTON, self.buttonMarkerRemove_Click)
        self.buttonMarkerSave.Bind(wx.EVT_BUTTON, self.buttonMarkerSave_Click)
        self.buttonMarkerLoad.Bind(wx.EVT_BUTTON, self.buttonMarkerLoad_Click)
        self.buttonMarkerLoadDefault.Bind(wx.EVT_BUTTON, self.buttonMarkerLoadDefault_Click)
        self.Bind(wx.EVT_LEFT_DOWN, self.WUW_MouseDown)
        self.Bind(wx.EVT_MOTION, self.WUW_MouseMove)
        self.Bind(wx.EVT_LEFT_UP, self.WUW_MouseUp)
        #self.Bind(wx.EVT_LEFT_DOWN , self.dragClock)
        self.btnExit.Bind(wx.EVT_BUTTON, self.btnExit_Click)
        self.btnShowHide.Bind(wx.EVT_BUTTON, self.btnShowHide_Click)

        # print self.comboBoxCameras.GetCurrentSelection()
        # print self.threadCapture
        # print dir(self.threadCapture)
        # self.comboBoxCameras.SetSelection(0)
        # print self.comboBoxCameras.GetCurrentSelection()

        if AUTO_LOAD_DEFAULT:
            self.__addedMarkerCount = 4
            self.__touchlessMgr.SetDefaultMarkers()

        self.nameMarkers()

    #线程——捕获某帧图像 
    class ThreadCapture(threading.Thread):
        def __init__(self, threadname, times, box, cam, panel):
            threading.Thread.__init__(self, name=threadname)
            self.__times = times
            self.__stop = False
            self.__box = box
            self.__cam = cam
            self.__panel = panel
        def run(self):
            while not self.__stop:
                self.__cam.ImageCaptured()
                self.__panel.UpdateLatestFrame()
                if self.__box.Shown:
                    wx.CallAfter(self.draw)
                time.sleep(self.__times)
        def stop(self):
            self.__stop = True

        def draw(self):
            #self.__box.Refresh()
            self.__panel.drawLatestImage()

    def refreshCam(self):
        if self.__latestFrame == None:
            return
        bmp = TouchlessLib.ImageToBitmap(self.__latestFrame)
        dc = wx.PaintDC(self.pictureBoxDisplay)
        dc.DrawBitmap(bmp,0,0)

    def UpdateLatestFrame(self):
        if not self.__fAddingMarker:
            self.__latestFrame = self.__touchlessMgr.CurrentCamera.GetCurrentImage()
            self.__latestFrameTime = time.time()
        else:
            markerWait = time.time()-self.__latestFrameTime
            if markerWait <= 5:
                self.__latestFrame = self.__touchlessMgr.CurrentCamera.GetCurrentImage()
                if markerWait * 1000 % 1000 < 100:
                    self.__latestFrameTimeSegment = True
                else:
                    self.__latestFrameTimeSegment = False

    #线程——追踪标记物
    class ThreadMarker(threading.Thread):
        def __init__(self, threadname, times, mgr, panel):
            threading.Thread.__init__(self, name=threadname)
            self.__times = times
            self.__mgr = mgr
            self.__stop = False
            self.__panel = panel
        def run(self):
            while not self.__stop:
                #if self.__mgr.MarkersCount == 4:
                wx.CallAfter(self.draw) # Si jamais ça bug: décommenter cette ligne et supprimer celle suivante
                #self.draw()
                time.sleep(self.__times)
        def stop(self):
            self.__stop = True
        def draw(self):
            self.__mgr.UpdateMarkers(self.__mgr.CurrentCamera.img_cv)
            self.__panel.AnalyzeMarkers()

    def StartDrawing(self):
        self.__drawingGesture = True
        self.__drawingStart = time.time()
        self.__drawingPoints = []
        print("START DRAWING")

    def EndDrawing(self):
        self.__drawingGesture = False
        result = self.__rec.Recognize(self.__drawingPoints)
        print("END DRAWING")
        print(result.Name)

    def AnalyzeMarkers(self):
        if self.__touchlessMgr.MarkersCount < 2:
            return
        m = self.__touchlessMgr.Markers[0]
        n = self.__touchlessMgr.Markers[1]

        if m.CurrData.Present and n.CurrData.Present:
            dist = ((m.CurrData.X - n.CurrData.X)**2 + (m.CurrData.Y - n.CurrData.Y)**2)**0.5
            isTouching = dist < 100
            if isTouching and not self.__drawingGesture:
                self.StartDrawing()
            elif not isTouching and self.__drawingGesture:
                self.EndDrawing()
        elif not m.CurrData.Present and not n.CurrData.Present:
            if self.__drawingGesture:
                self.EndDrawing()

        if self.__drawingGesture:
            if n.CurrData.Present and m.CurrData.Present:
                # On utilise la moyenne des deux points détectés
                point_x = (n.CurrData.X + m.CurrData.X) / 2
                point_y = (n.CurrData.Y + m.CurrData.Y) / 2
            else:
                # On utilise le seul point détecté
                point = n if n.CurrData.Present else m
                point_x = point.CurrData.X
                point_y = point.CurrData.Y
            self.__drawingPoints.append(PointR(point_x, point_y,time.clock()*1000))


    #线程——时间显示
    class ThreadTime(threading.Thread):
        def __init__(self, threadname, times, box):
            threading.Thread.__init__(self, name=threadname)
            self.__times = times
            self.__box = box
            self.__stop = False
        def run(self):
            while not self.__stop:
                self.__box.Refresh(True)
                time.sleep(self.__times)
        def stop(self):
            self.__stop = True

    ## Les actions de toutes les apps s'éxécutent dans ce thread
    class ThreadApps(threading.Thread):
        def __init__(self, threadname, times):
            threading.Thread.__init__(self, name=threadname)
            self.__stop = False

        def run(self):
            while not self.__stop:
                pass

        def stop(self):
            self.__stop = True


    ###Environmenmt
    def btnExit_Click(self, event):
        if self.__touchlessMgr.MarkersCount >= 4:
            self.m = None
            self.n = None
            self.o = None
            self.p = None
        self.GetParent().Close()

    def btnShowHide_Click(self, event):
        if self.__show_settings:
            self.tabSettings.Hide()
            self.pictureBoxDisplay.Hide()
            self.btnExit.Hide()
            self.__show_settings = False
            self._fAddingMarker = False
        else:
            self.tabSettings.Show()
            self.pictureBoxDisplay.Show()
            self.btnExit.Show()
            self.__show_settings = True

    def ResetEnvironment(self):
        self.__show_settings = False
        self.tabSettings.Hide()
        self.pictureBoxDisplay.Hide()
        self.btnExit.Hide()

    def StopOtherApps(self, event):
        pass

    ###WUW Management
    def WUW_Destroy(self, event):
        self.threadCapture.stop()
        self.threadMarker.stop()
        self.__touchlessMgr.CleanupCameras()
        # /!\ FERMER LES THREADS /!\


    def WUW_Paint(self, event):
        if len(self.__points) > 0:
            dc = wx.PaintDC(self)
            if self.__recording:
                brush = wx.Brush("red")
            else:
                brush = wx.Brush("blue")
            dc.SetBrush(brush)
            for p in self.__points:
                dc.DrawEllipse(p.X-2,p.Y-2,4,4)
            p = self.__points[0]
            dc.DrawEllipse(p.X-5,p.Y-5,10,10)


    ###Touchless Event Handling
    def drawLatestImage(self, event=None):
        if self.__touchlessMgr.CurrentCamera == None or not self.__show_settings:
            return
        if not self.__latestFrame == None:
            bmp = TouchlessLib.ImageToBitmap(self.__latestFrame)
            dc = wx.PaintDC(self.pictureBoxDisplay)
            dc.DrawBitmap(bmp,0,0)

            if self.__drawSelectionAdornment:
                dc.SetPen(wx.Pen("red", 1))
                #dc.SetBrush(wx.Brush("",wx.TRANSPARENT))
                dc.DrawEllipse(self.__markerCenter.x-self.__markerRadius,self.__markerCenter.y-self.__markerRadius,2*self.__markerRadius,2*self.__markerRadius)

            if self.__latestFrameTimeSegment:
                markerWait = 5-(int)(round(time.time()-self.__latestFrameTime))
                text = str.format("{0}", markerWait)
                dc.SetFont(wx.Font(5*self.Grid,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))
                dc.SetTextForeground("red")
                dc.DrawText(text,5*self.Grid,5*self.Grid)

    ###Marker Mode

    ##Marker Buttons
    def buttonMarkerAdd_Click(self, event):

        if not self.__fAddingMarker:
            self.buttonMarkerAdd.SetLabel("Cancel Adding Marker")
            wx.MessageBox('Please, add markers in the following order:\n\n- Right thumb\n- Right index\n- Left thumb\n- Left index', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.__fAddingMarker = True
        else:
            self.buttonMarkerAdd.SetLabel("Add A New Marker")
            self.__fAddingMarker = False

    def comboBoxMarkers_DropDown(self, event):
        pass

    def comboBoxMarkers_SelectedIndexChanged(self, event):
        pass

    ##UI Marker Editing
    def checkBoxMarkerHighlight_CheckedChanged(self, event):
        pass

    def checkBoxMarkerSmoothing_CheckedChanged(self, event):
        pass

    def MarkerThresh_ValueChanged(self, event):
        pass

    def buttonMarkerRemove_Click(self, event):
        pass

    def buttonMarkerSave_Click(self, event):
        pass

    def buttonMarkerLoad_Click(self, event):
        pass

    def buttonMarkerLoadDefault_Click(self, event):
        self.m = None
        self.p = None
        self.o = None
        self.n = None
        self.__points = []
        self.__markerCenter = None
        self.__markerRadius = 0
        self.__addedMarkerCount = 4
        self.__touchlessMgr.SetDefaultMarkers()
        self.nameMarkers()

    ##Display Interaction
    def pictureBoxDisplay_MouseDown(self, event):
        if not self.__fAddingMarker:
            return
        if not self.__touchlessMgr.CurrentCamera.isOn():
            return
        self.__markerCenter = event.GetPosition() - self.pictureBoxDisplay.GetPosition()
        self.__markerRadius = 0
        self.__drawSelectionAdornment = True

    def pictureBoxDisplay_MouseMove(self, event):
        if not self.__fAddingMarker:
            return
        if not self.__markerCenter == None:
            dx = event.GetX() - self.pictureBoxDisplay.GetPosition().x - self.__markerCenter.x
            dy = event.GetY() - self.pictureBoxDisplay.GetPosition().y - self.__markerCenter.y
            self.__markerRadius = math.sqrt(dx*dx + dy*dy)

            self.pictureBoxDisplay.Refresh()

    def pictureBoxDisplay_MouseUp(self, event):
        if not self.__fAddingMarker:
            self.__inBoxArea = False
            return
        if not self.__markerCenter == None:
            dx = event.GetX() - self.pictureBoxDisplay.GetPosition().x - self.__markerCenter.x
            dy = event.GetY() - self.pictureBoxDisplay.GetPosition().y - self.__markerCenter.y
            self.__markerRadius = math.sqrt(dx*dx + dy*dy)

            img = self.__latestFrame
            size = self.pictureBoxDisplay.GetSize()
            self.__markerCenter.x = (self.__markerCenter.x * img.size[0]) / size.width
            self.__markerCenter.y = (self.__markerCenter.y * img.size[1]) / size.height
            self.__markerRadius = (self.__markerRadius * img.size[1]) / size.height
            newMarker = self.__touchlessMgr.AddSelectedMarker(str.format("Marker #{0}", self.__addedMarkerCount), img, self.__markerCenter, self.__markerRadius)
            self.__addedMarkerCount += 1

        self.__markerCenter = None
        self.__markerRadius = 0
        self.__drawSelectionAdornment = False
        self.pictureBoxDisplay.Refresh()
        self.__inBoxArea = False

        if self.__touchlessMgr.MarkersCount == 4:
            self.__fAddingMarker = False
            self.buttonMarkerAdd.Label = "Add A New Marker"
        self.nameMarkers()


    ###Marker Functions

    ##Marker Initial Functions
    def nameMarkers(self):
        if self.__touchlessMgr.MarkersCount == 4:
            self.m = self.__touchlessMgr.Markers[0]
            self.n = self.__touchlessMgr.Markers[1]
            self.o = self.__touchlessMgr.Markers[2]
            self.p = self.__touchlessMgr.Markers[3]

            self.m.OnChange = self.m_OnChange
            self.n.OnChange = self.n_OnChange
            self.o.OnChange = self.o_OnChange
            self.p.OnChange = self.p_OnChange

            self.__ratioScreenCameraHeight = (1.0 * self.Height / self.__touchlessMgr.CurrentCamera.CaptureHeight)
            self.__ratioScreenCameraWidth = (1.0 * self.Width / self.__touchlessMgr.CurrentCamera.CaptureWidth)

    ##Marker_OnChange
    def m_OnChange(self, event):
        self.labelM.SetPosition(wx.Point((int)(event.X * self.__ratioScreenCameraWidth), (int)(event.Y * self.__ratioScreenCameraHeight)))

    def n_OnChange(self, event):
        self.labelN.SetPosition(wx.Point((int)(event.X * self.__ratioScreenCameraWidth), (int)(event.Y * self.__ratioScreenCameraHeight)))

    def o_OnChange(self, event):
        self.labelO.SetPosition(wx.Point((int)(event.X * self.__ratioScreenCameraWidth), (int)(event.Y * self.__ratioScreenCameraHeight)))

    def p_OnChange(self, event):
        self.labelP.SetPosition(wx.Point((int)(event.X * self.__ratioScreenCameraWidth), (int)(event.Y * self.__ratioScreenCameraHeight)))

    ##Marker Helper Functions

    ##Marker HandSigns Functions

    ###Gesture Buttons


    ###Gesture Functions
    def gestureLoad(self):
        folderName = "Gestures"
        filePath = os.listdir(folderName)
        for fileName in filePath:
            counts = len(fileName)
            if counts > 4:
                if fileName[counts-1]=='l' and fileName[counts-2]=='m' and fileName[counts-3]=='x' and fileName[counts-4]=='.':
                    self.__rec.LoadGesture(folderName + "/" + fileName)


    ###Gesture Mouse Events
    def WUW_MouseDown(self, event):
        if self.__show_settings:
            point = event.GetPosition()
            rect = self.pictureBoxDisplay.GetRect()
            if point.x >= rect.x and point.x <= rect.x + rect.width and point.y >= rect.y and point.y <= rect.y + rect.height:
                self.__inBoxArea = True
        if self.__inBoxArea:
            self.pictureBoxDisplay_MouseDown(event)
            return
        self.__isDown = True
        self.__points = []
        self.__points.append(PointR(event.GetX(), event.GetY(),time.clock()*1000))
        self.Refresh()

    def WUW_MouseMove(self, event):
        if self.__inBoxArea:
            self.pictureBoxDisplay_MouseMove(event)
            return
        if self.__isDown:
            self.__points.append(PointR(event.GetX(),event.GetY(),time.clock()*1000))
            self.Refresh(True, wx.Rect(event.GetX()-2,event.GetY()-2,4,4))

    def closeApp(self):
        self.gesturesActions.pop()


    def WUW_MouseUp(self, event):
        if self.__inBoxArea:
            self.pictureBoxDisplay_MouseUp(event)
            return
        if self.__isDown:
            self.__isDown = False
            if len(self.__points) >= 5: # require 5 points for a valid gesture
                if self.__recording:
                    pass

                elif self.__rec.NumGestures > 0:
                    result = self.__rec.Recognize(self.__points)
                    self.lblResult.Label = str.format("{0}: {1} ({2}px, {3}",
                                                 result.Name,
                                                 round(result.Score,2),
                                                 round(result.Distance,2),
                                                 round(result.Angle,2))

                    if result.Name == "close":
                        if len(self.apps) > 1:
                            self.apps[-1].End()
                    else:
                        actions = self.apps[-1].actions
                        action = actions.get(result.Name, lambda: None)
                        action()

    def buttonLearnDemo_Click(self, event):
        if self.learnDemo: # Fermeture de l'app
            self.learnDemo = False
            self.labelDemoName.Label = "WUW"
            self.buttonLearnDemo.Label = "Learn"
            self.BoxLearn.threadTime.stop()
            self.BoxLearn.threadTime=None
            self.BoxLearn.Hide()
            self.ResetEnvironment()
        else: # Ouverture de l'app
            self.ResetEnvironment()
            self.StopOtherApps(event)
            self.learnDemo = True
            self.labelDemoName.Label = "Learn"
            self.buttonLearnDemo.Label = "Stop Learn"
            self.BoxLearn.threadTime = self.ThreadTime("time", 1, self.BoxLearn)
            self.BoxLearn.threadTime.start()
            self.BoxLearn.Show()


    def get_latestFrame(self):
        return self.__latestFrame

    def get_isDown(self):
        return self.__isDown

    def get_touchlessMgr(self):
        return self.__touchlessMgr

def main():
    app = wx.App(False)
    frame = wx.Frame(None, wx.ID_ANY, "WUW", size=(WuwPanel.Width,WuwPanel.Height))
    frame.SetTitle("SixthSense Python")
    panel = WuwPanel(frame)

    appClock = AppClock(panel)

    appBase = AppBase(panel)
    appPhoto = AppPhoto(panel)
    appStock = AppStock(panel)
    appBook = AppBook(panel)
    appWeather = AppWeather(panel)
    appLearn = AppLearn(panel)

    appBase.actions = {
        "clock1": appClock.Start,
        "photo6": appPhoto.Start,
        "email": appBook.Start,
        "weather": appWeather.Start,
        }

    panel.apps.append(appBase)

    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()

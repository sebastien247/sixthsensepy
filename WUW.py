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
from classes.Value import Value
from classes.PointR import PointR
from classes.GeometricRecognizer import GeometricRecognizer
from classes.NBestList import NBestList


DEBUG = False

class WuwPanel(wx.Panel):
    Width = Value.WuwWidth
    Height = Value.WuwHeight
    def __init__(self, parent):
        if DEBUG: print "WuwPanel.__init__"
        self.Grid = self.Width / 100
        wx.Panel.__init__(self, parent)

        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.SetForegroundColour(wx.Colour(255, 255, 255))
        #Stock app
        panel = wx.Panel(self)
        self.trying=[]
        style = wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE
        self.text = wx.StaticText(panel, style=style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(self.text, 0, wx.EXPAND)
        sizer.AddStretchSpacer(1)
        panel.SetSizer(sizer)

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
        self.buttonClockDemo=wx.Button(self.tabPageApps,label="Clock",pos=(1*self.Grid,1*self.Grid),
                                       size=(8*self.Grid,2*self.Grid))
        self.buttonPhotoDemo=wx.Button(self.tabPageApps,label="Photo",pos=(1*self.Grid,4*self.Grid),
                                       size=(8*self.Grid,2*self.Grid))
        self.buttonWeatherDemo=wx.Button(self.tabPageApps,label="Weather",pos=(1*self.Grid,7*self.Grid),
                                         size=(8*self.Grid,2*self.Grid))
        self.buttonStockDemo=wx.Button(self.tabPageApps,label="Stock",pos=(1*self.Grid,10*self.Grid),
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
        self.BoxClock=wx.StaticBox(self,pos=(40*self.Grid,30*self.Grid),
                                   size=(20*self.Grid,20*self.Grid))
        self.BoxStock=wx.StaticBox(self,pos=(5*self.Grid,25*self.Grid),
                                     size=(90*self.Grid,50*self.Grid))
        self.BoxClock.threadTime=None
        self.BoxStock.threadTime=None
        self.BoxWeather=wx.StaticBox(self,pos=(40*self.Grid,20*self.Grid),
                                     size=(20*self.Grid,40*self.Grid))
        self.BoxStock=wx.StaticBox(self,pos=(5*self.Grid,25*self.Grid),
                                     size=(60*self.Grid,50*self.Grid))
        self.BoxPhoto=wx.StaticBox(self,pos=(18*self.Grid,16*self.Grid),
                                   size=(64*self.Grid,48*self.Grid))

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
        self.clockDemo = False
        self.photoDemo = False
        self.weatherDemo = False
        self.StockDemo = False
        self.trying = []


        ###Load
        self.__touchlessMgr = TouchlessLib.TouchlessMgr()
        self.__touchlessMgr.RefreshCameraList()
        self.__touchlessMgr.CurrentCamera.ImageCaptured()
        self.__touchlessMgr.CurrentCamera.GetCurrentImage().show()
        self.threadCapture = self.ThreadCapture("Capture", 0.03, self.pictureBoxDisplay, self.__touchlessMgr.CurrentCamera, self)
        self.threadCapture.setDaemon(True)
        self.threadCapture.start()
        self.threadMarker = self.ThreadMarker("Marker", 0.2, self.__touchlessMgr)
        self.threadMarker.setDaemon(True)
        self.threadMarker.start()
        self.gestureLoad()
        time.clock()
        self.BoxClock.Hide()
        self.BoxWeather.Hide()
        self.BoxStock.Hide()
        self.BoxPhoto.Hide()
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
        self.Bind(wx.EVT_LEFT_DOWN, self.WUW_MouseDown)
        self.Bind(wx.EVT_MOTION, self.WUW_MouseMove)
        self.Bind(wx.EVT_LEFT_UP, self.WUW_MouseUp)
        self.btnExit.Bind(wx.EVT_BUTTON, self.btnExit_Click)
        self.btnShowHide.Bind(wx.EVT_BUTTON, self.btnShowHide_Click)
        self.buttonClockDemo.Bind(wx.EVT_BUTTON, self.buttonClockDemo_Click)
        self.buttonPhotoDemo.Bind(wx.EVT_BUTTON, self.buttonPhotoDemo_Click)
        self.buttonWeatherDemo.Bind(wx.EVT_BUTTON, self.buttonWeatherDemo_Click)
        self.buttonStockDemo.Bind(wx.EVT_BUTTON, self.buttonStockDemo_Click)
        self.BoxClock.Bind(wx.EVT_PAINT, self.ShowTime)
        self.BoxPhoto.Bind(wx.EVT_PAINT, self.drawPhoto)
        self.BoxStock.Bind(wx.EVT_PAINT, self.showStock)

        # print self.comboBoxCameras.GetCurrentSelection()
        # print self.threadCapture
        # print dir(self.threadCapture)
        # self.comboBoxCameras.SetSelection(0)
        # print self.comboBoxCameras.GetCurrentSelection()

        self.__addedMarkerCount += 4
        self.__touchlessMgr.SetDefaultMarkers()

        self.nameMarkers()

    #线程——捕获某帧图像 
    class ThreadCapture(threading.Thread):
        def __init__(self, threadname, times, box, cam, panel):
            if DEBUG: print "ThreadCapture.__init__"
            threading.Thread.__init__(self, name=threadname)
            self.__times = times
            self.__stop = False
            self.__box = box
            self.__cam = cam
            self.__panel = panel
        def run(self):
            if DEBUG: print "ThreadCapture.run"
            while not self.__stop:
                self.__cam.ImageCaptured()
                self.__panel.UpdateLatestFrame()
                if self.__box.Shown:
                    wx.CallAfter(self.draw)
                time.sleep(self.__times)
        def stop(self):
            if DEBUG: print "ThreadCapture.stop"
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
        if DEBUG: print "UpdateLatestFrame"
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
        def __init__(self, threadname, times, mgr):
            if DEBUG: print "ThreadMarker.__init__"
            threading.Thread.__init__(self, name=threadname)
            self.__times = times
            self.__mgr = mgr
            self.__stop = False
        def run(self):
            if DEBUG: print "ThreadMarker.run"
            while not self.__stop:
                #if self.__mgr.MarkersCount == 4:
                wx.CallAfter(self.draw)
                time.sleep(self.__times)
        def stop(self):
            if DEBUG: print "ThreadMarker.stop"
            self.__stop = True
        def draw(self):
            self.__mgr.UpdateMarkers(self.__mgr.CurrentCamera.GetCurrentImage())

    #线程——时间显示
    class ThreadTime(threading.Thread):
        def __init__(self, threadname, times, box):
            if DEBUG: print "ThreadTime.__init__"
            threading.Thread.__init__(self, name=threadname)
            self.__times = times
            self.__box = box
            self.__stop = False
        def run(self):
            if DEBUG: print "ThreadTime.run"
            while not self.__stop:
                self.__box.Refresh(True)
                time.sleep(self.__times)
        def stop(self):
            print "ThreadTime.stop"
            self.__stop = True


    ###Environmenmt
    def btnExit_Click(self, event):
        if DEBUG: print "btnExit_Click"
        if self.__touchlessMgr.MarkersCount >= 4:
            self.m = None
            self.n = None
            self.o = None
            self.p = None
        self.GetParent().Close()

    def btnShowHide_Click(self, event):
        if DEBUG: print "btnShowHide_Click"
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
        if DEBUG: print "ResetEnvironment"
        self.__show_settings = False
        self.tabSettings.Hide()
        self.pictureBoxDisplay.Hide()
        self.btnExit.Hide()

    def StopOtherApps(self, event):
        if DEBUG: print "StopOtherApps"
        pass

    ###WUW Management
    def WUW_Destroy(self, event):
        if DEBUG: print "WUW_Destroy"
        self.threadCapture.stop()
        self.threadMarker.stop()
        self.__touchlessMgr.CleanupCameras()
        if not self.BoxClock.threadTime == None:
            self.BoxClock.threadTime.stop()
        if not self.BoxStock.threadTime == None:
            self.BoxStock.threadTime.stop()

    def WUW_Paint(self, event):
        if DEBUG: print "WUW_Paint"
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
        if DEBUG: print "drawLatestImage"
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
        if DEBUG: print "buttonMarkerAdd_Click"
        self.__fAddingMarker = not self.__fAddingMarker
        if self.__fAddingMarker:
            self.buttonMarkerAdd.SetLabel("Cancel Adding Marker")
        else:
            self.buttonMarkerAdd.SetLabel("Add A New Marker")

    def comboBoxMarkers_DropDown(self, event):
        if DEBUG: print "comboBoxMarkers_DropDown"
        pass

    def comboBoxMarkers_SelectedIndexChanged(self, event):
        if DEBUG: print "comboBoxMarkers_SelectedIndexChanged"
        pass

    ##UI Marker Editing
    def checkBoxMarkerHighlight_CheckedChanged(self, event):
        if DEBUG: print "checkBoxMarkerHighlight_CheckedChanged"
        pass

    def checkBoxMarkerSmoothing_CheckedChanged(self, event):
        if DEBUG: print "checkBoxMarkerSmoothing_CheckedChanged"
        pass

    def MarkerThresh_ValueChanged(self, event):
        if DEBUG: print "MarkerThresh_ValueChanged"
        pass

    def buttonMarkerRemove_Click(self, event):
        if DEBUG: print "buttonMarkerRemove_Click"
        pass

    def buttonMarkerSave_Click(self, event):
        if DEBUG: print "buttonMarkerSave_Click"
        pass

    def buttonMarkerLoad_Click(self, event):
        if DEBUG: print "buttonMarkerLoad_Click"
        pass

    ##Display Interaction
    def pictureBoxDisplay_MouseDown(self, event):
        if DEBUG: print "pictureBoxDisplay_MouseDown"
        if not self.__fAddingMarker:
            return
        if not self.__touchlessMgr.CurrentCamera.isOn():
            return
        self.__markerCenter = event.GetPosition() - self.pictureBoxDisplay.GetPosition()
        self.__markerRadius = 0
        self.__drawSelectionAdornment = True

    def pictureBoxDisplay_MouseMove(self, event):
        if DEBUG: print "pictureBoxDisplay_MouseMove"
        if not self.__fAddingMarker:
            return
        if not self.__markerCenter == None:
            dx = event.GetX() - self.pictureBoxDisplay.GetPosition().x - self.__markerCenter.x
            dy = event.GetY() - self.pictureBoxDisplay.GetPosition().y - self.__markerCenter.y
            self.__markerRadius = math.sqrt(dx*dx + dy*dy)

            self.pictureBoxDisplay.Refresh()

    def pictureBoxDisplay_MouseUp(self, event):
        if DEBUG: print "pictureBoxDisplay_MouseUp"
        if not self.__fAddingMarker:
            self.__inBoxArea = False
            return
        if not self.__markerCenter == None:
            dx = event.GetX() - self.pictureBoxDisplay.GetPosition().x - self.__markerCenter.x
            dy = event.GetY() - self.pictureBoxDisplay.GetPosition().y - self.__markerCenter.y
            self.__markerRadius = math.sqrt(dx*dx + dy*dy)

            img = self.__latestFrame
            size = self.pictureBoxDisplay.GetSize()
            self.__markerCenter.x = (self.__markerCenter.x * img.shape[0]) / size.width
            self.__markerCenter.y = (self.__markerCenter.y * img.shape[1]) / size.height
            self.__markerRadius = (self.__markerRadius * img.shape[1]) / size.height
            newMarker = self.__touchlessMgr.AddMarker(str.format("Marker #{0}", self.__addedMarkerCount), img, self.__markerCenter, self.__markerRadius)
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
        if DEBUG: print "nameMarkers"
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
        if DEBUG: print event.X, (int)(event.X * self.__ratioScreenCameraWidth), event.Y, (int)(event.Y * self.__ratioScreenCameraHeight)
        self.labelM.SetPosition(wx.Point((int)(event.X * self.__ratioScreenCameraWidth), (int)(event.Y * self.__ratioScreenCameraHeight)))

    def n_OnChange(self, event):
        if DEBUG: print event.X, (int)(event.X * self.__ratioScreenCameraWidth), event.Y, (int)(event.Y * self.__ratioScreenCameraHeight)
        self.labelN.SetPosition(wx.Point((int)(event.X * self.__ratioScreenCameraWidth), (int)(event.Y * self.__ratioScreenCameraHeight)))

    def o_OnChange(self, event):
        if DEBUG: print event.X, (int)(event.X * self.__ratioScreenCameraWidth), event.Y, (int)(event.Y * self.__ratioScreenCameraHeight)
        self.labelO.SetPosition(wx.Point((int)(event.X * self.__ratioScreenCameraWidth), (int)(event.Y * self.__ratioScreenCameraHeight)))

    def p_OnChange(self, event):
        if DEBUG: print event.X, (int)(event.X * self.__ratioScreenCameraWidth), event.Y, (int)(event.Y * self.__ratioScreenCameraHeight)
        self.labelP.SetPosition(wx.Point((int)(event.X * self.__ratioScreenCameraWidth), (int)(event.Y * self.__ratioScreenCameraHeight)))

    ##Marker Helper Functions

    ##Marker HandSigns Functions

    ###Gesture Buttons


    ###Gesture Functions
    def gestureLoad(self):
        if DEBUG: print "gestureLoad"
        folderName = "Gestures"
        filePath = os.listdir(folderName)
        for fileName in filePath:
            counts = len(fileName)
            if counts > 4:
                if fileName[counts-1]=='l' and fileName[counts-2]=='m' and fileName[counts-3]=='x' and fileName[counts-4]=='.':
                    self.__rec.LoadGesture(folderName + "/" + fileName)


    ###Gesture Mouse Events
    def WUW_MouseDown(self, event):
        if DEBUG: print "WUW_MouseDown"
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
        if DEBUG: print "WUW_MouseMove"
        if self.__inBoxArea:
            self.pictureBoxDisplay_MouseMove(event)
            return
        if self.__isDown:
            self.__points.append(PointR(event.GetX(),event.GetY(),time.clock()*1000))
            self.Refresh(True, wx.Rect(event.GetX()-2,event.GetY()-2,4,4))

    def WUW_MouseUp(self, event):
        if DEBUG: print "WUW_MouseUp"
        if self.__inBoxArea:
            self.pictureBoxDisplay_MouseUp(event)
            return
        if self.__isDown:
            self.__isDown = False
            if len(self.__points) >= 5: # require 5 points for a valid gesture
                print self.__recording
                print self.__rec.NumGestures
                if self.__recording:
                    pass

                elif self.__rec.NumGestures > 0:
                    result = self.__rec.Recognize(self.__points)
                    print result
                    self.lblResult.Label = str.format("{0}: {1} ({2}px, {3}",
                                                 result.Name,
                                                 round(result.Score,2),
                                                 round(result.Distance,2),
                                                 round(result.Angle,2))

                    dic={
                        "clock1":self.buttonClockDemo_Click,
                        "clock2":self.buttonClockDemo_Click,
                        "photo1":self.buttonPhotoDemo_Click,
                        "photo2":self.buttonPhotoDemo_Click,
                        "photo3":self.buttonPhotoDemo_Click,
                        "photo4":self.buttonPhotoDemo_Click,
                        "photo5":self.buttonPhotoDemo_Click,
                        "photo6":self.buttonPhotoDemo_Click,
                        "weather1":self.buttonWeatherDemo_Click,
                        "weather2":self.buttonWeatherDemo_Click,
                        "stock1":self.buttonStockDemo_Click,
                        "stock2":self.buttonStockDemo_Click,
                        }
                    dic[result.Name](event)


    ###Demo Mode
    ##Clock Demo
    def buttonClockDemo_Click(self, event):
        if DEBUG: print "buttonClockDemo_Click"
        if self.clockDemo:
            self.clockDemo = False
            self.labelDemoName.Label = "WUW"
            self.buttonClockDemo.Label = "Clock"
            self.BoxClock.threadTime.stop()
            self.BoxClock.threadTime=None
            self.BoxClock.Hide()
            self.ResetEnvironment()
        else:
            self.StopOtherApps(event)
            self.clockDemo = True
            self.labelDemoName.Label = "Clock"
            self.buttonClockDemo.Label = "Stop Clock"
            self.BoxClock.threadTime = self.ThreadTime("time", 1, self.BoxClock)
            self.BoxClock.threadTime.start()
            self.BoxClock.Show()

    def ShowTime(self, event):
        if DEBUG: print "ShowTime"
        dc = wx.PaintDC(self.BoxClock)
        dc.Clear()
        dc.DrawText(time.strftime("%H:%M:%S", time.localtime(time.time())),
                    8*self.Grid,8*self.Grid)

    ##Photo Demo
    def buttonPhotoDemo_Click(self, event):
        if DEBUG: print "buttonPhotoDemo_Click"
        if self.photoDemo:
            self.photoDemo = False
            self.labelDemoName.Label = "WUW"
            self.buttonPhotoDemo.Label = "Photo"
            self.BoxPhoto.Hide()
            self.ResetEnvironment()
        else:
            self.StopOtherApps(event)
            self.photoDemo = True
            self.labelDemoName.Label = "Photo"
            self.buttonPhotoDemo.Label = "Stop Photo"
            self.BoxPhoto.Show()
            #self.BoxPhoto.Refresh()
            # self.BoxPhoto.Show()
            img = self.__touchlessMgr.CurrentCamera.GetCurrentImage()
            bmp = TouchlessLib.ImageToBitmap(img)
            dc = wx.ClientDC(self.BoxPhoto)
            # dc.DrawBitmap(bmp,0,0)


    def drawPhoto(self, event):
        if DEBUG: print "drawPhoto"
        if self.__latestFrame == None:
            return
        if self.__isDown:
            return
        bmp = TouchlessLib.ImageToBitmap(self.__latestFrame)
        dc = wx.PaintDC(self.BoxPhoto)
        dc.DrawBitmap(bmp,0,0)

    def showStock(self, event):
        # TO FINISH
        """ Function to show the values of the stocks in real time """
        print(ystockquote.get_today_open(symbol))
        print(ystockquote.get_last_trade_price(symbol))
        print(ystockquote.get_change(symbol))
        print(ystockquote.get_eps(symbol))

    ##Weather Demo
    def buttonWeatherDemo_Click(self, event):
        if DEBUG: print "buttonWeatherDemo_Click"
        pass

    ##Stock Demo
    def stock(self):
        for i in self.trying:
            i.Destroy()
        self.trying = []
        stockValue2 = self.trying.append(wx.StaticText(self.BoxStock,-1,str(ystockquote.get_last_trade_price('AC.PA')),pos=(50,50)))
        stockValue3 = self.trying.append(wx.StaticText(self.BoxStock,-1,str(ystockquote.get_last_trade_price('AIR.PA')),pos=(350,50)))
        stockValue4 = self.trying.append(wx.StaticText(self.BoxStock,-1,str(ystockquote.get_last_trade_price('LR.PA')),pos=(650,50)))
        #labelStock = wx.StaticText(self.BoxStock,label=stockValue2,pos=(30,30))
        #self.text.SetLabel(str(stockValue2))
        # set a box that will contain the first stock values
        stock1 = 'Stock value 1:'
        # values to get from the actual stock exchange
        stockLabel1 = 'Accor S.A.'
        stockBox1 = wx.StaticBox(self.BoxStock,-1,stockLabel1, (5, 5), size=(290, 230))
        #Appending stock values on an array for the plot
        self.kept_array = []
        stockValue_kept = self.kept_array.append(wx.StaticText(self.BoxStock,-1,str(ystockquote.get_last_trade_price('AC.PA')),pos=(450,50)))
        if len(self.kept_array) > 3:
            i = 1
            while i <= 10:
                self.kept_array[i-1] = self.kept_array[i]
        #del self.kept_array[3]     

        # mild difference between wxPython26 and wxPython28
        if wx.VERSION[1] < 7:
            plotter = plot.PlotCanvas(stockBox1, pos=(15,10) ,size=(250, 190))
        else:    
            plotter = plot.PlotCanvas(stockBox1)
            plotter.SetInitialSize(size=(400, 300))
        # list of (x,y) data point tuples
        data = [(1,2), (2,3), (3,5), (4,6), (5,8), (6,8), (12,10), (13,4)]
        # draw points as a line
        line = plot.PolyLine(data, colour='black', width=1)
        marker = plot.PolyMarker(data, marker='dot')
        # set up text, axis and draw
        gc = plot.PlotGraphics([line, marker], 'Evolution of Accor SA', 'Time', 'Stock value')
        plotter.Draw(gc, xAxis=(0,15), yAxis=(0,15))

        wx.CallLater(5000, self.stock)

    def buttonStockDemo_Click(self, event):
        print "buttonStockDemo_Click"
        if self.StockDemo:
            self.StockDemo = False
            self.labelDemoName.Label = "WUW"
            self.buttonStockDemo.Label = "Stock"
            self.BoxStock.threadTime.stop()
            self.BoxStock.threadTime=None
            self.BoxStock.Hide()
            self.ResetEnvironment()
        else:
            self.StopOtherApps(event)
            self.StockDemo = True
            self.labelDemoName.Label = "Stock"
            self.buttonStockDemo.Label = "Stop Stock"
            self.BoxStock.threadTime = self.ThreadTime("time", 1, self.BoxStock)
            self.BoxStock.threadTime.start()
            #self.BoxStock.SetBackgroundColour('#ffffff')

            stockLabel2 = 'AIRBUS GROUP'
            stockLabel3 = 'Legrand SA'

            #get the the stock value from ystockquote app
            #stockValue1 = ystockquote.get_last_trade_price('AC.PA')
            #self.labelStock = wx.StaticText(self.BoxStock,label=stockValue1,pos=(50,25))

            stockBox2 = wx.StaticBox(self.BoxStock,-1,stockLabel2, (305, 5), size=(290, 230))

            stockBox3 = wx.StaticBox(self.BoxStock,-1,stockLabel3, (605, 5), size=(290, 230))

            self.BoxStock.Show()
            self.stock()

def main():
    app = wx.App(False)
    frame = wx.Frame(None, wx.ID_ANY, "WUW", size=(WuwPanel.Width,WuwPanel.Height))
    frame.SetTitle("SixthSense Python")
    panel = WuwPanel(frame)
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()

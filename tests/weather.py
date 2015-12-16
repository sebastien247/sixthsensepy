import wx
import  pywapi
import string
import  time as T
from testimage2 import  *



class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        panel = wx.Panel(self,-1)
        #self.panel.SetBackgroundColour('White')
        self.trying=[]
        style = wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE
        self.text = wx.StaticText(panel, style=style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(self.text, 0, wx.EXPAND)
        self.BoxStock=wx.StaticBox(self,pos=(30,35),
                                     size=(300,300))
        sizer.AddStretchSpacer(1)
        panel.SetSizer(sizer)
        self.Weather()
        


       
        

    def Weather(self):
        for i in self.trying:
            i.Destroy()
            
        self.trying = []
        sizer = wx.GridBagSizer()
        temp_actuel=T.time()
        weather_com_result = pywapi.get_weather_from_weather_com('10001')
        yahoo_result = pywapi.get_weather_from_yahoo('10001')
        noaa_result = pywapi.get_weather_from_noaa('KJFK')
        weather1 = self.trying.append(wx.StaticText(self.BoxStock,-1,str("Yahoo says: It is " + string.lower(yahoo_result['condition']['text']) + " and " +
         yahoo_result['condition']['temp'] + " C now "),pos=(50,50)))
       # labelStock = wx.StaticText(self.BoxStock,-1,label=weather1,pos=(30,30))
        #self.text.SetLabel(str(labelStock))
        #weather2 = "Weather.com says: It is " + string.lower(weather_com_result['current_conditions']['text']) + " and " + weather_com_result['current_conditions']['temperature'] + " C now "
        #labelStock = wx.StaticText(self.BoxStock,label=weather2,pos=(30,80))
        #self.text.SetLabel(str(labelStock))

        wx.CallLater(10000,self.Weather)
        message=string.lower(yahoo_result['condition']['text'])
        if message=="fair":
            #from PIL import Image
            #bidule = Image.open("image/nuage-noir-avec-de-la-pluie.jpg")
            #bidule.show()
            
            app= Application(redirect=True)
            app.MainLoop()

        

class App():     
      def OnInit(self):
            app= wx.App()
            frame=MyFrame(None, -1 , 'weather.py')
            frame.Show(True)
            frame.Centre()
            app.MainLoop()
            return True
app=App()
app.OnInit()
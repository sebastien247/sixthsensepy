#coding=utf-8

from App import App
import wx
import pywapi
import os

class AppWeather(App):
    def __init__(self, WuwPanel):
        App.__init__(self, WuwPanel)

        self.trying=[]

        self.name = "Weather"
        self.button = wx.Button(self.tabPageApps,label="Wheather",pos=(1*self.Grid,7*self.Grid),
                                       size=(8*self.Grid,2*self.Grid))

        self.box = wx.StaticBox(self.wuw,pos=(40*self.Grid,20*self.Grid),
                                     size=(20*self.Grid,40*self.Grid))

        self.box.Hide()
        self.button.Bind(wx.EVT_BUTTON, self.Weather)
        
        self.after_init()

    def Weather(self):
        for i in self.trying:
            i.Destroy()
        self.trying = []
        sizer = wx.GridBagSizer()

        city='limoges'
        lookup = pywapi.get_location_ids(city)

        #work around to access last item of dictionary
        for i in lookup:
            location_id = i

        weather_com_result = pywapi.get_weather_from_weather_com(location_id)
        yahoo_result = pywapi.get_weather_from_yahoo(location_id)
        self.box.SetForegroundColour(wx.Colour(0, 0, 0))

        txt_temperature = u"%s°C" % (yahoo_result['condition']['temp'])
        self.text = wx.StaticText(self.wuw,-1,txt_temperature, pos=(0,0))
        font1 = wx.Font(38, wx.NORMAL, wx.NORMAL, wx.NORMAL)
        self.text.SetFont(font1)
        text_align = self.text.GetTextExtent(txt_temperature)
        self.text.SetSize(text_align[0],text_align[1])
        self.text.SetPosition(((100*self.Grid/2)-text_align[0]/2, 100*self.Grid/2-text_align[1]/2))
        weather1 = self.trying.append(self.text)     
        pos_img_weather = (100*self.Grid/2-225/2, 100*self.Grid/2-225-text_align[1])

        if  'swon' in str.lower(str(yahoo_result['condition']['text'])):
            pass
            img= wx.Image(os.path.realpath('images/nuage-ensoleillé.png.png'),wx.BITMAP_TYPE_PNG)
            bmp= wx.BitmapFromImage(img)
            self.staticBmp= wx.StaticBitmap(self.wuw,wx.ID_ANY,bmp,pos=pos_img_weather)
        elif  'cloudy' in str.lower(str(yahoo_result['condition']['text'])):
            pass
            img= wx.Image(os.path.realpath('images/nuage.png'),wx.BITMAP_TYPE_PNG)
            bmp= wx.BitmapFromImage(img)
            self.staticBmp= wx.StaticBitmap(self.wuw,wx.ID_ANY,bmp,pos=pos_img_weather)   
        elif 'rain' in str.lower(str(yahoo_result['condition']['text'])):
            pass
            img= wx.Image(os.path.realpath('images/pluie.png'),wx.BITMAP_TYPE_PNG)
            bmp= wx.BitmapFromImage(img)
            self.staticBmp= wx.StaticBitmap(self.wuw,wx.ID_ANY,bmp,pos=pos_img_weather)    
        elif  'sun' in str.lower(str(yahoo_result['condition']['text'])):
            pass
            img= wx.Image(os.path.realpath('images/sun.jpeg'),wx.BITMAP_TYPE_JPEG)
            bmp= wx.BitmapFromImage(img)
            self.staticBmp= wx.StaticBitmap(self.wuw,wx.ID_ANY,bmp,pos=pos_img_weather)
        wx.CallLater(10000,self.Weather)

    def start(self):
        self.box.threadTime = self.wuw.ThreadTime("time", 1, self.box)
        self.box.threadTime.start()
        self.box.Show()
        self.Weather()

    def end(self):
        self.box.threadTime=None
        self.staticBmp.Hide()
        self.text.Hide()
        self.box.Hide()

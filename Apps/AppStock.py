from App import App
import wx
import ystockquote


class AppStock(App):
    def __init__(self, WuwPanel):
        App.__init__(self, WuwPanel)

        self.trying = []
        self.getChange = []

        self.name = "stock"
        self.button = wx.Button(self.tabPageApps,label="Stock",pos=(1*self.Grid,10*self.Grid), size=(8*self.Grid,2*self.Grid))

        self.box = wx.StaticBox(self.wuw,pos=(5*self.Grid,25*self.Grid), size=(90*self.Grid,50*self.Grid))

        self.box.threadTime=None
        self.box.Hide()
        self.box.Bind(wx.EVT_PAINT, self.show_stock)

        self.after_init()

    def show_stock(self, event):
        # TO FINISH
        """ Function to show the values of the stocks in real time """

    def stock(self):
        """Function that display different stocke's values """
        for i in self.trying:
            i.Destroy()
        self.trying = []
        # values to get from the actual stock exchange
        text2 = wx.StaticText(self.box,-1,str(ystockquote.get_volume('AC.PA')),pos=(self.Grid*50/10,self.Grid*50/10))
        text3 = wx.StaticText(self.box,-1,str(ystockquote.get_volume('AIR.PA')),pos=(self.Grid*350/10,self.Grid*50/10))
        text4 = wx.StaticText(self.box,-1,str(ystockquote.get_volume('EN.PA')),pos=(self.Grid*650/10,self.Grid*50/10))
        text5 = wx.StaticText(self.box,-1,str(ystockquote.get_volume('CAP.PA')),pos=(self.Grid*50/10,self.Grid*290/10))
        text6 = wx.StaticText(self.box,-1,str(ystockquote.get_volume('UG.PA')),pos=(self.Grid*350/10,self.Grid*290/10))
        text7 = wx.StaticText(self.box,-1,str(ystockquote.get_volume('ORA.PA')),pos=(self.Grid*650/10,self.Grid*290/10))
        text2.SetForegroundColour(wx.Colour(0,0,0))
        text3.SetForegroundColour(wx.Colour(0,0,0))
        text4.SetForegroundColour(wx.Colour(0,0,0))
        text5.SetForegroundColour(wx.Colour(0,0,0))
        text6.SetForegroundColour(wx.Colour(0,0,0))
        text7.SetForegroundColour(wx.Colour(0,0,0))
        font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        text2.SetFont(font)
        text3.SetFont(font)
        text4.SetFont(font)
        text5.SetFont(font)
        text6.SetFont(font)
        text7.SetFont(font)
        stockValue2 = self.trying.append(text2)
        stockValue3 = self.trying.append(text3)
        stockValue4 = self.trying.append(text4)        
        stockValue5 = self.trying.append(text5)
        stockValue6 = self.trying.append(text6)
        stockValue7 = self.trying.append(text7)
        #getting the change figure of each value to display the right evolution
        for j in self.getChange:
            j.Destroy()
        self.getChange = []
        test2 = ystockquote.get_change('AC.PA')
        value2 = wx.StaticText(self.box,-1,test2,pos=(self.Grid*150/10,self.Grid*50/10))
        changeValue2 = self.getChange.append(value2)
        test3 = str(ystockquote.get_change('AIR.PA'))
        value3 = wx.StaticText(self.box,-1,test3,pos=(self.Grid*450/10,self.Grid*50/10))
        changeValue3 = self.getChange.append(value3)
        test4 = str(ystockquote.get_change('EN.PA'))
        value4 = wx.StaticText(self.box,-1,test4,pos=(self.Grid*750/10,self.Grid*50/10))
        changeValue4 = self.getChange.append(value4)
        test5 = ystockquote.get_change('CAP.PA')
        value5 = wx.StaticText(self.box,-1,test5,pos=(self.Grid*150/10,self.Grid*290/10))
        changeValue5 = self.getChange.append(value5)
        test6 = str(ystockquote.get_change('UG.PA'))
        value6 = wx.StaticText(self.box,-1,test6,pos=(self.Grid*450/10,self.Grid*290/10))
        changeValue6 = self.getChange.append(value6)
        test7 = str(ystockquote.get_change('ORA.PA'))
        value7 = wx.StaticText(self.box,-1,test7,pos=(self.Grid*750/10,self.Grid*290/10))
        changeValue7 = self.getChange.append(value7)
        #changing the color of labels depending on the change
        if test2.find('-')!=-1:
            value2.SetForegroundColour(wx.Colour(255,0,0))
        elif test2.find('+')!=-1:
            value2.SetForegroundColour(wx.Colour(0,150,0))
        if test3.find('-')!=-1:
            value3.SetForegroundColour(wx.Colour(255,0,0))
        elif test3.find('+')!=-1:
            value3.SetForegroundColour(wx.Colour(0,150,0))
        if test4.find('-')!=-1:
            value4.SetForegroundColour(wx.Colour(255,0,0))
        elif test4.find('+')!=-1:
            value4.SetForegroundColour(wx.Colour(0,150,0))
        if test5.find('-')!=-1:
            value5.SetForegroundColour(wx.Colour(255,0,0))
        elif test5.find('+')!=-1:
            value5.SetForegroundColour(wx.Colour(0,150,0))
        if test6.find('-')!=-1:
            value6.SetForegroundColour(wx.Colour(255,0,0))
        elif test6.find('+')!=-1:
            value6.SetForegroundColour(wx.Colour(0,150,0))
        if test7.find('-')!=-1:
            value7.SetForegroundColour(wx.Colour(255,0,0))
        elif test7.find('+')!=-1:
            value7.SetForegroundColour(wx.Colour(0,150,0))
        value2.SetFont(font)
        value3.SetFont(font)
        value4.SetFont(font)
        value5.SetFont(font)
        value6.SetFont(font)
        value7.SetFont(font) 
        wx.CallLater(5000, self.stock)


    def start(self):
        self.box.threadTime = self.wuw.ThreadTime("time", 1, self.box)
        self.box.threadTime.start()
        stockLabel1 = 'Accor S.A.'
        stockLabel2 = 'AIRBUS GROUP'
        stockLabel3 = 'Legrand SA'
        stockLabel4 = 'Cap Gemini S.A.'
        stockLabel5 = 'Peugeot S.A.'
        stockLabel6 = 'Orange'
        # set a box that will contain the first stock values
        stockBox1 = wx.StaticBox(self.box,-1,stockLabel1, (self.Grid*5/10, self.Grid*5/10), size=(self.Grid*29, self.Grid*23))
        stockBox2 = wx.StaticBox(self.box,-1,stockLabel2, (self.Grid*305/10, self.Grid*5/10), size=(self.Grid*29, self.Grid*23))
        stockBox3 = wx.StaticBox(self.box,-1,stockLabel3, (self.Grid*605/10, self.Grid*5/10), size=(self.Grid*29, self.Grid*23))
        stockBox4 = wx.StaticBox(self.box,-1,stockLabel4, (self.Grid*5/10, self.Grid*240/10), size=(self.Grid*29, self.Grid*23))
        stockBox5 = wx.StaticBox(self.box,-1,stockLabel5, (self.Grid*305/10, self.Grid*240/10), size=(self.Grid*29, self.Grid*23))
        stockBox6 = wx.StaticBox(self.box,-1,stockLabel6, (self.Grid*605/10, self.Grid*240/10), size=(self.Grid*29, self.Grid*23))
        stockBox1.SetForegroundColour(wx.Colour(0,0,0))
        stockBox2.SetForegroundColour(wx.Colour(0,0,0))
        stockBox3.SetForegroundColour(wx.Colour(0,0,0))
        stockBox4.SetForegroundColour(wx.Colour(0,0,0))
        stockBox5.SetForegroundColour(wx.Colour(0,0,0))
        stockBox6.SetForegroundColour(wx.Colour(0,0,0))
        self.box.Show()
        self.stock()

    def end(self):
        self.box.threadTime.stop()
        self.box.threadTime=None
        self.box.Hide()
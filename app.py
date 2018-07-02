
#-*- coding: UTF-8 -*-
import wx
from mainframe import MainFrame

class MyApp(wx.App):
    """wxPython program start"""
    def OnInit(self):
        self.mainFrame = MainFrame(None, size = (wx.DisplaySize()[0]-50,wx.DisplaySize()[1]),
                                   title = "Flash download v1.0 2018-06-30")
        self.SetTopWindow(self.mainFrame)
        return True

def main():
    app = MyApp(False)
    app.MainLoop()

if __name__ == "__main__":
    main()

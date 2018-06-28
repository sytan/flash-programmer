
#-*- coding: UTF-8 -*-
import wx
import os,time
from dll.siUtil import *
from executor import Excutor

class MainFrame(wx.Frame):
    """MainFrame class"""
    def __init__(self, parent, ID = wx.ID_ANY, title = "",pos = wx.DefaultPosition,
                 size = wx.DefaultSize,style = wx.DEFAULT_FRAME_STYLE,name = "MainFrame"):
        super(MainFrame, self).__init__(parent, ID, title,pos = pos, size = size, style = style, name = name)
        # self.Bind(wx.EVT_CLOSE ,self.OnCloseWindow)
        self.panel = wx.Panel(self,-1)
        self.panel.SetBackgroundColour('white')


        self.EFMBB8FilePath = None
        self.ATTNY13FilePath = None
        self.executor = Excutor(self)
        self.executor.setDaemon(True)
        self.executor.start()

        self.InitMenu()
        self.createdFileBrowerUI()
        self.SelectFlash()
        self.creatResultDisplay()
        self.createButton()
        self.createFileBrowser()
        self.Show(True)
        self.OnOpenWindow()

    def OnOpenWindow(self):
        pass
        # dlg = wx.MessageDialog(None,"需要配置端口吗？\n如果端口没有变动，一般不用配置","提示",wx.CANCEL|wx.OK|wx.ICON_EXCLAMATION)
        # dlg.SetOKCancelLabels("Yes","No")
        # result = dlg.ShowModal()
        # dlg.Destroy()
        # if result == wx.ID_OK:
        #     pass
        # else:
        #     pass
    def SelectFlash(self):
        self.flashList = ["EFMBB8","ATTNY13"]
        size = (500,100)
        self.flashSlector = wx.RadioBox(self.panel, -1, "Flash selector",(50,100),size,
            self.flashList,2,wx.RA_SPECIFY_COLS)
    def creatResultDisplay(self):
         self.resultDisplay = wx.TextCtrl(self.panel, -1, "",size = (200,100), pos = (500, 400))
         self.resultDisplay.SetValue("RESULT")

    def createdFileBrowerUI(self):
        self.EFMBB8TextCtrl = wx.TextCtrl(self.panel, -1, "",size = (350,25), pos = (50, 0))
        self.EFMBB8FileButton = wx.Button(self.panel,label="选择烧录文件",pos=(400,0))
        self.Bind(wx.EVT_BUTTON, self.OnClickEFMBB8File, self.EFMBB8FileButton)
        self.ATTNY13TextCtrl = wx.TextCtrl(self.panel, -1, "",size = (350, 25), pos = (50, 50))
        self.ATTNY13FileButton = wx.Button(self.panel,label="选择烧录文件",pos=(400,50))
        self.Bind(wx.EVT_BUTTON, self.OnClickATTNY13File, self.ATTNY13FileButton)
    def OnClickEFMBB8File(self, event):
        if self.EFMBB8Dialog.ShowModal() == wx.ID_OK:
            self.EFMBB8FilePath =  self.EFMBB8Dialog.GetPath()
            self.EFMBB8TextCtrl.SetValue(self.EFMBB8FilePath)
            print self.EFMBB8FilePath

    def OnClickATTNY13File(self, event):
        if self.ATTNY13Dialog.ShowModal() == wx.ID_OK:
            self.ATTNY13FilePath = self.ATTNY13Dialog.GetPath()
            self.ATTNY13TextCtrl.SetValue(self.ATTNY13FilePath)
            print self.ATTNY13FilePath

    def createFileBrowser(self):
        wildcard = "*.hex"
        self.fileDialog = wx.FileDialog(self.panel, "Open XYZ file", wildcard="XYZ files (*.xyz)|*.xyz",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        # self.fileDialog.ShowModal()
        self.EFMBB8Dialog = wx.FileDialog(self.panel,"选择烧录文件",os.getcwd(),"",wildcard, wx.FD_OPEN)
        self.ATTNY13Dialog = wx.FileDialog(self.panel,"选择烧录文件",os.getcwd(),"",wildcard, wx.FD_OPEN)
    def createButton(self):
        self.buttonOne = wx.Button(self.panel,label="buttonOne",pos=(50,200),size=(100,50))
        self.Bind(wx.EVT_BUTTON, self.OnClickOne, self.buttonOne)
        self.buttonOne.Disable()
        self.buttonTwo = wx.Button(self.panel,label="buttonTwo",pos=(200,200),size=(100,50))
        self.buttonTwo.Disable()
        self.buttonThree = wx.Button(self.panel,label="buttonThree",pos=(350,200),size=(100,50))
        self.buttonThree.Disable()
        self.buttonFour = wx.Button(self.panel,label="buttonFour",pos=(500,200),size=(100,50))
        self.buttonFour.Disable()
        pass


    def OnClickOne(self, event):
        self.buttonOne.Disable()
        flashType = self.flashList[self.flashSlector.GetSelection()]
        print "the flash type is ", flashType
        self.executor.StartExecute(flashType)

    def UpdateTestResult(self, result):
        self.buttonOne.Enable()
        print "the download result is :", result
        if result == True :
            self.resultDisplay.SetValue("PASS")
        else:
            self.resultDisplay.SetValue("FAIL")

    def InitMenu(self):
        #create menuBar
        self.menuBar = wx.MenuBar()

        self.configMenu = wx.Menu()
        self.item = self.configMenu.Append(10001,"初始化\tF1","初始化")   #append a item to menu
        self.Bind(wx.EVT_MENU, self.DeviceInit, self.item)  # Create and assign a menu event.
        self.item = self.configMenu.Append(10002,"文件\tF2","退出")   #append a item to menu
        self.Bind(wx.EVT_MENU, self.ConfigPath, self.item)  # Create and assign a menu event.
        self.menuBar.Append(self.configMenu,"菜单")       #append menu to menuBar

        self.systemMenu = wx.Menu()
        self.item = self.systemMenu.Append(30001,"全屏\tF12","全屏")   #append a item to menu
        self.Bind(wx.EVT_MENU, self.FullScreen, self.item)  # Create and assign a menu event.
        self.item = self.systemMenu.Append(30002,"退出\tctrl-x","退出")   #append a item to menu
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, self.item)  # Create and assign a menu event.
        self.menuBar.Append(self.systemMenu,"系统")       #append menu to menuBar

        self.SetMenuBar(self.menuBar)  #Append menuBar to mainFrame

    def DeviceInit(self,event):
        avrStatus = self.CheckAvrProgrammer()
        usbStatus = self.CheckUsbDebugger()
        print "avrstatus,usbStatus :",avrStatus,usbStatus
        if avrStatus == True and usbStatus == True:

            self.buttonOne.Enable()
            self.buttonTwo.Enable()
            self.buttonThree.Enable()
            self.buttonFour.Enable()
            print "avr programmer is ready"
            print "usb debugger is ready"
        if avrStatus != True:
            print "avr programmer is missing"
        if usbStatus != True:
            print "usb debugger is missing"

    def CheckAvrProgrammer(self):
        # Check whether avr programmer is connected
        cmd = "atprogram list"
        self.popen=os.popen(cmd)
        time.sleep(1)
        text = self.popen.read()
        print "the find is"
        print text.find("avrispmk2")
        if text.find("avrispmk2") != -1:
            return True
        else:
            return False

    def CheckUsbDebugger(self):
        err,n = USBDebugDevices()
        print "the err and n is ", err, n
        if err == 0 and n == 1:
            return True
        else:
            return False

    def ConfigPath(self,event):
        print "i'm config path"
        pass

    def FullScreen(self,event):    #menu 系统-> 文件
        style=wx.FULLSCREEN_ALL^wx.FULLSCREEN_NOMENUBAR^wx.FULLSCREEN_NOCAPTION^wx.FULLSCREEN_NOSTATUSBAR
        self.ShowFullScreen(not self.IsFullScreen(),style= style)
        print "i'm full screen"

    def OnCloseWindow(self, event):
        """quit program """
        dlg = wx.MessageDialog(None,"确定要退出吗？","警告", wx.CANCEL|wx.OK|wx.ICON_EXCLAMATION)
        dlg.SetOKCancelLabels("是","否")
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.executor.Close()
            self.Destroy()
        else:
            pass


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
        self.Bind(wx.EVT_CLOSE ,self.OnCloseWindow)

        self.panel = wx.Panel(self,-1)
        # self.panel.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.panel.SetBackgroundColour('white')

        self.subPanel = wx.Panel(self.panel,-1)
        self.subPanel.SetBackgroundColour('white')
        # self.subPanel.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        image = wx.Image("pic/jig.png", type = wx.BITMAP_TYPE_PNG, index = -1)
        w = image.GetWidth()
        h = image.GetHeight()
        self.subPanel.SetSize(w,h)
        subPanelImage = wx.StaticBitmap(self.subPanel, -1, wx.Bitmap(image))

        self.flashType = "EFMBB8"
        self.isDeviceInit = False

        self.EFMBB8FilePath = None
        self.ATTNY13FilePath = None
        self.executor = Excutor(self)
        self.executor.setDaemon(True)
        self.executor.start()

        self.InitMenu()
        self.createFileBrowser()
        self.CreateUI()
        self.InitUI()
        self.Show(True)
        self.OnOpenWindow()

    def InitUI(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.tittle, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(self.panel), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        hbox1.Add((10,1),0,wx.EXPAND)
        hbox1.Add(self.EFMBB8Radio,0,wx.EXPAND)
        hbox1.Add(self.EFMBB8TextCtrl,1,wx.EXPAND)
        hbox1.Add(self.EFMBB8FileButton,0,wx.EXPAND)
        # hbox1.Add((100,1),1,wx.EXPAND)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add((10,1),0,wx.EXPAND)
        hbox2.Add(self.ATTNY13Radio,0, wx.EXPAND)
        hbox2.Add(self.ATTNY13TextCtrl,1, wx.EXPAND)
        hbox2.Add(self.ATTNY13FileButton,0,wx.EXPAND)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add((10,1), 1, wx.EXPAND)
        hbox3.Add(self.subPanel, 0 )
        hbox3.Add((10,1), 1, wx.EXPAND)

        mainSizer.Add(hbox1, 0, wx.EXPAND, 0)
        mainSizer.Add(hbox2, 0, wx.EXPAND,0)
        mainSizer.Add((1,1), 1, wx.EXPAND)
        mainSizer.Add(hbox3, 1, wx.EXPAND)
        mainSizer.Add((1,1), 1, wx.EXPAND)

        # mainSizer.Add(self.resultDisplay,0,wx.EXPAND, 0)
        mainSizer.Add(self.startButton,0,wx.EXPAND)

        # subSizer = wx.BoxSizer(wx.HORIZONTAL)
        # subSizer.Add(self.resultDisplay,0,wx.EXPAND)
        # self.subPanel.SetSizer(subSizer)

        self.panel.SetSizer(mainSizer)

        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)

    def CreateUI(self):
        tittleFont = wx.Font(50, wx.DECORATIVE,wx.NORMAL, wx.BOLD)
        self.tittle = wx.StaticText(self.panel, -1, "请选择烧录芯片及烧录文件")
        self.tittle.SetFont(tittleFont)

        #flash type select

        font = wx.Font(30, wx.DECORATIVE,wx.NORMAL, wx.BOLD)
        self.EFMBB8Radio = wx.RadioButton(self.panel, -1, "EFMBB8", style = wx.RB_GROUP, size = (200,50))
        self.EFMBB8Radio.SetFont(font)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, self.EFMBB8Radio)
        self.ATTNY13Radio = wx.RadioButton(self.panel, -1, "ATTNY13", size = (200, 50))
        self.ATTNY13Radio.SetFont(font)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, self.ATTNY13Radio)

        #flash file
        pathFont = wx.Font(25, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)
        self.EFMBB8TextCtrl = wx.TextCtrl(self.panel, -1, "", size = (600, 50))
        self.EFMBB8TextCtrl.SetFont(pathFont)
        self.EFMBB8TextCtrl.Disable()
        self.ATTNY13TextCtrl = wx.TextCtrl(self.panel, -1, "",size = (600, 50))
        self.ATTNY13TextCtrl.SetFont(pathFont)
        self.ATTNY13TextCtrl.Disable()

        #flash file browser button
        selectFont = wx.Font(25, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)
        self.EFMBB8FileButton = wx.Button(self.panel,label="选择文件")
        self.EFMBB8FileButton.SetFont(selectFont)
        self.Bind(wx.EVT_BUTTON, self.OnClickEFMBB8File, self.EFMBB8FileButton)
        self.ATTNY13FileButton = wx.Button(self.panel,label="选择文件")
        self.ATTNY13FileButton.SetFont(selectFont)
        self.Bind(wx.EVT_BUTTON, self.OnClickATTNY13File, self.ATTNY13FileButton)
        self.ATTNY13FileButton.Disable()

        #result display
        resultFont = wx.Font(60, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)
        self.resultDisplay = wx.StaticText(self.subPanel, -1, "初始化结果",size = (600, 100), style = wx.ALIGN_CENTER)
        self.resultDisplay.SetFont(resultFont)
        self.resultDisplay.SetPosition((315, 20))
        self.resultDisplay.Centre(wx.HORIZONTAL)

        # button

        buttonFont = wx.Font(40, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)
        self.startButton = wx.Button(self.panel,label="点击，开始烧录",size=(100,100))
        self.startButton.SetFont(buttonFont)
        self.startButton.SetBackgroundColour("#F0F0F0")
        self.Bind(wx.EVT_BUTTON, self.OnClickStartButton, self.startButton)

        self.startButton.Disable()

    # def OnKeyUp(self, event):
    #     key = event.GetKeyCode()
    #     print "key: ",key
    #     if key == wx.WXK_SPACE and self.isDeviceInit == True :
    #         self.OnClickStartButton(wx.EVT_BUTTON)

    def OnRadio(self, event):
        radioSelected = event.GetEventObject()
        self.flashType = radioSelected.GetLabel()
        if self.flashType == "EFMBB8":
            self.EFMBB8FileButton.Enable()
            self.ATTNY13FileButton.Disable()
        else:
            self.EFMBB8FileButton.Disable()
            self.ATTNY13FileButton.Enable()

        print "flash selected: ",radioSelected.GetLabel()
    def creatResultDisplay(self):
         self.resultDisplay = wx.TextCtrl(self.panel, -1, "",size = (200,100))
         self.resultDisplay.SetValue("RESULT")

    def OnClickEFMBB8File(self, event):
        if self.EFMBB8Dialog.ShowModal() == wx.ID_OK:
            path = self.EFMBB8Dialog.GetPath()
            if self.ATTNY13FilePath == None or path != self.ATTNY13FilePath:
                self.EFMBB8FilePath = path
                self.EFMBB8TextCtrl.SetValue(path)
                print "file path of EFMBB8: ",self.EFMBB8FilePath
            else:
                wx.MessageBox("请选择一个不同的文件")

    def OnClickATTNY13File(self, event):
        if self.ATTNY13Dialog.ShowModal() == wx.ID_OK:
            path = self.ATTNY13Dialog.GetPath()
            if self.EFMBB8FilePath == None or path != self.EFMBB8FilePath:
                self.ATTNY13FilePath = path
                self.ATTNY13TextCtrl.SetValue(path)
                print "file path of ATTNY13: ",self.ATTNY13FilePath
            else:
                wx.MessageBox("请选择一个不同的文件")

    def createFileBrowser(self):
        wildcard = "*.hex"
        self.fileDialog = wx.FileDialog(self.panel, "Open XYZ file", wildcard="XYZ files (*.xyz)|*.xyz",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        # self.fileDialog.ShowModal()
        self.EFMBB8Dialog = wx.FileDialog(self.panel,"选择烧录文件",os.getcwd(),"",wildcard, wx.FD_OPEN)
        self.ATTNY13Dialog = wx.FileDialog(self.panel,"选择烧录文件",os.getcwd(),"",wildcard, wx.FD_OPEN)

    def OnClickStartButton(self, event):
        isFile = False
        if self.flashType == "EFMBB8" and self.EFMBB8FilePath != None:
            isFile = True
        if self.flashType == "ATTNY13" and self.ATTNY13FilePath != None:
            isFile = True
        if isFile == True:
            self.startButton.Disable()
            self.startButton.SetLabel("进行中，勿动")
            self.resultDisplay.Show(False)
            print "flash type: ", self.flashType
            self.executor.StartExecute(self.flashType)
        else:
            wx.MessageBox("请选择烧录文件")
        # self.startButton.SetFocus()

    def UpdateTestResult(self, result):
        self.startButton.Enable()
        print "download result: ", result
        if result == True :
            self.resultDisplay.SetLabel("通过")
            self.resultDisplay.SetForegroundColour("blue")
        else:
            self.resultDisplay.SetLabel("失败")
            self.resultDisplay.SetForegroundColour("red")

        self.startButton.SetLabel("点击，开始烧录")
        self.resultDisplay.Show(True)
        self.startButton.SetFocus()

    def InitMenu(self):
        #create menuBar
        self.menuBar = wx.MenuBar()

        self.configMenu = wx.Menu()
        self.item = self.configMenu.Append(10001,"初始化\tF1","初始化")   #append a item to menu
        self.Bind(wx.EVT_MENU, self.DeviceInit, self.item)  # Create and assign a menu event.
        self.item = self.configMenu.Append(10001,"测试模式\tF2","测试模式")   #append a item to menu
        self.Bind(wx.EVT_MENU, self.TestMode, self.item)  # Create and assign a menu event.
        self.menuBar.Append(self.configMenu,"初始化")       #append menu to menuBar

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
        if avrStatus == True and usbStatus == True:
            self.isDeviceInit = True
            self.startButton.Enable()
            self.resultDisplay.SetLabel("初始化成功")
            self.resultDisplay.SetForegroundColour("blue")
            wx.MessageBox("初始化成功")
            print "avr programmer: ready"
            print "usb debugger: ready"

        if avrStatus != True:
            self.isDeviceInit = False
            self.startButton.Disable()
            self.resultDisplay.SetLabel("初始化失败")
            self.resultDisplay.SetForegroundColour("red")
            wx.MessageBox("初始始化失败\n未检测到avrispmk2,请连接后重试")
            print "avr programmer: missing"

        if usbStatus != True:
            self.isDeviceInit = False
            self.startButton.Disable()
            self.resultDisplay.SetLabel("初始化失败")
            wx.MessageBox("初始始化失败\n未检测到USB debugger,请连接后重试")
            print "usb debugger: missing"

    def TestMode(self, event):
        self.startButton.Enable()

    def CheckAvrProgrammer(self):
        # Check whether avr programmer is connected
        cmd = "atprogram list"
        self.popen=os.popen(cmd)
        time.sleep(1)
        text = self.popen.read()
        print cmd + ": "
        print text
        if text.find("avrispmk2") != -1:
            return True
        else:
            return False

    def CheckUsbDebugger(self):
        err,n = USBDebugDevices()
        print "err and n: ", err, n
        if err == 0 and n == 1:
            return True
        else:
            return False

    def FullScreen(self,event):    #menu 系统-> 文件
        style=wx.FULLSCREEN_ALL^wx.FULLSCREEN_NOMENUBAR^wx.FULLSCREEN_NOCAPTION^wx.FULLSCREEN_NOSTATUSBAR
        self.ShowFullScreen(not self.IsFullScreen(),style= style)

    def OnOpenWindow(self):
        self.DeviceInit(wx.EVT_MENU)

    def OnCloseWindow(self, event):
        #quit program
        dlg = wx.MessageDialog(None,"确定要退出吗？","警告", wx.CANCEL|wx.OK|wx.ICON_EXCLAMATION)
        dlg.SetOKCancelLabels("是","否")
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.executor.Close()
            self.Destroy()
        else:
            pass

#-*- coding: UTF-8 -*-
import wx, time, os , threading ,string
from dll.siUtil import *
import subprocess

"""thread to run the executor """
class Excutor(threading.Thread):
    def __init__(self,frame):
        super(Excutor, self).__init__()
        self.frame = frame
        self.varsDefine()

    def varsDefine(self):
        self.popenSubject = None
        self.isClose = False
        self.startTest = False
        self.flashType = None

    def Close(self):
        self.isClose = True

    def StartExecute(self, flashType):
        self.startTest = True
        self.flashType = flashType

    def run(self):
        while not self.isClose:
            if self.startTest == True:
                result = self.runScript(self.flashType)

                self.startTest = False#assume it's true
                wx.CallAfter(self.frame.UpdateTestResult,result)
            else:
                time.sleep(0.5)

    def runScript(self, flashType):
        if flashType == "EFMBB8":
            result = self.DownloadEFM8()
        elif flashType == "ATTNY13":
            result = self.DownloadATTNY13()

        return result

    def DownloadEFM8(self):
        result = False
        errCode = ConnectUSB()
        if errCode != 0:
            print "ConnectUSB: ", errCode
            return result
        if Connected() == 1:
            print "device connected"
        else:
            return result
        print "start to download"
        errCode = Download(self.frame.EFMBB8FilePath)
        if errCode != 0:
            print "Download: ", errCode
            return result
        else:
            DisconnectUSB()
            print "download finish, disconnect usb"
            # start to verify
            print "start to verify"

            cmd = 'FlashUtilCL VerifyUSB '+ self.frame.EFMBB8FilePath +' "" 1'
            popen = os.popen(cmd)
            text = popen.read()
            print cmd + ": "
            print text
            if "Failed Verifying Hex File" in text:
                result = False
                print "verify failed"
            elif "Could Not connect with target boardUnknown device" in text:
                result = False
                print "connect to device failed"
            elif text != "":
                result = False
            else:
                result = True

        return result

    def DownloadATTNY13(self):
        result = False

        cmd = "atprogram -t avrispmk2 -i isp -d attiny13a program -c -fl -f "+self.frame.ATTNY13FilePath
        # cmd = "atprogram -t avrispmk2 -i isp -d attiny13a program -c -fl -f eko.hex"
        print "start to download"
        p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        text = out + err
        print cmd + ": "
        print text
        if "Programming completed successfully" in text :
            print "program is ok"
            result = True
        else:
            result = False
            return result
        #start to verify
        print "start to verify"
        cmd = "atprogram -t avrispmk2 -i isp -d ATtiny13A verify -fl -f "+ self.frame.ATTNY13FilePath
        # cmd = "atprogram -t avrispmk2 -i isp -d ATtiny13A verify -fl -f eKo.hex"
        p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        text = out + err
        print cmd + ": "
        print text

        if "Verification OK" in text :
            print "verify is ok"
            result = True
        else:
            result = False
            print text

        return result

    def readResponse(self, popen, timeout):
        buffer = ""
        startTime = time.time()
        while True:
            text = popen.read()
            buffer += text
            timeEclapsed = time.time() - startTime
            if timeEclapsed >= timeout:
                break

        return buffer
if __name__ == "__main__":
    executor = Excutor(wx.Frame)
    executor.start()
    executor.isExecute = True
    pass

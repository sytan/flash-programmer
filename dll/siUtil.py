#-*- coding: UTF-8 -*-
from ctypes import *

dllObj = windll.LoadLibrary("SiUtil.dll")

def USBDebugDevices():
    #List all connected usb debug device
    i = c_ulong(0)
    errCode = dllObj.USBDebugDevices(byref(i))

    #reture error code and device number
    return errCode, i.value

def GetUSBDeviceSN(index):
    i = c_ulong(index)
    sn = c_char_p()
    errCode = dllObj.GetUSBDeviceSN(i,byref(sn))

    return errCode, sn.value

def ConnectUSB(serialNum = "", ECprotocol = 1, powerTarget = 0, disableDialogBoxes = 0):
    #serialNum-serial number of usb debug adapter.if only one usb debug adapter is connected,it can be emptyself.
    #          default to empty
    # ECprotocol-Connection protocol used by target device, JTAG(0), C2(1), default to C2
    # powerTarget-whether usb debug adapter continue supplying power after it has been disconnected from target device
    #             default to not provide(0)
    #disableDialogBoxes-disable(1) or enable(0) boxes within the DLL, default to 1

    sn = c_char_p(serialNum)
    ec = c_int(ECprotocol)
    pt = c_int(powerTarget)
    db = c_int(disableDialogBoxes)
    errCode = dllObj.ConnectUSB(sn, ec, pt, db)

    return errCode

def DisconnectUSB():
    errCode = dllObj.DisconnectUSB()
    return errCode

def Connected():
    isConnected = dllObj.Connected()
    return isConnected

def FlashErashUSB(serialNum = "", disableDialogBoxes = 0, ECprotocol = 1):
    sn = c_char_p(serialNum)
    dBox = c_int(disableDialogBoxes)
    protocol = c_int(ECprotocol)
    errCode = dllObj.FLASHEraseUSB(sn, dBox, protocol)

    return errCode


def Download(downloadFile, deviceErase = 1, disableDialogBoxes = 0, dowloadScratchPadSFLE = 0,
            bankSelect = -1, lockFlash = 0, persistFlash = 0):
    #downloadFile-path of hex file to be downloadFile
    #deviceErase-default to erase(1) before download
    #disableDialogBoxes-disable dialog boxes in DLL, default to disable(1)
    #downloadScrachPadSFLE-only for download of scratchpad memory, default to 0
    #bankSelect-default is -1
    #lockFlash-lock flash following the downlad, if flash is locked, DLL will no longer connected to device, default to not lock(0)
    #persistFlash-if pages to be programmed contain any data in flash that need to be preserved, set it to 1
    #             default to 0
    dfile = c_char_p(downloadFile)
    dErase = c_int(deviceErase)
    dBox = c_int(disableDialogBoxes)
    dScrath = c_int(dowloadScratchPadSFLE)
    bSelect = c_int(bankSelect)
    lFlash = c_int(lockFlash)
    pFlash = c_int(persistFlash)

    errCode = dllObj.Download(dfile, dErase, dBox, dScrath, bSelect, lFlash, pFlash)

    return errCode

def GetUSBFirmwareVersion():
    pass
def GetDLLVersion():
    pass
def GetDeviceName():
    # get target device name
    deviceName = c_char_p()
    errCode = dllObj.GetDeviceName(byref(deviceName))

    return errCode, deviceName.value

def main():
    import time
    print USBDebugDevices()
    print GetUSBDeviceSN(0)

    time.sleep(1)
    print "connectUSB:",ConnectUSB()
    time.sleep(1)
    print "is connected:",Connected()
    time.sleep(1)
    print "get device name:",GetDeviceName()
    file = "C:\Users\sy\Desktop\silicon_production_program\efm8.hex"
    file2 = "efm8.hex"
    Download(file2)
    print "disconnect usb:",DisconnectUSB()
    time.sleep(1)
    print "is connected:",Connected()

if __name__ == "__main__":
    main()

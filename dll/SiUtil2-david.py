#-*- coding: UTF-8 -*-

# _____ I M P O R T _______________________________________________________
from ctypes import *
import os
import re
import time
import argparse

# _____ G L O B A L  V A R I A B L E S ____________________________________
dllObj = windll.LoadLibrary("SiUtil.dll")

MAX_BYTES = 512

def byteToHex( byteStr ):
    """
    Convert a byte string to it's hex string representation
    e.g. converts byte string "\xFF\xFE\x00\x01" to the string "FF FE 00 01"
    """
    return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()


def hexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    e.g.  converts string "FF FE 00 01" to the byte string "\xFF\xFE\x00\x01"
    """
    bytes = []
    hexStr = ''.join( hexStr.split(" ") )
    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )
    return ''.join( bytes )


##########################################################################################
#	SiUtil.dll implementation
##########################################################################################


# 3 - Communications Functions

def ConnectUSB(sSerialNum = "", nECprotocol = 1, nPowerTarget = 0, nDisableDialogBoxes = 0):
	"""
		This function is used to connect to a target device using a USB Debug Adapter.
		Establishing a valid connection is necessary for all memory operations to succeed.
	
		sSerialNum						Serial number of USB debug adapter.
													If only one USB debug adapter is connected,it can be blank
													Default is blank ""
													
		nECprotocol						Connection protocol used by target device, JTAG(0), C2(1), 
													Default is C2
													
		nPowerTarget					If this parameter is set to 1, the USB Debug Adapter will be configured to
													continue supplying power after it has been disconnected from the target device. 
													The default is 0, configuring the adapter to discontinue supplying power when disconnected
													
    nDisableDialogBoxes		Disable(1) or Enable(0) dialog boxes within the DLL, 
    											Default is 0
	"""
	if dllObj.ConnectUSB(c_char_p(sSerialNum), c_int(nECprotocol), c_int(nPowerTarget), c_int(nDisableDialogBoxes)):
		raise Exception('Fail to connect to target!')


def DisconnectUSB():
	"""
		This function is used to disconnect from a target device using a USB Debug Adapter
	"""
	if dllObj.DisconnectUSB():
		raise Exception('Disconnect from target failed!')


def Connected():
	"""
		Returns the connection state of the target device
		False		not connected
		True		connected
	"""
	return (dllObj.Connected() > 0)


# 4 - Program Interface Functions

def Download(sDownloadFile, 
             nDeviceErase = 1, 
             nDisableDialogBoxes = 0, 
             nDownloadScratchPadSFLE = 0,
             nBankSelect = -1, 
             nLockFlash = 0, 
             bPersistFlash = 0):
	"""
		Downloads a hex file to the target C8051/EFM8 device
		
		sDownloadFile						Path of hex file to be downloaded
		
		nDeviceErase						Erase(1) or or not (2) flash before download
														Default is erase(1)
												
    nDisableDialogBoxes			Disable(1) or Enable(0) dialog boxes within the DLL, 
    												Default to Enable(0)
    											
    nDownloadScratchPadSFLE	Only for download of scratchpad memory, default to 0
    
    nBankSelect							Memory bank selection
    												Default is -1, no selection	
    
    nLockFlash							Lock the flash after download
    												If flash is locked, DLL will no longer connected to device, 
    												Default is 0, unlock
    
    bPersistFlash						If set to True(1), the contents of Flash will be read prior to programming. 
    												Flash pages are erased prior to programming. 
    												If the pages to be programmed contain any data in Flash that need to be preserved, 
    												then set this parameter to 1.																					

	"""
	if dllObj.Download(c_char_p(sDownloadFile), 
										 c_int(nDeviceErase), 
										 c_int(nDisableDialogBoxes), 
										 c_int(nDownloadScratchPadSFLE), 
										 c_int(nBankSelect), 
										 c_int(nLockFlash), 
										 c_int(bPersistFlash)):
		raise Exception('Fail to download')



def GetUSBFirmwareVersion():
	"""
	This function is used to retrieve the version of the USB Debug Adapter firmware
	"""
	return dllObj.GetUSBFirmwareVersion()


def GetDLLVersion():
	"""
		Returns the Utilities DLL version as string
	"""
	return dllObj.GetDLLVersion()

    
def GetDeviceName():
	"""
		Returns the name of the target C8051/EFM8 device.
	"""
	psDeviceName = c_char_p()
	if dllObj.GetDeviceName(byref(psDeviceName)):
		raise Exception('Fail to get device name')
	
	return psDeviceName.value
    
    
# 5 - Get Memory Functions

def GetRAMMemory(wStartAddress, nLength):
	"""
		Read RAM memory from a specified address.
		wStartAddress				The start address of the memory location to be referenced.
		nLength							The length of memory to be read.
	"""	
	ptrMem = c_char_p(nLength)
	if dllObj.GetRAMMemory(byref(ptrMem), c_ulong(wStartAddress), c_uint(nLength)):
		raise Exception('Fail to read RAM memory')
	return ptrMem.raw


def GetXRAMMemory(wStartAddress, nLength):
	"""
		Read XRAM memory from a specified address.
		wStartAddress				The start address of the memory location to be referenced.
		nLength							The length of memory to be read.
	"""	
	ptrMem = create_string_buffer(nLength)
	if dllObj.GetXRAMMemory(byref(ptrMem), c_ulong(wStartAddress), c_uint(nLength)):
		raise Exception('Fail to read XRAM memory')
	return ptrMem.raw


def GetCodeMemory(wStartAddress, nLength):
	"""
		Read Code memory from a specified address.
		wStartAddress				The start address of the memory location to be referenced.
		nLength							The length of memory to be read.
	"""	
	ptrMem = create_string_buffer(nLength)
	if dllObj.GetCodeMemory(byref(ptrMem), c_ulong(wStartAddress), c_uint(nLength)):
		raise Exception('Fail to read Code memory')
	return ptrMem.raw


# 6 - Set Memory Functions
def SetRAMMemory(ptrMem, wStartAddress, nLength):
	"""
		Writes value to a specified address in RAM memory.
		ptrMem								Transmit data buffer, an initialized unsigned char (BYTE) array of length nLength. 
		wStartAddress					The start address of the memory location to be referenced.
		nLength								The length of memory to be read.
	"""		
	if dllObj.SetRAMMemory(byref(ptrMem), c_ulong(wStartAddress), c_uint(nLength)):
		raise Exception('Fail to write RAM memory')	


def SetXRAMMemory(ptrMem, wStartAddress, nLength):
	"""
		Writes value to a specified address in XRAM memory.
		ptrMem								Transmit data buffer, an initialized unsigned char (BYTE) array of length nLength. 
		wStartAddress					The start address of the memory location to be referenced.
		nLength								The length of memory to be read.
	"""		
	if dllObj.SetXRAMMemory(byref(ptrMem), c_ulong(wStartAddress), c_uint(nLength)):
		raise Exception('Fail to write XRAM memory')	


def SetCodeMemory(ptrMem, wStartAddress, nLength, nDisableDialogBoxes = 0):
	"""
		Writes value to a specified address in Code memory.
		ptrMem								Transmit data buffer, an initialized unsigned char (BYTE) array of length nLength. 
		wStartAddress					The start address of the memory location to be referenced.
		nLength								The length of memory to be read.
		nDisableDialogBoxes		Disable(1) or Enable(0) dialog boxes within the DLL, 
    											Default is 0
	"""		
	if dllObj.SetCodeMemory(byref(ptrMem), c_ulong(wStartAddress), c_uint(nLength), c_int(nDisableDialogBoxes)):
		raise Exception('Fail to write Code memory')	


# 7 - Target Control Functions
# NOT IMPLEMENTED

# 8 - USB Debug Adapter Communication Functions

def USBDebugDevices():
	"""	
		Determines how many USB Debug Adapters are present.
	"""
	dwDevices = c_ulong(0)
	if dllObj.USBDebugDevices(byref(dwDevices)):
		raise Exception('Fail to check USB debug adapter presence')

	return dwDevices.value


def GetUSBDeviceSN(dwDeviceNum):
	"""
		List the serial number of the enumerated USB Debug Adapters.
		dwDeviceNum				Index of the device for which the serial number is desired. 
											To obtain the serial number of the first device, use 0.
	"""
	psSerialNum = c_char_p()
	
	if dllObj.GetUSBDeviceSN(c_ulong(dwDeviceNum),byref(psSerialNum)):
		raise Exception('Fail to get USB debug adapter serial number!')
	
	return psSerialNum.value


def GetUSBDLLVersion():
	"""
		This function will return the version of the driver for the USB Debug Adapter.
	"""
	pVersionString = c_char_p()
	
	if dllObj.GetUSBDeviceSN(byref(pVersionString)):
		raise Exception('Fail to get USB debug adapter serial number!')
	
	return pVersionString.value


# 9 - Stand-Alone Functions

def FlashEraseUSB(sSerialNum = "", nDisableDialogBoxes = 0, nECprotocol = 1):
	"""
		Erase the Flash program memory using a USB Debug Adapter.
		
		sSerialNumber							The serial number of the USB Debug Adapter.
															The default is an empty string.
												
		nDisableDialogBoxes				Disable (1) or enable (0) dialogs boxes within the DLL. 
															The default is 0.
															
		nECprotocol								Connection protocol used by target device, JTAG(0) or C2(1) 
															Default is C2	(1)												
	"""
	if dllObj.FLASHEraseUSB(c_char_p(sSerialNum), 
	                        c_int(nDisableDialogBoxes),
	                        c_int(nECprotocol)):
		raise Exception('Fail to erase program memory!')
	
	
##########################################################################################
#	User function
##########################################################################################

def userConnect():
	if USBDebugDevices() == 0:
		print "\ncan not find USB debug adapter "
		return
	print "\nconnect USB debug adapter %s ..." % (GetUSBDeviceSN(0)),
	time.sleep(1)
	ConnectUSB()
	time.sleep(1)
	if Connected():
		print "OK"
	else:
		return
	time.sleep(1)
	print "\nget target device name: ",GetDeviceName()


def userDisconnect():
	DisconnectUSB()
	print "\ndisconnect USB debug adapter ...",
	time.sleep(1)
	if not Connected():
		print "OK"


def userProgram(filename):
	print "\nprogram '%s' content to flash memory ..." % (filename)
	userConnect()
	Download(filename)
	userDisconnect()

def userRead(memory, address, length):
	if memory == 'RAM':
		userConnect()
		print "\nread [RAM] @ %08X : %d bytes :" % (address, length)
		print repr(GetRAMMemory(address, length))
		userDisconnect()
	elif memory == 'XRAM':
		userConnect()
		print "\nread [XRAM] @ %08X : %d bytes :" % (address, length)
		print repr(GetXRAMMemory(address, length))
		userDisconnect()
	elif memory == 'CODE':
		userConnect()
		print "\nread [CODE] @ %08X : %d bytes :" % (address, length)
		print repr(GetCodeMemory(address, length))
		userDisconnect()
	else:
		return 1

	return 0


def userWrite(memory, address, data):
	if memory == 'RAM':
		userConnect()		
		print "\nwrite [RAM] @ %08X : %d bytes :\n%s" % (address, len(data),repr(data))
		SetRAMMemory(create_string_buffer(data), address, len(data))
		userDisconnect()
	elif memory == 'XRAM':
		userConnect()		
		print "\nwrite [XRAM] @ %08X : %d bytes :\n%s" % (address, len(data),repr(data))
		SetXRAMMemory(create_string_buffer(data), address, len(data))
		userDisconnect()
	elif memory == 'CODE':
		userConnect()
		print "\nwrite [CODE] @ %08X : %d bytes :\n%s" % (address, len(data),repr(data))
		SetCodeMemory(create_string_buffer(data), address, len(data))
		userDisconnect()
	else:
		return 1

	return 0
	
	
##########################################################################################
#	MAIN PROGRAM
##########################################################################################
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	# Below arguments are exclusive, means only 1 can be set
	g = parser.add_mutually_exclusive_group()
	g.add_argument('-d', '--dwld', type=str, help='filename of the hex to program to device', required=False)
	g.add_argument('-r', type=str, nargs=3, help='<memory>[RAM,XRAM,CODE] <address> <length> : read @ hex <address> x byte <length>', required=False)
	g.add_argument('-w', type=str, nargs='+', help='<memory>[RAM,XRAM,CODE] <address> <data0> <data2> ... : write @ hex <address> <data>', required=False)
	args = parser.parse_args()

# Argumens handler
# For download	
	if  args.dwld != None:
		if (args.dwld[-4:] != ".hex"):
			print args.dwld[-4:]
			print "invalid filename, shall be .hex file"
			exit(0)
		try:
			if os.path.isfile(args.dwld):
				userProgram(args.dwld)
				quit(0)
			else:
				print "could not find '%s'" % (str(args.dwld))
		except:
			pass
			quit(0)


# For memory read	
	if  args.r != None:
		address = 0
		length = 0
		try:
			address = int(args.r[1],16)
		except:
			print "incorrect address format, shall be hex number"
			quit(0)		
		try:
			length = int(args.r[2])
		except:
			print "incorrect length, shall be number"
			quit(0)
		if length<0:
			print "incorrect length, shall be positive number"
			quit(0)
		
		if userRead(args.r[0].upper(), address, length) == 1:
			print "invalid memory type, shall be [RAM|XRAM|CODE]"
			quit(0)		


# For memory write			
	if  args.w != None:
		if len(args.w)<3:
			print "Incorrect number of argument for -w, shall be at least 3"
			quit(0)
		address = 0
		try:
			address = int(args.w[1],16)
		except:
			print "incorrect address format, shall be hex number"
			quit(0)
		if len(args.w) == 3:
			if not (len(args.w[2])%2 == 0):
				print "Incorrect data length shall be a multiple of 2, or space separated argument"
				quit(0)		
			# try to split 
			pdata = re.findall('..',args.w[2])
		else:
			pdata = args.w[2:]
		data = ''.join([ chr(int(x,16)) for x in pdata ]).strip()
		
		if userWrite(args.w[0].upper(), address, data) == 1:
			print "invalid memory type, shall be [RAM|XRAM|CODE]"
			quit(0)
global ORG_PATH
global sscListFile
global count
global sscPathParsing
global ethercatSSCDirMyPath
global createSSCFileSymbol
global clearFileSymbols
global mytcpipHttpNetComponent
global symbolList


#Disable all the file symbols
def clearFileSymbols():
	for symbol in symbolList:
		symbol.setEnabled(False)

#Return File symbols from the Symbol list.
def createSSCFileSymbol(count):
	return symbolList[count]

#Callback function which is called when there is a path configuration from MHC
def ethercatSSCMyPathVisible(sym, event):
	ORG_PATH = event["value"]
	sscPathParsing(ORG_PATH)

ethercatSSCDirMyPath = etherCatComponent.createStringSymbol("ETHERCAT_SLAVESTACK_DIRECTORY_MYPATH", None)
ethercatSSCDirMyPath.setLabel("Configure Slave Stack directory path")
ethercatSSCDirMyPath.setVisible(False)
ethercatSSCDirMyPath.setDescription("Configure Slave Stack directory path")
ethercatSSCDirMyPath.setDefaultValue(Module.getPath() + "slave_stack")
ethercatSSCDirMyPath.setDependencies(ethercatSSCMyPathVisible, ["TCPIP_HTTP_NET_ssc_DIRECTORY_PATH"])

def sscPathParsing(path):
	import re
	import os
	import sys

	count = 0
	# Get the Root PATH 
	ORG_PATH = path
	clearFileSymbols()
	for (root, dirs, fileNames) in os.walk(ORG_PATH):
		for fileName in fileNames:
			file = os.path.join(root,fileName)
			#file = file[file.find(ORG_PATH):]
			#Replace the module path from the Root path with empty string
			file = file.replace(Module.path, "")
			sepSSCDir = file[file.find(os.path.sep):]
			htmFile = sepSSCDir.replace(os.path.sep, "",1)
			srcFile = htmFile.rfind(".c")
			if srcFile == -1:
				print("Header file found")
				srcFileFound = 0
			else:
				print("Source file found")
				srcFileFound = 1
			# Get the ssc file symbol and each symbol is for the each file
			sscListFile = createSSCFileSymbol(count)
			#Set the source path
			sscListFile.setSourcePath(file)
			sscListFile.setOutputName(htmFile)
			print(file)
			print("htmFile : ")
			print(htmFile)
			fileList = file.split(os.path.sep)
			#set the destination path , the location where the ssc file will be copied
			#destPath = ".."+os.path.sep+".."+os.path.sep+fileList[0]
			destPath = ".."+os.path.sep+".."+os.path.sep+"slave_stack"
			#print("destination path: "+ destPath)
			sscListFile.setDestPath(destPath)
			fileList = fileList[0:len(fileList)-1]
			folderPath = ""
			print("fileStr : ")
			for fileStr in fileList:
				print(fileStr)
				folderPath += fileStr+os.path.sep
				print(folderPath)
			#set the project path , ssc diretory will be added to the project	
			sscListFile.setProjectPath(folderPath)
			if srcFileFound == 1:
				sscListFile.setType("SOURCE")
			else:
				sscListFile.setType("HEADER")
			sscListFile.setMarkup(False)
			sscListFile.setEnabled(True)
			count += 1



#ORG_PATH = "../src/web_pages"
ORG_PATH = Module.getPath() + "slave_stack"
etherCATSSCDirSymbol = etheercatSlaveStackcodeDirPath.getValue()
ORG_PATH = etherCATSSCDirSymbol
count = 0

#mytcpipHttpNetComponent = etherCatComponent
symbolList = []
fileCount = 0
MAX_NUMBER_ssc_FILES = 100
del symbolList[:]

#Create MAX_NUMBER_ssc_FILES file symbols during the instantiation . 
#use of createFileSymbol() is not possible during the dynamic configuration of ssc path configuration
#So due to that we create a max number of ssc files during componet instatiation

for fileCount in range(MAX_NUMBER_ssc_FILES):
	sscSymbolStr = "SSC_LIST_FILE"+str(fileCount)
	mySym = etherCatComponent.createFileSymbol(sscSymbolStr, None)
	mySym.setEnabled(False)
	symbolList.append(mySym)
	fileCount +=1

#default webapge path and diretory parsing
sscPathParsing(ORG_PATH)

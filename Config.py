import os

class Set_Directory():
    def __init__(self):
## Data File
        self.DirCurrent = os.getcwd()
        self.DirBin = self.DirMake('Bin')
        self.DirData = self.DirMake('Data')
        self.DirTemp = self.DirMake('Temp')
        self.DirSwiftData = self.DirMake('SwiftData',self.DirData)
        self.FileSwiftTable = os.path.join(self.DirData,'grb_table.txt')

        
        self.Temp_File_List = self.ErgodicFolder(self.DirTemp)
        self.TempClean(self.Temp_File_List)
        return

    def DirMake(self,DirName,DirPath=None):
        if DirPath == None:
            DirPath = self.DirCurrent
        DirNeed = os.path.join(DirPath,DirName)
        if os.path.exists(DirNeed):
            pass
        else:
            os.makedirs(DirNeed)
        return DirNeed

    def DirClean(self,Dir):
        File_List = self.ErgodicFolder(Dir)
        self.TempClean(File_List)
##        print 'Delete the folder \'Data\' by yourself, have a nice day.'
        return
    
    def ErgodicFolder(self,Directory):
        File_List = []
        for root, dirs, files in os.walk(Directory):
            for File in files:
                File_List.append(os.path.join(root,File))
        return File_List

    def TempClean(self,Temp_File_List):
        import os
        for Item in Temp_File_List:
            os.remove(Item)
        return

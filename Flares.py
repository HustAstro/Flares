#coding=utf-8
import Bin.DataDownload
import Bin.AnalysisSwift
import Config
import os

def main():
##################################
    Directory = Config.Set_Directory()
    DownloadType = ['Update','Complete','No']
    Bin.DataDownload.SwiftXRT(Directory,DownloadType[2])
###################################

###################################    
    DirTemp = os.path.join(Directory.DirSwiftData,'111209A')
##    DirTemp = os.path.join(Directory.DirSwiftData,'130427A')
##    DirTemp = os.path.join(Directory.DirSwiftData,'070110')
    Test = Bin.AnalysisSwift.AnalysisXRT(DirTemp)
    Test.PresetPipelineA()
###################################    


    Test.DataBaseKeysList()
    print 'Done!'    
    return
if __name__ == '__main__':
    main()

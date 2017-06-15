# coding=utf-8
import Bin.DataDownload
import Bin.AnalysisSwift
import Config
import os


def main():
    directory = Config.SetDirectory()
    download_type = ['Update', 'Complete', 'No']
    Bin.DataDownload.SwiftXRT(directory, download_type[2])

    dir_temp = os.path.join(directory.DirSwiftData, '111209A')
#    dir_temp = os.path.join(directory.DirSwiftData,'130427A')
#    dir_temp = os.path.join(directory.DirSwiftData,'070110')
    test = Bin.AnalysisSwift.AnalysisXRT(dir_temp)
    test.preset_pipeline_a()

#    Test.DataBaseKeysList()
    print 'Done!'    
    return
if __name__ == '__main__':
    main()

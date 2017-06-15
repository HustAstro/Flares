import os


class SetDirectory:
    def __init__(self):
        # Data File
        self.DirCurrent = os.getcwd()
        self.DirBin = self.dir_make('Bin')
        self.DirData = self.dir_make('Data')
        self.DirTemp = self.dir_make('Temp')
        self.DirSwiftData = self.dir_make('SwiftData', self.DirData)
        self.FileSwiftTable = os.path.join(self.DirData, 'grb_table.txt')
        
        self.TempFileList = self.ergodic_folder(self.DirTemp)
        self.temp_clean(self.TempFileList)
        return

    def dir_make(self, dir_name, dir_path=None):
        if dir_path is None:
            dir_path = self.DirCurrent
        dir_need = os.path.join(dir_path, dir_name)
        if os.path.exists(dir_need):
            pass
        else:
            os.makedirs(dir_need)
        return dir_need

    def dir_clean(self, dir_cleaned):
        file_list = self.ergodic_folder(dir_cleaned)
        self.temp_clean(file_list)
        # print "Delete the folder \'Data\' by yourself, have a nice day."
        return

    @staticmethod
    def ergodic_folder(directory):
        file_list = []
        for root, dirs, files in os.walk(directory):
            for single_file in files:
                file_list.append(os.path.join(root, single_file))
        return file_list

    @staticmethod
    def temp_clean(temp_file_list):
        import os
        for item in temp_file_list:
            os.remove(item)
        return

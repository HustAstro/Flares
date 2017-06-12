import os

class AnalysisXRT():
    def __init__(self,DirGRB):
        
        self.DirGRB = DirGRB
        self.GRBName = os.path.split(self.DirGRB)[-1]
        self.DirXRT = self.__DirMake__('XRT',self.DirGRB)
        self.DirReturn = self.__DirMake__('Return',self.DirGRB)
        self.ListXRT = self.__ErgodicFolder__(self.DirXRT)
        self.DataBase = dict()
        self.FileXRTFull = [
            'xrt_cf_pc_BATBAND.qdp',
            'xrt_cf_pc_DENSITY.qdp',
            'xrt_cf_pc_XRTBAND.qdp',
            'xrt_cf_wt_BATBAND.qdp',
            'xrt_cf_wt_DENSITY.qdp',
            'xrt_cf_wt_XRTBAND.qdp',
            'xrt_cf_wtslew_BATBAND.qdp',
            'xrt_cf_wtslew_DENSITY.qdp',
            'xrt_cf_wtslew_XRTBAND.qdp',
            'xrt_flux_pc_BATBAND.qdp',
            'xrt_flux_pc_DENSITY.qdp',
            'xrt_flux_pc_XRTBAND.qdp',
            'xrt_flux_wt_BATBAND.qdp',
            'xrt_flux_wt_DENSITY.qdp',
            'xrt_flux_wt_XRTBAND.qdp',
            'xrt_flux_wtslew_BATBAND.qdp',
            'xrt_flux_wtslew_DENSITY.qdp',
            'xrt_flux_wtslew_XRTBAND.qdp',
            'xrt_gamma_pc.qdp',
            'xrt_gamma_wt.qdp',
            'xrt_gamma_wtslew.qdp',
            'xrt_flux_pc_BATBAND_nosys.qdp',
            'xrt_flux_pc_DENSITY_nosys.qdp',
            'xrt_flux_pc_XRTBAND_nosys.qdp',
            'xrt_flux_wt_BATBAND_nosys.qdp',
            'xrt_flux_wt_DENSITY_nosys.qdp',
            'xrt_flux_wt_XRTBAND_nosys.qdp',
            'xrt_flux_wtslew_BATBAND_nosys.qdp',
            'xrt_flux_wtslew_DENSITY_nosys.qdp',
            'xrt_flux_wtslew_XRTBAND_nosys.qdp'
            ]
##        self.LCFluxDensityAll = self.LoadXRTFile()
        return

    def __DirMake__(self,DirName,DirPath=None):
        if DirPath == None:
            DirPath = self.DirCurrent
        DirNeed = os.path.join(DirPath,DirName)
        if os.path.exists(DirNeed):
            pass
        else:
            os.makedirs(DirNeed)
        return DirNeed

    def __ErgodicFolder__(self,Directory):
        File_List = []
        for root, dirs, files in os.walk(Directory):
            for File in files:
                File_List.append(os.path.join(root,File))
        return File_List

    def DataBaseSave(self,Keyword,Value):
        self.DataBase[Keyword] = Value
        return

    def DataBaseLoad(self,Keyword):
        return self.DataBase[Keyword]

    def DataBaseKeysList(self):
        for Item in self.DataBase:
            print Item
        return

    def LoadSwiftFile(self,FilePath,DataType=0):
        import linecache
        import re
        """DataType == 0, Just use good data; DataType == 1, Use good and bad data"""

        File_Cache = []
        fp = open(FilePath,'rU')
        
        for eachline in fp:
            eachline = eachline.rstrip('\n')
            if r'!#' in eachline:
                eachline = re.sub(r'!#', '', eachline)
                LineCache = eachline.split('\t')
                for i in range(len(LineCache)):
                    LineCache[i] = float(LineCache[i])
                if DataType == 0:
                    continue
            else:
                try:
                    LineCache = eachline.split('\t')
                    for i in range(len(LineCache)):
                        LineCache[i] = float(LineCache[i])
                except:
                    continue
            File_Cache.append(LineCache)
        fp.close()
        return File_Cache

    def LoadXRTFile(self,InputFileNameGroup,SaveKeyword):
        def __LoadXRTFileAddTag__(self,FileName,Tag):
            FilePath = os.path.join(self.DirXRT,FileName)
            FileCache = []
            if os.path.exists(FilePath):
                FileCache = self.LoadSwiftFile(FilePath)
                for Item in FileCache:
                    Item.append(Tag)
            return FileCache
        
        TotalCache = []

        for FileName,Tag in InputFileNameGroup:
            FileCache = __LoadXRTFileAddTag__(self,FileName,Tag)
            TotalCache.extend(FileCache)

        self.DataBaseSave(SaveKeyword,TotalCache)
        return


    def DeadTimeIdentify(self, InputLCDataKeyWord, SaveKeywordDeadTimeIndex, TimeBinGapThresholdJudge=10, TimeBinGapThresholdIgnoreRatio=5):
        File = self.DataBaseLoad(InputLCDataKeyWord)
        DeadTimeGroup = []
        for i in range(len(File)-1):
            TimeValuePreEnd = File[i][0] + File[i][1]
            TimeValueLatBeg = File[i+1][0] + File[i+1][2]
            TimeBinGap = TimeValueLatBeg - TimeValuePreEnd
            
            if (TimeBinGap > TimeBinGapThresholdJudge):
                if (File[i][0]/TimeBinGap < TimeBinGapThresholdIgnoreRatio)and(File[i][0]<200000):
                    DeadTimeGroup.append(i)
        self.DataBaseSave(SaveKeywordDeadTimeIndex, DeadTimeGroup)
        return

    def SplitByDeadTime(self,InputGroup,SaveKeywordLCSplited):
        LCSplited = []
        
        InputLC = self.DataBaseLoad(InputGroup[0])
        
        InputDeadTimeIndex = self.DataBaseLoad(InputGroup[1])[::-1]
        InputDeadTimeIndex.append(-1)
        
        SplitTemp = -1
        LengthGroup = len(InputLC)
        
        for Item in InputDeadTimeIndex:
            if (Item+1 != SplitTemp)&(Item+2 != LengthGroup):
                SplitTempSub = InputLC[Item+1:SplitTemp]
                if SplitTemp == -1:
                    SplitTempSub.append(InputLC[SplitTemp])
                LCSplited.append(SplitTempSub)
            else:
                LCSplited.append([InputLC[Item+1]])
            SplitTemp = Item + 1
            
        LCSplited = LCSplited[::-1]
        self.DataBaseSave(SaveKeywordLCSplited, LCSplited)
        return


    def XRTFilter(self,InputLCKeyword,SaveGroupKeywords):
        
        def __XRTFilterCore__(GroupIn):
            from scipy import signal
            import numpy as np
            
            def __XRTFilterCoreLPF__(LC,LCError,b,a,MCTimes=100):
                def __XRTFilterCoreMC__(LC,LCError):
                    LCNewMC = []
                    for i in range(len(Value)):
                        LCNewMC.append(np.random.normal(LC[i],abs(LCError[i])))
                    return LCNewMC
            
                LCNewMCFGroup = []
                LCNewMCFFinalValue = []
                LCNewMCFFinalError = []
                LCNewMCFFinal = []
                
                for i in range(MCTimes):
                    LCNewMC = __XRTFilterCoreMC__(LC,LCError)
                    LCNewMCF = signal.filtfilt(b,a,LCNewMC)
                    LCNewMCFGroup.append(LCNewMCF)
                LCNewMCFGroup = map(list, zip(*LCNewMCFGroup))
                
                for i in range(len(LCNewMCFGroup)):
                    LCNewMCFFinalValue.append(np.mean(LCNewMCFGroup[i]))
                    LCNewMCFFinalError.append(np.sqrt(np.var(LCNewMCFGroup[i])))
                    
                LCNewMCFFinal = [LCNewMCFFinalValue, LCNewMCFFinalError]
                return LCNewMCFFinal
            

            GroupIn = map(list, zip(*GroupIn))
            Value = GroupIn[3]
            ErrPos = GroupIn[4]
            ErrNeg = GroupIn[5]

            GroupSamplingFs = []
            for i in range(len(GroupIn[0])-1):
                TimeGap = GroupIn[0][i+1]-GroupIn[0][i]
                GroupSamplingFs.append(1.0/TimeGap)
            Fs = np.mean(GroupSamplingFs)
            FsErr = np.sqrt(np.var(GroupSamplingFs))
            Wn = 0.04/(Fs/2)
            print 'Wn:',Wn,', Fs:',Fs,'Hz, FsErr(Per):',100*FsErr/Fs,'%'
            Wn = min([Wn,0.25])

            MCNumber = 1000

            b,a = signal.butter(3,Wn,'low')

            LCNewMCFFinalPos = __XRTFilterCoreLPF__(Value,ErrPos,b,a,MCNumber)
            ValuePos = LCNewMCFFinalPos[0]
            ErrPos = LCNewMCFFinalPos[1]

            LCNewMCFFinalNeg = __XRTFilterCoreLPF__(Value,ErrPos,b,a,MCNumber)
            ValueNeg = LCNewMCFFinalNeg[0]
            ErrNeg = LCNewMCFFinalNeg[1]

            ValueF = []
            for i in range(len(ValuePos)):
                ValueF.append(np.mean([ValuePos[i],ValueNeg[i]]))
            
            GroupOut = GroupIn
            GroupOut[3] = ValueF
            GroupOut[4] = ErrPos
            GroupOut[5] = ErrNeg
            GroupOut = map(list, zip(*GroupOut))
            return GroupOut
        
        def __SpectrumFFT__(GroupIn):
            import numpy as np
            import scipy.signal as signal
            GroupIn = map(list, zip(*GroupIn))
            GroupOut = []
            Sample = GroupIn[3]
            
            GroupSamplingFs = []
            for i in range(len(GroupIn[0])-1):
                TimeGap = GroupIn[0][i+1]-GroupIn[0][i]
                GroupSamplingFs.append(1.0/TimeGap)
            Fs = np.mean(GroupSamplingFs)
            FFTSize = len(Sample)
            xf = np.fft.rfft(Sample)/FFTSize
            freqs = np.linspace(0, Fs/2, FFTSize/2+1)
            xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100))

            GroupOut.append(freqs)
            GroupOut.append(xfp)
            GroupOut = map(list, zip(*GroupOut))
            
            return GroupOut


        LCSplitedFFT = []
        LCSplitedFilteredFFT = []

        LCSplited = self.DataBaseLoad(InputLCKeyword)
            
        for i in range(len(LCSplited)):
            if len(LCSplited[i]) > 12:
                LCSplitedFFT.append(__SpectrumFFT__(LCSplited[i]))
                LCSplited[i] = __XRTFilterCore__(LCSplited[i])
                LCSplitedFilteredFFT.append(__SpectrumFFT__(LCSplited[i]))

        LCFiltered = []
        
        for i in range(len(LCSplited)):
            LCFiltered.extend(LCSplited[i])

        self.DataBaseSave(SaveGroupKeywords[0], LCFiltered)
        self.DataBaseSave(SaveGroupKeywords[1], LCSplitedFFT)
        self.DataBaseSave(SaveGroupKeywords[2], LCSplitedFilteredFFT)
        
        return

    def FindPeakInGroup(self,InputGroupKeyword,SaveGroupKeywords):
        def __FindPeakInLC__(InputLC):
            return
        return

    def CalLCSlopeInGroup(self,InputGroupKeyword,SaveGroupKeywords):
        def __CalLCSlopeInLC__(InputLC):
            
            def __CalPonitSlopeByMC__(P1,P2):
                import numpy as np

                def __GiveValueByMC__(Value,ErrPos,ErrNeg):
                    np.random.normal(Value,abs(ErrPos))
                    np.random.normal(Value,abs(ErrPos))
                    return
                
##                x1Value = InputLC[i][0]
##                x1ErrPos = InputLC[i][1]
##                x1ErrNeg = InputLC[i][2]
##                y1Value = InputLC[i][3]
##                y1ErrPos = InputLC[i][4]
##                y1ErrNeg = InputLC[i][5]
##
##                x2Value = InputLC[i+1][0]
##                x2ErrPos = InputLC[i+1][1]
##                x2ErrNeg = InputLC[i+1][2]
##                y2Value = InputLC[i+1][3]
##                y2ErrPos = InputLC[i+1][4]
##                y2ErrNeg = InputLC[i+1][5]

                return Slope
##            InputLC = map(list, zip(*InputLC))
            SlopeCurve = []
            for i in range(len(InputLC)-1):
                P1 = InputLC[i]
                P2 = InputLC[i+1]
                Slope = __CalPonitSlopeByMC__(P1,P2)
            SlopeCurve.append(Slope)
            return SlopeCurve
        
        LCSplited = self.DataBaseLoad(InputGroupKeyword)
        LCGroupReturn = []
        
        for i in range(len(LCSplited)):
            if len(LCSplited[i]) > 3:
                SlopeCurve = __CalLCSlopeInLC__(LCSplited[i])
                LCGroupReturn.append(SlopeCurve)
            
        self.DataBaseSave(SaveGroupKeywords, LCGroupReturn)
        return

    def PlotLcTypeA(self,PlotKeywordGroup=['XRTFiltered','Swift XRT wtslew','Swift XRT wt','Swift XRT pc']):
        def __PlotGroupEst__(GroupIn):
            GroupOut = GroupIn
            GroupOut = map(list, zip(*GroupOut))
            GroupOut[2] = map(abs, GroupOut[2])
            GroupOut[5] = map(abs, GroupOut[5])
            return GroupOut
        
        import matplotlib.pyplot as plt
        import numpy as np
        
        plt.style.use('bmh')
        Plot_Label_Group = [r'wt',r'pc',r'wtslew']
        fig, (ax0,ax1) = plt.subplots(ncols=2, figsize=(13,6))
        ax0.patch.set_facecolor('white')
        ax0.set_xscale('log')
        ax0.set_yscale('log')
        ax0.set_xlabel(r'$\rm Time\ After\ Trigger\ $[$s$]',fontsize=16)
        ax0.set_ylabel(r'$\rm Flux\ Density\ at\ 10$$\ KeV$',fontsize=16)
        PicSubTitle = r'Swift LC Filtered GRB '+self.GRBName[1]
        ax0.set_title(PicSubTitle,fontsize=16)
        ax1.patch.set_facecolor('white')
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel(r'$\rm Time\ After\ Trigger\ $[$s$]',fontsize=16)
        ax1.set_ylabel(r'$\rm Flux\ Density\ at\ 10$$\ KeV$',fontsize=16)
        PicSubTitle = r'Swift LC Origin GRB '+self.GRBName[1]
        ax1.set_title(PicSubTitle, fontsize=16)


        XRTFiltered = self.DataBaseLoad(PlotKeywordGroup[0])
        File_Cache_wtslew = self.DataBaseLoad(PlotKeywordGroup[1])
        File_Cache_wt = self.DataBaseLoad(PlotKeywordGroup[2])
        File_Cache_pc = self.DataBaseLoad(PlotKeywordGroup[3])
        
        if XRTFiltered != []:
            PlotTemp = __PlotGroupEst__(XRTFiltered)
            ax0.errorbar(PlotTemp[0], PlotTemp[3],
                         xerr=[PlotTemp[2],PlotTemp[1]], yerr=[PlotTemp[5],PlotTemp[4]],
                         label=r'Swift XRT', alpha=0.8,linestyle='',marker='')
            
        if File_Cache_wtslew != []:
            PlotTemp_wtslew = __PlotGroupEst__(File_Cache_wtslew)
            ax1.errorbar(PlotTemp_wtslew[0], PlotTemp_wtslew[3],
                         xerr=[PlotTemp_wtslew[2],PlotTemp_wtslew[1]], yerr=[PlotTemp_wtslew[5],PlotTemp_wtslew[4]],
                         label=r'Swift XRT wtslew', alpha=0.8,linestyle='', color='cyan', marker='')

        if File_Cache_wt != []:
            PlotTemp_wt = __PlotGroupEst__(File_Cache_wt)
            ax1.errorbar(PlotTemp_wt[0], PlotTemp_wt[3],
                         xerr=[PlotTemp_wt[2],PlotTemp_wt[1]], yerr=[PlotTemp_wt[5],PlotTemp_wt[4]],
                         label=r'Swift XRT wt', alpha=0.8,linestyle='', color='royalblue', marker='')

        if File_Cache_pc != []:
            PlotTemp_pc = __PlotGroupEst__(File_Cache_pc)
            ax1.errorbar(PlotTemp_pc[0], PlotTemp_pc[3],
                         xerr=[PlotTemp_pc[2],PlotTemp_pc[1]], yerr=[PlotTemp_pc[5],PlotTemp_pc[4]],
                         label=r'Swift XRT pc', alpha=0.8,linestyle='', color='r', marker='')


        legend_ax0 = ax0.legend(loc='upper right')
        plt.show()
        plt.close('all')
        
        return

    def PlotFFTTypeA(self):
        import matplotlib.pyplot as plt
        plt.style.use('bmh')
        fig,axes = plt.subplots(ncols=2, nrows=3, figsize=(13,6))

        
        LCFluxDensityAllSplitedFFT = self.DataBaseLoad('LCFDASFFT')
        LCFluxDensityAllSplitedFFTFiltered = self.DataBaseLoad('LCFDASFilteredFFT')
        
        axes[0,0].patch.set_facecolor('white')
        axes[0,0].set_ylabel(r'$\rm 1st\ Obs$ [$Db$]',fontsize=16)
        PicSubTitle = r'Swift LC FFT GRB '+self.GRBName[1]
        axes[0,0].set_title(PicSubTitle,fontsize=16)
        AxisX = map(list, zip(*LCFluxDensityAllSplitedFFT[0]))[0]
        AxisY = map(list, zip(*LCFluxDensityAllSplitedFFT[0]))[1]
        axes[0,0].plot(AxisX,AxisY)
        axes[0,0].set_yticks([-60,-80,-100,-120,-140])
        axes[0,0].set_xticks([0.00,0.04,0.08,0.12,0.16])
        axes[0,0].set_xlim([0,0.16])

        axes[0,1].patch.set_facecolor('white')
        axes[0,1].set_ylabel(r'$\rm 1st\ Obs$ [$Db$]',fontsize=16)
        PicSubTitle = r'Swift LC FFT Filtered GRB '+self.GRBName[1]
        axes[0,1].set_title(PicSubTitle,fontsize=16)
        AxisX = map(list, zip(*LCFluxDensityAllSplitedFFTFiltered[0]))[0]
        AxisY = map(list, zip(*LCFluxDensityAllSplitedFFTFiltered[0]))[1]
        axes[0,1].plot(AxisX,AxisY)
        axes[0,1].set_yticks([-60,-80,-100,-120,-140])
        axes[0,1].set_xticks([0.00,0.04,0.08,0.12,0.16])
        axes[0,1].set_xlim([0,0.16])
        
        axes[1,0].patch.set_facecolor('white')
        axes[1,0].set_ylabel(r'$\rm 2nd\ Obs$ [$Db$]',fontsize=16)
        AxisX = map(list, zip(*LCFluxDensityAllSplitedFFT[1]))[0]
        AxisY = map(list, zip(*LCFluxDensityAllSplitedFFT[1]))[1]
        axes[1,0].plot(AxisX,AxisY)
        axes[1,0].set_yticks([-60,-80,-100,-120,-140])
        axes[1,0].set_xticks([0.00,0.02,0.04,0.06,0.08])
        axes[1,0].set_xlim([0,0.08])


        axes[1,1].patch.set_facecolor('white')
        axes[1,1].set_ylabel(r'$\rm 2nd\ Obs$ [$Db$]',fontsize=16)
        AxisX = map(list, zip(*LCFluxDensityAllSplitedFFTFiltered[1]))[0]
        AxisY = map(list, zip(*LCFluxDensityAllSplitedFFTFiltered[1]))[1]
        axes[1,1].plot(AxisX,AxisY)
        axes[1,1].set_yticks([-60,-80,-100,-120,-140])
        axes[1,1].set_xticks([0.00,0.02,0.04,0.06,0.08])
        axes[1,1].set_xlim([0,0.08])


        axes[2,0].patch.set_facecolor('white')
        axes[2,0].set_xlabel(r'$\rm Frequence $ [$Hz$]',fontsize=16)
        axes[2,0].set_ylabel(r'$\rm 3rd\ Obs$ [$Db$]',fontsize=16)
        AxisX = map(list, zip(*LCFluxDensityAllSplitedFFT[2]))[0]
        AxisY = map(list, zip(*LCFluxDensityAllSplitedFFT[2]))[1]
        axes[2,0].plot(AxisX,AxisY)
        axes[2,0].set_yticks([-60,-80,-100,-120,-140])
        axes[2,0].set_xticks([0.00,0.01,0.02,0.03,0.04])
        axes[2,0].set_xlim([0,0.04])


        axes[2,1].patch.set_facecolor('white')
        axes[2,1].set_xlabel(r'$\rm Frequence $ [$Hz$]',fontsize=16)
        axes[2,1].set_ylabel(r'$\rm 3rd\ Obs$ [$Db$]',fontsize=16)
        AxisX = map(list, zip(*LCFluxDensityAllSplitedFFTFiltered[2]))[0]
        AxisY = map(list, zip(*LCFluxDensityAllSplitedFFTFiltered[2]))[1]
        axes[2,1].plot(AxisX,AxisY)
        axes[2,1].set_yticks([-60,-80,-100,-120,-140])
        axes[2,1].set_xticks([0.00,0.01,0.02,0.03,0.04])
        axes[2,1].set_xlim([0,0.04])


        plt.show()
        plt.close('all')
        return

    def PlotGroup(self,PlotGroupKeyword):
        import matplotlib.pyplot as plt
        
        def PlorSingle(ax, PlotSingelData, DTT):
            labelTS = r'XRT TimeSlice: ' + str(DTT)
            PlotTemp = map(list, zip(*PlotSingelData))

            PlotTemp[2] = map(abs, PlotTemp[2])
            PlotTemp[5] = map(abs, PlotTemp[5])
            
            ax.errorbar(PlotTemp[0], PlotTemp[3],
                        xerr=[PlotTemp[2],PlotTemp[1]], yerr=[PlotTemp[5],PlotTemp[4]],
                        label=labelTS, alpha=0.8,linestyle='-',marker='')
            return

        plt.style.use('bmh')
        fig,ax = plt.subplots(figsize=(8,6))
        ax.set_xscale('log')
##        ax.set_yscale('log')

        PlotGroup = self.DataBaseLoad(PlotGroupKeyword)
        for i in range(len(PlotGroup)):
            PlotSingelData = PlotGroup[i]
            PlorSingle(ax, PlotSingelData, i)
            
        ax.legend(loc='upper right')
        plt.show()
        plt.close('all')
        return

    def PresetPipelineA(self):
        InputFileNameGroup = [
            ['xrt_flux_wtslew_DENSITY_nosys.qdp','wtslew'],
            ['xrt_flux_wt_DENSITY_nosys.qdp','wt'],
            ['xrt_flux_pc_DENSITY_nosys.qdp','pc']
            ]
        self.LoadXRTFile(InputFileNameGroup,'LCFluxDensityAll')
        self.LoadXRTFile([['xrt_flux_wtslew_DENSITY_nosys.qdp','wtslew']],'Swift XRT wtslew')
        self.LoadXRTFile([['xrt_flux_wt_DENSITY_nosys.qdp','wt']],'Swift XRT wt')
        self.LoadXRTFile([['xrt_flux_pc_DENSITY_nosys.qdp','pc']],'Swift XRT pc')

        if self.DataBaseLoad('LCFluxDensityAll') != []:
            self.DeadTimeIdentify('LCFluxDensityAll', 'FDADeadTime', 10, 10)
            self.SplitByDeadTime(['LCFluxDensityAll', 'FDADeadTime'],'LCFluxDensityAllSplited')
            self.XRTFilter('LCFluxDensityAllSplited',
                           ['XRTFiltered','LCFDASFFT','LCFDASFilteredFFT'])
            
            self.SplitByDeadTime(['XRTFiltered', 'FDADeadTime'],'XRTFSplited')
            
            self.PlotLcTypeA()
            self.PlotGroup('XRTFSplited')
            self.PlotFFTTypeA()
            
        else:
            print 'This GRB No Obs XRT Data!'
        return



##    def CalLCInGroup(self,InputGroupKeyword,SaveGroupKeywords):
##        def __CalLCInLC__(InputLC):
##            InputLC = map(list, zip(*InputLC))
##            SlopeCurve = []
##            
##            return SlopeCurve
##        
##        LCSplited = self.DataBaseLoad(InputGroupKeyword)
##        LCGroupReturn = []
##        
##        for i in range(len(LCSplited)):
##            SlopeCurve = __CalLCInLC__(LCSplited[i])
##            LCGroupReturn.append(SlopeCurve)
##            
##        self.DataBaseSave(SaveGroupKeywords, LCGroupReturn)
##        return

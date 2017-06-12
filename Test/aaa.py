import urllib
status=urllib.urlopen("http://www.swift.ac.uk/burst_analyser/00676595/bat/bat_z_cf_snr4_XRTBAND.qdp").code
print status
print (status == 200)

def DownloadSwiftLC(Table_Data, Directory):
    import socket
    import sys
    
    DownloadItem = [
#### BAT        
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_flux_timedel0.064_OBSDENSITY.qdp','BatLcBin64ms_','.qdp',Directory.BAT64ms_Data_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_gamma_timedel0.064_OBSDENSITY.qdp', 'BatLcBin64msGamma_','.qdp',Directory.BAT64msGamma_Data_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_cf_timedel0.064_OBSDENSITY.qdp', 'BatLcBin64msECF_','.qdp',Directory.BAT64msECF_Data_Directory],

        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_flux_timedel1_OBSDENSITY.qdp','BatLcBin1s_','.qdp',Directory.BAT1s_Data_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_gamma_timedel1_OBSDENSITY.qdp', 'BatLcBin1sGamma_','.qdp',Directory.BAT1sGamma_Data_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_cf_timedel1_OBSDENSITY.qdp', 'BatLcBin1sECF_','.qdp',Directory.BAT1sECF_Data_Directory],

        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_flux_timedel10_OBSDENSITY.qdp','BatLcBin10s_','.qdp',Directory.BAT10s_Data_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_gamma_timedel10_OBSDENSITY.qdp', 'BatLcBin10sGamma_','.qdp',Directory.BAT10sGamma_Data_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_cf_timedel10_OBSDENSITY.qdp', 'BatLcBin10sECF_','.qdp',Directory.BAT10sECF_Data_Directory],

        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_z_flux_snr5_DENSITY.qdp','BatLcBinSNR5_','.qdp',Directory.BATSNR5_Data_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_z_gamma_snr5_DENSITY.qdp', 'BatLcBinSNR5Gamma_','.qdp',Directory.BATSNR5Gamma_Data_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_z_cf_snr5_DENSITY.qdp', 'BatLcBinSNR5ECF_','.qdp',Directory.BATSNR5ECF_Data_Directory],

        [ 'http://gcn.gsfc.nasa.gov/swift_gnd_ana_lc/','_bat64ms_lc.txt','BatCounts64ms_','.txt',Directory.BATCounts64ms_Data_Directory],
#### XRT
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_flux_wtslew_DENSITY.qdp', 'xrtfluxwtslewDENSITY_','.qdp',Directory.xrt_flux_wtslew_DENSITY_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_flux_wtslew_DENSITY_nosys.qdp', 'xrtfluxwtslewDENSITYnosys_','.qdp',Directory.xrt_flux_wtslew_DENSITY_nosys_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_gamma_wtslew.qdp', 'XrtGammaWtslew_','.qdp',Directory.xrt_gamma_wtslew_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_cf_wtslew_DENSITY.qdp', 'XrtCfWtslewDENSITY_','.qdp',Directory.xrt_cf_wtslew_DENSITY_Directory],

        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_flux_wt_DENSITY.qdp', 'XrtFluxWtDENSITY_','.qdp',Directory.xrt_flux_wt_DENSITY_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_flux_wt_DENSITY_nosys.qdp', 'XrtFluxWtDENSITYnosys_','.qdp',Directory.xrt_flux_wt_DENSITY_nosys_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_gamma_wt.qdp', 'XrtGammaWt_','.qdp',Directory.xrt_gamma_wt_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_cf_wt_DENSITY.qdp', 'XrtCfWtDENSITY_','.qdp',Directory.xrt_cf_wt_DENSITY_Directory],

        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_flux_pc_DENSITY.qdp', 'XrtFluxPcDENSITY_','.qdp',Directory.xrt_flux_pc_DENSITY_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_flux_pc_DENSITY_nosys.qdp', 'XrtFluxPcDENSITYnosys_','.qdp',Directory.xrt_flux_pc_DENSITY_nosys_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_gamma_pc.qdp', 'XrtGammaPc_','.qdp',Directory.xrt_gamma_pc_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_cf_pc_DENSITY.qdp', 'XrtCfPcDENSITY_','.qdp',Directory.xrt_cf_pc_DENSITY_Directory],
#### BAT XRT 10KeV
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_flux_timedel0.064_XRTBAND.qdp', 'BatFluxTimedel64msXRTBAND_','.qdp',Directory.bat_flux_timedel64ms_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_gamma_timedel0.064_XRTBAND.qdp', 'BatGammaTimedel64msXRTBAND_','.qdp',Directory.bat_gamma_timedel64ms_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_cf_timedel0.064_XRTBAND.qdp', 'BatCfTimedel64msXRTBAND_','.qdp',Directory.bat_cf_timedel64ms_XRTBAND_Directory],

        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_flux_timedel1_XRTBAND.qdp', 'BatFluxTimedel1XRTBAND_','.qdp',Directory.bat_flux_timedel1_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_gamma_timedel1_XRTBAND.qdp', 'BatGammaTimedel1XRTBAND_','.qdp',Directory.bat_gamma_timedel1_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_cf_timedel1_XRTBAND.qdp', 'BatCfTimedel1XRTBAND_','.qdp',Directory.bat_cf_timedel1_XRTBAND_Directory],

        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_flux_timedel10_XRTBAND.qdp', 'BatFluxTimedel10XRTBAND_','.qdp',Directory.bat_flux_timedel10_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_gamma_timedel10_XRTBAND.qdp', 'BatGammaTimedel10XRTBAND_','.qdp',Directory.bat_gamma_timedel10_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_cf_timedel10_XRTBAND.qdp', 'BatCfTimedel10XRTBAND_','.qdp',Directory.bat_cf_timedel10_XRTBAND_Directory],

        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_z_flux_snr5_XRTBAND.qdp', 'BatZFluxSnr5XRTBAND_','.qdp',Directory.bat_z_flux_snr5_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_z_gamma_snr5_XRTBAND.qdp', 'BatZGammaSnr5XRTBAND_','.qdp',Directory.bat_z_gamma_snr5_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/bat/bat_z_cf_snr5_XRTBAND.qdp', 'BatZCfSnr5XRTBAND_','.qdp',Directory.bat_z_cf_snr5_XRTBAND_Directory],

        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_flux_wtslew_XRTBAND.qdp', 'XrtFluxWtslewXRTBAND_','.qdp',Directory.xrt_flux_wtslew_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_flux_wtslew_XRTBAND_nosys.qdp', 'XrtFluxWtslewXRTBANDnosys_','.qdp',Directory.xrt_flux_wtslew_XRTBAND_nosys_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_gamma_wtslew.qdp', 'XrtGammaWtslew_','.qdp',Directory.xrt_gamma_wtslew_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_cf_wtslew_XRTBAND.qdp', 'XrtCfWtslewXRTBAND_','.qdp',Directory.xrt_cf_wtslew_XRTBAND_Directory],

        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_flux_wt_XRTBAND.qdp', 'XrtFluxWtXRTBAND_','.qdp',Directory.xrt_flux_wt_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_flux_wt_XRTBAND_nosys.qdp', 'XrtFluxWtXRTBANDnosys_','.qdp',Directory.xrt_flux_wt_XRTBAND_nosys_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_gamma_wt.qdp', 'XrtGammaWt_','.qdp',Directory.xrt_gamma_wt_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_cf_wt_XRTBAND.qdp', 'XrtCfWtXRTBAND_','.qdp',Directory.xrt_cf_wt_XRTBAND_Directory],

        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_flux_pc_XRTBAND.qdp', 'XrtFluxPcXRTBAND_','.qdp',Directory.xrt_flux_pc_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_flux_pc_XRTBAND_nosys.qdp', 'XrtFluxPcXRTBANDnosys_','.qdp',Directory.xrt_flux_pc_XRTBAND_nosys_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_gamma_pc.qdp', 'XrtGammaPc_','.qdp',Directory.xrt_gamma_pc_XRTBAND_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/xrt/xrt_cf_pc_XRTBAND.qdp', 'XrtCfPcXRTBAND_','.qdp',Directory.xrt_cf_pc_XRTBAND_Directory],
#### UVOT
        [ 'http://www.swift.ac.uk/burst_analyser/00','/uvot/white.qdp', 'UVOTWhite_','.qdp',Directory.UVOT_white_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/uvot/white_UL.qdp', 'UVOTWhiteUL_','.qdp',Directory.UVOT_white_UL_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/uvot/v_UL.qdp', 'UVOTvUL_','.qdp',Directory.UVOT_v_UL_Directory],

        [ 'http://www.swift.ac.uk/burst_analyser/00','/uvot/b_UL.qdp', 'UVOTbUL_','.qdp',Directory.UVOT_b_UL_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/uvot/u.qdp', 'UVOTu_','.qdp',Directory.UVOT_u_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/uvot/u_UL.qdp', 'UVOTuUL_','.qdp',Directory.UVOT_u_UL_Directory],

        [ 'http://www.swift.ac.uk/burst_analyser/00','/uvot/uvw1.qdp', 'UVOTuvw1_','.qdp',Directory.UVOT_uvw1_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/uvot/uvw1_UL.qdp', 'UVOTuvw1UL_','.qdp',Directory.UVOT_uvw1_UL_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/uvot/uvw2_UL.qdp', 'UVOTuvw2UL_','.qdp',Directory.UVOT_uvw2_UL_Directory],
        [ 'http://www.swift.ac.uk/burst_analyser/00','/uvot/uvm2_UL.qdp', 'UVOTuvm2UL_','.qdp',Directory.UVOT_uvm2_UL_Directory]
####        [ 'http://www.swift.ac.uk/burst_analyser/00','', '','.qdp',Directory.]

        ]
    table_axis_y = len(Table_Data)
    Timeout = 60.0
    TimpOutCatalog = []
    
    for EachDLItem in DownloadItem:
        print 'Download: ',EachDLItem[2][:-1]
        for i in range(table_axis_y):
            Tigger_Number = Table_Data[i][2]
            try:
                int(Tigger_Number)
            except:
##                print Tigger_Number
                continue
            GRB_Name = Table_Data[i][0]
            DownLoad_Page = EachDLItem[0] + Tigger_Number + EachDLItem[1]
            GRB_File_Name = EachDLItem[2] + GRB_Name + EachDLItem[3]
            GRB_File_Position = os.path.join(EachDLItem[4],GRB_File_Name)
##            if EachDLItem[1] == '/bat/bat_z_cf_snr5_DENSITY.qdp':
##                print 'Download: ',i+1,' in ',table_axis_y
            if os.path.exists(GRB_File_Position):
##                print GRB_File_Name,' already exist, pass.'
                pass
            else:
                print 'Download: ',i+1,' in ',table_axis_y
                try:
##                    print DownLoad_Page,GRB_File_Position
                    socket.setdefaulttimeout(Timeout)
                    urllib.urlretrieve(DownLoad_Page,GRB_File_Position)
                except:
                    TimpOutCatalog.append([DownLoad_Page,GRB_File_Position])
                    if os.path.exists(GRB_File_Position):
                        os.remove(GRB_File_Position)
                        print 'Error file has been remove:',GRB_File_Name
                    if socket.error:
                        errno, errstr = sys.exc_info()[:2] 
                        if errno == socket.timeout:
                            print 'There was a timeout:',GRB_File_Name
                    else: 
                        print 'Download: ',GRB_File_Name,' Fail, pass.'

    print '====================='
    if TimpOutCatalog != []:
        print 'TimpOutCatalog: '
        for Item in TimpOutCatalog:
            print Item[0]
        print 'Try Again...'

        for Item in TimpOutCatalog:
            DownLoad_Page = Item[0]
            GRB_File_Position = Item[1]
            try:
                socket.setdefaulttimeout(Timeout*2)
                urllib.urlretrieve(DownLoad_Page,GRB_File_Position)
            except:
                print DownLoad_Page,'\t',GRB_File_Position
                if os.path.exists(GRB_File_Position):
                    os.remove(GRB_File_Position)
                    print 'Error file has been remove:',GRB_File_Position
                if socket.error:
                    errno, errstr = sys.exc_info()[:2] 
                    if errno == socket.timeout:
                        print 'There was a timeout:'
                else: 
                    print 'Download Fail, pass.'
    
    return

#coding=utf-8
import urllib
import socket
import os
import re
import sys

class Set_Website():
    def __init__(self):
        return

def __UpdateSwiftTable__(Directory):
    from bs4 import BeautifulSoup

    Dir = Directory.DirTemp
    Match = None
    Website = 'https://swift.gsfc.nasa.gov/archive/grb_table/fullview/'
    WebsiteNASA = 'https://swift.gsfc.nasa.gov/'
    DirTemp = os.path.join(Dir,'fullview.html')
    urllib.urlretrieve(Website,DirTemp)
    SwiftTable = open(DirTemp, "rU")
    soup = BeautifulSoup(SwiftTable)
    for link in soup.find_all('li'):
        for href in link.find_all('a'):
            Match = re.search('.*grb_table.*\.txt',href.get('href'))
            if Match:
                URLSwiftTable = WebsiteNASA + Match.group()
                break
    urllib.urlretrieve(URLSwiftTable,Directory.FileSwiftTable)
    SwiftTable.close()
    os.remove(DirTemp)
    return

def __FileReadSwiftTable__(File_Position):
    Table_Data = []
    fp = open(File_Position,'rU')
    for eachline in fp:
        eachline = eachline.rstrip('\n')
#        eachline = re.sub(',+', ' ', eachline)
#        eachline = re.sub(' +', '\t', eachline)
#        eachline = re.sub('\t+', '\t', eachline)
#        eachline = eachline.lstrip('\t')
        DataCache = eachline.split('\t')
        Table_Data.append(DataCache)
    fp.close()
    table_axis_x = len(Table_Data[0])
    table_axis_y = len(Table_Data)
    
    for i in range(table_axis_y):
        for j in range(table_axis_x):
#'Trigger Number' and 'name' not convert to int 
            if (j == 2)or(j == 0):
                continue
            try:
                Table_Data[i][j] = float(Table_Data[i][j])
            except:
                pass
    return Table_Data


def GetTrigger(Table_Data):
    TriggerGroup = []
    table_axis_y = len(Table_Data)
    for i in range(table_axis_y):
        Tigger_Number = Table_Data[i][2]
        try:
            int(Tigger_Number)
        except:
##            print Tigger_Number
            continue
        GRB_Name = Table_Data[i][0]
        TriggerGroup.append([GRB_Name,Tigger_Number])
    return TriggerGroup

def DownloadSingleGRBCore(DirSingle,Class,Tigger_Number,DownloadFile,TryNumber=0):
    Timeout = 60.0
    MaxTry = 3
    WebsiteTotal = 'http://www.swift.ac.uk/burst_analyser/00'
    TempClass = Class.lower()
    WebsiteSingle = WebsiteTotal + Tigger_Number + '/' + TempClass + '/'
    TempClass = Class.upper()
    DirSaveSingle = os.path.join(DirSingle,TempClass)
    for Item in DownloadFile:
##        print Item
        WebsiteSingelFinal = WebsiteSingle + Item
        DirSaveSingleFinal = os.path.join(DirSaveSingle,Item)
##        print WebsiteSingelFinal
##        print DirSaveSingleFinal
        if os.path.exists(DirSaveSingleFinal):
##            print DirSaveSingleFinal,' already exist, pass.'
            pass
        else:
            status=urllib.urlopen(WebsiteSingelFinal).code
            if status == 200:
                try:
                    socket.setdefaulttimeout(Timeout)
                    urllib.urlretrieve(WebsiteSingelFinal,DirSaveSingleFinal)
                except:
                    print DirSingle
                    if os.path.exists(DirSaveSingleFinal):
                        os.remove(DirSaveSingleFinal)
                        print 'Error file has been remove:',Item
                    if socket.error:
                        errno, errstr = sys.exc_info()[:2] 
                        if errno == socket.timeout:
                            print 'There was a timeout:',Item
                        TryNumber+=1
                        if TryNumber <= MaxTry:
                            print 'Download: ',Item,' Fail, Try Again.'
                            DownloadSingleGRBCore(DirSingle,Class,Tigger_Number,[Item],TryNumber)
            else:
                continue
    return

def DownloadSingleGRB(Single,Directory):
    print 'Download: GRB',Single[0]
    
    DownloadFileBAT = [
        'bat_cf_timedel0.064_BATBAND.qdp',
        'bat_cf_timedel0.064_OBSDENSITY.qdp',
        'bat_cf_timedel0.064_XRTBAND.qdp',
        'bat_cf_timedel1_BATBAND.qdp',
        'bat_cf_timedel1_OBSDENSITY.qdp',
        'bat_cf_timedel1_XRTBAND.qdp',
        'bat_cf_timedel10_BATBAND.qdp',
        'bat_cf_timedel10_OBSDENSITY.qdp',
        'bat_cf_timedel10_XRTBAND.qdp',
        'bat_flux_timedel0.064_BATBAND.qdp',
        'bat_flux_timedel0.064_OBSDENSITY.qdp',
        'bat_flux_timedel0.064_XRTBAND.qdp',
        'bat_flux_timedel1_BATBAND.qdp',
        'bat_flux_timedel1_OBSDENSITY.qdp',
        'bat_flux_timedel1_XRTBAND.qdp',
        'bat_flux_timedel10_BATBAND.qdp',
        'bat_flux_timedel10_OBSDENSITY.qdp',
        'bat_flux_timedel10_XRTBAND.qdp',
        'bat_gamma_timedel0.064_BATBAND.qdp',
        'bat_gamma_timedel0.064_OBSDENSITY.qdp',
        'bat_gamma_timedel0.064_XRTBAND.qdp',
        'bat_gamma_timedel1_BATBAND.qdp',
        'bat_gamma_timedel1_OBSDENSITY.qdp',
        'bat_gamma_timedel1_XRTBAND.qdp',
        'bat_gamma_timedel10_BATBAND.qdp',
        'bat_gamma_timedel10_OBSDENSITY.qdp',
        'bat_gamma_timedel10_XRTBAND.qdp',
        'bat_z_cf_snr4_BATBAND.qdp',
        'bat_z_cf_snr4_XRTBAND.qdp',
        'bat_z_cf_snr5_BATBAND.qdp',
        'bat_z_cf_snr5_DENSITY.qdp',
        'bat_z_cf_snr5_XRTBAND.qdp',
        'bat_z_cf_snr6_BATBAND.qdp',
        'bat_z_cf_snr6_XRTBAND.qdp',
        'bat_z_cf_snr7_BATBAND.qdp',
        'bat_z_cf_snr7_XRTBAND.qdp',
        'bat_z_flux_snr4_BATBAND.qdp',
        'bat_z_flux_snr4_XRTBAND.qdp',
        'bat_z_flux_snr5_BATBAND.qdp',
        'bat_z_flux_snr5_DENSITY.qdp',
        'bat_z_flux_snr5_XRTBAND.qdp',
        'bat_z_flux_snr6_BATBAND.qdp',
        'bat_z_flux_snr6_XRTBAND.qdp',
        'bat_z_flux_snr7_BATBAND.qdp',
        'bat_z_flux_snr7_XRTBAND.qdp',
        'bat_z_gamma_snr4_BATBAND.qdp',
        'bat_z_gamma_snr4_XRTBAND.qdp',
        'bat_z_gamma_snr5_BATBAND.qdp',
        'bat_z_gamma_snr5_DENSITY.qdp',
        'bat_z_gamma_snr5_XRTBAND.qdp',
        'bat_z_gamma_snr6_BATBAND.qdp',
        'bat_z_gamma_snr6_XRTBAND.qdp',
        'bat_z_gamma_snr7_BATBAND.qdp',
        'bat_z_gamma_snr7_XRTBAND.qdp'
        ]
    DownloadFileXRT = [
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
    DownloadFileUVOT = [
        'b.qdp',
        'b_UL.qdp',
        'u.qdp',
        'u_UL.qdp',
        'uvm2.qdp',
        'uvm2_UL.qdp',
        'uvw1.qdp',
        'uvw1_UL.qdp',
        'uvw2.qdp',
        'uvw2_UL.qdp',
        'v.qdp',
        'v_UL.qdp',
        'white.qdp',
        'white_UL.qdp'
        ]
        
    GRB_Name = Single[0]
    Tigger_Number = Single[1]
    DirTotal = Directory.DirSwiftData
    DirSingle = os.path.join(DirTotal,GRB_Name)
    if os.path.exists(DirSingle):
        pass
    else:
        os.makedirs(DirSingle)
        os.makedirs(os.path.join(DirSingle,'BAT'))
        os.makedirs(os.path.join(DirSingle,'XRT'))
        os.makedirs(os.path.join(DirSingle,'UVOT'))
    DownloadSingleGRBCore(DirSingle,'BAT',Tigger_Number,DownloadFileBAT)
    DownloadSingleGRBCore(DirSingle,'XRT',Tigger_Number,DownloadFileXRT)
##    DownloadSingleGRBCore(DirSingle,'UVOT',Tigger_Number,DownloadFileUVOT)
    return

def __UpdateSwiftXRTdata__(Directory):
    from multiprocessing import Pool, cpu_count
    DirGroup = []
    Table_Data = __FileReadSwiftTable__(Directory.FileSwiftTable)
    TriggerGroup = GetTrigger(Table_Data)

    pool = Pool(cpu_count())
    RangeGroup = len(TriggerGroup)
    for i in range(RangeGroup):
        pool.apply_async(DownloadSingleGRB, (TriggerGroup[i],Directory))
    pool.close()
    pool.join()
    return

def SwiftXRT(Directory,DownloadType='Update'):
    if DownloadType == 'Complete':
        Directory.DirClean(Directory.DirSwiftData)
    if DownloadType == 'No':
        return
    else:
##        print 'Swift Table Updating...'
##        __UpdateSwiftTable__(Directory)
        print 'Swift Data Updating...'
        __UpdateSwiftXRTdata__(Directory)
    return


import os


class AnalysisXRT:
    def __init__(self, dir_grb):
        
        self.dir_grb = dir_grb
        self.dir_current = os.getcwd()
        self.grb_name = os.path.split(self.dir_grb)[-1]
        self.dir_xrt = self.dir_make('XRT', self.dir_grb)
        self.dir_return = self.dir_make('Return', self.dir_grb)
        self.list_xrt = self.ergodic_folder(self.dir_xrt)
        self.data_base = dict()
        self.file_xrt_full = [
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
#        self.lcFluxDensityAll = self.load_xrt_file()
        return

    def dir_make(self, dir_name, dir_path=None):
        if dir_path is None:
            dir_path = self.dir_current
        dir_need = os.path.join(dir_path, dir_name)
        if os.path.exists(dir_need):
            pass
        else:
            os.makedirs(dir_need)
        return dir_need
    
    @staticmethod
    def ergodic_folder(directory):
        file_list = []
        for root, dirs, files in os.walk(directory):
            for single_file in files:
                file_list.append(os.path.join(root, single_file))
        return file_list

    def data_base_save(self, keyword, value):
        self.data_base[keyword] = value
        return

    def data_base_load(self, keyword):
        return self.data_base[keyword]

    def data_base_keys_list(self):
        for item in self.data_base:
            print item
        return

    @staticmethod
    def load_swift_file(file_path, data_type=0):
        import re
        """data_type == 0, Just use good data; data_type == 1, Use good and bad data"""

        file_cache = []
        fp = open(file_path, 'rU')
        
        for each_line in fp:
            each_line = each_line.rstrip('\n')
            if r'!#' in each_line:
                each_line = re.sub(r'!#', '', each_line)
                line_cache = each_line.split('\t')
                for i in range(len(line_cache)):
                    line_cache[i] = float(line_cache[i])
                if data_type == 0:
                    continue
            else:
                try:
                    line_cache = each_line.split('\t')
                    for i in range(len(line_cache)):
                        line_cache[i] = float(line_cache[i])
                except:
                    continue
            file_cache.append(line_cache)
        fp.close()
        return file_cache

    def load_xrt_file(self, input_file_name_group, save_kw):

        def load_xrt_file_add_tag(self, file_name, tag):
            file_cache = []
            file_path = os.path.join(self.dir_xrt, file_name)
            if os.path.exists(file_path):
                file_cache = self.load_swift_file(file_path)
                for Item in file_cache:
                    Item.append(tag)
            return file_cache
        
        total_cache = []

        for file_name, tag in input_file_name_group:
            file_cache = load_xrt_file_add_tag(self, file_name, tag)
            total_cache.extend(file_cache)

        self.data_base_save(save_kw, total_cache)
        return

    def dead_time_identify(
            self, load_lc_data_kw, save_dead_time_index_kw, time_gap_threshold=10, time_bin_gap_ignore_ratio=5):

        file = self.data_base_load(load_lc_data_kw)
        dead_time_group = []
        for i in range(len(file)-1):
            time_value_pre_end = file[i][0] + file[i][1]
            time_value_lat_beg = file[i+1][0] + file[i+1][2]
            time_bin_gap = time_value_lat_beg - time_value_pre_end
            
            if time_bin_gap > time_gap_threshold:
                if (file[i][0]/time_bin_gap < time_bin_gap_ignore_ratio)and(file[i][0] < 200000):
                    dead_time_group.append(i)
        self.data_base_save(save_dead_time_index_kw, dead_time_group)
        return

    def split_by_dead_time(self, input_group, save_kw_lc_split):
        lc_split = []
        
        input_lc = self.data_base_load(input_group[0])
        
        input_dead_time_index = self.data_base_load(input_group[1])[::-1]
        input_dead_time_index.append(-1)
        
        split_temp = -1
        length_group = len(input_lc)
        
        for Item in input_dead_time_index:
            if (Item+1 != split_temp) & (Item+2 != length_group):
                split_temp_sub = input_lc[Item+1:split_temp]
                if split_temp == -1:
                    split_temp_sub.append(input_lc[split_temp])
                lc_split.append(split_temp_sub)
            else:
                lc_split.append([input_lc[Item+1]])
            split_temp = Item + 1
            
        lc_split = lc_split[::-1]
        self.data_base_save(save_kw_lc_split, lc_split)
        return

    def xrt_filter(self, input_lc_kw, save_group_kw):
        
        def _xrt_filter_core(group_in):
            from scipy import signal
            import numpy as np
            
            def _xrt_filter_core_lpf(lc, lc_error, b, a, mc_times=100):
                
                def _xrt_filter_core_mc(lc, lc_error):
                    lc_new_by_mc = []
                    for i in range(len(value)):
                        lc_new_by_mc.append(np.random.normal(lc[i], abs(lc_error[i])))
                    return lc_new_by_mc
            
                lc_new_by_mc_f_group = []
                lc_new_by_mc_f_final_value = []
                lc_new_by_mc_f_final_error = []
                
                for i in range(mc_times):
                    lc_new_by_mc = _xrt_filter_core_mc(lc, lc_error)
                    lc_new_by_mc_f = signal.filtfilt(b, a, lc_new_by_mc)
                    lc_new_by_mc_f_group.append(lc_new_by_mc_f)
                lc_new_by_mc_f_group = map(list, zip(*lc_new_by_mc_f_group))
                
                for i in range(len(lc_new_by_mc_f_group)):
                    lc_new_by_mc_f_final_value.append(np.mean(lc_new_by_mc_f_group[i]))
                    lc_new_by_mc_f_final_error.append(np.sqrt(np.var(lc_new_by_mc_f_group[i])))
                    
                lc_new_by_mc_f_final = [lc_new_by_mc_f_final_value, lc_new_by_mc_f_final_error]
                return lc_new_by_mc_f_final
            
            group_in = map(list, zip(*group_in))
            value = group_in[3]
            err_pos = group_in[4]
            err_neg = group_in[5]

            group_sampling_fs = []
            for i in range(len(group_in[0])-1):
                time_gap = group_in[0][i+1]-group_in[0][i]
                group_sampling_fs.append(1.0/time_gap)
            fs = np.mean(group_sampling_fs)
            fs_err = np.sqrt(np.var(group_sampling_fs))
            wn = 0.04/(fs/2)
            print 'Wn:', wn, ', Fs:', fs, 'Hz, Fs_err(Per):', 100*fs_err/fs, '%'
            wn = min([wn, 0.25])

            mc_number = 1000

            b, a = signal.butter(3, wn, 'low')

            lc_new_by_mc_f_final_pos = _xrt_filter_core_lpf(value, err_pos, b, a, mc_number)
            value_pos = lc_new_by_mc_f_final_pos[0]
            err_pos = lc_new_by_mc_f_final_pos[1]

            lc_new_by_mc_f_final_neg = _xrt_filter_core_lpf(value, err_neg, b, a, mc_number)
            value_neg = lc_new_by_mc_f_final_neg[0]
            err_neg = lc_new_by_mc_f_final_neg[1]

            value_f = []
            for i in range(len(value_pos)):
                value_f.append(np.mean([value_pos[i], value_neg[i]]))
            
            group_out = group_in
            group_out[3] = value_f
            group_out[4] = err_pos
            group_out[5] = err_neg
            group_out = map(list, zip(*group_out))
            return group_out
        
        def _spectrum_fft(group_in):

            import numpy as np
            group_in = map(list, zip(*group_in))
            group_out = []
            sample = group_in[3]
            
            group_sampling_fs = []
            for i in range(len(group_in[0])-1):
                time_gap = group_in[0][i+1]-group_in[0][i]
                group_sampling_fs.append(1.0/time_gap)
            fs = np.mean(group_sampling_fs)
            fft_size = len(sample)
            xf = np.fft.rfft(sample)/fft_size
            freqs = np.linspace(0, fs/2, fft_size/2+1)
            xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100))

            group_out.append(freqs)
            group_out.append(xfp)
            group_out = map(list, zip(*group_out))
            
            return group_out

        lc_split_fft = []
        lc_split_filtered_fft = []

        lc_split = self.data_base_load(input_lc_kw)
            
        for i in range(len(lc_split)):
            if len(lc_split[i]) > 12:
                lc_split_fft.append(_spectrum_fft(lc_split[i]))
                lc_split[i] = _xrt_filter_core(lc_split[i])
                lc_split_filtered_fft.append(_spectrum_fft(lc_split[i]))

        lc_filtered = []
        
        for i in range(len(lc_split)):
            lc_filtered.extend(lc_split[i])

        self.data_base_save(save_group_kw[0], lc_filtered)
        self.data_base_save(save_group_kw[1], lc_split_fft)
        self.data_base_save(save_group_kw[2], lc_split_filtered_fft)
        
        return

    # def find_peak_in_group(self,input_group_kw, save_group_kw):
    #     def _find_peak_in_lc(input_lc):
    #         return
    #     return

    def cal_lc_slope_in_group(self, input_group_kw, save_group_kw):
        def _cal_lc_slope_in_lc(input_lc):
            
            def _cal_ponit_slope_by_mc(p1, p2):
                import numpy as np

                def _give_value_by_mc(value, err_pos, err_neg):
                    pn = np.random.rand()
                    if pn > 0.5:
                        value = value + np.random.normal(0.0, abs(err_pos))
                    else:
                        value = value - np.random.normal(0.0, abs(err_neg))
                    return value

                mc_slope_group = []
                for i in range(1000):
                    p1_value_mc = _give_value_by_mc(p1[3], p1[4], p1[5])
                    p2_value_mc = _give_value_by_mc(p2[3], p2[4], p2[5])
                    temp_mc_slope = (p2_value_mc-p1_value_mc)/(p2[0]-p1[0])
                    mc_slope_group.append(temp_mc_slope)
                    
                slope_most_prob = (p2[3]-p1[3])/(p2[0]-p1[0])
#                slope_most_prob = np.mean(mc_slope_group)
                mc_slope_group_err_pos = []
                mc_slope_group_err_neg = []
                for i in range(len(mc_slope_group)):
                    if mc_slope_group[i] > slope_most_prob:
                        mc_slope_group_err_pos.append(mc_slope_group[i])
                        err = abs(mc_slope_group[i] - slope_most_prob)
                        value_mirror = slope_most_prob - err
                        mc_slope_group_err_pos.append(value_mirror)
                    elif mc_slope_group[i] < slope_most_prob:
                        mc_slope_group_err_neg.append(mc_slope_group[i])
                        err = abs(slope_most_prob - mc_slope_group[i])
                        value_mirror = slope_most_prob + err
                        mc_slope_group_err_pos.append(value_mirror)
                    
                slope = slope_most_prob
                slope_err_pos = np.var(mc_slope_group_err_pos)
                slope_err_neg = np.var(mc_slope_group_err_neg)
                return [slope, slope_err_pos, slope_err_neg]
#            input_lc = map(list, zip(*input_lc))
            slope_curve = []
            for i in range(len(input_lc)-1):
                p1 = input_lc[i]
                p2 = input_lc[i+1]
                slope = _cal_ponit_slope_by_mc(p1, p2)
                slope_curve.append([input_lc[i][0], input_lc[i][1], input_lc[i][2], slope[0], slope[1], slope[2]])
            return slope_curve
        
        lc_split = self.data_base_load(input_group_kw)
        lc_group_return = []
        
        for i in range(len(lc_split)):
            if len(lc_split[i]) > 3:
                slope_curve = _cal_lc_slope_in_lc(lc_split[i])
                lc_group_return.append(slope_curve)
            
        self.data_base_save(save_group_kw, lc_group_return)
        return

    def cal_log_in_group(self, input_group_kw, save_group_kw):
        import math

        def _cal_log_in_lc(input_lc):
            new_curve = []
            for i in range(len(input_lc)):
                new_value_x = math.log10(input_lc[i][0])
                new_err_pos_x = math.log10(input_lc[i][0]+abs(input_lc[i][1])) - new_value_x
                new_err_neg_x = new_value_x - math.log10(input_lc[i][0]-abs(input_lc[i][2]))
                new_value_y = math.log10(input_lc[i][3])
                new_err_pos_y = math.log10(input_lc[i][3]+abs(input_lc[i][4])) - new_value_y
                new_err_neg_y = new_value_y - math.log10(input_lc[i][3]-abs(input_lc[i][5]))

                new_curve.append(
                    [new_value_x, new_err_pos_x, new_err_neg_x,
                     new_value_y, new_err_pos_y, new_err_neg_y,
                     input_lc[i][6]])

            return new_curve
        
        lc_split = self.data_base_load(input_group_kw)
        lc_group_return = []

        for i in range(len(lc_split)):
            new_curve = _cal_log_in_lc(lc_split[i])
            lc_group_return.append(new_curve)
            
        self.data_base_save(save_group_kw, lc_group_return)
        return

    def plot_lc_type_a(self, plot_kw_group=['xrt_filtered', 'Swift XRT wtslew', 'Swift XRT wt', 'Swift XRT pc']):
        def _plot_group_est(group_in):
            group_out = group_in
            group_out = map(list, zip(*group_out))
            group_out[2] = map(abs, group_out[2])
            group_out[5] = map(abs, group_out[5])
            return group_out
        
        import matplotlib.pyplot as plt
        
        plt.style.use('bmh')
        fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(13, 6))
        ax0.patch.set_facecolor('white')
        ax0.set_xscale('log')
        ax0.set_yscale('log')
        ax0.set_xlabel(r'$\rm Time\ After\ Trigger\ $[$s$]', fontsize=16)
        ax0.set_ylabel(r'$\rm Flux\ Density\ at\ 10$$\ KeV$', fontsize=16)
        pic_sub_title = r'Swift lc Filtered GRB '+self.grb_name[1]
        ax0.set_title(pic_sub_title, fontsize=16)
        ax1.patch.set_facecolor('white')
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel(r'$\rm Time\ After\ Trigger\ $[$s$]', fontsize=16)
        ax1.set_ylabel(r'$\rm Flux\ Density\ at\ 10$$\ KeV$', fontsize=16)
        pic_sub_title = r'Swift lc Origin GRB '+self.grb_name[1]
        ax1.set_title(pic_sub_title, fontsize=16)

        xrt_filtered = self.data_base_load(plot_kw_group[0])
        file_cache_wtslew = self.data_base_load(plot_kw_group[1])
        file_cache_wt = self.data_base_load(plot_kw_group[2])
        file_cache_pc = self.data_base_load(plot_kw_group[3])
        
        if xrt_filtered is not []:
            plot_temp = _plot_group_est(xrt_filtered)
            ax0.errorbar(plot_temp[0], plot_temp[3],
                         xerr=[plot_temp[2], plot_temp[1]],
                         yerr=[plot_temp[5], plot_temp[4]],
                         label=r'Swift XRT', alpha=0.8, linestyle='', marker='')
            
        if file_cache_wtslew is not []:
            plot_temp_wtslew = _plot_group_est(file_cache_wtslew)
            ax1.errorbar(plot_temp_wtslew[0], plot_temp_wtslew[3],
                         xerr=[plot_temp_wtslew[2], plot_temp_wtslew[1]],
                         yerr=[plot_temp_wtslew[5], plot_temp_wtslew[4]],
                         label=r'Swift XRT wtslew', alpha=0.8, linestyle='', color='cyan', marker='')

        if file_cache_wt is not []:
            plot_temp_wt = _plot_group_est(file_cache_wt)
            ax1.errorbar(plot_temp_wt[0], plot_temp_wt[3],
                         xerr=[plot_temp_wt[2], plot_temp_wt[1]],
                         yerr=[plot_temp_wt[5], plot_temp_wt[4]],
                         label=r'Swift XRT wt', alpha=0.8, linestyle='', color='royalblue', marker='')

        if file_cache_pc is not []:
            plot_temp_pc = _plot_group_est(file_cache_pc)
            ax1.errorbar(plot_temp_pc[0], plot_temp_pc[3],
                         xerr=[plot_temp_pc[2], plot_temp_pc[1]],
                         yerr=[plot_temp_pc[5], plot_temp_pc[4]],
                         label=r'Swift XRT pc', alpha=0.8, linestyle='', color='r', marker='')

        ax0.legend(loc='upper right')
        plt.show()
        plt.close('all')
        
        return

    def plot_fft_type_a(self):
        import matplotlib.pyplot as plt
        plt.style.use('bmh')
        fig, axes = plt.subplots(ncols=2, nrows=3, figsize=(13, 6))
        
        lc_flux_density_all_split_fft = self.data_base_load('lcFDASFFT')
        lc_flux_density_all_split_fft_filtered = self.data_base_load('lcFDASFilteredFFT')
        
        axes[0, 0].patch.set_facecolor('white')
        axes[0, 0].set_ylabel(r'$\rm 1st\ Obs$ [$Db$]', fontsize=16)
        pic_sub_title = r'Swift lc FFT GRB '+self.grb_name[1]
        axes[0, 0].set_title(pic_sub_title, fontsize=16)
        axis_x = map(list, zip(*lc_flux_density_all_split_fft[0]))[0]
        axis_y = map(list, zip(*lc_flux_density_all_split_fft[0]))[1]
        axes[0, 0].plot(axis_x, axis_y)
        axes[0, 0].set_yticks([-60, -80, -100, -120, -140])
        axes[0, 0].set_xticks([0.00, 0.04, 0.08, 0.12, 0.16])
        axes[0, 0].set_xlim([0, 0.16])

        axes[0, 1].patch.set_facecolor('white')
        axes[0, 1].set_ylabel(r'$\rm 1st\ Obs$ [$Db$]', fontsize=16)
        pic_sub_title = r'Swift lc FFT Filtered GRB '+self.grb_name[1]
        axes[0, 1].set_title(pic_sub_title, fontsize=16)
        axis_x = map(list, zip(*lc_flux_density_all_split_fft_filtered[0]))[0]
        axis_y = map(list, zip(*lc_flux_density_all_split_fft_filtered[0]))[1]
        axes[0, 1].plot(axis_x, axis_y)
        axes[0, 1].set_yticks([-60, -80, -100, -120, -140])
        axes[0, 1].set_xticks([0.00, 0.04, 0.08, 0.12, 0.16])
        axes[0, 1].set_xlim([0, 0.16])
        
        axes[1, 0].patch.set_facecolor('white')
        axes[1, 0].set_ylabel(r'$\rm 2nd\ Obs$ [$Db$]', fontsize=16)
        axis_x = map(list, zip(*lc_flux_density_all_split_fft[1]))[0]
        axis_y = map(list, zip(*lc_flux_density_all_split_fft[1]))[1]
        axes[1, 0].plot(axis_x, axis_y)
        axes[1, 0].set_yticks([-60, -80, -100, -120, -140])
        axes[1, 0].set_xticks([0.00, 0.02, 0.04, 0.06, 0.08])
        axes[1, 0].set_xlim([0, 0.08])

        axes[1, 1].patch.set_facecolor('white')
        axes[1, 1].set_ylabel(r'$\rm 2nd\ Obs$ [$Db$]', fontsize=16)
        axis_x = map(list, zip(*lc_flux_density_all_split_fft_filtered[1]))[0]
        axis_y = map(list, zip(*lc_flux_density_all_split_fft_filtered[1]))[1]
        axes[1, 1].plot(axis_x, axis_y)
        axes[1, 1].set_yticks([-60, -80, -100, -120, -140])
        axes[1, 1].set_xticks([0.00, 0.02, 0.04, 0.06, 0.08])
        axes[1, 1].set_xlim([0, 0.08])

        axes[2, 0].patch.set_facecolor('white')
        axes[2, 0].set_xlabel(r'$\rm Frequence $ [$Hz$]', fontsize=16)
        axes[2, 0].set_ylabel(r'$\rm 3rd\ Obs$ [$Db$]', fontsize=16)
        axis_x = map(list, zip(*lc_flux_density_all_split_fft[2]))[0]
        axis_y = map(list, zip(*lc_flux_density_all_split_fft[2]))[1]
        axes[2, 0].plot(axis_x, axis_y)
        axes[2, 0].set_yticks([-60, -80, -100, -120, -140])
        axes[2, 0].set_xticks([0.00, 0.01, 0.02, 0.03, 0.04])
        axes[2, 0].set_xlim([0, 0.04])

        axes[2, 1].patch.set_facecolor('white')
        axes[2, 1].set_xlabel(r'$\rm Frequence $ [$Hz$]', fontsize=16)
        axes[2, 1].set_ylabel(r'$\rm 3rd\ Obs$ [$Db$]', fontsize=16)
        axis_x = map(list, zip(*lc_flux_density_all_split_fft_filtered[2]))[0]
        axis_y = map(list, zip(*lc_flux_density_all_split_fft_filtered[2]))[1]
        axes[2, 1].plot(axis_x, axis_y)
        axes[2, 1].set_yticks([-60, -80, -100, -120, -140])
        axes[2, 1].set_xticks([0.00, 0.01, 0.02, 0.03, 0.04])
        axes[2, 1].set_xlim([0, 0.04])

        plt.show()
        plt.close('all')
        return

    def plot_group(self, plot_group_kw):
        import matplotlib.pyplot as plt
        
        def plot_single(ax, plot_single_data, dtt):
            label_ts = r'XRT TimeSlice: ' + str(dtt)
            plot_temp = map(list, zip(*plot_single_data))

            plot_temp[2] = map(abs, plot_temp[2])
            plot_temp[5] = map(abs, plot_temp[5])
            
            ax.errorbar(plot_temp[0], plot_temp[3],
                        xerr=[plot_temp[2], plot_temp[1]], 
                        yerr=[plot_temp[5], plot_temp[4]],
                        label=label_ts, alpha=0.8, linestyle='-', marker='')
            return

        plt.style.use('bmh')
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_xscale('log')
#        ax.set_yscale('log')

        plot_group = self.data_base_load(plot_group_kw)
        for i in range(len(plot_group)):
            plot_single_data = plot_group[i]
            plot_single(ax, plot_single_data, i)
            
        ax.legend(loc='upper right')
        plt.show()
        plt.close('all')
        return

    def preset_pipeline_a(self):
        input_file_name_group = [
            ['xrt_flux_wtslew_DENSITY_nosys.qdp', 'wtslew'],
            ['xrt_flux_wt_DENSITY_nosys.qdp', 'wt'],
            ['xrt_flux_pc_DENSITY_nosys.qdp', 'pc']
            ]
        self.load_xrt_file(input_file_name_group, 'lcFluxDensityAll')
        self.load_xrt_file([['xrt_flux_wtslew_DENSITY_nosys.qdp', 'wtslew']], 'Swift XRT wtslew')
        self.load_xrt_file([['xrt_flux_wt_DENSITY_nosys.qdp', 'wt']], 'Swift XRT wt')
        self.load_xrt_file([['xrt_flux_pc_DENSITY_nosys.qdp', 'pc']], 'Swift XRT pc')

        if self.data_base_load('lcFluxDensityAll') is not []:
            self.dead_time_identify('lcFluxDensityAll', 'FDADeadTime', 10, 10)
            self.split_by_dead_time(['lcFluxDensityAll', 'FDADeadTime'], 'lcFluxDensityAllSplited')
            self.xrt_filter('lcFluxDensityAllSplited', ['xrt_filtered', 'lcFDASFFT', 'lcFDASFilteredFFT'])
            
            self.split_by_dead_time(['xrt_filtered', 'FDADeadTime'], 'XRTFSplited')
            # self.cal_lc_slope_in_group('XRTFSplited', 'XRTFSplitedslope')
            # self.cal_lc_slope_in_group('XRTFSplitedslope', 'XRTFSplitedslopeslope')
            #
            # self.cal_log_in_group('XRTFSplited', 'XRTFSplitedLoged')
            # self.cal_lc_slope_in_group('XRTFSplitedLoged', 'XRTFSplitedLogedslope')
            # self.cal_lc_slope_in_group('XRTFSplitedLogedslope', 'XRTFSplitedLogedslopeslope')
      
            self.plot_lc_type_a()
#            self.plot_fft_type_a()
            
            self.plot_group('XRTFSplited')
            # self.plot_group('XRTFSplitedslope')
            # self.plot_group('XRTFSplitedslopeslope')
            #
            # self.plot_group('XRTFSplitedLoged')
            # self.plot_group('XRTFSplitedLogedslope')
            # self.plot_group('XRTFSplitedLogedslopeslope')

        else:
            print 'This GRB No Obs XRT Data!'
        return

#    def CallcInGroup(self,input_group_kw,save_group_kw):
#        def __CallcInlc__(input_lc):
#            input_lc = map(list, zip(*input_lc))
#            slope_curve = []
#
#            return slope_curve
#
#        lc_split = self.data_base_load(input_group_kw)
#        lc_group_return = []
#
#        for i in range(len(lc_split)):
#            slope_curve = __CallcInlc__(lc_split[i])
#            lc_group_return.append(slope_curve)
#
#        self.data_base_save(save_group_kw, lc_group_return)
#        return

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 16:50:39 2019

@author: ZhongWei Sun
"""
import numpy as np
import pandas as pd
import os, os.path

#global parameter: design_parameter - design parameters
#columns = length, width, height, l_layers, w_layers, h_layers, vol_frac, lat_type, pre_modu, pre_yield
#index = The name of test pieces. 
#sheet_name is the batch of experiment
design_paras = pd.read_excel(os.getcwd() + r'\design\design_las.xlsx', sheet_name='Experiment')
#The length of test piece: design_paras.loc['the name of test piece'].loc['The attribute of test piece']
#las_desi_l = design_paras.loc['las_1_11'].loc['length']

#global parameter: quality_paras
#columns: length, width, height, diameter, aperture, description
#index: the name of test pieces
quality_paras = pd.read_excel(os.getcwd() + r'\quality\las_quality.xlsx', sheet_name='Experiment')
#las_qua_l = quality_paras.loc['las_1_11'].loc['length']
#test_date = '19.08.27'
#test_date = '19.09.26'
test_date = '19.11.14'
test_path = os.getcwd() + r'\test\%s'%test_date

#the path of data file

class las_txt:
    ''' las is test pieces class
        parameters: the name of test result file
            las_1_11: the number of experiment is 1, the number of design piece is 1 and the number of test piece is 1'''
    
    def __init__(self, test_name):
        '''test_name: las_the number of experiment_the number of design piece and the number of test piece_test date_the number of test'''
        self.test_name = test_name.split('.')[0]
        print(self.test_name)
        
        name_list = self.test_name.split('_')
        self.class_name = name_list[0]               # The class name of speciment: las-lattice speciments
        self.num_exp = name_list[1]                  # The number of experiment
        self.num_spec = name_list[2][0]              # The number of speciment
        self.num_test_piece = name_list[2][1]        # The number of test pieces that belong to specific design speciment
        self.num_test = name_list[3]                 # The number of test of given test pieces
        self.date = name_list[4]                     # The date of test
        self.description = name_list[5]              # The description of specific test 
        self.des_qua_name = self.test_name
        self._des_name = name_list[0] + '_' + name_list[1] + '_' + name_list[2][0]     # _des_name is used to get design parameters
        self._qua_name = name_list[0] + '_' + name_list[1] + '_' + name_list[2]        # _qua_name is used to get quality parameters
        
        self._raw_data = self.read_data()            # The test data
        self._load = self._raw_data[:, 0]            # load data of test
        self._dis = self._raw_data[:, 1]             # displacement of test
        self._n = len(self._load)                    # the length of test data
        self.ult_load = self.Ult_load()              # The ultimate load of test load
        
        #design parameters
        global design_paras
        self.des_length = design_paras.loc[self._des_name].loc['length']          # The Length of design speciment
        self.des_width = design_paras.loc[self._des_name].loc['width']            # The width of design speciment
        self.des_height = design_paras.loc[self._des_name].loc['height'] - 2      # The height of design speciment
        self.des_Llength = design_paras.loc[self._des_name].loc['l_layers']       # The number of layers in the length direction of the design specimen
        self.des_Lwidth = design_paras.loc[self._des_name].loc['w_layers']        # The number of layers in the width direction of the design specimen
        self.des_Lheight = design_paras.loc[self._des_name].loc['h_layers']       # The number of layers in the height direction of the design specimen
        self.des_dia = design_paras.loc[self._des_name].loc['diameter']           # The diameter of design specimen
        self.des_ape = design_paras.loc[self._des_name].loc['aperture']           # The aperture of design specimen
        self.des_vol_fra = design_paras.loc[self._des_name].loc['vol_frac']           # The volume fraction of design specimen
        self.des_porosity = (1 - self.des_vol_fra) * 100                              # The porosity of design specimen
        self.lat_type = design_paras.loc[self._des_name].loc['lat_type']          # The lattice type of design specimen
        self.pre_modu = design_paras.loc[self._des_name].loc['pre_modu']          # The predictive modulsu of design specimen
        self.pre_yield = design_paras.loc[self._des_name].loc['pre_yield']        # The predictive yield strenght of design specimen
        self.sim_modu = design_paras.loc[self._des_name].loc['sim_modu']          # The simulation modulus of design specimen
        self.sim_yield = design_paras.loc[self._des_name].loc['sim_yield']        # The simulation yield strenght of design specimen
        # The design parameter of unit cell
        self.des_cell_L = self.des_length / self.des_Llength                      # The length of unit cell (design parameter)
        self.des_cell_H = self.des_height / self.des_Lheight                      # The height of unit cell (design parameter)  
        self.des_cell_W = self.des_width / self.des_Lwidth                        # The width of unit cell (design parameter)
        self.des_AR = [self.des_cell_L/self.des_cell_H, self.des_cell_W/self.des_cell_H] # The aspect ratio of unit cell (design parameter)
        # The predictive modulus and yield strength (design parameter)
#        self.des_pre_modu, self.des_pre_yield = las.cal_modulus_yield(self.des_vol_fra, self.des_AR)
        
        #quality parameters
        global quality_paras
        self.qua_length = quality_paras.loc[self._qua_name].loc['length']        # The length of test piece
        self.qua_width = quality_paras.loc[self._qua_name].loc['width']          # The width of test piece
        self.qua_area = self.qua_length * self.qua_width                           
        self.qua_thickness_plate = quality_paras.loc[self._qua_name].loc['Plate_thickness']   # The thickness of plate
        self.qua_vol_frac = quality_paras.loc[self._qua_name].loc['volume_fraction']          # The volume fraction of printed peice
        self.qua_height = quality_paras.loc[self._qua_name].loc['height'] - 2*self.qua_thickness_plate    # The height of lattice
        self.qua_weight = quality_paras.loc[self._qua_name].loc['weight']        # The weight of test piece
        self.qua_dia = quality_paras.loc[self._qua_name].loc['diameter']         # The diameter of test piece
        self.qua_ape = quality_paras.loc[self._qua_name].loc['aperture']         # The aperture of test piece
        self.qua_des = quality_paras.loc[self._qua_name].loc['description']      # The description of test piece
        #The quality parameter of unit cell
        self.qua_cell_L = self.qua_length / self.des_Llength                     # The length of unit cell (quality parameter)
        self.qua_cell_W = self.qua_width / self.des_Lwidth                       # The width of unit cell (quality parameter)
        self.qua_cell_H = self.qua_height / self.des_Lheight                     # The height of unit cell (quality parameter)
        self.qua_AR = [self.qua_cell_L/self.qua_cell_H, self.qua_cell_W/self.qua_cell_H] # The aspect ratio of unit cell (quality parameter)
        # The predictive modulus and yield strength (quality parameter)
        self.qua_pre_modu, self.qua_pre_yield = las_txt.cal_modulus_yield(self.qua_vol_frac, self.qua_AR)

    # Calculate the yield load
    @staticmethod
    def cal_yield(load, dis, i, height, stiffness):
        ''' calculate the yield laod
        parameters:
            load: the load array
            dia: the diaplacement array
            i: the start point of load to calculate yield load
            height: the height of test piece
            stiffness: the stiffness of test piece
            intercept: the intercept of line'''
        
        for i2 in range(i, len(load)):
            pla_strain = load[i2] - (dis[i2] - 0.002 * height) * stiffness
            if pla_strain <= 0.002:
                yield_load = load[i2]
                return yield_load
        else:
            yield_load = 0
            return yield_load
    
    @property
    def test_modu_0307(self):
        '''calculate stiffness and mudulus using 0307 method'''
        
        max_load = self.ult_load * 0.7
        min_load = self.ult_load * 0.3
        
        for i in range(self._n):
            if self._load[i] > min_load:
                self.i_min_0307 = i
                break
        for j in range(i+1, self._n):
            if self._load[j] > max_load:
                self.i_max_0307 = j
                break
        
        from scipy.stats import linregress
        self.stiff_0307, self.inter_0307, self.r_value_0307, _, _ = linregress(self._dis[self.i_min_0307:self.i_max_0307+1], \
            self._load[self.i_min_0307:self.i_max_0307+1])
        if self.r_value_0307 < 0.9:
            print(self.test_name, '0307 Mthod: Correlation coefficient < 0.9')
        
        self.data_plot = np.row_stack(([[0,0]],np.column_stack((self._dis[self.i_min_0307:] + \
            self.inter_0307/self.stiff_0307, self._load[self.i_min_0307:]))))
        
        self.test_yL_0307 = las_txt.cal_yield(self.data_plot[:, 1], self.data_plot[:, 0], self.i_min_0307, self.qua_height, self.stiff_0307)
        self.test_yS_0307 = self.test_yL_0307 / self.qua_area
        self.test_yR_0307 = self.test_yL_0307 / self.ult_load
        
        return self.stiff_0307/self.qua_area * self.qua_height
    
    @property
    def test_modu_maxS(self):
        '''calculate the modulus using maximum slope method'''
        #Smax-maxmium slope; Imax-maxmium intercept; Rmax-maxmium correlation cofficient
        Smax, Imax, Rmax = (0, 0, 0)
        from scipy.stats import linregress
        for i in range(self._n - 101):
            slope, intercept, r_value, _, _ = linregress(abs(self._dis)[i:i+100], abs(self._load)[i:i+100])
            if slope > Smax:
                Smax = slope
                Imax = intercept
                Rmax = r_value
            else:
                break
        self.i_max_MS = i
        
        if Rmax < 0.9:
            print(self.des_qua_name, 'Maxmium slope method: Correlation coefficient < 0.9')
            print(self.des_qua_name, 'Maxmium slope method, intercept = ', Imax)
        
        self.data_plot = np.row_stack(([[0,0]],np.column_stack((self._dis[self.i_max_MS:] + \
            self.inter_0307/self.stiff_0307, self._load[self.i_max_MS:]))))

        self.stiff_MS = Smax
        self.r_value_MS = Rmax
        
        self.test_yL_maxS = las_txt.cal_yield(self._load, self._dis, self.i_max_MS, self.qua_height, self.stiff_MS)
        self.test_yS_maxS = self.test_yL_maxS / self.qua_area
        self.test_yR_max = self.test_yL_maxS / self.ult_load
        
        return self.stiff_MS / self.qua_area * self.qua_height
     
    @property
    def test_modu_SA(self):
        '''Calculate the modulus using stepwise approach;
        test_modu_SA: test_modu_stepAppro'''
        
        from scipy.stats import linregress
        slope, intercept, _, _, _ = linregress(abs(self._dis)[200:250], abs(self._load)[200:250])

        dis_load = np.row_stack(([[0,0]], np.column_stack((abs(self._dis)[200:] + intercept/slope, abs(self._load)[200:]))))
        load = dis_load[:, 1]
        dis = dis_load[:, 0]
        
        # 1. The difference must 
        yield_load = self.ult_load * 0.7
        previous_diff = np.inf
#        current_diff = 0
        diff_2points = (load[81] - load[1])/40
        # diff_min: the minmium difference of given yield load ang calculated yield load
        diff_min = 1
        #diff: The difference of given yield load and calculated yield load
        diff = diff_2points + 10
        while diff > diff_2points and diff > diff_min and diff < previous_diff:
            load_01 = yield_load * 0.1
            load_05 = yield_load * 0.5
            
            id_01 = np.where(np.abs(load - load_01) == np.min(np.abs(load - load_01)))[0][0]
            load_01 = load[id_01]
            dis_01 = dis[id_01]
            
            id_05 = np.where(np.abs(load - load_05) == np.min(np.abs(load - load_05)))[0][0]
            load_05 = load[id_05]
            dis_05 = dis[id_05]
            
            stiff = (load_05 - load_01) / (dis_05 - dis_01)
            diff_all = np.abs(load - (dis - 0.002*self.qua_height) * stiff)
            cross_point_load = load[np.where(diff_all == np.min(diff_all))[0][0]]
            diff = abs(yield_load - cross_point_load)
            yield_load = cross_point_load
        
        self.data_plot = np.row_stack(([[0,0]],np.column_stack((self._dis[id_01:] + intercept/stiff, self._load[id_01:]))))

        self.test_yL_SA = yield_load
        self.test_yS_SA = self.test_yL_SA/self.qua_area
        self.test_yR_SR = self.test_yL_SA/self.ult_load
        self.stiff_SA = stiff
        
        return self.stiff_SA / self.qua_area * self.qua_height         
        
    def read_data(self):
        '''return the raw data of test'''
        #Load, deformation
        return np.loadtxt(test_path + r'\%s.txt'%self.test_name, skiprows=20, dtype=float, usecols=(1,2))

    def Ult_load(self):
        '''find the maximum load and return it'''
        
        maxL = -np.inf
        for i in range(self._n - 16):
            max_load = []
            # The ultimate load is the first extreme load. if load of point i is larger than the next 15 point of i, the load of point i is ultimate load!
            for j in range(15):
                max_load.append(self._load[i+j])
            if self._load[i] == max(max_load):
                if self._load[i] > maxL:
                    maxL = self._load[i] 
        else:
            maxL = max(self._load)
        
        return maxL
            
    @property
    def plot_dis_load(self):
        '''plot the displacment load curve'''
        
        import matplotlib.pyplot as plt
        
        plt.figure()
        plt.plot(self._dis, self._load, 'k', label=self._qua_name)
        plt.xlabel('Deformation_mm')
        plt.ylabel('Load_N')
        plt.title('Displcement-Load curve')
        plt.legend()
        out_path = os.getcwd() + r'\output\Dis_Load.png'
        plt.savefig(out_path)
    
    @property
    def plot_stre_stra(self):
        '''plot the stress-strain curve'''
        
        import matplotlib.pyplot as plt
        
        plt.figure()
        plt.plot(self._dis/self.qua_height, self._load/self.qua_area, label=self._qua_name)
        plt.xlabel('Strain')
        plt.ylabel('Stress')
        plt.title('Stress-Strain curve')
        plt.legend()
        out_path = os.getcwd() + r'\output\stress_strain.png'
        plt.savefig(out_path)

    @property
    def plot_dis_load_M(self):
        ''' plot the displacement-load curve was output by compression test machine '''
        
        dis_load_M = np.loadtxt(os.getcwd() + r'\test' + r'\%s.txt'%self.test_name, skiprows=17, dtype=float, usecols=(1,3))
        
        import matplotlib.pyplot as plt

        plt.figure()
        plt.plot(dis_load_M[:, 1], dis_load_M[:, 0], 'k', label=self._qua_name)
        plt.xlabel('Displacement_mm')
        plt.ylabel('Load_N')
        plt.title('Displcement-Load curve (Mechine)')
        plt.legend()
        out_path = os.getcwd() + r'\output\Dis_Load.png'
        plt.savefig(out_path)

    @staticmethod
    def cal_modulus_yield(vol_frac, aspect_ratio):
        '''Return the predictive modulus caculating by volume fraction and respectio'''
        
        csv_path = os.getcwd() + r'\ForSpecimens.csv'
        vol_AR_mod = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=(0,1,2,5,7))
        X_data = np.dstack((vol_AR_mod[:,0], vol_AR_mod[:,1], vol_AR_mod[:,2]))[0]
        Y_mod = vol_AR_mod[:,3]
        Y_yield = vol_AR_mod[:,4]
        
        from scipy.interpolate import griddata
        
        pre_mod = griddata(X_data, Y_mod, [vol_frac, aspect_ratio[0], aspect_ratio[1]], method='linear')[0]
        if pd.isnull(pre_mod) :
            pre_mod = griddata(X_data, Y_mod, [vol_frac, aspect_ratio[1], aspect_ratio[0]], method='linear')[0]
        
        pre_yield = griddata(X_data, Y_yield, [vol_frac, aspect_ratio[0], aspect_ratio[1]], method='linear')[0]
        if pd.isnull(pre_yield):
            pre_yield = griddata(X_data, Y_yield, [vol_frac, aspect_ratio[1], aspect_ratio[0]], method='linear')[0]
        # The Corrective factor is 1.06
        return pre_mod * 1.06, pre_yield * 1.06
        
    def __str__(self):
        '''return the test modulus, yield strength, yield ratio'''
        
        return '0307 Method: \n Test modulus (MPa):{}; \n Test yield strength (MPa):{}; \n Test yield ratio:{}'.format(self.test_modu_0307,  self.test_yS_0307, self.test_yR_0307) 
            

class las_piece:
    ''' Intergration the test pieces of specific design piece'''
    
    def __init__(self, piece_name):
        global test_date
        self.piece_name = piece_name
        test_path = os.getcwd() + r'\test\%s'%test_date
        for file in os.listdir(test_path):
            if piece_name not in file: continue
            if piece_name + '_1' in file:
                self.first = las_txt(file)
            elif piece_name + '_2' in file:
                self.second = las_txt(file)
                self.Modu_0307_second = self.second.test_modu_0307
#                self.Modu_maxS_second = self.second.test_modu_maxS
            else:
                self.third = las_txt(file)
          
        self.Modu_0307 = self.third.test_modu_0307
        
        self.Pre_Yield = self.second.pre_yield

    @property
    def Yield_0307(self):
        ''' calculate yield strength of test piece using second test data and third modulus'''
        
#        self.yield_0307 = las.cal_yield(self.second._load, self.second._dis, 200, 
#                                        self.second.qua_height, self.second.stiff_0307, self.second.inter_0307)
        self.yield_0307 = las_txt.cal_yield(self.second.data_plot[:, 1], self.second.data_plot[:, 0], self.second.i_min_0307, 
                                        self.second.qua_height, self.third.stiff_0307)
        
        return self.yield_0307/self.second.qua_area
        
    @property
    def Yield_maxS(self):
        
        self.Modu_maxS = self.third.test_modu_maxS
        self.yieldL_MS = las_txt.cal_yield(self.second.data_plot[:, 1], self.second.data_plot[:, 0], \
            self.second, self.second.qua_height, self.third.stiff_MS)

        return self.yieldL_MS/self.second.qua_area
    
    def Plt_Dis_Load(self):
        
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(self.first._dis, self.first._load, label = self.first._qua_name+self.first.num_test)
        plt.plot(self.second._dis, self.second._load, label = self.second._qua_name+self.second.num_test)
        plt.plot(self.third._dis, self.third._load, label = self.third._qua_name+self.third.num_test)
        plt.legend()
        plt.xlabel('Displacement (mm)')
        plt.ylabel('Load (N)')
        plt.title('Displacement-Load Curve (%s)'%self.piece_name)
        png_path = os.getcwd() + r'\output\Dis&Load_%s.png'%self.piece_name
        plt.savefig(png_path)
    









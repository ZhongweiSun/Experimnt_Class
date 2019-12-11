# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:11:25 2019

@author: ZhongWei Sun
"""
import os, os.path
import pandas as pd
import numpy as np
import math

design_path = os.getcwd() + r'\design\design_tra.xlsx'
design_para = pd.read_excel(design_path, index_col='name')

quality_path = os.getcwd() + r'\quality\quality_tra.xlsx'
quality_para = pd.read_excel(quality_path, index_col='name')

test_date = '19.05.07'
file_path = os.getcwd() + r'\test\%s'%test_date

class tra_txt:
    '''The special test data file of test piece'''
    def __init__(self, file_name):
        self.file_name = file_name.split('.')[0]
        name_list = self.file_name.split('_')
        print(self.file_name)
        
        # Basic information
        global file_path, design_para, quality_para
        self.test_piece = name_list[0] + '_' + name_list[1] + '_' + name_list[2]
        self.des_piece = self.test_piece[:-1]
        self.num_test = name_list[3]
        self.test_piece_num = self.test_piece + '_' + self.num_test            # tra_1_A1_1
        self.date = name_list[4]
        if len(name_list) > 5: self.description = name_list[5]
        
        self.raw_data = self.read_data(file_name)
        self.load = self.raw_data[:, 0]
        self.dis = self.raw_data[:, 1]
        self.n = len(self.load)
        
        #design parameter
        self.shape_des = design_para.loc[self.des_piece, 'shape']
        self.des_plateTh = design_para.loc[self.des_piece, 'plate_thickness']
        if 'cylinder' in self.shape_des:
            self.des_dia = design_para.loc[self.des_piece, 'length']
            self.des_area = math.pi * self.des_dia**2 / 4
        else:
            self.des_length = design_para.loc[self.des_piece, 'length']
            self.des_width = design_para.loc[self.des_piece, 'width']
            self.des_area = self.des_length * self.des_width
        self.des_height = design_para.loc[self.des_piece, 'height'] - 2*self.des_plateTh
        self.des_VolFra = design_para.loc[self.des_piece, 'VolFra']
        self.des_porosity = (1 - self.des_VolFra) * 100
        
        #quality parameters
        self.shape_qua = quality_para.loc[self.test_piece, 'shape']
        self.qua_plateTh = quality_para.loc[self.test_piece, 'plate_thickness']
        if 'cylinder' in self.shape_qua:
            self.qua_dia = quality_para.loc[self.test_piece, 'length']
            self.qua_area = math.pi * self.qua_dia**2 / 4
        else:
            self.qua_length = quality_para.loc[self.test_piece, 'length']
            self.qua_width = quality_para.loc[self.test_piece, 'width']
            self.qua_area = self.qua_length * self.qua_width
        self.qua_height = quality_para.loc[self.test_piece, 'height'] - 2*self.qua_plateTh
        self.qua_VolFra = quality_para.loc[self.test_piece, 'VolFra']
        self.qua_porosity = (1 - self.qua_VolFra) * 100
        
        #test parameter
        self.ult_load = self.Ult_load()
        
    def Ult_load(self):
        '''find the maximum load and return it'''
        maxL = -np.inf
        for i in range(self.n - 16):
            max_load = []
            # The ultimate load is the first extreme load. if load of point i is larger than the next 15 point of i, the load of point i is ultimate load!
            for j in range(15):
                max_load.append(self.load[i+j])
            if self.load[i] == max(max_load):
                if self.load[i] > maxL:
                    maxL = self.load[i] 
        else:
            maxL = max(self.load)
        return maxL            
        
    def read_data(self, file_name):
        '''return the raw data of test'''
        return np.loadtxt(os.path.join(file_path, file_name), skiprows=20, dtype=float, usecols=(1,2))      
        

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
        
        for i in range(self.n):
            if self.load[i] > min_load:
                self.i_min_0307 = i
                break
        for j in range(i+1, self.n):
            if self.load[j] > max_load:
                self.i_max_0307 = j
                break
        
        from scipy.stats import linregress
        self.stiff_0307, self.inter_0307, r_value, _, _ = linregress(self.dis[self.i_min_0307:self.i_max_0307+1], \
            self.load[self.i_min_0307:self.i_max_0307+1])
        
        if r_value < 0.9:
            print(self.test_piece_num, '0307 Mthod: Correlation coefficient < 0.9')
        self.data_plot = np.row_stack(([[0,0]],np.column_stack((self.dis[self.i_min_0307:] + self.inter_0307/self.stiff_0307, \
            self.load[self.i_min_0307:]))))

        self.test_yL_0307 = tra_txt.cal_yield(self.data_plot[:, 1], self.data_plot[:, 0], self.i_min_0307, self.qua_height, self.stiff_0307)
        self.test_yS_0307 = self.test_yL_0307 / self.qua_area
        self.test_yR_0307 = self.test_yL_0307 / self.ult_load
        
        return self.stiff_0307 / self.qua_area * self.qua_height

    @property
    def test_modu_maxS(self):
        '''calculate the modulus using maximum slope method'''
        
        #Smax-maxmium slope; Imax-maxmium intercept; Rmax-maxmium correlation cofficient
        Smax, Imax, Rmax = (0, 0, 0)
        from scipy.stats import linregress
        for i in range(self.n - 101):
            slope, intercept, r_value, _, _ = linregress(abs(self.dis)[i:i+100], abs(self.load)[i:i+100])
            if slope > Smax:
                Smax = slope
                Imax = intercept
                Rmax = r_value
            else:
                break
        
        self.i_max_MS = i
        self.inter_MS = Imax
        self.stiff_maxS = Smax
        
        if Rmax < 0.9:
            print(self.test_piece_num, 'Maxmium slope method: Correlation coefficient < 0.9')
            print(self.test_piece_num, 'Maxmium slope method, intercept = ', Imax)

        self.data_plot = np.row_stack(([[0,0]], np.column_stack((self.dis[self.i_max_MS:] \
            + Imax/Smax, self.load[self.i_max_MS:]))))
        
        self.test_yL_maxS = tra_txt.cal_yield(self.data_plot[:, 1], self.data_plot[:, 0], self.i_max_MS, self.qua_height, self.stiff_maxS)
        self.test_yS_maxS = self.test_yL_maxS / self.qua_area
        self.test_yR_maxS = self.test_yL_maxS / self.ult_load
        
        return self.stiff_maxS / self.qua_area * self.qua_height

    @property
    def test_modu_SA(self):
        '''Calculate the modulus using stepwise approach; test_modu_SA: test_modu_stepAppro'''
        
        from scipy.stats import linregress

        if self.num_test == '2':
            yield_load = self.ult_load * 0.9
            int_start = 100
        else:
            yield_load = self.ult_load * 0.7
            int_start = 200

        slope, intercept, _, _, _ = linregress(abs(self.dis)[int_start:250], abs(self.load)[int_start:250])
        dis_load = np.row_stack(([[0,0]], np.column_stack((abs(self.dis)[int_start:] + intercept/slope, abs(self.load)[int_start:]))))
        load = dis_load[:, 1]
        dis = dis_load[:, 0]
        
        # 1. The difference must 

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
#            print(diff_all)
            cross_point_load = load[np.where(diff_all == np.min(diff_all))[0][0]]
            diff = abs(yield_load - cross_point_load)
            yield_load = cross_point_load

        self.data_plot = np.row_stack(([[0,0]],np.column_stack((self.dis[load_01:] + intercept/stiff, self.load[load_01:]))))

        self.test_yL_SA = yield_load
        self.test_yS_SA = self.test_yL_SA/self.qua_area
        self.test_yR_SR = self.test_yL_SA/self.ult_load
        self.stiff_SA = stiff
        
        return self.stiff_SA / self.qua_area * self.qua_height   
    
    @property
    def plot_dis_load(self):
        '''plot the displacment load curve'''
        
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(self.dis, self.load, 'k', label=self.test_piece_num)
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
        plt.plot(self.dis/self.qua_height, self.load/self.qua_area, label=self.test_piece_num)
        plt.xlabel('Strain')
        plt.ylabel('Stress')
        plt.title('Stress-Strain curve')
        plt.legend()
        out_path = os.getcwd() + r'\output\stress_strain.png'
        plt.savefig(out_path)

class tra_piece:
    ''' Intergration the test pieces of specific design piece'''
    
    def __init__(self, piece_name):
        
        global file_path
        self.piece_name = piece_name
        for file in os.listdir(file_path):
            if piece_name not in file: continue
            if piece_name + '_1' in file:
                self.first = tra_txt(file)
            elif piece_name + '_2' in file:
                self.second = tra_txt(file)
                self.Modu_0307_second = self.second.test_modu_0307
#                self.Modu_maxS_second = self.second.test_modu_maxS
            else:
                self.third = tra_txt(file)
          
        self.Modu_0307 = self.third.test_modu_0307
        
    @property
    def Yield_0307(self):
        ''' calculate yield strength of test piece using second test data and third modulus'''
        
        self.yieldL_0307 = tra_txt.cal_yield(self.second.data_plot[:, 1], self.second.data_plot[:, 0], \
            self.second.i_max_0307, self.second.qua_height, self.third.stiff_0307)
        
        return self.yieldL_0307/self.second.qua_area
        
    @property
    def Yield_MS(self):
        
        self.Modu_MS = self.third.test_modu_maxS
        self.yieldL_MS = tra_txt.cal_yield(self.second.data_plot[:, 1], self.second.data_plot[:, 0], \
            self.second.i_max_MS, self.second.qua_height, self.third.stiff_maxS)
        return self.yieldL_MS/self.second.qua_area
    
    def Plt_Dis_Load(self):
        
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(self.first.dis, self.first.load, label = self.first.test_piece_num)
        plt.plot(self.second.dis, self.second.load, label = self.second.test_piece_num)
        plt.plot(self.third.dis, self.third.load, label = self.third.test_piece_num)
        plt.legend()
        plt.xlabel('Displacement (mm)')
        plt.ylabel('Load (N)')
        plt.title('Displacement-Load Curve (%s)'%self.piece_name)
        png_path = os.getcwd() + r'\output\Dis&Load_%s.png'%self.piece_name
        plt.savefig(png_path)

        

# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 09:11:16 2019

@author: ADMINISTRATOR
"""
import numpy as np
import pandas as pd
import const
import os, os.path, sys
from scipy.stats import linregress

# #定义全局常量类
# class _const:
#     class ConstError(TypeError): pass
#     def __setattr__(self, name, value):
#         if name in self.__dict__:
#             raise self.ConstError( "Can't rebind const (%s)" %name)
#         self.__dict__[name] = value
# #把常量类_const注册到sys.modules(全局字典)中。
# sys.modules[__name__] = _const()

LY12_dict = {}
test_path = os.getcwd() + r'\test\%s'%(const.DATE)
design_BZ_path = os.getcwd() + r'\design\design_BZ.xlsx'
infos = pd.read_excel(design_BZ_path, sheet_name='AL')

# global parameter: LY12_info - The dict data of LY12 speices information, 
# The key is the name of LY12, values are the parameters of LY12
for i in range(len(infos)):
    LY12_dict[infos.iloc[i][0]] = dict(infos.iloc[i].iloc[1:])
# add strain and stress to LY12
LY12_dict['strain_stress'] = pd.read_excel(design_BZ_path, sheet_name='strain_stress')

class LY12_txt:

    global LY12_dict
    def __init__(self, file_name):
        ''' Get attributes of test pieces data '''

        name_info = file_name.split('.')[0].split('_')           # file_name: LY12_6_A1_20190507_11.txt
        self.piece_name = '_'.join(name_info[:3])                # piece name + test number, LY12_6_A1
        self.num_exp = name_info[1]                              # Number of experiment, 6
        # self.num_test_piece = name_info[2][0]                    # The number of test pieces, A
        self.num_test = name_info[2][1]                          # The number of experiment, 1
        # self.test_date = name_info[3]                          # The date of experiment
        if len(name_info) > 4 : self.desc = name_info[4]         # The description

        # The size of test piece (Theoretical value)
        self.diameter =  LY12_dict['LY12_AL']['diameter']         # The diameter of test piece
        self.area = np.pi * (self.diameter)**2 / 4                # The area of test piece
        self.height = LY12_dict['LY12_AL']['height']              # The height of test piece
        self.density = LY12_dict['LY12_AL']['density']            # The density of LY12_AL
        self.LY12_modu_GB = LY12_dict['LY12_AL']['LY12_modu_GB']  # The modulus of LY12 (GB)
        self.LY12_ultS_min_GB = LY12_dict['LY12_AL']['LY12_ultimateS_min_GB']         # The minimum of ultimate strength of LY12
        self.LY12_yieldS_min_GB = LY12_dict['LY12_AL']['LY12_yieldS_min_GB']          # The minumum of yield strength of LY12 (GB)
        self.LY12_elo_min_GB = LY12_dict['LY12_AL']['LY12_elo_min_GB']                # The minimum of elngation of LY12 (GB)
        self.LY12_yieldS = LY12_dict['LY12_AL']['LY12_yieldS']                        # The yield strength of LY12
        self.LY12_ultS = LY12_dict['LY12_AL']['LY12_ultimateS']                       # The ultimate strength of LY12
        self.LY12_modu = LY12_dict['LY12_AL']['LY12_modu']                            # The modulus of LY12
        self.stra_stre = LY12_dict['strain_stress']                                   #['LY12_AL'] The strain-stress data of LY12 (GB)

        #The test parameters
        self.raw_data = self.read_data()
        self.load = self.raw_data[:, 0]
        self.dis = self.raw_data[:, 1]                                              # The displacement of Extensometer(引伸计)
        self.Dis = self.raw_data[:, 2]                                              # The displacement of Testing Machine

        self.ult_load = self.Ult_load()
        self.ult_stre = self.ult_load / self.area
        self.n = len(self.load)
        # modulus: 0307
        self.stiff_0307 = self.Stiff_0307()
        self.modu_0307 = self.stiff_0307/self.area*self.height
        self.plot_0307 = np.row_stack(([[0,0]], np.column_stack((self.dis[self.i_min_0307:] + \
            self.inter_0307/self.stiff_0307, self.load[self.i_min_0307:]))))
        # yield load and yield strength
        self.yieldL_0307 = LY12_txt.cal_yield(self.plot_0307[:, 1], self.plot_0307[:, 0], \
            self.i_min_0307, self.height, self.stiff_0307)
        self.yieldS_0307 = self.yieldL_0307 / self.area
        self.yieldR_0307 = self.yieldL_0307 / self.ult_load             # The yield ratio of test piece
        # modulus: MS
        self.stiff_MS = self.Stiff_MS()
        self.modu_MS = self.stiff_MS/self.area * self.height
        self.plot_MS = np.row_stack(([[0,0]], np.column_stack((self.dis[self.i_max_maxS:] \
            + self.inter_MS/self.stiff_MS, self.load[self.i_max_maxS:]))))
        self.yieldL_MS = LY12_txt.cal_yield(self.data_plot[:, 1], self.data_plot[:, 0], \
            self.i_max_maxS, self.height, self.stiff_MS)
        self.yieldS_MS = self.yieldL_MS / self.area
        self.yieldR_MS = self.yieldL_MS / self.ult_load

    def Stiff_0307(self):
        '''calculate stiffness and mudulus using 0307 method'''
        
        if self.num_test == '3':
            max_coe = 0.7
            min_coe = 0.3
        else:
            max_coe = 0.55
            min_coe = 0.1

        max_load = self.ult_load * max_coe
        min_load = self.ult_load * min_coe

        for i in range(self.n):
            if self.load[i] > min_load:
                self.i_min_0307 = i
                break
        for j in range(i+1, self.n):
            if self.load[j] > max_load:
                self.i_max_0307 = j
                break

        self.stiff_0307, self.inter_0307, self.r_value_0307, _, _ = linregress(self.dis[self.i_min_0307:self.i_max_0307+1], \
            self.load[self.i_min_0307:self.i_max_0307+1])

        if self.r_value_0307 < 0.9:
            print(self.piece_name, '0307 Mthod: Correlation coefficient < 0.9')

        return self.stiff_0307

    def Stiff_MS(self):
        '''calculate the modulus using maximum slope method'''

        #Smax-maxmium slope; Imax-maxmium intercept; Rmax-maxmium correlation cofficient
        Smax, Imax, Rmax = (0, 0, 0)
        for i in range(0, self.n-51, 20) :
            slope, intercept, r_value, _, _ = linregress(abs(self.dis)[i:i+50], abs(self.load)[i:i+50])
#             slope, self.inter_MS, r_value, _, _ = linregress(self._dis[i:i+50], self._load[i:i+50])
        # for i in range(0, self.n-1001, 50):
        #     slope, intercept , r_value, _, _ = linregress(abs(self.dis)[i:i+1000], abs(self.load)[i:i+1000])
#        for i in range(0, self.n - 401, 50):
#            slope, intercept , r_value, _, _ = linregress(abs(self._dis)[i:i+400], abs(self._load)[i:i+400])
            if abs(slope) > Smax:
                Smax = abs(slope)
                Imax = intercept 
                Rmax = r_value
            else:
                break
        self.i_max_maxS = i
        
        if Rmax < 0.9:
            print(self.piece_name, 'Maxmium slope method: Correlation coefficient < 0.9')
            print(self.piece_name, 'Maxmium slope method, intercept = ', Imax)

        self.inter_MS = Imax
        self.r_value_maxSlope = r_value

        return Smax

    @property
    def test_modu_SA(self):
        '''Calculate the modulus using stepwise approach'''

        from scipy.stats import linregress

        slope, intercept, _, _, _ = linregress(abs(self.dis)[200:250], abs(self.load)[200:250])
        dis_load = np.row_stack(([[0,0]], np.column_stack((abs(self.dis)[200:] + intercept/slope, abs(self.load)[200:]))))
        load = dis_load[:, 1]
        dis = dis_load[:, 0]

        yield_load = self.ult_load * 0.7
        previous_diff = np.inf
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
            diff_all = np.abs(load - (dis - 0.002*self.height) * stiff)
            cross_point_load = load[np.where(diff_all == np.min(diff_all))[0][0]]
            diff = abs(yield_load - cross_point_load)
            yield_load = cross_point_load
        #data_plot数据计算有问题
        self.data_plot = np.row_stack(([[0,0]],np.column_stack((self.dis[load_01:] + intercept/stiff, self.load[load_01:]))))

        self.yieldL_SA = yield_load
        self.yieldS_SA = self.yieldL_SA/self.area
        self.yieldR_SA = self.yieldL_SA/self.ult_load
        self.stiff_SA = stiff

        return self.stiff_SA/self.area*self.height

    # The methods of class LY12
    @property
    def plot_dis_load(self):
        '''plot the displacment load curve'''

        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(self._dis, self._load, 'k', label=self.name[0:10])
        plt.xlabel('Deformation_mm')
        plt.ylabel('Load_N')
        plt.title('Displcement-Load curve')
        plt.legend()
        out_path = os.getcwd() + r'\output\Dis_Load.png'
        plt.savefig(out_path)
    
    @property
    def plot_Dis_load(self):
        ''' Plot the Displacement-Load curve'''
        import matplotlib.pyplot as plt
        
        plt.figure()
        plt.plot(self._Dis, self._load, 'k')
        plt.xlabel('Displacement_mm')
        plt.ylabel('Load_N')
        plt.title('Displcement-Load curve')
        out_path = os.getcwd() + r'\output\Dis_Load_%s.png'%self.name
        plt.savefig(out_path)
    
    @property
    def plot_stre_stra(self):
        '''plot the stress-strain curve'''

        import matplotlib.pyplot as plt

        plt.figure()
        plt.plot(self._dis/self.height, self._load/self.area, label='Raw Data')
        plt.plot(LY12_dict['strain_stress']['strain'], LY12_dict['strain_stress']['stress'], label='strain-stress curve (GB)')
        plt.plot(self.data_plot[:, 0]/self.height, self.data_plot[:, 1]/self.area, label='part of raw data')
        plt.legend()
        plt.xlabel('Strain')
        plt.ylabel('Stress (MPa)')
        plt.title('Stress-Strain curve')
        out_path = os.getcwd() + r'\output\stress_strain.png'
        plt.savefig(out_path)

    def read_data(self):
        '''return the raw data of test'''
        return np.loadtxt(test_path + r'\%s.txt'%self.name, skiprows=20, dtype=float, usecols=(1,2,3))

    def Ult_load(self):
        '''find the maximum load and return it'''

        maxL = -np.inf
        for i in range(len(self._load) - 16):
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

    # Calculate the yield load
    @staticmethod
    def cal_yield(load, dis, i, height, stiffness):
        ''' calculate the yield laod
        parameters:
            load: the load array (the first node is (0, 0))
            dis: the displacement array
            i: the start point of load to calculate yield load
            height: the height of test piece
            stiffness: the stiffness of test piece
            intercept: the intercept of line'''

        for i2 in range(i, len(load)):
            pla_strain = load[i2] - (dis[i2] - 0.002 * height) * stiffness
            if pla_strain <= 0 :
                yield_load = load[i2]
                return yield_load
        else:
            yield_load = 0
            return yield_load

    def __str__(self):
        '''return the test modulus, yield strength, yield ratio'''

        return '0307 Method: \n Test modulus (MPa):{}; \n Test yield strength (MPa):{}; \n Test yield ratio:{}'.format(self.test_modu_0307, \
            self.test_yieldS_0307, self.test_yieldR_0307)

class LY12_piece:
    '''Intergration the test pieces of specific LY12 piece'''

    def __init__(self, piece_name):

        print(piece_name)
        global test_path
        self.piece_name = piece_name
        if 'LY12' not in self.piece_name: assert AssertionError('must be LY12 piece!')
        self.first = None
        self.second = None
        self.third = None
        for file in os.listdir(test_path):
            if piece_name not in file : continue
            if piece_name + '1' in file:
                self.first = LY12_txt(file)
                # print(file)
            if piece_name +'2' in file:
                self.second = LY12_txt(file)
                self.modu_0307_second = self.second.test_modu_0307
                self.modu_MS_second = self.second.test_modu_MS
                # print(file)
            if piece_name + '3' in file:
                self.third = LY12_txt(file)
                # print(file)
        self.Modu_0307 = self.third.test_modu_0307
        self.Modu_MS = self.third.test_modu_MS

    @property
    def YieldS_0307(self):
        ''' calculate yield strength of test piece using second test data and third modulus'''
        if self.second:
            self.yieldL_0307 = LY12_txt.cal_yield(self.second.data_plot[:, 1], self.second.data_plot[:, 0], \
                self.second.i_max_0307, self.second.height, self.third.stiff_0307)   
            if self.yieldL_0307 == 0 or self.yieldL_0307 < 100 * self.second.area:
                self.yieldL_0307 = self.third.test_yieldL_0307
            return self.yieldL_0307/self.second.area
        else : 
            self.yieldL_0307 = self.third.test_yieldL_0307
            return self.yieldL_0307/self.third.area  

    @property
    def YieldS_MS(self):
        
        if self.second :
            self.yieldL_MS = LY12_txt.cal_yield(self.second.data_plot[:, 1], self.second.data_plot[:, 0], self.second.i_max_maxS, \
                self.second.height, self.third.stiff_MS)
            if self.yieldL_MS == 0 or self.yieldL_MS < 100 * self.second.area:
                if self.third : self.yieldL_MS = self.third.test_yieldL_MS
            return self.yieldL_MS/self.second.area
        else : 
            self.yieldL_MS = self.third.test_yieldL_MS
            return self.yieldL_MS/self.third.area
        

    def Plt_Dis_Load(self):
        
        import matplotlib.pyplot as plt
        plt.figure()
        if self.first: plt.plot(self.first._dis, self.first._load, label = self.first.piece_name)
        if self.second: plt.plot(self.second._dis, self.second._load, label = self.second.piece_name)
        plt.plot(self.third._dis, self.third._load, label = self.third.piece_name)
        plt.legend()
        plt.xlabel('Displacement (mm)')
        plt.ylabel('Load (N)')
        plt.title('Displacement-Load Curve (%s)'%self.piece_name)
        png_path = os.getcwd() + r'\LY12_output\Dis&Load_%s.png'%self.piece_name
        plt.show()
        # plt.savefig(png_path)


    def Plt_Dis(self):
        
        import matplotlib.pyplot as plt
        plt.figure()
        # if self.first: plt.plot(self.first.data_plot[:, 1], self.first.data_plot[:, 1], label = self.first.piece_name)
        if self.second: plt.plot(self.second.data_plot[:, 0], self.second.data_plot[:, 1], label = self.second.piece_name)
        plt.plot(self.third.data_plot[:, 0], self.third.data_plot[:, 1], label = self.third.piece_name)
        plt.legend()
        plt.xlabel('Displacement (mm)')
        plt.ylabel('Load (N)')
        plt.title('Displacement-Load Curve (%s)'%self.piece_name)
        # png_path = os.getcwd() + r'\LY12_output\Dis&Load_%s.png'%self.piece_name
        plt.show()
        # plt.savefig(png_path)
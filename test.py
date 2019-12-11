# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 14:26:55 2019

@author: ZhongWei Sun
"""

from Class_las import *
import os,os.path
import re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#print(os.getcwd() + r'\quality\las_quality_parameters\las_9_quality_parameter.xlsx')


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


path = r'C:\Users\ZhongWei Sun\OneDrive - FNC\Experiment\Experiment_Class\test\19.11.14'
#des_piece = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
#des_piece = ['A1', 'A2', 'A3', 'A']
#des_piece = ['B1', 'B2', 'B3', 'B']
#des_piece = ['C1', 'C2', 'C3', 'C']
#des_piece = ['D1', 'D2', 'D3', 'D']
#des_piece = ['E1', 'E2', 'E3', 'E']
#des_piece = ['F1', 'F2', 'F3', 'F']
#des_piece = ['G1', 'G2', 'G3', 'G']
#des_piece = ['H1', 'H2', 'H3', 'H']
#des_piece = ['I1', 'I2', 'I3', 'I']

#des_piece = ['a1', 'a2', 'a3', 'a']
#des_piece = ['b1', 'b2', 'b3', 'b']
#des_piece = ['c1', 'c2', 'c3', 'c']
#for letter in des_piece:
#    plt.figure()
#    for file in os.listdir(path):
#        if letter not in file[4:12]: continue
#        las_latter = las(file)
#        plt.plot(las_latter._dis, las_latter._load, label=file[0:10])
#    plt.legend()
#    plt.xlabel('Displacement(mm)')
#    plt.ylabel('Load(N)')
#    plt.title('las_9_%s Displacement-Load Curve'%letter)
#    fig_path = os.getcwd() + r'\output' + r'\las_9_%s'%letter
#    plt.savefig(fig_path)



#modu_0307 = []
#modu_max = []
#des_piece = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'a', 'b', 'c']
#for letter in des_piece:
#    for file in os.listdir(path):
#        if (letter not in file[4:12]) or ('_1' in file[7:11]) or ('_2' in file[7:11]): continue
#        las_test = las(file)
#        modu_0307.append([file[6:10], las_test.des_pre_modu, las_test.qua_pre_modu, las_test.test_modu_0307,
#                          las_test.des_pre_yield, las_test.qua_pre_yield, las_test.test_yieldS])
#        modu_max.append([file[6:10], las_test.des_pre_modu, las_test.qua_pre_modu, las_test.test_modu_maxSlope,
#                         las_test.des_pre_yield, las_test.qua_pre_yield, las_test.test_yieldS])
#columns_0307 = ['name', 'des_pre_modu', 'qua_pre_modu', 'test_modu_0307', 
#           'des_pre_yield', 'qua_pre_yield', 'test_yield_0307']
#modu_0307_frame = pd.DataFrame(modu_0307, columns=columns_0307)
#columns_max = ['name', 'des_pre_modu', 'qua_pre_modu', 'test_modu_max', 
#           'des_pre_yield', 'qua_pre_yield', 'test_yield_max']
#modu_max_frame = pd.DataFrame(modu_max, columns = columns_max)
#las_path = os.getcwd() + r'\output' + r'\las_9_modu_yiled_3.xlsx'
#with pd.ExcelWriter(las_path) as writer:
#    modu_0307_frame.to_excel(writer, sheet_name='modu_0307', index=None)
#    modu_max_frame.to_excel(writer, sheet_name='modu_max', index=None)

quality_file = os.getcwd() + r'\output\quality_las9.xlsx'
quality_las9 = pd.read_excel(quality_file)
yield_S = []
for piece_name in quality_las9.index:
    piece = las_piece(piece_name)
#    print(piece.second.pre_yield, piece.second.qua_pre_yield)
    yield_S.append([piece_name, piece.Pre_Yield, piece.second.qua_pre_yield, piece.second.test_yS_0307, 
                    piece.third.test_yS_0307, piece.Yield_0307])
#    piece.Plt_Dis_Load()

columns = ['piece_name', 'pre_yield', 'qua_yield', 'yield_sec_0307', 'yield_third_0307','test_yield']
yield_S_frame = pd.DataFrame(yield_S, columns = columns)
#yield_S_frame.to_excel(os.getcwd() + r'\output\Yield_3.xlsx', index = None)

yield_S = yield_S_frame.set_index('piece_name')
for label in yield_S.index:
    yield_S['pre_error'] = (yield_S.test_yield - yield_S.pre_yield)/yield_S.pre_yield *100
    yield_S['qua_error'] = (yield_S.test_yield - yield_S.qua_yield)/yield_S.qua_yield *100
    yield_S['sec_error'] = (yield_S.test_yield - yield_S.yield_sec_0307)/yield_S.yield_sec_0307 *100
yield_S.to_excel(os.path.dirname(quality_file) + r'\yield_Error.xlsx')    
 
#piece_name = 'las_9_b2'
#las_9_b2 = las_piece(piece_name)
#print('qua_pre_yield:', las_9_b2.second.qua_pre_yield)
#print('yield_strength:', las_9_b2.Yield_0307)
#
#las_9_b1 = las_piece('las_9_b1')
#print('qua_pre_yield:', las_9_b1.second.qua_pre_yield)
#print('yield_strength:', las_9_b1.Yield_0307)



 
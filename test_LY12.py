# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 15:01:04 2019

@author: ADMINISTRATOR
"""
import pandas as pd
from Class_LY12 import *
import os, os.path
import matplotlib.pyplot as plt
'''Test date'''
test_date = '19.05.07'

def LY12_extract_Data():

    txt_path = os.getcwd() + r'\test\%s'%test_date
    modu_10 = []

    for file in os.listdir(txt_path):

        if 'LY12_10' in file and file.endswith('.txt'):
            test_10 = LY12(file)
            if test_10.num_test != '3': continue
#            test_10.plot_dis_load
            modu_10.append([file.split('.')[0][0:10], test_10.test_modu_0307, test_10.test_modu_maxSlope])

    columns=['name', 'modu_0307', 'modu_maxSlope']

    modu_frame_10  = pd.DataFrame(modu_10, columns=columns)
    LY12_path = os.getcwd() + r'\output\LY12_10.xlsx'

    with pd.ExcelWriter(LY12_path) as writer:

        modu_frame_10.to_excel(writer, sheet_name='modu_10', index=None)


pieces_name = ['LY12_6_1', 'LY12_6_2', 'LY12_6_3']
LY12_test = []
for piece_name in pieces_name:
    LY = LY12_pieces(piece_name)
    LY12_test.append([piece_name, LY.modu_MS_second, LY.Modu_MS, LY.Yield_MS])
    print(piece_name, LY.third.test_yieldS_MS, LY.third.test_yieldL_MS)
    print(LY.Yield_MS)
    LY.Plt_Dis_Load()
LY12_test_frame = pd.DataFrame(LY12_test, columns=['name', 'Modu_MS_Second', 'Modu_MS', 'Yied_strength_MS'])
LY12_test_frame.to_excel('0507_LY12.xlsx', index=None)

# name = 'LY12_6_33_20190507_33.txt'
# LY12_test = LY12_txt(name)
# modu = LY12_test.test_modu_MS
# print(LY12_test.test_yieldS_MS)
# print(LY12_test.test_yieldL_MS)


# modu = LY12_test.test_modu_0307
# print(LY12_test.test_yieldS_0307)
# print(LY12_test.test_yieldL_0307)
#for file in file_names:
#    
#    LY12_plot = LY12(file)
#    plt.plot(LY12_plot._raw_data[:, 1], LY12_plot._raw_data[:, 0], label='%s'%('LY12_10_' + LY12_plot.num_test_piece + LY12_plot.num_test))
    
#    print('modulus:', LY12_plot.test_modu_maxSlope, '\n')
#    LY12_plot.test_modu_0307
#    plt.plot(LY12_plot.data_plot[:, 0], LY12_plot.data_plot[:, 1], label='%s'%('LY12_7_' + LY12_plot.num_test_piece + LY12_plot.num_test +'_0307'))
#    
#    LY12_plot.test_modu_maxSlope
#    plt.plot(LY12_plot.data_plot[:, 0], LY12_plot.data_plot[:, 1], label='%s'%('LY12_7_' + LY12_plot.num_test_piece + LY12_plot.num_test +'_maxslope'))
##
#plt.legend()
#plt.xlabel('displacement_mm')
#plt.ylabel('load_mm')   
#plt.title('Displacement-Load curve')
#png_path = os.getcwd() + r'\output\%s'%'LY12_10_4.png'
#plt.savefig(png_path)
##    
    












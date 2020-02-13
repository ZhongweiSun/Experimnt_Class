# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 15:01:04 2019

@author: ADMINISTRATOR
"""
import pandas as pd
import Class_LY12
import os, os.path
import matplotlib.pyplot as plt

'''Test date'''
test_date = '20.01.20'

txt_path =  os.getcwd() + r'\test\%s'%test_date

def find_pieces():

    LY12_pieces = []
    tra_pieces = []

    for file in os.listdir(txt_path) :
        if os.path.isdir(file) : continue
        if 'LY12' in file :
            name_list = file.split('_')
            piece_name = '_'.join(name_list[:3])[:-1]
            if piece_name in LY12_pieces : pass
            else: LY12_pieces.append(piece_name)
        else: continue

    return LY12_pieces, tra_pieces

#Y12_R_1212 = []
#LY12_pieces, _ = find_pieces()
#for piece in LY12_pieces:
#    LY12 = Class_LY12.LY12_piece(piece)
#    LY12.Plt_Dis_Load()
    # Y12_R_1212.append([piece, LY12.Modu_MS/1000/0.85, LY12.Modu_MS/1000/0.8, LY12.YieldS_MS])

# Y12_R_1212_frame = pd.DataFrame(Y12_R_1212, columns=['name', 'modu_0.85', 'modu_0.8', 'yield strength'])
# excel_path = os.getcwd() + r'\LY12_output\1212.xlsx'
# Y12_R_1212_frame.to_excel(excel_path, index=None)

# Q235_pieces = ['LY12_11_6', 'LY12_11_7', 'LY12_11_8']
# Q235_pieces = ['LY12_11_4']
# for piece in Q235_pieces:
#     Q235 = Class_LY12.LY12_piece(piece)
#     Q235.Plt_Dis_Load()
    # Q235.Plt_Dis()
    # print(Q235.second.data_plot)
    # print('0307:', piece, Q235.Modu_MS)
    # print('MS:', piece, Q235.YieldS_MS)

# print( 235 * 3.1415926 * 10 * 10 / 4)
    
txt_files = ['LY12_12_11_20200120_中船重工.txt', 'LY12_12_21_20200120_中船重工.txt', 'LY12_12_31_20200120_中船重工.txt']
#
#LY_1 = Class_LY12.LY12_txt('LY12_12_11_20200120_中船重工.txt')
#print(LY_1.test_modu_0307, LY_1.stiff_0307, LY_1.stiff_0307/0.85)
#LY_2 = Class_LY12.LY12_txt('LY12_12_21_20200120_中船重工.txt')
#print(LY_2.test_modu_0307, LY_1.stiff_0307, LY_2.stiff_0307/0.85)
#LY_3 = Class_LY12.LY12_txt('LY12_12_31_20200120_中船重工.txt')
#print(LY_3.test_modu_0307, LY_1.stiff_0307, LY_3.stiff_0307/0.85)

#plt.figure(1)
#plt.plot(LY_1._dis, LY_1._load, label = LY_1.piece_num)
#plt.plot(LY_2._dis, LY_2._load, label = LY_2.piece_num)
#plt.plot(LY_3._dis, LY_3._load, label = LY_3.piece_num)
#plt.xlabel('strain (%)')
#plt.ylabel('load (N)')
#plt.legend()
#plt.savefig('strain_stress.png')
#plt.close()
#
#plt.figure(2)
#plt.plot(LY_1.data_plot[:, 0], LY_1.data_plot[:, 1], label = LY_1.piece_num)
#plt.plot(LY_2.data_plot[:, 0], LY_2.data_plot[:, 1], label = LY_2.piece_num)
#plt.plot(LY_3.data_plot[:, 0], LY_3.data_plot[:, 1], label = LY_3.piece_num)
#plt.xlabel('strain (%)')
#plt.ylabel('load (N)')
#plt.legend()
#plt.savefig('strain_stress_fix.png')
#plt.close()

#txt_files = ['LY12_12_11_20200120_中船重工.txt']
for txt_file in txt_files:
    LY = Class_LY12.LY12_txt(txt_file)
    
#    LY.plot_dis_load
    LY.test_modu_0307
    print(LY.stiff_0307*100)



















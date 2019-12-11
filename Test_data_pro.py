# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 10:48:27 2019

@author: ZhongWei Sun
"""
from Class_las import *
import os,os.path
import matplotlib.pyplot as plt
import pandas as pd

test_design = []
test_pieces = []
test_las_list = []

def testdata_process():
    ''' Process the test data and return the Data processing result'''
    
    for file in os.listdir(os.getcwd() + r'\test\19.09.26'):
#    for file in os.listdir(os.getcwd() + r'\test\19.08.27'):
        
        if (not file.endswith('.txt')) or ('las' not in file): continue
        global test_design, test_pieces
        name = file.split('.')[0]
        test_las = las(file)
        if test_las.num_test == '1' : continue
        test_las_list.append(test_las)
        test_design.append([name[0:10], test_las.des_pre_modu, test_las.des_pre_yield, test_las.qua_pre_modu, test_las.qua_pre_yield, 
                            test_las.test_modu_0307, test_las.test_yieldL, test_las.test_yieldS, test_las.ult_load, 
                            test_las.test_modu_maxSlope, test_las.test_yieldL, test_las.test_yieldS, test_las.ult_load])

#        test_design.append([name[0:10], test_las.test_modu_0307, test_las.test_yieldL, test_las.test_yieldS, 
#                        test_las.test_modu_maxSlope, test_las.test_yieldL, test_las.test_yieldS])
    
#        test_design.append([name[0:10], test_las.pre_modu, test_las.sim_modu, 
#                            test_las.test_modu_0307, test_las.error_test_sim_modu, 
#                            test_las.test_yieldL, test_las.test_yieldS, test_las.ult_load])
        if name[0:8] in test_pieces:
            pass
        else:
            test_pieces.append(name[0:8])

# 画图：  
#    for test_piece in test_pieces:
#        
#        plt.figure()
#        
#        for test_la in test_las_list:
#            
#            if test_piece in test_la._qua_name:
#                
#                plt.plot(test_la._raw_data[:, 1], test_la._raw_data[:, 0], label='The %s test data'%test_la.num_test)
#                plt.xlabel('Displacement (mm)')
#                plt.ylabel('Load (N)')
#                plt.title('The displacment-load curve of %s'%test_piece)
#                plt.legend()
#                fig_path = os.getcwd() + r'\output\%s.png'%test_piece
#                plt.savefig(fig_path)
    
    columns = ['name', 'des_pre_modu', 'des_pre_yield', 'qua_pre_modu', 'qua_pre_yield',
               'test_modu_0307', 'test_yieldL_0307', 'test_yieldS_0307', 'ult_load_0307', 
               'test_modu_maxS', 'test_yieldL_maxS', 'test_yieldS_maxS', 'ult_load_maxS']
    
#    columns = ['name', 'test_modu_0307', 'test_yieldL_0307', 'test_yieldS_0307', 
#               'test_modu_maxS', 'test_yieldL_maxS', 'test_yieldS_maxS']

    test_design_frame = pd.DataFrame(test_design, columns=columns)
    xlsx_path = os.getcwd() + r'\output\las_0926_test.xlsx'
    test_design_frame.to_excel(xlsx_path, sheet_name='09.26', index=None)
        

printed_pieces = []
LY12_pieces = []


    






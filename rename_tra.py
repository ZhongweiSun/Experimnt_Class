# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:58:44 2019

@author: ZhongWei Sun
"""
import os, os.path
import pandas as pd
from tra import *

num_letter = {'2': 'A', '4': 'B', '5': 'C', '6': 'D', '7': 'E'}

def rename():
    
    test_file_path = os.getcwd() + r'\test\19.04.18'
    
    for file in os.listdir(test_file_path):
        if file.endswith('.txt'):
            name_list = file.split('.')[0].split('-')
            new_name = 'tra_1_' + num_letter[name_list[0][-2]] + name_list[0][-1] + '_' \
            + name_list[-1][-1] + '_' + name_list[2] + '_' + name_list[-1] + '.txt'
            os.rename(os.path.join(test_file_path, file), os.path.join(test_file_path, new_name))
#            print(os.path.join(test_file_path, file), os.path.join(test_file_path, new_name))
#rename()
            
            
#from tra import *
#name = 'tra_1_A1_3_20190418_213.txt'

#test = tra_txt(name)
#print(test.load[100])
#print(test.ult_load * 0.9*0.5)
#print('modu_0307', test.test_modu_0307, 'stiff_ness:', test.stiff_0307)
#print('modu_maxS', test.test_modu_maxS)
#print('modu_SA', test.test_modu_SA)

# num = ['A', 'B', 'C', 'D', 'E']
# for letter in num:
    
#     test_piece = tra_piece('tra_1_%s1'%letter)
#     test_piece.Plt_Dis_Load()
#     print('yield Stress:', test_piece.Yield_0307)
    
#     test_piece = tra_piece('tra_1_%s2'%letter)
#     test_piece.Plt_Dis_Load()
#     print('yield Stress:', test_piece.Yield_0307)
    
#     test_piece = tra_piece('tra_1_%s3'%letter)
#     test_piece.Plt_Dis_Load()
#     print('yield Stress:', test_piece.Yield_0307)
#
#    print('*******************************************')
#
#test_date = '19.04.18'
#file_path = os.getcwd() + r'\test\%s'%test_date
#result = []
#for file in os.listdir(file_path) :
#    if '_1_' in file[8:]: continue
#    if '_2_' in file[8:]: continue
#    txt = tra_txt(file)
#       
#    result.append([txt.test_piece_num, txt.ult_load, txt.test_modu_0307, txt.test_yL_0307, txt.test_yR_0307])
#    
#columns = ['name', 'ult_load', 'modu_0307', 'yield_load_0307', 'yield_Ratio_0307']
#result_frame = pd.DataFrame(result, columns = columns)
#result_frame.to_excel('Tra_modu_yieldL_2.xlsx', index=None)

               
#def searchGraph(graph, start, end):
#    results = []
#    generatePath(graph, [start], end, results)
#    results.sort(key=lambda x:len(x))
#    return results
#def generatePath (graph, path, end, results):
#    state = path[-1]
#    if state == end:
#        results.append(path)
#    else:
#        for arc in graph[state]:
#            if arc not in path:
#                generatePath(graph, path+[arc], end, results)
#graph = {'A':['B', 'C', 'D'],
#         'B':['E'], 
#         'C':['D', 'F'],
#         'D':['B', 'E', 'G'], 
#         'E':[], 
#         'F':['D', 'G'], 
#         'G':['E']}
#r = searchGraph(graph, 'A', 'E')
#print(r)

txt_path = os.getcwd() + r'\test\19.05.07'
for file in os.listdir(txt_path):
    if os.path.isdir(os.path.join(txt_path, file)) : continue
    if 'lvya3' in file: 
        t_file = file.replace('lvya3', 'LY12')
        name_list = t_file.split('-')
        name_list.insert(2, name_list[-1][:-4])
        new_name = '_'.join(name_list)
        os.rename(os.path.join(txt_path, file), os.path.join(txt_path, new_name))
        # print(os.path.join(txt_path, file), os.path.join(txt_path, new_name))
    # if 'lattice31' in file:
    #     t_file = file.replace('lattice31-6-', 'tra-1-')
    #     name_list = t_file.split('-')
    #     if 'S' in name_list[-1] :
    #         temp_list = name_list[-1].split('.')
    #         temp_name = temp_list[0][0] + temp_list[0][-1] + temp_list[0][1]
    #         name_list.insert(2, temp_name)
    #         name_list.insert(3, temp_list[0][2])
    #         new_name = '_'.join(name_list)
    #         print(new_name)
    #     else :
    #         temp_list = name_list[-1].split('.')
    #         name_list.insert(2, temp_list[0][:-1])
    #         name_list.insert(3, temp_list[0][-1])
    #         new_name = '_'.join(name_list)
    #         # print(new_name)
    #     os.rename(os.path.join(txt_path, file), os.path.join(txt_path, new_name))
        # print(os.path.join(txt_path, file), os.path.join(txt_path, new_name))


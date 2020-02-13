
# -*- coding: utf-8 -*-

import os, os.path
import pandas as pd 
import Class_LY12, tra
import os, os.path


txt_path =  os.getcwd() + r'\test\19.05.07'

def find_pieces():

    LY12_pieces = []
    tra_pieces = []

    for file in os.listdir(txt_path) :
        if os.path.isdir(file) : continue
        if 'LY12' in file :
            if file[:8] in LY12_pieces : pass
            else: LY12_pieces.append(file[:8])
        if 'tra_1_' in file :
            if 'S' in file :
                if file[:9] in tra_pieces : pass
                else: tra_pieces.append(file[:9])
            else: 
                if file[:8] in tra_pieces: pass 
                else: tra_pieces.append(file[:8])
    
    return LY12_pieces, tra_pieces

#铝压试件
def LY12_BZ():

    LY12_pieces, _ = find_pieces()
    LY12_R = []                           #数据处理结果
    for pieces in LY12_pieces :
        LY12 = Class_LY12.LY12_piece(pieces)
        LY12.Plt_Dis_Load()
        print(LY12.Yield_MS)
        LY12_R.append([pieces, LY12.Modu_MS, LY12.third.test_yieldS_MS])
    LY12_R_frame = pd.DataFrame(LY12_R, columns=['piece_name', 'Modulus', 'Yield_strength'])
    LY12_R_path = os.getcwd() + r'\LY12_output\L12_20190507.xlsx'
    LY12_R_frame.to_excel(LY12_R_path, index=None)

def Tra():

    _, tra_pieces = find_pieces()
    Tra_R_MS = []
    Tra_R_0307 = []
    for piece in tra_pieces:

        tra_p = tra.tra_piece(piece)
        if tra_p.Yield_MS != 0.0 : Tra_R_MS.append([piece, tra_p.Modu_MS, tra_p.Yield_MS])
        else: Tra_R_MS.append([piece, tra_p.Modu_MS, tra_p.third.test_yS_maxS])

        if tra_p.Yield_0307 != 0.0 : Tra_R_0307.append([piece, tra_p.Modu_0307, tra_p.Yield_0307])
        else : Tra_R_0307.append([piece, tra_p.Modu_0307, tra_p.third.test_yS_0307])

    Tra_R_MS_frame = pd.DataFrame(Tra_R_MS, columns=['piece_name', 'Modulus_MPa', 'Yield_strength'])
    tra_MS_path = os.getcwd() + r'\tra_output\tra_MS_20190507.xlsx'
    Tra_R_MS_frame.to_excel(tra_MS_path, index=None)

    Tra_R_0307_Frame = pd.DataFrame(Tra_R_0307, columns=['piece_name', 'Modulus_MPa', 'Yield_strength'])
    tra_0307_path = tra_MS_path = os.getcwd() + r'\tra_output\tra_0307_20190507.xlsx'
    Tra_R_0307_Frame.to_excel(tra_0307_path, index=None)
    # tra_p.Plt_Dis_Load()

# Tra()

des_parameter = pd.read_excel(os.getcwd() + r'\design\design_tra.xlsx', sheet_name='Experiment', index_col='name')
tra_0307_path = tra_MS_path = os.getcwd() + r'\tra_output\tra_0307_20190507.xlsx'
tra_R = pd.read_excel(tra_0307_path, index_col='piece_name')
des_pieces = {}
for p_name in tra_R.index:
    # print(p_name)
    if p_name[:-1] in des_pieces: des_pieces[p_name[:-1]].append(p_name)
    else: 
        des_pieces[p_name[:-1]] = []
        des_pieces[p_name[:-1]].append(p_name)

# ave_modu_dic = {}
# ave_strength_dic = {}
for des_piece in des_pieces:
    sum_mudu = 0
    sum_strength = 0
    for test_piece in des_pieces[des_piece]:
        sum_mudu += tra_R.loc[test_piece, 'Modulus_MPa']
        sum_strength += tra_R.loc[test_piece, 'Yield_strength']
    ave_modu = sum_mudu / len(des_pieces[des_piece])
    # ave_modu_dic[des_piece] = ave_modu
    ave_strength = sum_strength / len(des_pieces[des_piece])
    # ave_strength_dic[des_piece] = ave_strength

    tra_R.loc[des_pieces[des_piece][0], 'des_name'] = des_piece
    tra_R.loc[des_pieces[des_piece][0], 'ave_modu'] = ave_modu
    tra_R.loc[des_pieces[des_piece][0], 'ave_Strength'] = ave_strength
    tra_R.loc[des_pieces[des_piece][0], 'des_modu'] = des_parameter.loc[des_piece, 'des_modu']*1000
des_parameter = pd.read_excel(os.getcwd() + r'\design\design_tra.xlsx', sheet_name='Experiment')

for des_piece in des_pieces:
    for test_piece in des_pieces[des_piece]:
        tra_R.loc[test_piece, 'Bias_Modu_%'] = (tra_R.loc[test_piece, 'Modulus_MPa'] - \
            tra_R.loc[des_pieces[des_piece][0], 'ave_modu']) / \
                tra_R.loc[des_pieces[des_piece][0], 'ave_modu'] * 100
        tra_R.loc[test_piece, 'Bias_S_%'] = (tra_R.loc[test_piece, 'Yield_strength'] - \
            tra_R.loc[des_pieces[des_piece][0], 'ave_Strength']) / \
                tra_R.loc[des_pieces[des_piece][0], 'ave_Strength'] * 100
    tra_R.loc[des_pieces[des_piece][0], 'Error_Modu_%'] = (tra_R.loc[des_pieces[des_piece][0], 'ave_modu'] - \
        tra_R.loc[des_pieces[des_piece][0], 'des_modu']) / \
            tra_R.loc[des_pieces[des_piece][0], 'des_modu'] * 100

print(tra_R['Error_Modu_%'])
Tra_an_path = os.getcwd() + r'\tra_output\tra_analysis.xlsx'
tra_R.to_excel(Tra_an_path)




# print(des_pieces)










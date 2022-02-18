# -*- coding: utf-8 -*-
"""
"""
import pandas
import numpy as np

# import data files
gla = pandas.read_csv('GLA.txt', sep="#\|#", engine="python")
glab = pandas.read_csv('GLAB.txt', sep="#\|#", engine="python")
jet = pandas.read_csv('JET.txt', sep="#\|#", engine="python")

# check if any GLA accounts do not appear in GLAB
glab['inGLAB']=True
glab_accs = glab.drop_duplicates(subset='accountNumber',keep='last')
gla_in_glab = gla.merge(glab_accs, how='left', on='accountNumber')
gla_in_glab = gla_in_glab.loc[:,('accountNumber', 'inGLAB')].fillna(False)
# print('\nGLA accounts that do not appear in GLAB')
# print(gla_in_glab[gla_in_glab['inGLAB']==False])

# check if duplicate accounts in GLA
print('\nCheck duplicate GLA accounts (none found if returns Empty DataFrame):')
print(gla[gla.duplicated(subset='accountNumber', keep=False)].sort_values(by='accountNumber'))

# check if any GLAB accounts do not appear in GLA
# print('\nCheck if any GLAB accounts do not appear in GLA')
gla['inGLA']=True
gla_accs = gla.drop_duplicates(subset='accountNumber',keep='last')
glab_in_gla = glab.merge(gla_accs, how='left', on='accountNumber')
glab_in_gla = glab_in_gla.loc[:,('accountNumber', 'inGLA')].fillna(False)

# print(glab_in_gla[glab_in_gla['inGLA']==False])


glab_gla_merged = glab_in_gla.merge(gla_in_glab, how='outer', on='accountNumber').fillna(False)
print('\nCross comparison of GLA and GLAB accounts:')
print(glab_gla_merged[(glab_gla_merged['inGLA']==False) | (glab_gla_merged['inGLAB']==False)])

# check if any JET accounts do not appear in GLAB
print('\nCheck if any JET accounts do not appear in GLAB:')
jet_accs = jet.drop_duplicates(subset='accountNumber', keep='first').loc[:, ('accountNumber')].to_frame()
jet_in_glab = jet_accs.merge(glab, how='left', on='accountNumber')
jet_in_glab = jet_in_glab.loc[:, ('accountNumber', 'inGLAB')].fillna(False)
print(jet_in_glab[jet_in_glab['inGLAB']==False])

